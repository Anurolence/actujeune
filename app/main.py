import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE, "app", "templates")
STATIC_DIR = os.path.join(BASE, "app", "static")
if not os.path.exists(TEMPLATES_DIR): TEMPLATES_DIR = "app/templates"
if not os.path.exists(STATIC_DIR): STATIC_DIR = "app/static"

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.on_event("startup")
def startup():
    try:
        from app.database import init_db
        init_db()
        print("DB init done")
    except Exception as e: print(e)

try:
    from app.routes import router
    app.include_router(router)
except Exception as e: print(f"router: {e}")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@app.get("/post/{post_id}", response_class=HTMLResponse)
def detail(request: Request, post_id: int):
    from app import crud
    from app.database import SessionLocal
    db = SessionLocal()
    post = crud.get_post(db, post_id)
    return templates.TemplateResponse(request, "post_detail.html", {"request": request, "post": post})
