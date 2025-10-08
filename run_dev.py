#!/usr/bin/env python3
"""
Development runner - use this to test locally.
Usage: python run_dev.py
"""

from loggerheads.scheduler import run_scheduled_tracker

if __name__ == "__main__":
    run_scheduled_tracker()
