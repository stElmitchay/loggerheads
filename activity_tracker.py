import time
import pygetwindow as gw

def track_activity(duration=10, interval=2):
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
