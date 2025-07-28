from typing import List
from vault.cli.commands.base import Command
import subprocess
import sys

class CeleryCommand(Command):
    """Start the Celery worker"""

    def execute(self, args: List[str]) -> None:
        try:
            print("Starting Celery worker...")
            subprocess.run([
                sys.executable, "-m", "celery", "-A", "vault.workers.thumbnail_worker", "worker", "--loglevel=info"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error starting Celery worker: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def get_help(self):
        return "celery - Start the Celery worker for background tasks"