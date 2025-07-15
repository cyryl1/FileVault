from vault.services.file_service import FileService
from vault.cli.commands.uploads import UploadCommand
from vault.cli.commands.list import ListCommand
from vault.cli.commands.read import ReadCommand
from vault.cli.commands.delete import DeleteCommand
from vault.cli.commands.help import HelpCommand
from typing import List

class CommandRouter:
    """Routes command to appropriate handlers"""

    def __init__(self):
        self.file_service = FileService()
        self.commands = {
            'upload': UploadCommand(self.file_service),
            'list': ListCommand(self.file_service),
            'read': ReadCommand(self.file_service),
            'delete': DeleteCommand(self.file_service)
        }
        self.commands['help'] = HelpCommand(self.file_service, self.commands)

    def route(self, command_name: str, args: List[str]) -> None:
        """Route command to appropriate handler"""
        if command_name in self.commands:
            self.commands[command_name].execute(args)
        else:
            print(f"Unknown command: {command_name}")
            print("Use `vault help` to see available commands")
