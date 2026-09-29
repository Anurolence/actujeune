import sqlite3
import os

# Vercel needs writable /tmp
IS_VERCEL = os.environ.get("VERCEL") == "1" or os.path.exists("/var/task")
DB_PATH = "/tmp/actujeune.db" if IS_VERCEL else os.path.join(os.path.dirname(__file__), "actujeune.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Recreate tables if missing - safe for Vercel
    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT,
        author TEXT,
        image_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        views INTEGER DEFAULT 0
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)
    # Add other tables if you have them - this ensures seed won't crash
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()
    print(f"DB initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
