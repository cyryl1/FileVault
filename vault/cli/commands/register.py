import getpass
from vault.cli.commands.base import Command
from typing import List


class RegisterCommand(Command):
    """Register a new user"""

    def execute(self, args: List[str]) -> None:
        try:
            email = input("Email: ").strip()
            password = getpass.getpass("Password: ")

            user = self.auth_service.register(email, password)
            print("User registered successfully!")
            print(f"User ID: {user['id']}")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error registering user:m {e}")

    def get_help(self) -> str:
        return "register - Register a new user account"

