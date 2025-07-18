from vault.cli.commands.base import Command
from typing import List
from datetime import datetime
from vault.utils.helpers import format_file_size

class ListCommand(Command):
    "List all files"

    # def execute(self, args: List[str]) -> None:
    #     try:
    #         files = self.file_service.list_files()

    #         if not files:
    #             print("No files found")
    #             return
            
    #         print(f"{'ID':<12} | {'Name':<20} | {'Size':<10} | {'Uploaded At':<20}")
    #         print("-" * 70)

    #         for file in files:
    #             upload_time = datetime.fromisoformat(file['upload_time'])
    #             formatted_time = upload_time.strftime("%Y-%m-%d %H:%M:%S")
    #             size_str = format_file_size(file['size'])

    #             print(f"{file['file_id']:<12} | {file['filename']:<20} | {size_str:<10} | {formatted_time:<20}")

    #     except Exception as e:
    #         print(f"Error listing files: {e}")

    def execute(self, args: List[str]) -> None:
        try:
            user = self.require_auth()
            files = self.file_service.list_files(user["id"])

            if not files:
                print("No files found")
                return
            
            print(f"{'ID':<12} | {'Name':<20} | {'Size':<10} | {'Uploaded At':<20}")
            print("-" * 70)

            for file in files:
                created_at = datetime.fromisoformat(file['created_at'])
                formatted_time = created_at.strftime("%Y-%m-%d %H:%M:%S")
                size_str = format_file_size(file['size'])
                
                print(f"{file['file_id']:<12} | {file['filename']:<20} | {size_str:<10} | {formatted_time:<20}")

        except SystemExit:
            pass  # Error already printed by require_auth
        except Exception as e:
            print(f"Error listing files: {e}")

    def get_help(self) -> str:
        return "list - List all uploaded files"