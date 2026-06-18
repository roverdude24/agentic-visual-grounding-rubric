import os
import json
import hashlib
from typing import Dict, Any, Optional

class ArtifactRegistry:
    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path
        self.artifacts: Dict[str, Any] = {}
        self.load()
        
    def load(self):
        if os.path.exists(self.manifest_path):
            try:
                with open(self.manifest_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                self.artifacts = loaded if isinstance(loaded, dict) else {}
            except json.JSONDecodeError:
                self.artifacts = {}
                
    def save(self):
        parent = os.path.dirname(os.path.abspath(self.manifest_path))
        os.makedirs(parent, exist_ok=True)
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            json.dump(self.artifacts, f, indent=2)
            
    def register(self, file_path: str, label: str, purpose: str) -> str:
        """
        Register a file to the manifest and return its local URI.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File to register does not exist: {file_path}")
            
        # Compute SHA256 hash
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        file_hash = sha256.hexdigest()
        
        # Get dimensions if image
        dims = None
        try:
            from PIL import Image
            with Image.open(file_path) as im:
                dims = list(im.size)
        except Exception:
            pass # Not an image or PIL missing
            
        file_size = os.path.getsize(file_path)
        basename = os.path.basename(file_path)
        # Prevent collisions by prefixing with hash
        local_uri = f"local://{file_hash[:12]}-{basename}"
        
        self.artifacts[local_uri] = {
            "path": os.path.abspath(file_path),
            "label": label,
            "purpose": purpose,
            "hash": file_hash,
            "size_bytes": file_size,
            "dimensions": dims
        }
        self.save()
        return local_uri

    def get(self, local_uri: str) -> Optional[Dict[str, Any]]:
        return self.artifacts.get(local_uri)
