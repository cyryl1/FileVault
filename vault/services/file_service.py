import json
import uuid
from datetime import datetime
import shutil
from pathlib import Path
from typing import Dict, List, Any
from vault.utils.helpers import validate_file_type


class FileService:
    """Service layer for file operations"""

    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            script_dir = Path(__file__).parent
            storage_dir = script_dir / "storage"
        
        self.storage_dir = Path(storage_dir)
        self.uploads_dir = self.storage_dir / "uploads"
        self.metadata_file = self.storage_dir / "metadata.json"

        self.storage_dir.mkdir(exist_ok=True)
        self.uploads_dir.mkdir(exist_ok=True)

        if not self.metadata_file.exists():
            self._save_metadata({})

    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata from JSON file"""
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
        
    def _save_metadata(self, metadata: Dict[str, Any]) -> None:
        """Save metadata to JSON file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

    def upload_file(self, filepath: str) -> Dict[str, Any]:
        """Upload a file and return metadata"""
        source_path = Path(filepath)

        if not source_path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        if not validate_file_type(filepath):
            raise ValueError("File type not allowed: {source_path}")
        
        file_id = str(uuid.uuid4())[:8]

        file_size = source_path.stat().st_size
        upload_time = datetime.now().isoformat()

        dest_path = self.uploads_dir / f"{file_id}_{source_path.name}"
        shutil.copy2(source_path, dest_path)

        metadata = self._load_metadata()
        metadata[file_id] = {
            "filename": source_path.name,
            "size": file_size,
            "upload_time": upload_time,
            "path": str(dest_path),
            "original_path": str(source_path)
        }

        self._save_metadata(metadata)

        return {
            "file_id": file_id,
            "filename": source_path.name,
            "size": file_size,
            "upload_time": upload_time
        }
    
    def list_files(self) -> List[Dict[str, Any]]:
        """List all uploaded files"""
        metadata = self._load_metadata()
        files = []

        for file_id, data in metadata.items():
            files.append({
                "file_id": file_id,
                "filename": data["filename"],
                "size": data["size"],
                "upload_time": data["upload_time"]
            })
        
        files.sort(key=lambda x: x["upload_time"], reverse=True)
        return files
    
    def get_file_info(self, file_id: str) -> Dict[str, Any]:
        """Get detailed file information"""
        metadata = self._load_metadata()

        if file_id not in metadata:
            raise FileNotFoundError(f"File not found: {file_id}")

        return {
            "file_id": file_id,
            **metadata[file_id]
        }
    
    def delete_file(self, file_id: str) -> bool:
        """Delete a file and its metadata"""
        metadata = self._load_metadata()

        if file_id not in metadata:
            raise FileNotFoundError(f"File not found: {file_id}")
        
        file_path = Path(metadata[file_id]["path"])
        if file_path.exists():
            file_path.unlink()

        del metadata[file_id]
        self._save_metadata(metadata)

        return True