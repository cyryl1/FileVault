from typing import Dict, Any, Optional
from vault.services.databse import DatabaseService
from vault.services.session import SessionService
from vault.utils.helpers import validate_email

class AuthService:
    """Authentication service"""
    
    def __init__(self):
        self.db = DatabaseService()
        self.session = SessionService()

    def register(self, email: str, password: str) -> Dict[str, Any]:
        """Registe a new user"""
        if not validate_email(email):
            raise ValueError("Invalid email format")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        return self.db.create_user(email, password)
    
    def login(self, email: str, password: str) -> str:
        """Login user and return session token"""

        user = self.db.authenticate_user(email, password)
        if not user:
            raise ValueError("Invalid email or password")
        
        return self.session.create_session(user["id"])
    
    def logout(self, token: str) -> bool:
        """Logout user"""
        return self.session.delete_session(token)
    
    def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get current user from session token"""
        user_id = self.session.get_user_id(token)
        if user_id:
            return self.db.get_user_by_id(user_id)
        return