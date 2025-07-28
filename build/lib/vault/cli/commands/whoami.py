from vault.cli.commands.base import Command
from typing import List

class WhoAmICommand(Command):
    """Show current user"""
    def execute(self, args: List[str]) -> None:
        try:
            user = self.require_auth()
            print(f"Logged in as: {user['email']}")
            print(f"User ID: {user['id']}")
        except SystemExit:
            pass
        except Exception as e:
            print(f"Error: {e}")

    def get_help(self) -> str:
        return "whoami - Show current logged in user"