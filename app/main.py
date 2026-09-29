import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routes import router
from app.database import init_db
from app.seed_data import seed_database

app = FastAPI(title="ActuJeune")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOADS_DIR = "/tmp/uploads" if os.environ.get("VERCEL") else os.path.join(STATIC_DIR, "uploads")
try:
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    os.makedirs(STATIC_DIR, exist_ok=True)
except: pass

@app.on_event("startup")
def on_startup():
    try:
        init_db()
        print("init_db OK")
    except Exception as e:
        print(f"init_db failed: {e}")
    try:
        seed_database()
        print("seed OK")
    except Exception as e:
        print(f"seed failed (non-fatal): {e}")

app.include_router(router)

try:
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
except: pass

@app.get("/", response_class=HTMLResponse)
def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path) as f:
            return f.read()
    return "<h1>ActuJeune LIVE</h1><p>Site is working</p><a href='/docs'>/docs</a>"
