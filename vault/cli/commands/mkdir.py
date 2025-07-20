from vault.cli.commands.base import Command
from typing import List


class MkdirCommand(Command):
    """Create a file"""
    
    def execute(self, args: List[str]) -> None:
        if len(args) < 1 or len(args) > 2:
            print("Error: mkdir requries folder_name [parent_id]")
            return
        try:
            user = self.require_auth()
            folder_name = args[0]
            parent_id = args[1] if len(args) > 1 else None
            
            result = self.file_service.create_folder(user["id"], folder_name, parent_id)
            print(f"Folder created: {result['name']}")
            
        except SystemExit:
            pass
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error creating folder: {e}")

    def get_help(self) -> str:
        return "mkdir <folder_nake> [parent_id] - Create a new folder"