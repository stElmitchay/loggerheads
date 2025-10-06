# Daily Activity Tracker with OCR Analysis

An intelligent work tracker that captures screenshots during work hours, extracts text using OCR, and generates detailed end-of-day summaries focused on actual work accomplished.

## Features

- 📸 **Automatic Screenshot Capture**: Takes screenshots every 10 seconds during work hours
- 🔍 **OCR Text Extraction**: Extracts text from screenshots using Tesseract OCR
- 🤖 **Smart Work Analysis**: Analyzes work content to identify:
  - Tasks worked on and completed
  - Problems solved and blockers
  - Code written (functions, classes, imports)
  - Technical topics and technologies used
  - Solana ecosystem news (from Twitter screenshots)
- 📊 **End-of-Day Summary**: Generates structured daily summary at 4:30pm
- ⏰ **Business Hours Only**: Runs Mon-Fri, 9:30am-4:30pm (configurable)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

## Usage

### Start the Tracker

```bash
python scheduler.py
```

The tracker will:
- Start automatically at 9:30am on weekdays
- Capture screenshots every 10 seconds
- Track window activity every 2 seconds
- Generate summary at 4:30pm
- Pause until next work day

### Manual Stop

Press `Ctrl+C` to stop and generate summary immediately.

## Configuration

Edit `config.py` to customize:

```python
# Work hours
WORK_START_TIME = "09:30"
WORK_END_TIME = "16:30"
WORK_DAYS = [0, 1, 2, 3, 4]  # Mon-Fri

# Screenshot settings
SCREENSHOT_INTERVAL = 10  # seconds
SCREENSHOT_DIR = "./screenshots/"
AUTO_CLEANUP_DAYS = 1  # days

# Activity tracking
TRACKING_INTERVAL = 2  # seconds
```

## Summary Format

The end-of-day summary includes:

```
✅ What I Worked on Today:
  • [Detailed tasks from screenshot analysis]

🏁 What I Completed:
  • [Tasks marked as finished/deployed/merged]

📰 What's the latest in the Solana Ecosystem:
  • [Solana news from Twitter screenshots]

⚠️ Issues / Blockers:
  • [Problems and errors encountered]

🔜 Focus for Tomorrow:
  • [AI-generated recommendations]
  (Skipped on Fridays)
```

## Database

All data is stored in SQLite: `activity_log.db`

**Tables:**
- `logs` - Window activity records
- `screenshots` - Screenshot metadata and OCR text

## File Structure

```
daily_log_ai/
├── scheduler.py           # Main service runner
├── activity_tracker.py    # Window tracking
├── screen_recorder.py     # Screenshot capture
├── ocr_processor.py       # OCR text extraction
├── text_analyzer.py       # Work content analysis
├── database.py            # SQLite operations
├── config.py             # Configuration
└── screenshots/          # Screenshot storage
```

## Privacy

- All data stays local on your machine
- Screenshots stored in `./screenshots/` directory
- Auto-cleanup after 1 day (configurable)
- No data sent to external services

## Requirements

- Python 3.7+
- macOS, Linux, or Windows
- Tesseract OCR installed
- Sufficient disk space for screenshots

## Troubleshooting

**"Tesseract not found" error:**
- Make sure Tesseract is installed and in PATH
- On macOS: `brew install tesseract`

**Screenshots not capturing:**
- Check permissions for screen recording (macOS System Preferences)
- Verify `screenshots/` directory exists

**No text extracted:**
- Screenshots may have low resolution or poor contrast
- Check Tesseract installation: `tesseract --version`
