import os
import time
import subprocess
from datetime import datetime
from pathlib import Path


def check_screen_recording_permission():
    """
    Check if the app has screen recording permission on macOS.
    Returns True if permission is granted, False otherwise.
    """
    try:
        # Try to take a test screenshot to check permissions
        test_path = "/tmp/test_screenshot.png"
        result = subprocess.run(
            ["screencapture", "-x", test_path],
            capture_output=True,
            timeout=2
        )

        # Check if file was created
        if os.path.exists(test_path):
            os.remove(test_path)
            return True
        return False
    except Exception as e:
        print(f"Permission check failed: {e}")
        return False


def ensure_screenshot_directory(directory="screenshots"):
    """
    Create screenshot directory if it doesn't exist.
    Returns the absolute path to the directory.
    """
    screenshot_dir = Path(directory)
    screenshot_dir.mkdir(exist_ok=True)
    return screenshot_dir.absolute()


def capture_screenshot(save_directory="screenshots"):
    """
    Capture a single screenshot and save it with a timestamp.
    Returns the file path of the captured screenshot, or None if failed.
    """
    try:
        # Ensure directory exists
        screenshot_dir = ensure_screenshot_directory(save_directory)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = screenshot_dir / filename

        # Capture screenshot using macOS screencapture utility
        # -x: don't play sound
        # -C: capture cursor (optional, remove if you don't want cursor)
        result = subprocess.run(
            ["screencapture", "-x", str(filepath)],
            capture_output=True,
            timeout=5
        )

        if result.returncode == 0 and filepath.exists():
            return str(filepath)
        else:
            print(f"Screenshot capture failed: {result.stderr.decode()}")
            return None

    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None


def record_screen(duration=10, interval=30, save_directory="screenshots"):
    """
    Record screen by taking periodic screenshots.

    Args:
        duration: Total recording time in seconds (default: 10 seconds for testing)
        interval: Time between screenshots in seconds (default: 30)
        save_directory: Directory to save screenshots (default: "screenshots")

    Returns:
        List of file paths to captured screenshots
    """
    # Check permissions first
    if not check_screen_recording_permission():
        print("⚠️  Screen recording permission not granted!")
        print("Please grant screen recording permission in System Settings:")
        print("   System Settings → Privacy & Security → Screen Recording")
        return []

    print(f"📸 Starting screen recording for {duration} seconds (interval: {interval}s)")

    screenshots = []
    start_time = time.time()

    while time.time() - start_time < duration:
        filepath = capture_screenshot(save_directory)

        if filepath:
            screenshots.append(filepath)
            elapsed = int(time.time() - start_time)
            print(f"   ✓ Captured screenshot {len(screenshots)} ({elapsed}s elapsed)")
        else:
            print(f"   ✗ Failed to capture screenshot")

        time.sleep(interval)

    print(f"✅ Recording complete! Captured {len(screenshots)} screenshots")
    return screenshots


def cleanup_old_screenshots(directory="screenshots", days_to_keep=7):
    """
    Delete screenshots older than specified days.

    Args:
        directory: Screenshot directory to clean
        days_to_keep: Number of days to retain screenshots (default: 7)
    """
    try:
        screenshot_dir = Path(directory)
        if not screenshot_dir.exists():
            return

        current_time = time.time()
        days_in_seconds = days_to_keep * 24 * 60 * 60
        deleted_count = 0

        for file_path in screenshot_dir.glob("screenshot_*.png"):
            file_age = current_time - file_path.stat().st_mtime
            if file_age > days_in_seconds:
                file_path.unlink()
                deleted_count += 1

        if deleted_count > 0:
            print(f"🧹 Cleaned up {deleted_count} old screenshot(s)")

    except Exception as e:
        print(f"Error during cleanup: {e}")


if __name__ == "__main__":
    # Test the screen recorder
    print("🧪 Testing screen recorder...")

    # Test permission check
    if check_screen_recording_permission():
        print("✅ Screen recording permission granted")
    else:
        print("❌ Screen recording permission not granted")
        exit(1)

    # Capture a few test screenshots
    screenshots = record_screen(duration=10, interval=3)

    print(f"\n📁 Screenshots saved to: {ensure_screenshot_directory()}")
    for screenshot in screenshots:
        print(f"   - {screenshot}")
