import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="ActuJeune")

BASE = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE, "app", "templates")
STATIC_DIR = os.path.join(BASE, "app", "static")
if not os.path.exists(TEMPLATES_DIR):
    TEMPLATES_DIR = os.path.join(BASE, "templates")
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = os.path.join(BASE, "static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.on_event("startup")
def startup():
    try:
        from app.database import init_db
        init_db()
    except: pass
    try:
        from app.seed_data import seed_database
        seed_database()
    except: pass

try:
    from app.routes import router
    app.include_router(router)
except Exception as e:
    print(f"Router failed: {e}")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    try:
        # FIXED for Starlette 1.7: request FIRST
        return templates.TemplateResponse(request, "index.html", {"request": request})
    except Exception as e:
        import traceback
        return HTMLResponse(f"<h1>Error</h1><pre>{e}\n{traceback.format_exc()}</pre>", status_code=500)

@app.get("/post/{post_id}", response_class=HTMLResponse)
def post_detail(request: Request, post_id: int):
    try:
        from app import crud
        post = crud.get_post(post_id)
        return templates.TemplateResponse(request, "post_detail.html", {"request": request, "post": post})
    except Exception as e:
        import traceback
        return HTMLResponse(f"<h1>Error</h1><pre>{e}\n{traceback.format_exc()}</pre>", status_code=500)
