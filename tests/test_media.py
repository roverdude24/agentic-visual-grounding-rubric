import pytest
import os
from PIL import Image
from cgv.media import crop_image, compare_frames, draw_overlay

def test_crop_image(tmp_path):
    img_path = tmp_path / "img.png"
    Image.new("RGB", (100, 100), color="blue").save(img_path)
    
    out_path = tmp_path / "crop.png"
    crop_image(str(img_path), (10, 10, 50, 50), str(out_path))
    assert os.path.exists(out_path)
    with Image.open(out_path) as cropped:
        assert cropped.size == (40, 40)
        
    # Test out of bounds
    with pytest.raises(ValueError):
        crop_image(str(img_path), (10, 10, 150, 50), str(out_path))

def test_compare_frames(tmp_path):
    img_a = tmp_path / "a.png"
    img_b = tmp_path / "b.png"
    Image.new("RGB", (10, 10), color="white").save(img_a)
    
    # Same image
    Image.new("RGB", (10, 10), color="white").save(img_b)
    out_path = tmp_path / "diff.png"
    _, diff = compare_frames(str(img_a), str(img_b), str(out_path))
    assert diff == 0.0
    assert os.path.exists(out_path)
    
    # Different image (lossless PNG ensures exact 1 pixel difference)
    im = Image.new("RGB", (10, 10), color="white")
    im.putpixel((0, 0), (0, 0, 0)) # Change one pixel
    im.save(img_b)
    _, diff2 = compare_frames(str(img_a), str(img_b), str(out_path))
    assert diff2 == 1.0 # exactly 1 out of 100 pixels changed
