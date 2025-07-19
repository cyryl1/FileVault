from vault.repositories.base_repository import BaseRepository
from typing import Dict, Optional, Any, List
from pathlib import Path
from config import Config
from vault.utils.helpers import generate_session_token
import json
from datetime import datetime, timedelta

class SessionRepository(BaseRepository):
    """Repository for session operations using Redis"""
    
    def __init__(self, redis_client=None):
        self.redis_client = redis_client
        self.session_file = Path(Config.STORAGE_DIR) / ".vault_session"
    
    def create_session(self, user_id: str) -> str:
        """Create a new session"""
        token = generate_session_token()
        
        if self.redis_client:
            self.redis_client.setex(
                f"session:{token}",
                Config.SESSION_TIMEOUT,
                user_id
            )
        else:
            session_data = {
                "token": token,
                "user_id": user_id,
                "expires_at": (datetime.now() + timedelta(seconds=Config.SESSION_TIMEOUT)).isoformat()
            }
            self.session_file.parent.mkdir(exist_ok=True)
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f)
        
        return token
    
    def get_user_id(self, token: str) -> Optional[str]:
        """Get user ID from session token"""
        if self.redis_client:
            user_id = self.redis_client.get(f"session:{token}")
            return user_id
        else:
            if self.session_file.exists():
                try:
                    with open(self.session_file, 'r') as f:
                        session_data = json.load(f)
                    
                    if session_data.get("token") == token:
                        expires_at = datetime.fromisoformat(session_data["expires_at"])
                        if datetime.now() < expires_at:
                            return session_data["user_id"]
                        else:
                            self.session_file.unlink()
                except (json.JSONDecodeError, KeyError):
                    pass
            return None
    
    def delete_session(self, token: str) -> bool:
        """Delete a session"""
        if self.redis_client:
            result = self.redis_client.delete(f"session:{token}")
            return result > 0
        else:
            if self.session_file.exists():
                self.session_file.unlink()
                return True
            return False
