import uuid
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from vault.config import Config
from typing import Dict, Optional, List, Any
from vault.utils.helpers import hash_password, verify_password


class DatabaseService:
    """Database service for MongoDB operations"""

    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.DATABASE_NAME]
        self.users = self.db.users
        self.files = self.db.files

        self.users.create_index("email", unique=True)
        self.files.create_index("user_id")
        self.files.create_index("file_id", unique=True)

    def create_user(self, email: str, password: str) -> Dict[str, Any]:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        hashed_password = hash_password(password)

        user_doc = {
            "id": user_id,
            "email": email,
            "hashed_password": hashed_password,
            "created_at": datetime.now().isoformat()
        }

        try:
            self.users.insert_one(user_doc)
            return {"id": user_id, "email": email}
        except DuplicateKeyError:
            raise ValueError("Emailalready registered")
        
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user credentials"""
        user = self.users.find_one({"email": email})
        if user and verify_password(password, user["hashed_password"]):
            return {"id": user["id"], "email": user["email"]}
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        user = self.users.find_one({"id": user_id})
        if user:
            return {"id": user["id"], "email": user["email"]}
        return None

    def create_file(self, user_id: str, file_data: Dict[str, Any]) -> str:
        """Create a file record"""
        file_id = str(uuid.uuid4())[:8]
        file_doc = {
            "id": file_id,
            "user_id": user_id,
            "name": file_data["name"],
            "size": file_data["size"],
            "path": file_data["path"],
            "created_at": datetime.now().isoformat()
        }

        self.files.insert_one(file_doc)
        return file_id
    
    def get_user_files(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all files for a user"""
        files = self.files.find({"user_id": user_id}).sort("created_at", -1)
        return list(files)
    
    def get_file_by_id(self, file_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get file by ID (only if owned by user)"""
        return self.files.find_one({"id": file_id, "user_id": user_id})
    
    def delete_file(self, file_id: str, user_id: str) -> bool:
        """Delete a file (only if owned by user)"""
        result = self.files.delete_one({"id": file_id, "user_id": user_id})
        return result.deleted_count > 0

