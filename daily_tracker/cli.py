"""
Command-line interface for daily-tracker.
"""

import sys
import os
from .scheduler import run_scheduled_tracker


def main():
    """
    Main CLI entry point.
    """
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "start":
            run_scheduled_tracker()
        elif command == "version":
            from . import __version__
            print(f"daily-tracker v{__version__}")
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
Daily Tracker - Automated work tracking with AI summaries

Usage:
  daily-tracker              Start the tracker
  daily-tracker start        Start the tracker
  daily-tracker version      Show version
  daily-tracker help         Show this help

Configuration:
  Edit ~/.daily-tracker/config.py to customize settings

Requirements:
  - Ollama (with llama3.2 model)
  - Tesseract OCR
  - Discord webhook configured
    """)


if __name__ == "__main__":
    main()
