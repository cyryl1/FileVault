from vault.services.file_service import FileService
from vault.services.auth import AuthService
from vault.cli.commands.uploads import UploadCommand
from vault.cli.commands.list import ListCommand
from vault.cli.commands.read import ReadCommand
from vault.cli.commands.delete import DeleteCommand
from vault.cli.commands.help import HelpCommand
from vault.cli.commands.register import RegisterCommand
from vault.cli.commands.login import LoginCommand
from vault.cli.commands.logout import LogoutCommand
from vault.cli.commands.whoami import WhoAmICommand
from vault.cli.commands.mkdir import MkdirCommand
from vault.cli.commands.mv import MvCommand
from vault.cli.commands.publish import PublishCommand
from vault.cli.commands.unpublish import UnpublishCommand
from vault.cli.commands.celery import CeleryCommand

from vault.repositories.file_repository import FileRepository
from vault.repositories.user_repository import UserRepository
from vault.repositories.session_repository import SessionRepository

from typing import List

class CommandRouter:
    """Routes command to appropriate handlers"""

    def __init__(self):
        self.file_repo = FileRepository()
        self.user_repo = UserRepository()
        self.session_repo = SessionRepository()
        self.file_service = FileService(self.file_repo)
        self.auth_service = AuthService(self.user_repo, self.session_repo)
        self.commands = {
            'register': RegisterCommand(self.auth_service, self.file_service),
            'login': LoginCommand(self.auth_service, self.file_service),
            'logout': LogoutCommand(self.auth_service, self.file_service),
            'whoami': WhoAmICommand(self.auth_service, self.file_service),
            'upload': UploadCommand(self.auth_service, self.file_service),
            'ls': ListCommand(self.auth_service, self.file_service),
            'read': ReadCommand(self.auth_service, self.file_service),
            'delete': DeleteCommand(self.auth_service, self.file_service),
            'mkdir': MkdirCommand(self.auth_service, self.file_service),
            'publish': PublishCommand(self.auth_service, self.file_service),
            'upublish': UnpublishCommand(self.auth_service, self.file_service),
            'mv': MvCommand(self.auth_service, self.file_service),
            'celery': CeleryCommand(self.auth_service, self.file_service)
        }
        self.commands['help'] = HelpCommand(self.auth_service, self.file_service, self.commands)

    def route(self, command_name: str, args: List[str]) -> None:
        """Route command to appropriate handler"""
        if command_name in self.commands:
            self.commands[command_name].execute(args)
        else:
            print(f"Unknown command: {command_name}")
            print("Use `vault help` to see available commands")