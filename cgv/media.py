import subprocess
import os
import shutil
from PIL import Image, ImageDraw
import numpy as np
from typing import List, Tuple

def _ensure_parent(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)

def _validate_box(box: Tuple[int, int, int, int], width: int, height: int) -> None:
    left, top, right, bottom = box
    if left < 0 or top < 0 or right > width or bottom > height:
        raise ValueError(f"Crop/overlay box {box} is outside image bounds {(width, height)}")
    if right <= left or bottom <= top:
        raise ValueError(f"Crop/overlay box {box} must have positive width and height")

def extract_frames(video_path: str, timestamps: List[float], out_dir: str) -> List[str]:
    """
    Extract keyframes at specific timestamps from a video using FFmpeg.
    """
    os.makedirs(out_dir, exist_ok=True)
    frame_paths = []
    
    if shutil.which('ffmpeg') is None:
        raise RuntimeError("FFmpeg is required but was not found on PATH.")
        
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    for i, ts in enumerate(timestamps):
        out_path = os.path.join(out_dir, f"frame_{i}_t{ts:.2f}.jpg")
        cmd = [
            'ffmpeg', '-y',
            '-ss', str(ts),
            '-i', video_path,
            '-frames:v', '1',
            '-q:v', '2',
            out_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg failed to extract frame at {ts}s: {res.stderr}")
        if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
            raise RuntimeError(f"FFmpeg did not produce a frame at {ts}s: {out_path}")
        frame_paths.append(out_path)
    return frame_paths

def crop_image(image_path: str, box: Tuple[int, int, int, int], out_path: str) -> str:
    """
    Crop an image to a specific bounding box (left, top, right, bottom) using Pillow.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Source image not found: {image_path}")
        
    with Image.open(image_path) as im:
        _validate_box(box, *im.size)
        _ensure_parent(out_path)
        cropped = im.crop(box)
        cropped.save(out_path, quality=95)
    return out_path

def draw_overlay(image_path: str, boxes: List[Tuple[int, int, int, int, str]], out_path: str) -> str:
    """
    Draw boxes and labels onto an image using Pillow.
    Each box is (left, top, right, bottom, label).
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Source image not found: {image_path}")
        
    with Image.open(image_path).convert("RGB") as im:
        draw = ImageDraw.Draw(im)
        for box in boxes:
            left, top, right, bottom, label = box
            _validate_box((left, top, right, bottom), *im.size)
            # Draw rectangle
            draw.rectangle([left, top, right, bottom], outline="red", width=3)
            draw.text((left + 5, top + 5), label, fill="red")
        _ensure_parent(out_path)
        im.save(out_path, quality=95)
    return out_path

def compare_frames(a_path: str, b_path: str, out_path: str) -> Tuple[str, float]:
    """
    Perform a pixel-by-pixel diff between two frames and save the diff visualization.
    Returns the out_path and the percentage of changed pixels.
    """
    if not os.path.exists(a_path) or not os.path.exists(b_path):
        raise FileNotFoundError("One or both source frames do not exist.")
        
    with Image.open(a_path).convert("RGB") as im_a, Image.open(b_path).convert("RGB") as im_b:
        if im_a.size != im_b.size:
            raise ValueError(f"Frame sizes differ: {im_a.size} != {im_b.size}")
            
        arr_a = np.array(im_a, dtype=np.int16)
        arr_b = np.array(im_b, dtype=np.int16)
        
        # Absolute difference
        diff_arr = np.abs(arr_a - arr_b)
        
        # Scale diff to visible range and save
        diff_vis = (diff_arr.astype(np.float32) * (255.0 / max(1.0, np.max(diff_arr)))).astype(np.uint8)
        im_diff = Image.fromarray(diff_vis)
        _ensure_parent(out_path)
        im_diff.save(out_path)
        
        # Threshold changed pixels where any RGB channel differs materially
        diff_pixels = np.count_nonzero(np.any(diff_arr > 15, axis=2))
        total_pixels = arr_a.shape[0] * arr_a.shape[1]
        diff_percent = (diff_pixels / total_pixels) * 100.0
        
    return out_path, diff_percent
