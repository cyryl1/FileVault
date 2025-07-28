import sys
from vault.cli.command_router import CommandRouter

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: vault <command> [arguments]")
        print("Use 'vault help' to see available commands")
        return
    command_name = sys.argv[1]
    args = sys.argv[2:]
    router = CommandRouter()
    router.route(command_name, args)

if __name__ == "__main__":
    main()