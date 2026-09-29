import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="ActuJeune")

# Vercel runs in /var/task — detect both paths
BASE = os.path.dirname(os.path.dirname(__file__))
POSSIBLE_TEMPLATES = [
    os.path.join(BASE, "app", "templates"),
    os.path.join(BASE, "templates"),
    "app/templates",
    "templates",
    os.path.join(os.getcwd(), "app", "templates"),
]
POSSIBLE_STATIC = [
    os.path.join(BASE, "app", "static"),
    os.path.join(BASE, "static"),
    "app/static",
    "static",
    os.path.join(os.getcwd(), "app", "static"),
]

TEMPLATES_DIR = next((p for p in POSSIBLE_TEMPLATES if os.path.exists(p)), POSSIBLE_TEMPLATES[0])
STATIC_DIR = next((p for p in POSSIBLE_STATIC if os.path.exists(p)), POSSIBLE_STATIC[0])

print(f"Using TEMPLATES: {TEMPLATES_DIR} exists={os.path.exists(TEMPLATES_DIR)} list={os.listdir(TEMPLATES_DIR) if os.path.exists(TEMPLATES_DIR) else 'NO'}")
print(f"Using STATIC: {STATIC_DIR} exists={os.path.exists(STATIC_DIR)}")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Init DB safely
@app.on_event("startup")
def startup():
    try:
        from app.database import init_db
        init_db()
        print("DB init ok")
    except Exception as e:
        print(f"DB init failed: {e}")
    try:
        from app.seed_data import seed_database
        seed_database()
        print("Seed ok")
    except Exception as e:
        print(f"Seed failed: {e}")

# API routes
try:
    from app.routes import router
    app.include_router(router)
    print("API router loaded")
except Exception as e:
    print(f"Router load failed: {e}")

# Mount static
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    print(f"Mounted /static -> {STATIC_DIR}")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        # Return error as HTML instead of 500 so you can see it
        import traceback
        tb = traceback.format_exc()
        print(f"TEMPLATE ERROR: {e}\n{tb}")
        return HTMLResponse(f"<h1>Template Error</h1><pre>{e}\n\n{tb}</pre><p>Dir: {TEMPLATES_DIR} Exists: {os.path.exists(TEMPLATES_DIR)} Files: {os.listdir(TEMPLATES_DIR) if os.path.exists(TEMPLATES_DIR) else 'none'}</p>", status_code=500)

@app.get("/post/{post_id}", response_class=HTMLResponse)
def post_detail(request: Request, post_id: int):
    try:
        from app import crud
        post = crud.get_post(post_id)
        return templates.TemplateResponse("post_detail.html", {"request": request, "post": post})
    except Exception as e:
        return HTMLResponse(f"<h1>Error post {post_id}</h1><pre>{e}</pre>", status_code=500)

@app.get("/debug")
def debug():
    return {
        "templates_dir": TEMPLATES_DIR,
        "templates_exists": os.path.exists(TEMPLATES_DIR),
        "templates_files": os.listdir(TEMPLATES_DIR) if os.path.exists(TEMPLATES_DIR) else [],
        "static_dir": STATIC_DIR,
        "static_exists": os.path.exists(STATIC_DIR),
        "cwd": os.getcwd(),
        "base": BASE,
    }
