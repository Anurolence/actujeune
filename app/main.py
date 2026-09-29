import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title="ActuJeune")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Your structure from screenshot: app/static and app/templates
APP_DIR = os.path.join(BASE_DIR, "app")
TEMPLATES_DIR = os.path.join(APP_DIR, "templates")
STATIC_DIR = os.path.join(APP_DIR, "static")

# Fallback for Vercel root structure
if not os.path.exists(TEMPLATES_DIR):
    TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = os.path.join(BASE_DIR, "static")

print(f"TEMPLATES_DIR: {TEMPLATES_DIR} exists={os.path.exists(TEMPLATES_DIR)}")
print(f"STATIC_DIR: {STATIC_DIR} exists={os.path.exists(STATIC_DIR)}")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.on_event("startup")
def on_startup():
    try:
        from app.database import init_db
        init_db()
    except Exception as e:
        print(f"init_db: {e}")
    try:
        from app.seed_data import seed_database
        seed_database()
    except Exception as e:
        print(f"seed: {e}")

# Include API routes
try:
    from app.routes import router
    app.include_router(router)
    print("routes loaded")
except Exception as e:
    print(f"routes failed: {e}")

# Mount static from app/static
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    print(f"static mounted: {STATIC_DIR}")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Serve YOUR original template
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/post/{post_id}", response_class=HTMLResponse)
def post_detail(request: Request, post_id: int):
    try:
        from app import crud
        post = crud.get_post(post_id)
        return templates.TemplateResponse("post_detail.html", {"request": request, "post": post})
    except:
        return templates.TemplateResponse("post_detail.html", {"request": request, "post": None})
