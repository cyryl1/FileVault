from vault.cli.commands.base import Command
from typing import List
from datetime import datetime
from vault.utils.helpers import format_file_size

class ReadCommand(Command):
    "Read file metadata"
    
    def execute(self, args: List[str]) -> None:
        if len(args) != 1:
            print("Error: read command requires exactly one argument (file_id)")
            return

        try:
            user = self.require_auth()
            file_id = args[0]

            file_info = self.file_service.get_file_info(file_id, user["id"])
            created_at = datetime.fromisoformat(file_info['created_at'])
            formatted_time = created_at.strftime("%Y-%m-%d %H:%M:%S")

            print(f"Filename: {file_info['filename']}")
            print(f"Size: {format_file_size(file_info['size'])}")
            print(f"Path: {file_info['path']}")
            print(f"Uploaded at: {formatted_time}")

        except SystemExit:
            pass
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error reading file info: {e}")

    def get_help(self):
        return "read <file_id> Display metadata for a specific file"
    