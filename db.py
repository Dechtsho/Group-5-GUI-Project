
import sqlite3
from pathlib import Path


# =========================================
# DATABASE CONFIGURATION
# =========================================

DB_FILE = Path(__file__).resolve().parent / "tourism.db"


# =========================================
# DATABASE CONNECTION
# =========================================

def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================
# INITIALIZE DATABASE
# =========================================

def init_db():

    conn = connect()

    try:

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
            INSERT OR IGNORE INTO settings
            (id, dark_mode, notifications, language)
            VALUES (1, 0, 1, 'English')
        """)

        conn.commit()

    finally:
        conn.close()


# =========================================
# GET ALL TOURIST RECORDS
# =========================================

def get_all():

    conn = connect()

    try:

        rows = conn.execute("""
            SELECT * FROM tourists
            ORDER BY id ASC
        """).fetchall()

        return rows

    finally:
        conn.close()


# =========================================
# GET ONE TOURIST RECORD
# =========================================

def get_one(record_id):

    conn = connect()

    try:

        row = conn.execute("""
            SELECT * FROM tourists
            WHERE id=?
        """, (record_id,)).fetchone()

        return row

    finally:
        conn.close()


# =========================================
# ADD TOURIST RECORD
# =========================================

def add(data):

    conn = connect()

    try:

        conn.execute("""
            INSERT INTO tourists
            (
                full_name,
                country,
                passport_number,
                arrival_date,
                accommodation,
                destination,
                purpose
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["full_name"],
            data["country"],
            data["passport_number"],
            data["arrival_date"],
            data["accommodation"],
            data["destination"],
            data["purpose"]
        ))

        conn.commit()

        return True, "Tourist record added successfully."

    except sqlite3.IntegrityError:

        return False, "Passport number already exists."

    except sqlite3.Error as e:

        return False, f"Database error: {e}"

    finally:
        conn.close()


# =========================================
# UPDATE TOURIST RECORD
# =========================================

def update(record_id, data):

    conn = connect()

    try:

        cursor = conn.execute("""
            UPDATE tourists
            SET
                full_name=?,
                country=?,
                passport_number=?,
                arrival_date=?,
                accommodation=?,
                destination=?,
                purpose=?
            WHERE id=?
        """, (
            data["full_name"],
            data["country"],
            data["passport_number"],
            data["arrival_date"],
            data["accommodation"],
            data["destination"],
            data["purpose"],
            record_id
        ))

        conn.commit()

        if cursor.rowcount > 0:

            return True, "Tourist record updated successfully."

        return False, "Tourist record was not found."

    except sqlite3.IntegrityError:

        return False, "Passport number already belongs to another record."

    except sqlite3.Error as e:

        return False, f"Database error: {e}"

    finally:
        conn.close()


# =========================================
# DELETE TOURIST RECORD
# =========================================

def delete(record_id):

    conn = connect()

    try:

        cursor = conn.execute("""
            DELETE FROM tourists
            WHERE id=?
        """, (record_id,))

        conn.commit()

        if cursor.rowcount > 0:

            return True, "Tourist record deleted successfully."

        return False, "Tourist record was not found."

    except sqlite3.Error as e:

        return False, f"Database error: {e}"

    finally:
        conn.close()


# =========================================
# SEARCH TOURIST RECORDS
# =========================================

def search(keyword="", destination="", arrival_date=""):

    conn = connect()

    try:

        like = f"%{keyword}%"

        rows = conn.execute("""
            SELECT * FROM tourists

            WHERE
                (
                    full_name LIKE ?
                    OR country LIKE ?
                    OR passport_number LIKE ?
                    OR destination LIKE ?
                )

            AND (?='' OR destination=?)

            AND (?='' OR arrival_date=?)

            ORDER BY id ASC
        """, (
            like,
            like,
            like,
            like,
            destination,
            destination,
            arrival_date,
            arrival_date
        )).fetchall()

        return rows

    finally:
        conn.close()


# =========================================
# GET SETTINGS
# =========================================

def get_settings():

    conn = connect()

    try:

        row = conn.execute("""
            SELECT * FROM settings
            WHERE id=1
        """).fetchone()

        return row

    finally:
        conn.close()


# =========================================
# SAVE SETTINGS
# =========================================

def save_settings(dark_mode, notifications, language):

    conn = connect()

    try:

        conn.execute("""
            UPDATE settings

            SET
                dark_mode=?,
                notifications=?,
                language=?

            WHERE id=1
        """, (
            int(dark_mode),
            int(notifications),
            language
        ))

        conn.commit()

        return True, "Settings saved successfully."

    except sqlite3.Error as e:

        return False, f"Database error: {e}"

    finally:
        conn.close()
