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
            customer_name TEXT,
            contact_information TEXT,
            suburb TEXT,
            issue_summary TEXT,
            service_type TEXT,
            urgency TEXT,
            preferred_time TEXT,
            status TEXT,
            final_action TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enquiry_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            text TEXT NOT NULL,
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

def add_message(enquiry_id, sender, text):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO messages (enquiry_id, sender, text, created_at) VALUES (?, ?, ?, ?)",
        (enquiry_id, sender, text, created_at)
    )

    connection.commit()
    connection.close()


def get_enquiry(enquiry_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM enquiries WHERE id = ?", (enquiry_id,))
    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None
    return dict(row)


def get_messages(enquiry_id):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM messages WHERE enquiry_id = ? ORDER BY id",
        (enquiry_id,)
    )
    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def update_enquiry_processed(enquiry_id, extracted, status, final_action):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    updated_at = datetime.now().isoformat()

    cursor.execute(
        """
        UPDATE enquiries
        SET customer_name = ?,
            contact_information = ?,
            suburb = ?,
            issue_summary = ?,
            service_type = ?,
            urgency = ?,
            preferred_time = ?,
            status = ?,
            final_action = ?,
            updated_at = ?
        WHERE id = ?
        """,
        (
            extracted.get("customer_name"),
            extracted.get("contact_information"),
            extracted.get("suburb"),
            extracted.get("issue_summary"),
            extracted.get("service_type"),
            extracted.get("urgency"),
            extracted.get("preferred_time"),
            status,
            final_action,
            updated_at,
            enquiry_id,
        )
    )

    connection.commit()
    connection.close()

def get_all_enquiries():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM enquiries ORDER BY id DESC")
    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]