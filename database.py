import sqlite3

DB_FILE = "jobs.db"

def init_db():
    con = sqlite3.connect(DB_FILE)
    cursr = con.cursor()

    cursr.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            command TEXT,
            state TEXT,
            attempts INTEGER,
            max_retries INTEGER,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    cursr.execute("""
        CREATE TABLE IF NOT EXISTS dlq (
            id TEXT PRIMARY KEY,
            command TEXT,
            reason TEXT,
            failed_at TEXT
        )
    """)

    con.commit()
    con.close()
    print("Database initialized successfully.")

def connect():
    return sqlite3.connect(DB_FILE)
