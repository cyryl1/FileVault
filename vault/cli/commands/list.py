from vault.cli.commands.base import Command
from typing import List
from datetime import datetime
from vault.utils.helpers import format_file_size

class ListCommand(Command):
    "List all files"

    def execute(self, args: List[str]) -> None:
        parent_id = args[0] if args else None
        try:
            user = self.require_auth()
            # files = self.file_service.list_files(user["id"])
            query = {"user_id": user["id"]}
            if parent_id:
                query["parent_id"] = parent_id
            else:
                query["parent_id"] = None

            files = self.db.files.find(query).sort("type", -1).sort("name", 1)
            if not files:
                print("No files found")
                return
            
            print(f"{'ID':<12} | {'Name':<20} | {'Size':<10} | {'Uploaded At':<20}")
            print("-" * 75)

            for file in files:
                created_at = datetime.fromisoformat(file['created_at'])
                formatted_time = created_at.strftime("%Y-%m-%d %H:%M:%S")
                size_str = format_file_size(file['size']) if file['type'] == "file" else ""
                type_display = "[folder]" if file[type] == "folder" else "[file]"
                
                print(f"{file['id']:<12} | {type_display:<10} | {file['name']:<20} | {size_str:<10} | {formatted_time:<20}")

        except SystemExit:
            pass  # Error already printed by require_auth
        except Exception as e:
            print(f"Error listing files: {e}")

    def get_help(self) -> str:
        return "list - List all uploaded files"