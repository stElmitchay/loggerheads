"""
Command-line interface for loggerheads.
"""

import sys
import os
from .scheduler import run_scheduled_tracker
from .user_context import UserContext
from .autostart import install_autostart, uninstall_autostart, check_autostart_status


def main():
    """
    Main CLI entry point.
    """
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "start":
            run_scheduled_tracker()
        elif command == "setup":
            # Run interactive setup for user context
            context = UserContext()
            context.setup_interactive()
        elif command == "config":
            # Show current configuration
            context = UserContext()
            print(f"\n📄 Configuration file: {context.config_path}")
            print(f"👤 Role: {context.config.get('user_role', 'Not set')}")
            print(f"🏢 Industry: {context.config.get('industry', 'Not set')}")
            print(f"\nTo edit configuration, run: loggerheads setup")
        elif command == "install":
            # Install auto-start on boot
            install_autostart()
        elif command == "uninstall":
            # Uninstall auto-start
            uninstall_autostart()
        elif command == "status":
            # Check auto-start status
            check_autostart_status()
        elif command == "version":
            from . import __version__
            print(f"loggerheads v{__version__}")
        elif command == "help":
            print_help()
        else:
            print(f"Unknown command: {command}")
            print_help()
    else:
        # Default: start tracker
        run_scheduled_tracker()


def print_help():
    """Print help message."""
    print("""
Loggerheads - Automated work tracking with AI summaries

Usage:
  loggerheads              Start the tracker
  loggerheads start        Start the tracker
  loggerheads setup        Configure work context (role, industry, apps)
  loggerheads config       Show current configuration
  loggerheads install      Install auto-start on system boot
  loggerheads uninstall    Remove auto-start
  loggerheads status       Check auto-start status
  loggerheads version      Show version
  loggerheads help         Show this help

First Time Setup:
  1. Run 'loggerheads setup' to configure what counts as "work"
  2. Run 'loggerheads install' to enable auto-start on boot

  This helps the AI understand your role and filter out personal activities.

Configuration:
  Edit loggerheads/config.py to customize tracking settings
  Edit ~/.loggerheads_context.json to customize work categorization

Auto-start:
  Once installed, loggerheads will start automatically on system boot
  and run during configured work hours (9:30 AM - 4:30 PM, Mon-Fri)

Requirements:
  - Ollama (with llama3.2 model)
  - Tesseract OCR
  - Discord webhook configured
    """)


if __name__ == "__main__":
    main()
