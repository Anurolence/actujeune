"""Database connection using SQLite - Vercel compatible."""
import os
import sqlite3
from contextlib import contextmanager

# Vercel is read-only, use /tmp which is writable
DB_PATH = "/tmp/acujeune.db"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initializes tables if they do not exist and runs migrations"""
    with get_db() as conn:
        cursor = conn.cursor()
        # keep your existing table creation here - paste your old init_db body below
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        # ADD your other CREATE TABLE IF NOT EXISTS here if you had them
        conn.commit()
