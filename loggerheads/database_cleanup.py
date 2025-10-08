"""
Database cleanup utilities - deletes all data after summary generation.
"""

import sqlite3
import os


def clear_all_database_data():
    """
    Delete all logs and screenshots from database.
    Called after summary is generated and sent.
    """
    try:
        conn = sqlite3.connect("activity_log.db")
        cursor = conn.cursor()

        # Delete all screenshots
        cursor.execute("DELETE FROM screenshots")
        screenshots_deleted = cursor.rowcount

        # Delete all logs
        cursor.execute("DELETE FROM logs")
        logs_deleted = cursor.rowcount

        conn.commit()
        conn.close()

        print(f"🗑️  Database cleaned: {logs_deleted} logs, {screenshots_deleted} screenshots deleted")

    except Exception as e:
        print(f"❌ Error cleaning database: {e}")


def delete_database_file():
    """
    Completely delete the database file.
    Use this for complete reset.
    """
    db_path = "activity_log.db"

    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"✅ Database file deleted: {db_path}")
        except Exception as e:
            print(f"❌ Error deleting database file: {e}")
    else:
        print(f"⚠️  Database file not found: {db_path}")
