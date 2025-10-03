from activity_tracker import track_activity
from database import init_db, save_logs
from summarizer import summarize_logs


def run_day_tracker():
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


if __name__ == "__main__":
    run_day_tracker()
