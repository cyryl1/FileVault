from typing import Dict, Optional, Any, List
from vault.config import Visibility
from vault.config import Config
from pymongo import MongoClient

class FileRepository:
    """Repository for file operations"""
    
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.DATABASE_NAME]
        self.files = self.db.files
        # Create indexes
        self.files.create_index("user_id")
        self.files.create_index("id", unique=True)
        self.files.create_index("parent_id")
        self.files.create_index("visibility")
    
    def create(self, file_data: Dict[str, Any]) -> str:
        """Create a file record"""
        self.files.insert_one(file_data)
        return file_data["id"]
    
    def find_by_id(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Find file by ID"""
        return self.files.find_one({"id": file_id})
    
    def find_by_user_and_id(self, file_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Find file by ID and user (ownership check)"""
        return self.files.find_one({"id": file_id, "user_id": user_id})
    
    def find_by_parent(self, parent_id: Optional[str], user_id: str) -> List[Dict[str, Any]]:
        """Find files by parent folder"""
        query = {"user_id": user_id}
        if parent_id is not None:
            query["parent_id"] = parent_id
        else:
            query["parent_id"] = None
        return list(self.files.find(query).sort([("type", -1), ("name", 1)]))
    
    def find_public_files(self, parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Find public files"""
        query = {"visibility": Visibility.PUBLIC.value}
        if parent_id:
            query["parent_id"] = parent_id
        else:
            query["parent_id"] = None
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
        query = {"name": name, "user_id": user_id}
        if parent_id is not None:
            query["parent_id"] = parent_id
        else:
            query["parent_id"] = None
        return self.files.find_one(query)
    
    def count(self) -> int:
        """Count total files"""
        total_file = self.files.count_documents({})
        return total_file