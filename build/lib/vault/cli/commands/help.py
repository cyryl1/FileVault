from vault.cli.commands.base import Command
from typing import List, Dict
from vault.services.file_service import FileService
from vault.services.auth import AuthService

class HelpCommand(Command):
    "Show help information"

    def __init__(self, auth_service: AuthService, file_service: FileService, commands: Dict[str, Command]):
        super().__init__(auth_service, file_service)
        self.commands = commands

    def execute(self, args: List[str]) -> None:
        print("FileVault CLI - Available Commands:")
        print("=" * 40)

        print("\nAuthentication Commands: ")
        for name in ['register', 'login', 'whoami', 'logout']:
            if name in self.commands:
                print(f" {self.commands[name].get_help()}")

        print("\nFile Commands (require authentication):")
        for name in ['mkdir', 'upload', 'ls', 'read', 'delete', 'publish', 'unpublish', 'mv']:
            if name in self.commands:
                print(f" {self.commands[name].get_help()}")
        
        print("\nSystem Commands:")
        for name in ['celery']:
            if name in self.commands:
                print(f"  {self.commands[name].get_help()}")

        
        print("\nExample usage:")
        print(" vault register")
        print(" vault login")
        print(" mkdir Documents")
        print(" vault upload ./document.pdf Documents")
        print(" vault ls")
        print(" vault ls Documents")
        print(" vault ls --public")
        print(" vault read <file_id>")
        print(" vault delete <file_id>")
        print(" vault publish <file_id>")
        print(" vault unpublish <file_id>")
        print(" vault mv <file_id> <parent_id>")
        print(" vault whoami")
        print(" vault logout")
        print(" vault celery")

    def get_help(self) -> str:
        return "help - Show this help message"
