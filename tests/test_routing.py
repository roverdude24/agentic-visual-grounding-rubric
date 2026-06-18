import pytest
from cgv.routing import check_model_capabilities, verify_bounding_box_overlap

def test_check_model_capabilities():
    registry = [
        {"id": "vlm-model", "input": ["text", "image"]},
        {"id": "text-model", "input": ["text"]}
    ]
    assert check_model_capabilities("vlm-model", registry) is True
    
    with pytest.raises(ValueError, match="does NOT support visual inputs"):
        check_model_capabilities("text-model", registry)
        
    with pytest.raises(ValueError, match="not found in the model registry"):
        check_model_capabilities("missing-model", registry)

def test_verify_bounding_box_overlap():
    box_a = (10, 10, 50, 50)
    box_b = (20, 20, 50, 50)
    iou = verify_bounding_box_overlap(box_a, box_b)
    assert iou > 0.0
    
    # Touch only
    assert verify_bounding_box_overlap((0,0,10,10), (10,10,10,10)) == 0.0
    
    # Invalid size
    with pytest.raises(ValueError):
        verify_bounding_box_overlap((0,0,-1,10), (0,0,10,10))
