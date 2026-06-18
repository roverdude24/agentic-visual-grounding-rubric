import pytest
import os
import json
from cgv.manifest import ArtifactRegistry

def test_manifest_lifecycle(tmp_path):
    manifest_file = tmp_path / "manifest.json"
    registry = ArtifactRegistry(str(manifest_file))
    
    # Create a dummy file to register
    dummy_file = tmp_path / "test.txt"
    dummy_file.write_text("hello world")
    
    uri = registry.register(str(dummy_file), "test_file", "testing manifest register")
    assert uri.startswith("local://")
    
    # Load registry in another instance
    reg2 = ArtifactRegistry(str(manifest_file))
    item = reg2.get(uri)
    assert item is not None
    assert item["label"] == "test_file"
    assert item["purpose"] == "testing manifest register"
    
    # Test collision avoidance (same file contents & diff filename, or diff file contents)
    dummy_file2 = tmp_path / "test2.txt"
    dummy_file2.write_text("different content")
    uri2 = reg2.register(str(dummy_file2), "test_file2", "testing collision")
    assert uri != uri2
