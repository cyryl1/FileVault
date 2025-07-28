from vault.cli.commands.base import Command
from typing import List
from datetime import datetime
from vault.utils.helpers import format_file_size
from vault.config import FileType

class ListCommand(Command):
    "List all files"

    def execute(self, args: List[str]) -> None:
        try:
            user = self.require_auth()
            parent_id = None
            show_public = "--public" in args
            if args and not show_public:
                parent_id = args[0]
            elif args and show_public and len(args) > 1:
                parent_id = args[0] if args[0] != '--public' else args[1]
            files = self.file_service.list_files(user["id"], parent_id, show_public)
            
            if not files:
                print("No files found")
                return

            print(f"{'Type':<8} | {'ID':<12} | {'Name':<25} | {'Size':<10} | {'Visibility':<10} | {'Created':<20}")
            print("-" * 95)

            for file in files:
                created_at = datetime.fromisoformat(file['created_at'])
                formatted_time = created_at.strftime("%Y-%m-%d %H:%M:%S")
                
                if file['type'] == FileType.FOLDER.value:
                    type_display = "[folder]"
                    size_display = "-"
                elif file['type'] == FileType.IMAGE.value:
                    type_display = "[image]"
                    size_display = format_file_size(file['size'])
                else:
                    type_display = "[file]"
                    size_display = format_file_size(file['size'])
                

                print(f"{type_display:<8} | {file['file_id']:<12} | {file['filename']:<25} | {size_display:<10} | {file['visibility']:<10} | {formatted_time:<20}")

        except SystemExit:
            pass  # Error already printed by require_auth
        except Exception as e:
            print(f"Error listing files: {e}")

    def get_help(self) -> str:
        return "list - List all uploaded files"