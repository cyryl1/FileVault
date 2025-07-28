from typing import Dict, Any, Optional
from vault.utils.helpers import validate_email, hash_password, verify_password
from vault.repositories.user_repository import UserRepository
from vault.repositories.session_repository import SessionRepository
import uuid
from datetime import datetime


class AuthService:
    """Authentication service"""
    
    def __init__(self, user_repo: UserRepository = None, session_repo: SessionRepository = None):
        self.user_repo = user_repo or UserRepository()
        self.session_repo = session_repo or SessionRepository()

    def register(self, email: str, password: str) -> Dict[str, Any]:
        """Registe a new user"""
        if not validate_email(email):
            raise ValueError("Invalid email format")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        user_id = str(uuid.uuid4())[:8]
        user_data = {
            "id": user_id,
            "email": email,
            "hashed_password": hash_password(password),
            "created_at": datetime.now().isoformat()
        }
        
        self.user_repo.create(user_data)
        return {"id": user_id, "email": email}
    
    def login(self, email: str, password: str) -> str:
        """Login user and return session token"""
        user = self.user_repo.find_by_email(email)
        if not user or not verify_password(password, user["hashed_password"]):
            raise ValueError("Incorrect email or password")
        
        return self.session_repo.create_session(user["id"])
    
    def logout(self, token: str) -> bool:
        """Logout user"""
        return self.session_repo.delete_session(token)
    
    def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get current user from session token"""
        user_id = self.session_repo.get_user_id(token)
        if user_id:
            user = self.user_repo.find_by_id(user_id)
            if user:
                return {"id": user["id"], "email": user["email"]}
        return None