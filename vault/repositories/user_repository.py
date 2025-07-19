from vault.repositories.base_repository import BaseRepository
from typing import Dict, Any, List, Optional
from pymongo.errors import DuplicateKeyError

class UserRepository(BaseRepository):
    """Repository for user operations"""
    def __init__(self, db):
        super().__init__(db)
        self.users = db.users

        self.users.create_index("email", unique=True)
        self.users.create_index("id", unique=True)

    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        try:
            result = self.users.insert_one(user_data)
            return user_data
        except DuplicateKeyError:
            raise ValueError("Email alreadu registered")
        
    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find user by email"""
        return self.users.find_one({"email": email})
    
    def find_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Find user by ID"""
        return self.users.find_one({"id": user_id})