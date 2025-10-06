"""
Scheduler for running activity tracker as a background service during business hours.
Runs Monday-Friday, 9:30am-4:30pm by default.
Captures screenshots, performs OCR, and generates end-of-day summary.
"""

import time
import threading
import os
from datetime import datetime
from activity_tracker import track_activity
from database import init_db, save_logs, save_screenshot, get_screenshots
from summarizer import summarize_logs
from screen_recorder import capture_screenshot
from ocr_processor import extract_text_from_image
from text_analyzer import analyze_text, generate_structured_summary, format_summary_for_display
from config import (
    WORK_START_TIME,
    WORK_END_TIME,
    WORK_DAYS,
    TRACKING_INTERVAL,
    SCREENSHOT_INTERVAL,
    SCREENSHOT_DIR,
    TARGET_WINDOW
)


def is_work_hours():
    """
    Check if current time is within work hours on a work day.

    Returns:
        bool: True if within work hours, False otherwise
    """
    now = datetime.now()

    # Check if today is a work day
    if now.weekday() not in WORK_DAYS:
        return False

    # Parse work hours
    start_hour, start_minute = map(int, WORK_START_TIME.split(':'))
    end_hour, end_minute = map(int, WORK_END_TIME.split(':'))

    # Convert to minutes for easier comparison
    current_minutes = now.hour * 60 + now.minute
    start_minutes = start_hour * 60 + start_minute
    end_minutes = end_hour * 60 + end_minute

    return start_minutes <= current_minutes < end_minutes


def track_single_activity():
    """Track a single activity snapshot."""
    try:
        import pygetwindow as gw
        window = gw.getActiveWindow()
        if window:
            title = window.title
            if callable(title):
                title = title()
            if title:
                return str(title)
    except Exception as e:
        print(f"Error tracking activity: {e}")
    return None


def process_and_generate_summary():
    """
    Process all screenshots with OCR and generate the work summary.
    """
    print("\n🔄 Processing screenshots with OCR...")

    # Get all screenshots from database
    screenshots = get_screenshots()

    if not screenshots:
        print("No screenshots to process.")
        return

    screenshot_data = []

    for screenshot_id, file_path, timestamp, extracted_text in screenshots:
        # If text not already extracted, do OCR now
        if not extracted_text or extracted_text.strip() == "":
            if os.path.exists(file_path):
                print(f"  Processing: {os.path.basename(file_path)}")
                extracted_text = extract_text_from_image(file_path)
                # Update database with extracted text
                # Note: We'd need an update function, for now just use it

        # Analyze the text
        if extracted_text and extracted_text.strip():
            analysis = analyze_text(extracted_text)
            screenshot_data.append({
                'timestamp': timestamp,
                'analysis': analysis
            })

    # Generate summary
    if screenshot_data:
        # Check if today is Friday (4 = Friday in weekday())
        is_friday = datetime.now().weekday() == 4

        summary = generate_structured_summary(screenshot_data, is_friday=is_friday)
        formatted_summary = format_summary_for_display(summary)

        print("\n" + "="*70)
        print("📊 END OF DAY WORK SUMMARY")
        print("="*70)
        print(formatted_summary)
        print("="*70 + "\n")
    else:
        print("No text extracted from screenshots.")


def run_scheduled_tracker():
    """
    Main scheduler loop that tracks activity during business hours.
    Captures screenshots, performs OCR, and generates end-of-day summary.
    """
    init_db()
    print("🚀 Activity tracker service started")
    print(f"📅 Work hours: {WORK_START_TIME} - {WORK_END_TIME}")
    print(f"📆 Work days: {', '.join(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'][day] for day in WORK_DAYS)}")
    print(f"📸 Screenshot interval: {SCREENSHOT_INTERVAL} seconds")
    print("Press Ctrl+C to stop the service\n")

    session_logs = []
    last_status = None
    last_screenshot_time = time.time()
    last_minute_log = time.time()
    screenshot_count = 0
    activity_count = 0

    try:
        while True:
            current_status = is_work_hours()

            # Status change notifications
            if current_status != last_status:
                if current_status:
                    print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Work hours started - tracking active")
                    last_screenshot_time = time.time()  # Reset screenshot timer
                    last_minute_log = time.time()
                    screenshot_count = 0
                    activity_count = 0
                else:
                    print(f"⏸️  [{datetime.now().strftime('%H:%M:%S')}] Work hours ended - generating summary...")

                    # Save activity logs
                    if session_logs:
                        save_logs(session_logs)
                        session_logs = []

                    # Process screenshots and generate summary
                    process_and_generate_summary()

                    print(f"\n📸 Total screenshots captured today: {screenshot_count}")
                    screenshot_count = 0
                    activity_count = 0

                last_status = current_status

            # Track activity if within work hours
            if current_status:
                activity = track_single_activity()
                if activity:
                    session_logs.append(activity)
                    activity_count += 1

                # Capture screenshot at intervals
                current_time = time.time()
                if current_time - last_screenshot_time >= SCREENSHOT_INTERVAL:
                    screenshot_path = capture_screenshot(SCREENSHOT_DIR)
                    if screenshot_path:
                        # Extract text immediately
                        extracted_text = extract_text_from_image(screenshot_path)
                        # Save to database
                        save_screenshot(screenshot_path, extracted_text)
                        screenshot_count += 1

                    last_screenshot_time = current_time

                # Log status every minute
                if current_time - last_minute_log >= 60:
                    print(f"⏱️  [{datetime.now().strftime('%H:%M:%S')}] Status: {screenshot_count} screenshots, {activity_count} activities tracked")
                    last_minute_log = current_time

            # Sleep for tracking interval
            time.sleep(TRACKING_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n🛑 Service stopped by user")

        # Save any remaining logs
        if session_logs:
            save_logs(session_logs)

        # Process and generate final summary
        print("\nGenerating final summary...")
        process_and_generate_summary()

        print(f"\n📸 Total screenshots captured: {screenshot_count}")


def run_as_daemon():
    """
    Run the tracker as a background daemon thread.
    """
    daemon_thread = threading.Thread(target=run_scheduled_tracker, daemon=True)
    daemon_thread.start()
    print("Daemon started in background")
    return daemon_thread


if __name__ == "__main__":
    run_scheduled_tracker()
