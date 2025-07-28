from typing import List
from vault.services.auth import AuthService
from vault.config import Config
from vault.cli.commands.base import Command
from pathlib import Path

class LogoutCommand(Command):
    """Logout a user"""

    def execute(self, args: List[str]) -> None:
        try:
            token = self._get_session_token()
            if token:
                self.auth_service.logout(token)

            session_file = Path(Config.STORAGE_DIR) / ".vault_session"

            if session_file.exists():
                session_file.unlink()

            print("Logged out succesfully!")

        except Exception as e:
            print(f"Error logging our: {e}")

    def get_help(self) -> str:
        return "logout - Logout from your account"
    
