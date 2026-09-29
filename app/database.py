import sqlite3, os
IS_VERCEL = os.environ.get("VERCEL") == "1" or os.path.exists("/var/task")
DB_PATH = "/tmp/actujeune.db" if IS_VERCEL else os.path.join(os.path.dirname(__file__), "actujeune.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    return get_db_connection()

def init_db():
    if IS_VERCEL and os.path.exists(DB_PATH):
        try: os.remove(DB_PATH)
        except: pass
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS posts")
    cur.execute("""
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        summary TEXT,
        category TEXT,
        author TEXT,
        author_role TEXT,
        image_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        views INTEGER DEFAULT 0,
        slug TEXT,
        status TEXT DEFAULT 'published',
        featured INTEGER DEFAULT 0
    )
    """)
    cur.execute("DROP TABLE IF EXISTS categories")
    cur.execute("CREATE TABLE categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)")
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
    cur.execute("DROP TABLE IF EXISTS comments")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        content TEXT,
        author TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    print(f"DB OK at {DB_PATH}")
