import sqlite3
from datetime import datetime

DB_NAME = "enquiries.db"


def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_enquiry(raw_message):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO enquiries (raw_message, created_at) VALUES (?, ?)",
        (raw_message, created_at)
    )

    new_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return new_id