"""
Scheduler for running activity tracker as a background service during business hours.
Runs Monday-Friday, 9:30am-4:30pm by default.
Captures screenshots, performs OCR, and generates end-of-day summary.
"""

import time
import threading
import os
from datetime import datetime
from pynput import keyboard
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich import box
from rich.text import Text
from .activity_tracker import track_activity
from .database import init_db, save_logs, save_screenshot, get_screenshots
from .summarizer import summarize_logs
from .screen_recorder import capture_screenshot
from .ocr_processor import extract_text_from_image
from .text_analyzer import analyze_text, generate_structured_summary, format_summary_for_display
from .ai_summarizer import summarize_work_with_ai, format_ai_summary_for_display
from .discord_notifier import send_summary_to_discord
from .database_cleanup import clear_all_database_data
from .config import (
    WORK_START_TIME,
    WORK_END_TIME,
    WORK_DAYS,
    TRACKING_INTERVAL,
    SCREENSHOT_INTERVAL,
    SCREENSHOT_DIR,
    TARGET_WINDOW,
    DISCORD_WEBHOOK_URL,
    SEND_TO_DISCORD,
    USE_AI_SUMMARIZATION,
    OLLAMA_API_URL,
    OLLAMA_MODEL
)

console = Console()


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


def cleanup_screenshots():
    """
    Delete all screenshot files and clean up the screenshots directory.
    """
    console.print("\n[bold yellow]🗑️  Cleaning up screenshots...[/bold yellow]")

    try:
        # Get all screenshots from database
        screenshots = get_screenshots()
        deleted_count = 0

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("[cyan]Deleting screenshot files...", total=len(screenshots))

            for screenshot_id, file_path, timestamp, extracted_text in screenshots:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Could not delete {file_path}: {e}[/yellow]")
                progress.advance(task)

        console.print(f"[bold green]✅ Deleted {deleted_count} screenshot files[/bold green]")

    except Exception as e:
        console.print(f"[bold red]❌ Error cleaning up screenshots: {e}[/bold red]")


def process_and_generate_summary():
    """
    Process all screenshots with OCR and generate the work summary.
    Uses AI summarization if enabled, otherwise falls back to keyword extraction.
    """
    console.print("\n[bold cyan]🔄 Processing screenshots with OCR...[/bold cyan]")

    # Get all screenshots from database
    screenshots = get_screenshots()

    if not screenshots:
        console.print("[yellow]No screenshots to process.[/yellow]")
        return

    all_ocr_texts = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:
        task = progress.add_task("[cyan]Processing screenshots...", total=len(screenshots))

        for screenshot_id, file_path, timestamp, extracted_text in screenshots:
            # If text not already extracted, do OCR now
            if not extracted_text or extracted_text.strip() == "":
                if os.path.exists(file_path):
                    progress.update(task, description=f"[cyan]Processing: {os.path.basename(file_path)}")
                    extracted_text = extract_text_from_image(file_path)

            # Collect all OCR text
            if extracted_text and extracted_text.strip():
                all_ocr_texts.append(extracted_text)

            progress.advance(task)

    # Generate summary
    if all_ocr_texts:
        # Check if today is Friday (4 = Friday in weekday())
        is_friday = datetime.now().weekday() == 4

        # Use AI summarization if enabled
        if USE_AI_SUMMARIZATION:
            console.print(f"\n[bold magenta]🤖 Using Ollama AI to analyze {len(all_ocr_texts)} screenshots...[/bold magenta]")
            with console.status("[bold green]Analyzing with AI...", spinner="dots"):
                ai_summary = summarize_work_with_ai(all_ocr_texts, OLLAMA_API_URL, OLLAMA_MODEL, is_friday)

            if ai_summary:
                formatted_summary = format_ai_summary_for_display(ai_summary)
            else:
                console.print("[yellow]⚠️  AI summarization failed, falling back to keyword extraction[/yellow]")
                # Fallback to keyword extraction
                screenshot_data = []
                for text in all_ocr_texts:
                    analysis = analyze_text(text)
                    screenshot_data.append({'analysis': analysis, 'timestamp': datetime.now()})
                summary = generate_structured_summary(screenshot_data, is_friday=is_friday)
                formatted_summary = format_summary_for_display(summary)
        else:
            # Use keyword extraction
            console.print(f"\n[bold blue]🔍 Using keyword extraction to analyze {len(all_ocr_texts)} screenshots...[/bold blue]")
            screenshot_data = []
            for text in all_ocr_texts:
                analysis = analyze_text(text)
                screenshot_data.append({'analysis': analysis, 'timestamp': datetime.now()})
            summary = generate_structured_summary(screenshot_data, is_friday=is_friday)
            formatted_summary = format_summary_for_display(summary)

        # Print to console with rich panel
        console.print()
        console.print(Panel(
            formatted_summary,
            title="[bold cyan]📊 END OF DAY WORK SUMMARY[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE,
            padding=(1, 2)
        ))
        console.print()

        # Send to Discord if enabled
        if SEND_TO_DISCORD and DISCORD_WEBHOOK_URL:
            console.print("[bold blue]📤 Sending summary to Discord...[/bold blue]")
            send_summary_to_discord(DISCORD_WEBHOOK_URL, formatted_summary)
        elif SEND_TO_DISCORD and not DISCORD_WEBHOOK_URL:
            console.print("[yellow]⚠️  Discord notifications enabled but webhook URL not configured[/yellow]")

        # Clean up screenshots after summary is generated
        cleanup_screenshots()

        # Clean up database - delete all logs and screenshots
        clear_all_database_data()
    else:
        console.print("[yellow]No text extracted from screenshots.[/yellow]")


def run_scheduled_tracker():
    """
    Main scheduler loop that tracks activity during business hours.
    Captures screenshots, performs OCR, and generates end-of-day summary.
    """
    init_db()

    # Create startup banner
    console.print()
    console.print(Panel(
        f"[bold green]🚀 Activity Tracker Service Started[/bold green]\n\n"
        f"[cyan]📅 Work hours:[/cyan] {WORK_START_TIME} - {WORK_END_TIME}\n"
        f"[cyan]📆 Work days:[/cyan] {', '.join(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'][day] for day in WORK_DAYS)}\n"
        f"[cyan]📸 Screenshot interval:[/cyan] {SCREENSHOT_INTERVAL} seconds\n\n"
        f"[yellow]⌨️  Controls:[/yellow]\n"
        f"  [bold]P[/bold] - Pause tracking\n"
        f"  [bold]R[/bold] - Resume tracking\n"
        f"  [bold]Ctrl+C[/bold] - Stop and generate summary",
        title="[bold magenta]Loggerheads Activity Tracker[/bold magenta]",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2)
    ))
    console.print()

    session_logs = []
    last_status = None
    last_screenshot_time = time.time()
    last_minute_log = time.time()
    screenshot_count = 0
    activity_count = 0
    is_paused = False
    pause_start_time = None
    total_pause_time = 0

    def on_press(key):
        """Handle keyboard input for pause/resume."""
        nonlocal is_paused, pause_start_time, total_pause_time

        try:
            if hasattr(key, 'char'):
                if key.char == 'p' or key.char == 'P':
                    if not is_paused:
                        is_paused = True
                        pause_start_time = time.time()
                        console.print(f"\n[bold yellow]⏸️  [{datetime.now().strftime('%H:%M:%S')}] PAUSED[/bold yellow] - Press 'R' to resume")
                elif key.char == 'r' or key.char == 'R':
                    if is_paused:
                        is_paused = False
                        if pause_start_time:
                            total_pause_time += time.time() - pause_start_time
                        console.print(f"\n[bold green]▶️  [{datetime.now().strftime('%H:%M:%S')}] RESUMED[/bold green] - Tracking active")
        except AttributeError:
            pass

    # Start keyboard listener in background
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        while True:
            current_status = is_work_hours()

            # Status change notifications
            if current_status != last_status:
                if current_status:
                    console.print(f"[bold green]✅ [{datetime.now().strftime('%H:%M:%S')}] Work hours started[/bold green] - tracking active")
                    last_screenshot_time = time.time()  # Reset screenshot timer
                    last_minute_log = time.time()
                    screenshot_count = 0
                    activity_count = 0
                else:
                    console.print(f"[bold yellow]⏸️  [{datetime.now().strftime('%H:%M:%S')}] Work hours ended[/bold yellow] - generating summary...")

                    # Save activity logs
                    if session_logs:
                        save_logs(session_logs)
                        session_logs = []

                    # Process screenshots and generate summary
                    process_and_generate_summary()

                    console.print(f"\n[cyan]📸 Total screenshots captured today: {screenshot_count}[/cyan]")
                    screenshot_count = 0
                    activity_count = 0

                last_status = current_status

            # Track activity if within work hours AND not paused
            if current_status and not is_paused:
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
                    table = Table(show_header=False, box=None, padding=(0, 1))
                    table.add_row("[bold cyan]⏱️  Status Update[/bold cyan]", f"[dim]{datetime.now().strftime('%H:%M:%S')}[/dim]")
                    table.add_row("[cyan]📸 Screenshots[/cyan]", f"[bold]{screenshot_count}[/bold]")
                    table.add_row("[cyan]📝 Activities[/cyan]", f"[bold]{activity_count}[/bold]")
                    console.print(table)
                    last_minute_log = current_time

            # Show paused status every minute when paused
            if is_paused:
                current_time = time.time()
                if current_time - last_minute_log >= 60:
                    console.print(f"[bold yellow]⏸️  [{datetime.now().strftime('%H:%M:%S')}] PAUSED[/bold yellow] - Press 'R' to resume")
                    last_minute_log = current_time

            # Sleep for tracking interval
            time.sleep(TRACKING_INTERVAL)

    except KeyboardInterrupt:
        console.print("\n\n[bold red]🛑 Service stopped by user[/bold red]")

        # Stop keyboard listener
        listener.stop()

        # Save any remaining logs
        if session_logs:
            save_logs(session_logs)

        # Process and generate final summary
        console.print("\n[bold cyan]Generating final summary...[/bold cyan]")
        process_and_generate_summary()

        # Show stats in a nice table
        stats_table = Table(title="[bold]📊 Session Statistics[/bold]", box=box.ROUNDED, border_style="cyan")
        stats_table.add_column("Metric", style="cyan", no_wrap=True)
        stats_table.add_column("Value", style="bold green")

        stats_table.add_row("📸 Total Screenshots", str(screenshot_count))
        stats_table.add_row("⏸️  Total Pause Time", f"{int(total_pause_time / 60)} minutes")
        stats_table.add_row("⏱️  Active Tracking Time", f"{int((time.time() - last_status if last_status else 0 - total_pause_time) / 60)} minutes")

        console.print()
        console.print(stats_table)
        console.print()


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
