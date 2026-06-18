import pytest
import json
import os
from cgv.routing import check_model_capabilities, verify_bounding_box_overlap, prepare_prompt_for_vlm

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

def test_prepare_prompt_for_vlm(tmp_path, monkeypatch):
    local_dir = tmp_path / "local"
    local_dir.mkdir()
    dummy_img = local_dir / "frame_0.jpg"
    dummy_img.write_text("fake image data")
    
    monkeypatch.setenv("PI_EVAL_LOCAL_ROOTS", json.dumps({"local": str(local_dir)}))
    
    prompt = "Check image: local://frame_0.jpg"
    temp_workspace_dir = tmp_path / "workspace_temp"
    
    safe_prompt = prepare_prompt_for_vlm(prompt, temp_dir=str(temp_workspace_dir))
    
    expected_copied_path = temp_workspace_dir / "frame_0.jpg"
    assert os.path.exists(expected_copied_path)
    assert safe_prompt == f"Check image: {expected_copied_path}"
