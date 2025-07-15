from vault.cli.commands.base import Command
from typing import List

class UploadCommand(Command):
    """Upload a file"""

    def execute(self, args: List[str]) -> None:
        if len(args) != 1:
            print("Error: upload command requires exactly one argument (filepath)")
            return
        filepath = args[0]

        try:
            result = self.file_service.upload_file(filepath)
            print(f"File uploaded successfully! ID: {result['file_id']}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def get_help(self) -> str:
        return "upload <filepath> - Upload a file to the vault"
    
