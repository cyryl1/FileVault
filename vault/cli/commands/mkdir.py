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
            parent_id = args[1] if len(args) == 2 else None
            if parent_id:
                parent = self.db.get_file_by_id(parent_id, user["id"])
                if not parent or parent["type"] != "folder":
                    raise ValueError("Invalid or non-folder parent_id")
            folder_data = {
                "name": folder_name,
                "type": "folder",
                "parent_id": parent_id
            }

            folder_id = self.db.create_file(user["id"], folder_data)
            print(f"Folder created: {folder_name} (ID: {folder_id})")
        except SystemExit:
            pass
        except ValueError as e:
            print(f"Error creating folder: {e}")

    def get_help(self) -> str:
        return "mkdir <folder_nake> [parent_id] - Create a new folder"