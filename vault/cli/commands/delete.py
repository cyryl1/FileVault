from vault.cli.commands.base import Command
from typing import List

class DeleteCommand(Command):
    """Delete a file"""

    def execute(self, args: List[str]):
        if len(args) != 1:
            print("Error: delete command requires exactly one argument (file_id)")
            return
        
        file_id = args[0]

        try:
            self.file_service.delete_file(file_id)
            print("file deleted successfully!")

        except FileNotFoundError as e:
            print(f"Error as e")
        except Exception as e:
            print(f"Error deleting file: {e}")

    def get_help(self) -> str:
        return "delete <file_id> - Delete a file  from  the vault"
