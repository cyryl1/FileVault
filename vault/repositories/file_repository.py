from vault.repositories.base_repository import BaseRepository
from typing import Dict, Optional, Any, List
from config import Visibility

class FileRepository(BaseRepository):
    """Repository for file operations"""
    
    def __init__(self, db):
        super().__init__(db)
        self.files = db.files
        # Create indexes
        self.files.create_index("user_id")
        self.files.create_index("id", unique=True)
        self.files.create_index("parent_id")
        self.files.create_index("visibility")
    
    def create(self, file_data: Dict[str, Any]) -> str:
        """Create a file record"""
        result = self.files.insert_one(file_data)
        return file_data["id"]
    
    def find_by_id(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Find file by ID"""
        return self.files.find_one({"id": file_id})
    
    def find_by_user_and_id(self, file_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Find file by ID and user (ownership check)"""
        return self.files.find_one({"id": file_id, "user_id": user_id})
    
    def find_by_parent(self, parent_id: Optional[str], user_id: str) -> List[Dict[str, Any]]:
        """Find files by parent folder"""
        query = {"user_id": user_id, "parent_id": parent_id}
        return list(self.files.find(query).sort([("type", -1), ("name", 1)]))
    
    def find_public_files(self, parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Find public files"""
        query = {"visibility": Visibility.PUBLIC.value}
        if parent_id:
            query["parent_id"] = parent_id
        return list(self.files.find(query).sort([("type", -1), ("name", 1)]))
    
    def update_visibility(self, file_id: str, user_id: str, visibility: Visibility) -> bool:
        """Update file visibility"""
        result = self.files.update_one(
            {"id": file_id, "user_id": user_id},
            {"$set": {"visibility": visibility.value}}
        )
        return result.modified_count > 0
    
    def update_parent(self, file_id: str, user_id: str, parent_id: Optional[str]) -> bool:
        """Move file to different parent"""
        result = self.files.update_one(
            {"id": file_id, "user_id": user_id},
            {"$set": {"parent_id": parent_id}}
        )
        return result.modified_count > 0
    
    def delete(self, file_id: str, user_id: str) -> bool:
        """Delete a file"""
        result = self.files.delete_one({"id": file_id, "user_id": user_id})
        return result.deleted_count > 0
    
    def find_by_name_and_parent(self, name: str, parent_id: Optional[str], user_id: str) -> Optional[Dict[str, Any]]:
        """Find file by name and parent (for duplicate checking)"""
        return self.files.find_one({
            "name": name,
            "parent_id": parent_id,
            "user_id": user_id
        })