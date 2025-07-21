from datetime import datetime
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from vault.utils.helpers import validate_file_type, generate_file_id, get_file_type
from vault.repositories.file_repository import FileRepository
from vault.config import Config, FileType, Visibility
from vault.workers.thumbnail_worker import generate_thumbnail

class FileService:
    """Service layer for file operations"""

    def __init__(self, file_repo: FileRepository):
        self.file_repo = file_repo
        self.storage_dir = Path(Config.STORAGE_DIR)
        self.uploads_dir = Path(Config.UPLOADS_DIR)
        self.thumbnails_dir = Path(Config.THUMBNAILS_DIR)

        self.storage_dir.mkdir(exist_ok=True)
        self.uploads_dir.mkdir(exist_ok=True)
        self.thumbnails_dir.mkdir(exist_ok=True)

    # def create_folder(self, user_id: str, folder_name: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
    #     """Create a new folder"""
    #     existing = self.file_repo.find_by_name_and_parent(folder_name, parent_id, user_id)
    #     if existing:
    #         raise ValueError(f"Folder '{folder_name}' already exists in this location")

    #     if parent_id:
    #         parent = self.file_repo.find_by_user_and_id(parent_id, user_id)
    #         if not parent:
    #             raise ValueError(f"Parent folder not found: {parent_id}")
    #         if parent["type"] != FileType.FOLDER.value:
    #             raise ValueError("Parent must be a folder")

    #     folder_id = generate_file_id()
    #     folder_data = {
    #         "id": folder_id,
    #         "user_id": user_id,
    #         "name": folder_name,
    #         "type": FileType.FOLDER.value,
    #         "parent_id": parent_id,
    #         "size": 0,
    #         "visibility": Visibility.PRIVATE.value,
    #         "path": "",
    #         "created_at": datetime.now().isoformat()
    #     }

    #     self.file_repo.create(folder_data)
    #     return {"folder_id": folder_id, "name": folder_name}

    def create_folder(self, user_id: str, folder_name: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new folder"""
        existing = self.file_repo.find_by_name_and_parent(folder_name, parent_id, user_id)
        if existing:
            raise ValueError(f"Folder '{folder_name}' already exists in this location")  # Fixed: added closing quote

        if parent_id:
            parent = self.file_repo.find_by_user_and_id(parent_id, user_id)
            if not parent:
                raise ValueError(f"Parent folder not found: {parent_id}")
            if parent["type"] != FileType.FOLDER.value:
                raise ValueError("Parent must be a folder")

        folder_id = generate_file_id()
        folder_data = {
            "id": folder_id,
            "user_id": user_id,
            "name": folder_name,
            "type": FileType.FOLDER.value,
            "parent_id": parent_id,
            "size": 0,
            "visibility": Visibility.PRIVATE.value,
            "path": "",
            "created_at": datetime.now().isoformat()
        }

        self.file_repo.create(folder_data)
        return {"folder_id": folder_id, "name": folder_name}

    def upload_file(self, user_id: str, filepath: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """Upload a file and return metadata"""
        source_path = Path(filepath)

        if not source_path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        if not validate_file_type(filepath):
            raise ValueError("File type not allowed: {source_path}")
        if parent_id:
            parent = self.file_repo.find_by_user_and_id(parent_id, user_id)
            if not parent:
                raise ValueError(f"Parent folder not found: {parent_id}")
            if parent["type"] != FileType.FOLDER.value:
                raise ValueError("Parent must be a folder")
        existing = self.file_repo.find_by_name_and_parent(source_path.name, parent_id, user_id)
        if existing:
            raise ValueError(f"File '{source_path.name}' already exists in the location")
        file_id = generate_file_id()
        file_size = source_path.stat().st_size
        file_type = get_file_type(filepath)
        dest_path = self.uploads_dir / f"{file_id}_{source_path.name}"
        shutil.copy2(source_path, dest_path)

        file_data = {
            "id": file_id,
            "user_id": user_id,
            "name": source_path.name,
            "type": file_type.value,
            "parent_id": parent_id,
            "size": file_size,
            "visibility": Visibility.PRIVATE.value,
            "path": str(dest_path),
            "created_at": datetime.now().isoformat()
        }
        

        self.file_repo.create(file_data)
        if file_type == FileType.IMAGE:
            try:
                success = generate_thumbnail(file_id, str(dest_path))
                if success:
                    print("Thumbnail generated successfully")
                else:
                    print("Failed to generate thumbnail")
            except Exception as e:
                print(f"Thumbnail generation error: {e}")
        return {
            "file_id": file_id,
            "filename": source_path.name,
            "size": file_size,
            "type": file_type.value,
            "upload_time": datetime.now().isoformat()
        }
    
    def list_files(self, user_id: str, parent_id: Optional[str] = None, show_public: bool = True) -> List[Dict[str, Any]]:
        """List all uploaded files"""
        if show_public:
            files = self.file_repo.find_public_files(parent_id)
        else:
            files = self.file_repo.find_by_parent(parent_id, user_id)
        return [self._format_file_info(f) for f in files]
    
    
    def get_file_info(self, file_id: str, user_id: str) -> Dict[str, Any]:
        """Get file information"""
        file_info = self.file_repo.find_by_user_and_id(file_id, user_id)
        if not file_info:
            raise FileNotFoundError(f"File not found: {file_id}")
        
        return {
            "file_id": file_info["id"],
            "filename": file_info["name"],
            "type": file_info["type"],
            "size": file_info.get("size", 0),
            "path": file_info.get("path", ""),
            "parent_id": file_info.get("parent_id"),
            "visibility": file_info["visibility"],
            "thumbnail_path": file_info.get("thumbnail_path"),
            "created_at": file_info["created_at"]
        }

    def delete_file(self, file_id: str, user_id: str) -> bool:
        """Delete a file"""
        file_info = self.file_repo.find_by_user_and_id(file_id, user_id)
        if not file_info:
            raise FileNotFoundError(f"File not found: {file_id}")
        
        # Delete physical file if it exists
        if file_info["path"]:
            file_path = Path(file_info["path"])
            if file_path.exists():
                file_path.unlink()
        
        # Delete thumbnail if it exists
        if file_info["type"] == FileType.IMAGE.value:
            thumb_path = self.thumbnails_dir / f"{file_id}.jpg"
            if thumb_path.exists():
                thumb_path.unlink()
        
        return self.file_repo.delete(file_id, user_id)
    
    def set_visibility(self, file_id: str, user_id: str, visibility: Visibility) -> bool:
        """Set file visibility"""
        file_info = self.file_repo.find_by_user_and_id(file_id, user_id)
        if not file_info:
            raise FileNotFoundError(f"File not found: {file_id}")
        
        return self.file_repo.update_visibility(file_id, user_id, visibility)
    
    def move_file(self, file_id: str, user_id: str, parent_id: Optional[str]) -> bool:
        """Move file to different parent"""
        file_info = self.file_repo.find_by_user_and_id(file_id, user_id)
        if not file_info:
            raise FileNotFoundError(f"File not found: {file_id}")
        
        # Validate parent if specified
        if parent_id:
            parent = self.file_repo.find_by_user_and_id(parent_id, user_id)
            if not parent:
                raise ValueError(f"Parent folder not found: {parent_id}")
            if parent["type"] != FileType.FOLDER.value:
                raise ValueError("Parent must be a folder")
        
        # Check for name conflicts
        existing = self.file_repo.find_by_name_and_parent(file_info["name"], parent_id, user_id)
        if existing and existing["id"] != file_id:
            raise ValueError(f"File '{file_info['name']}' already exists in destination")
        
        return self.file_repo.update_parent(file_id, user_id, parent_id)
    
    def _format_file_info(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Format file info for display"""
        return {
            "file_id": file_info["id"],
            "filename": file_info["name"],
            "type": file_info["type"],
            "size": file_info["size"],
            "parent_id": file_info.get("parent_id"),
            "visibility": file_info.get("visibility", Visibility.PRIVATE.value),
            "created_at": file_info["created_at"]
        }