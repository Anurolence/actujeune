import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI(title="ActuJeune")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

@app.on_event("startup")
def on_startup():
    try:
        from app.database import init_db
        init_db()
        print("init_db OK")
    except Exception as e:
        print(f"init_db failed: {e}")
    try:
        from app.seed_data import seed_database
        seed_database()
        print("seed OK")
    except Exception as e:
        print(f"seed failed (non-fatal): {e}")

# Include routes if exists
try:
    from app.routes import router
    app.include_router(router)
    print("routes OK")
except Exception as e:
    print(f"routes failed: {e}")

# Static
try:
    os.makedirs(STATIC_DIR, exist_ok=True)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
except: pass

@app.get("/", response_class=HTMLResponse)
def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, encoding="utf-8") as f:
            return f.read()
    return '<h1>ActuJeune LIVE - Vercel FIXED</h1><p><a href="/docs">/docs</a> | <a href="/api/health">/api/health</a></p>'
