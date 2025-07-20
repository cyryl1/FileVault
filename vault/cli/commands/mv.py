from vault.cli.commands.base import Command
from typing import List

class MvCommand(Command):
    """Move a file or folder to another folder"""

    def execute(self, args: List[str]) -> None:
        if len(args) != 2:
            print("Error: mv command requires exactly two arguments (file_id parent_id)")
            return
        
        try:
            user = self.require_auth()
            file_id, parent_id = args
            self.file_service.move_file(file_id, user["id"], parent_id)
            print(f"Moved {file_id} to folder {parent_id}")
        except SystemExit:
            pass
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error moving file: {e}")

    def get_help(self) -> str:
        return "mv <file_id> <parent_id> - Move a file or folder to another folder"
