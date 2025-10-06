import time
import pygetwindow as gw


def track_activity(duration=10, interval=2):
    """Legacy function - tracks activity for a fixed duration."""
    logs = []
    start_time = time.time()

    while time.time() - start_time < duration:
        try:
            window = gw.getActiveWindow()
            if window:
                title = window.title
                # Ensure it's a string
                if callable(title):
                    title = title()
                if title:
                    logs.append(str(title))
        except Exception:
            pass
        time.sleep(interval)

    return logs


def is_window_open(window_name):
    """
    Check if a window with the given name (partial match) is currently open.

    Args:
        window_name (str): Window name or partial name to search for

    Returns:
        bool: True if window is found, False otherwise
    """
    try:
        windows = gw.getAllTitles()
        for title in windows:
            if window_name.lower() in title.lower():
                return True
        return False
    except Exception:
        return False


def track_until_window_closes(target_window, interval=2, callback=None):
    """
    Track activity until a specific window closes.

    Args:
        target_window (str): Name (or partial name) of window to monitor
        interval (int): Seconds between activity checks
        callback (function, optional): Function to call with each window title captured

    Returns:
        list: List of window titles captured during tracking
    """
    logs = []

    # Check if target window exists before starting
    if not is_window_open(target_window):
        print(f"Target window '{target_window}' not found. Please open it first.")
        return logs

    print(f"Tracking activity until '{target_window}' closes...")
    print("Press Ctrl+C to stop manually.")

    try:
        while is_window_open(target_window):
            try:
                window = gw.getActiveWindow()
                if window:
                    title = window.title
                    # Ensure it's a string
                    if callable(title):
                        title = title()
                    if title:
                        logs.append(str(title))
                        if callback:
                            callback(str(title))
            except Exception:
                pass
            time.sleep(interval)

        print(f"\nTarget window '{target_window}' closed. Stopping tracker.")

    except KeyboardInterrupt:
        print("\nTracking stopped manually.")

    return logs
