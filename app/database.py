"""Database connection and initialization module using SQLite."""
import sqlite3
import os
from contextlib import contextmanager

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "acujeune.db")

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
    """Initializes tables if they do not exist and runs migrations for Cameroonian youth features."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Posts table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            region TEXT NOT NULL,
            author_name TEXT NOT NULL,
            author_role TEXT DEFAULT 'Jeune Reporter',
            image_url TEXT,
            tags TEXT,
            opportunity_type TEXT DEFAULT 'story',
            deadline TEXT,
            remuneration_fcfa TEXT,
            contact_whatsapp TEXT,
            apply_link TEXT,
            likes_count INTEGER DEFAULT 0,
            views_count INTEGER DEFAULT 0,
            is_featured INTEGER DEFAULT 0,
            status TEXT DEFAULT 'published',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Migration helper: ensure new columns exist if table was already created
        cursor.execute("PRAGMA table_info(posts)")
        existing_cols = {col["name"] for col in cursor.fetchall()}
        
        new_columns = [
            ("opportunity_type", "TEXT DEFAULT 'story'"),
            ("deadline", "TEXT"),
            ("remuneration_fcfa", "TEXT"),
            ("contact_whatsapp", "TEXT"),
            ("apply_link", "TEXT")
        ]
        
        for col_name, col_def in new_columns:
            if col_name not in existing_cols:
                cursor.execute(f"ALTER TABLE posts ADD COLUMN {col_name} {col_def}")

        # Comments table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            author_name TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
        )
        """)

        # Likes tracking table (by anonymous client token or IP)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            client_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(post_id, client_id),
            FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
        )
        """)
