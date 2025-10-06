"""
Configuration settings for the activity tracker.
"""

import os

# Screenshot settings
SCREENSHOT_INTERVAL = 10  # seconds between screenshots
SCREENSHOT_DIR = "./screenshots/"  # directory to store screenshots
AUTO_CLEANUP_DAYS = 1  # delete screenshots older than X days (0 = no auto-cleanup)

# Activity tracking settings
TRACKING_INTERVAL = 2  # seconds between activity checks

# Database settings
DATABASE_NAME = "activity_log.db"

# Scheduled service settings
WORK_START_TIME = "09:30"  # Start time in HH:MM format (24-hour)
WORK_END_TIME = "16:30"    # End time in HH:MM format (24-hour)
WORK_DAYS = [0, 1, 2, 3, 4]  # Monday=0, Tuesday=1, ..., Sunday=6 (Mon-Fri)

# Target window for tracking (None = track all activity)
TARGET_WINDOW = None  # e.g., "Chrome", "VSCode", "PyCharm", or None for continuous tracking

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
