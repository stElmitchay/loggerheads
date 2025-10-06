import sqlite3


def init_db():
    conn = sqlite3.connect("activity_log.db")
    cursor = conn.cursor()

    # Create logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            window_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create screenshots table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS screenshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            extracted_text TEXT,
            log_id INTEGER,
            FOREIGN KEY (log_id) REFERENCES logs(id)
        )
    """)

    conn.commit()
    conn.close()


def save_logs(logs):
    conn = sqlite3.connect("activity_log.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO logs (window_name) VALUES (?)", [(log,) for log in logs])
    conn.commit()
    conn.close()


def save_screenshot(file_path, extracted_text="", log_id=None):
    """
    Save screenshot metadata to database.

    Args:
        file_path (str): Path to the screenshot file
        extracted_text (str): OCR-extracted text from the screenshot
        log_id (int, optional): ID of related activity log entry
    """
    conn = sqlite3.connect("activity_log.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO screenshots (file_path, extracted_text, log_id) VALUES (?, ?, ?)",
        (file_path, extracted_text, log_id)
    )
    conn.commit()
    conn.close()


def get_screenshots(limit=None):
    """
    Retrieve screenshots from database.

    Args:
        limit (int, optional): Maximum number of screenshots to retrieve

    Returns:
        list: List of tuples containing screenshot data
    """
    conn = sqlite3.connect("activity_log.db")
    cursor = conn.cursor()

    if limit:
        cursor.execute(
            "SELECT id, file_path, timestamp, extracted_text FROM screenshots ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
    else:
        cursor.execute(
            "SELECT id, file_path, timestamp, extracted_text FROM screenshots ORDER BY timestamp DESC"
        )

    results = cursor.fetchall()
    conn.close()
    return results
