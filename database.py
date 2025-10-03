import sqlite3


def init_db():
    conn = sqlite3.connect("activity_log.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            window_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
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
