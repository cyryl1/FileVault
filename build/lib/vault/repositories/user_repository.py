from typing import Dict, Any, Optional
from pymongo.errors import DuplicateKeyError
from vault.utils.helpers import hash_password
from vault.config import Config
from pymongo import MongoClient

class UserRepository:
    """Repository for user operations"""
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.DATABASE_NAME]
        self.users = self.db.users

        self.users.create_index("email", unique=True)
        self.users.create_index("id", unique=True)

    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        
        try:
            self.users.insert_one(user_data)
            return {"id": user_data["id"], "email": user_data["email"]}
        except DuplicateKeyError:
            raise ValueError("Email alreadu registered")
        
    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find user by email"""
        user = self.users.find_one({"email": email})
        if user:
            return {
                "id": user["id"], 
                "email": user["email"],
                "password": user["hashed_password"]
            }
        return None
    
    def find_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Find user by ID"""
        user = self.users.find_one({"id": user_id})
        if user:
            return {
                "id": user["id"], 
                "email": user["email"],
                "password": user["hashed_password"]
            }
        return None

    def count(self) -> int:
        """Count total users"""
        total_users = self.users.count_documents({})
        return total_users

