import redis
import json
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta
from vault.config import Config
from vault.utils.helpers import generate_session_token

class SessionService:
    """Session service using Redis"""

    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host=Config.REDIS_HOST,
                port=Config.REDIS_PORT,
                db=Config.REDIS_DB,
                decode_responses=True
            )

            self.redis_client.ping()
        except redis.ConnectionError:
            print("Warning: Redis not available. Using file-based sessions.")
            self.redis_client = None
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

                except (json.JSONDecoder, KeyError):
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
