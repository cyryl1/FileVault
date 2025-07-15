from vault.cli.commands.base import Command
from typing import List, Dict
from vault.services.file_service import FileService

class HelpCommand(Command):
    "Show help information"

    def __init__(self, file_service: FileService, commands: Dict[str, Command]):
        super().__init__(file_service)
        self.commands = commands

    def execute(self, args: List[str]) -> None:
        print("FileVault CLI - Available Commands:")
        print("=" * 40)
        for name, command in self.commands.items():
            if name != 'help':
                print(f" {command.get_help}")
        print("\nExample usage:")
        print(" vault upload ./document.pdf")
        print(" vault list")
        print(" vault read 8f7a1c21")
        print(" vault delete 8f7a1c21")

    def get_help(self) -> str:
        return "help - Show this help message"
