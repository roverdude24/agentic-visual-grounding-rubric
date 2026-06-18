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
