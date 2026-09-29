from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
app = FastAPI()
BASE = os.path.dirname(os.path.dirname(__file__))
T_DIR = os.path.join(BASE,"app","templates")
if not os.path.exists(T_DIR): T_DIR="app/templates"
S_DIR = os.path.join(BASE,"app","static")
if not os.path.exists(S_DIR): S_DIR="app/static"
templates = Jinja2Templates(directory=T_DIR)
if os.path.exists(S_DIR):
    app.mount("/static", StaticFiles(directory=S_DIR), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@app.get("/post/{post_id}")
def detail(request: Request, post_id: int):
    post={"id":1,"title":"Concours ENS Yaoundé","content":"Details...","category":"Concours"}
    return templates.TemplateResponse(request, "post_detail.html", {"request": request, "post": post})

@app.get("/{full_path:path}")
def catch_all(request: Request, full_path: str):
    return templates.TemplateResponse(request, "index.html", {"request": request})
