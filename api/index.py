from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

app = FastAPI()
BASE = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE, "app", "templates")
if not os.path.exists(TEMPLATES_DIR): TEMPLATES_DIR = "app/templates"
STATIC_DIR = os.path.join(BASE, "app", "static")
if not os.path.exists(STATIC_DIR): STATIC_DIR = "app/static"

templates = Jinja2Templates(directory=TEMPLATES_DIR)
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

DEMO_POSTS = [
    {"id":1,"title":"Concours ENS Yaoundé 2026","content":"Le concours ENS Yaoundé est ouvert.","category":"Concours","region":"Centre","author":"MINESUP","created_at":"2026-09-29"},
]

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@app.get("/post/{post_id}")
def detail(request: Request, post_id: int):
    return templates.TemplateResponse(request, "post_detail.html", {"request": request, "post": DEMO_POSTS[0]})
