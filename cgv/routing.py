import os
import shutil
import re
import json
from typing import List, Dict, Any, Tuple

def check_model_capabilities(model_id: str, registry_models: List[Dict[str, Any]]) -> bool:
    """
    Check if the selected model is registered as image-capable.
    Raises ValueError if the model is text-only or missing from registry.
    """
    for m in registry_models:
        if m.get('id') == model_id:
            inputs = m.get('input', [])
            if 'image' in inputs:
                return True
            raise ValueError(
                f"FAIL-CLOSED: Model '{model_id}' is registered but does NOT support visual inputs: {inputs}. "
                "Text fallback is strictly prohibited by CGV visual grounding rules."
            )
    raise ValueError(
        f"FAIL-CLOSED: Model '{model_id}' was not found in the model registry. "
        "Text fallback is strictly prohibited."
    )

def verify_bounding_box_overlap(box_a: Tuple[float, float, float, float], 
                                box_b: Tuple[float, float, float, float]) -> float:
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes (x, y, w, h).
    Used to mathematically verify overlap claims before asking VLM.
    """
    xa, ya, wa, ha = box_a
    xb, yb, wb, hb = box_b
    
    if wa <= 0 or ha <= 0 or wb <= 0 or hb <= 0:
        raise ValueError("Bounding boxes must use positive width and height.")
        
    # Convert to left, top, right, bottom
    l_a, t_a, r_a, b_a = xa, ya, xa + wa, ya + ha
    l_b, t_b, r_b, b_b = xb, yb, xb + wb, yb + hb
    
    # Compute intersection area
    inter_l = max(l_a, l_b)
    inter_t = max(t_a, t_b)
    inter_r = min(r_a, r_b)
    inter_b = min(b_a, b_b)
    
    if inter_r <= inter_l or inter_b <= inter_t:
        return 0.0
        
    inter_area = (inter_r - inter_l) * (inter_b - inter_t)
    area_a = wa * ha
    area_b = wb * hb
    union_area = area_a + area_b - inter_area
    
    if union_area <= 0:
        return 0.0
        
    return inter_area / union_area

def prepare_prompt_for_vlm(prompt_str: str, temp_dir: str = ".omp_vlm_temp") -> str:
    """
    Scans the prompt for local:// URIs, copies the referenced files to a temporary 
    directory inside the active workspace, and replaces the URIs with relative workspace 
    paths. This prevents the harness read() tool from dumping raw binary bytes of 
    out-of-workspace files, which can cause model hangs.
    """
    uris = re.findall(r'local://[^\s"\'<>]+', prompt_str)
    if not uris:
        return prompt_str
        
    os.makedirs(temp_dir, exist_ok=True)
    
    # Fetch local root config from harness environment
    roots_env = os.environ.get('PI_EVAL_LOCAL_ROOTS')
    if not roots_env:
        return prompt_str
        
    try:
        roots = json.loads(roots_env)
    except json.JSONDecodeError:
        return prompt_str
        
    local_root = roots.get('local')
    if not local_root:
        return prompt_str
        
    updated_prompt = prompt_str
    for uri in uris:
        filename = uri.replace('local://', '')
        # Handle hash prefix if present
        basename = filename.split('-', 1)[1] if '-' in filename and not filename.startswith('.') else filename
        
        src_path = os.path.join(local_root, filename)
        if not os.path.exists(src_path):
            src_path = os.path.join(local_root, basename)
            
        if os.path.exists(src_path):
            dest_path = os.path.join(temp_dir, basename)
            shutil.copy(src_path, dest_path)
            updated_prompt = updated_prompt.replace(uri, dest_path)
            
    return updated_prompt
