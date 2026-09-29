from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

@router.get("/api/health")
def health():
    return {"status": "ok", "app": "ActuJeune LIVE"}

@router.get("/api/posts")
def get_posts():
    try:
        from app.database import get_db_connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT 50")
        posts = [dict(row) for row in cur.fetchall()]
        conn.close()
        return posts
    except Exception as e:
        return {"error": str(e), "posts": []}

@router.get("/{full_path:path}", response_class=HTMLResponse)
def serve_frontend(full_path: str):
    # Serve index.html for frontend routing
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>ActuJeune LIVE</h1><p>Frontend not built yet</p><a href='/docs'>API Docs</a>"
