# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based activity tracker that monitors active windows, categorizes them, and generates daily work summaries. The application tracks what applications you're using throughout the day and provides insights into time spent on different activities.

## Architecture

The codebase follows a modular architecture with clear separation of concerns:

- **main.py**: Orchestrates the entire workflow by calling functions from other modules in sequence
- **activity_tracker.py**: Monitors active window titles using pygetwindow library
- **database.py**: Handles SQLite database initialization and data persistence
- **summarizer.py**: Categorizes window titles into activity types (Research, Coding, Communication, etc.)

Data flow: Activity tracking → Raw logs → Database storage → Categorization/Summary → Console output

## Running the Application

Start the activity tracker:
```bash
python main.py
```

The default configuration tracks activity for 10 seconds with 2-second intervals (configurable in main.py:10).

## Database

- SQLite database: `activity_log.db`
- Schema: `logs` table with columns: id (PRIMARY KEY), window_name (TEXT), timestamp (DATETIME)
- Database is auto-created on first run via `init_db()` in database.py:4

## Dependencies

Required Python packages:
- `pygetwindow` - for tracking active window titles
- `sqlite3` - built-in, for database operations

Install dependencies:
```bash
pip install pygetwindow
```

## Activity Categorization

Window titles are mapped to categories in summarizer.py:2-7:
- Chrome → Research
- PyCharm → Coding
- Slack → Communication
- Word → Documentation
- Unknown → Other

To add new categories, modify the `categories` dictionary in summarizer.py.
