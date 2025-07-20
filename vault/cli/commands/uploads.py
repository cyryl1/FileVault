from vault.cli.commands.base import Command
from typing import List
from vault.config import FileType

class UploadCommand(Command):
    """Upload a file"""

    def execute(self, args: List[str]) -> None:
        if len(args) < 1:
            print("Error: upload command requires a file path")
            return
        

        try:
            user = self.require_auth()
            filepath = args[0]
            parent_id = None

            if len(args) > 1:
                folder_name = args[1]

                files = self.file_service.list_files(user["id"], None)
                folder = next((f for f in files if f["filename"] == folder_name and f["type"] == FileType.FOLDER.value), None)

                if folder:
                    parent_id = folder["file_id"]
                else:
                    result = self.file_service.create_folder(user["id"], folder_name)
                    parent_id = result["folder_id"]
                    print(f"Created folder: {folder_name}")

            result = self.file_service.upload_file(user["id"], filepath, parent_id)
            print(f"File uploaded successfully! ID: {result['file_id']}")

            if result["type"] == FileType.IMAGE.value:
                print("Thumbnail generation Scheduled...")

        except SystemExit:
            pass
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def get_help(self) -> str:
        return "upload <filepath> - Upload a file to the vault"
    
