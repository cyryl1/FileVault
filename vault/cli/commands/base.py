from abc import ABC, abstractmethod
from typing import List
from vault.services.file_service import FileService

class Command(ABC):
    """Abstract base class for commands"""
    def __init__(self, file_service: FileService):
        self.file_service = file_service

    @abstractmethod
    def execute(self, args: List[str]) -> None:
        """Execute the command"""
        pass

    @abstractmethod
    def get_help(self) -> str:
        """Get help text for the command"""
        pass