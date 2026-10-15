import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "tourism.db"

def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tourists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            country TEXT NOT NULL,
            passport_number TEXT NOT NULL UNIQUE,
            arrival_date TEXT NOT NULL,
            accommodation TEXT,
            destination TEXT,
            purpose TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY CHECK(id=1),
            dark_mode INTEGER NOT NULL DEFAULT 0,
            notifications INTEGER NOT NULL DEFAULT 1,
            language TEXT NOT NULL DEFAULT 'English'
        )
    """)
    conn.execute("""
        INSERT OR IGNORE INTO settings(id, dark_mode, notifications, language)
        VALUES(1, 0, 1, 'English')
    """)
    conn.commit()
    conn.close()

def get_all():
    conn = connect()
    rows = conn.execute("SELECT * FROM tourists ORDER BY id DESC").fetchall()
    conn.close()
    return rows

def get_one(record_id):
    conn = connect()
    row = conn.execute("SELECT * FROM tourists WHERE id=?", (record_id,)).fetchone()
    conn.close()
    return row

def add(data):
    conn = connect()
    try:
        conn.execute("""
            INSERT INTO tourists
            (full_name,country,passport_number,arrival_date,
             accommodation,destination,purpose)
            VALUES (?,?,?,?,?,?,?)
        """, (
            data["full_name"], data["country"], data["passport_number"],
            data["arrival_date"], data["accommodation"],
            data["destination"], data["purpose"]
        ))
        conn.commit()
        return True, "Tourist record added successfully."
    except sqlite3.IntegrityError:
        return False, "Passport number already exists."
    finally:
        conn.close()

def update(record_id, data):
    conn = connect()
    try:
        conn.execute("""
            UPDATE tourists SET
            full_name=?, country=?, passport_number=?, arrival_date=?,
            accommodation=?, destination=?, purpose=?
            WHERE id=?
        """, (
            data["full_name"], data["country"], data["passport_number"],
            data["arrival_date"], data["accommodation"],
            data["destination"], data["purpose"], record_id
        ))
        conn.commit()
        return True, "Tourist record updated successfully."
    except sqlite3.IntegrityError:
        return False, "Passport number already belongs to another record."
    finally:
        conn.close()

def delete(record_id):
    conn = connect()
    conn.execute("DELETE FROM tourists WHERE id=?", (record_id,))
    conn.commit()
    conn.close()

def search(keyword="", destination="", arrival_date=""):
    conn = connect()
    like = f"%{keyword}%"
    rows = conn.execute("""
        SELECT * FROM tourists
        WHERE (full_name LIKE ? OR country LIKE ?
               OR passport_number LIKE ? OR destination LIKE ?)
        AND (?='' OR destination=?)
        AND (?='' OR arrival_date=?)
        ORDER BY id DESC
    """, (like, like, like, like,
          destination, destination,
          arrival_date, arrival_date)).fetchall()
    conn.close()
    return rows

def get_settings():
    conn = connect()
    row = conn.execute("SELECT * FROM settings WHERE id=1").fetchone()
    conn.close()
    return row

def save_settings(dark_mode, notifications, language):
    conn = connect()
    conn.execute("""
        UPDATE settings
        SET dark_mode=?, notifications=?, language=?
        WHERE id=1
    """, (int(dark_mode), int(notifications), language))
    conn.commit()
    conn.close()
