from typing import List
from vault.config import Visibility
from vault.cli.commands.base import Command

class UnpublishCommand(Command):
    """Make a file or folder private"""

    def execute(self, args: List[str]) -> None:
        if len(args) != 1:
            print("Error: unpublish command requires exactly one argument (file_id)")
            return
        try:
            user = self.require_auth()
            file_id = args[0]
            self.file_service.set_visibility(file_id, user["id"], Visibility.PRIVATE)
            print(f"File {file_id} is now private")
        except SystemExit:
            pass
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error unpublishing file: {e}")

    def get_help(self) -> str:
        return "unpublish <file_id> - Make a file or folder private"