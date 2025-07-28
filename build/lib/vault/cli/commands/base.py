import sys
import os
import json
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from vault.services.file_service import FileService
from vault.services.auth import AuthService
from vault.config import Config

class Command(ABC):
    """Abstract base class for commands"""
    def __init__(self, auth_service: AuthService, file_service: FileService):
        self.auth_service = auth_service
        self.file_service = file_service

    @abstractmethod
    def execute(self, args: List[str]) -> None:
        """Execute the command"""
        pass

    @abstractmethod
    def get_help(self) -> str:
        """Get help text for the command"""
        pass

    def require_auth(self) -> Dict[str, Any]:
        """Require auth and return currnt user"""
        token = self._get_session_token()
        if not token:
            print("Error: You must be logged in to use this command")
            print("Use 'vault login' to authenticate")
            sys.exit(1)
        user = self.auth_service.get_current_user(token)
        if not user:
            print("Error: Invalid or expired session")
            print("Use 'vault login' to authenticate")
            sys.exit(1)

        return user
    
    def _get_session_token(self) -> Optional[str]:
        """Get session token from environment or file"""

        token = os.getenv('VAULT_SESSION_TOKEN')
        if token:
            return token
        
        session_file = Path(Config.STORAGE_DIR) / ".vault_session"
        if session_file.exists():
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                return session_data.get("token")
            except (json.JSONDecodeError, KeyError):
                pass
        return None

