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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enquiry_id INTEGER NOT NULL,
            customer_name TEXT,
            contact_information TEXT,
            suburb TEXT,
            issue_summary TEXT,
            urgency TEXT,
            preferred_time TEXT,
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

def save_job_request(enquiry_id, data):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO job_requests
            (enquiry_id, customer_name, contact_information, suburb,
             issue_summary, urgency, preferred_time, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            enquiry_id,
            data.get("customer_name"),
            data.get("contact_information"),
            data.get("suburb"),
            data.get("issue_summary"),
            data.get("urgency"),
            data.get("preferred_time"),
            created_at,
        )
    )

    new_job_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return new_job_id