import getpass
import json
from vault.cli.commands.base import Command
from typing import List
from pathlib import Path
from vault.config import Config
from datetime import datetime, timedelta

class LoginCommand(Command):
    """Login a user"""

    def execute(self, args: List[str]) -> None:
        try:
            email = input("Email: ").strip()
            password = getpass.getpass("Password: ")

            token = self.auth_service.login(email, password)
            print("Login successful!")
            print(f"Your session token: {token}")

            session_file = Path(Config.STORAGE_DIR) / ".vault_session"
            session_file.parent.mkdir(exist_ok=True)

            session_data = {
                "token": token,
                "user_id": self.auth_service.get_current_user(token)["id"],
                "expires_at": (datetime.now() + timedelta(seconds=Config.SESSION_TIMEOUT)).isoformat()
            }

            with open(session_file, 'w') as f:
                json.dump(session_data, f)
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error logging in: {e}")

    def get_help(self) -> str:
        return "login - Login to your account"
