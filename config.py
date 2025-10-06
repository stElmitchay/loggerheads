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

# Discord webhook settings
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1424700386476032124/XfMUExyX9K24wY4emDSGNRPGwisFsAv5k1MGlweqjn7LVXew1GubjaolQfuLqAI6a_QX"  # Add your Discord webhook URL here
SEND_TO_DISCORD = True  # Set to True to enable Discord notifications

# AI Summarization settings (using Ollama local LLM)
USE_AI_SUMMARIZATION = True  # Set to False to use basic keyword extraction instead
OLLAMA_MODEL = "llama3.2"  # Ollama model to use (llama3.2, mistral, phi3, etc.)
OLLAMA_API_URL = "http://localhost:11434"  # Ollama API endpoint

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
