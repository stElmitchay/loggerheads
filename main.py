from activity_tracker import track_activity, track_until_window_closes
from database import init_db, save_logs
from summarizer import summarize_logs
import sys


def run_day_tracker():
    """Legacy function - tracks activity for fixed duration."""
    init_db()

    print("🔍 Tracking activity...")
    logs = track_activity(duration=10, interval=2)

    save_logs(logs)
    summary = summarize_logs(logs)

    print("\n📅 Daily Log")
    print("✅ What I Worked On:")
    for category, count in summary.items():
        print(f"   - {category}: {count} sessions")

    print("\n🏁 What I Completed:")
    print("   - Tasks inferred from activity")

    print("\n📰 Solana News:")
    print("   - (placeholder)")

    print("\n⚠️ Issues:")
    print("   - None today")

    print("\n🔜 Focus for Tomorrow:")
    print("   - Keep coding!")


def run_window_tracker(target_window=None):
    """Track activity until a specific window closes."""
    init_db()

    # Get target window from command line or prompt user
    if not target_window:
        if len(sys.argv) > 1:
            target_window = sys.argv[1]
        else:
            target_window = input("Enter window name to track (e.g., 'Chrome', 'VSCode', 'PyCharm'): ")

    print("🔍 Starting window-based tracking...")
    logs = track_until_window_closes(target_window, interval=2)

    if logs:
        save_logs(logs)
        summary = summarize_logs(logs)

        print("\n📅 Activity Summary")
        print("✅ What You Worked On:")
        for category, count in summary.items():
            print(f"   - {category}: {count} sessions")
    else:
        print("\nNo activity tracked.")


if __name__ == "__main__":
    # Check if user wants window-based tracking
    if len(sys.argv) > 1 and sys.argv[1] != "--legacy":
        run_window_tracker()
    else:
        # Default to legacy mode for backward compatibility
        run_day_tracker()
