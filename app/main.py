from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
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
    {"id":1,"title":"Concours ENS Yaoundé 2026 - Inscriptions ouvertes","content":"Le concours d'entrée à l'ENS Yaoundé est ouvert. Date limite 15 Octobre.","category":"Concours","region":"Centre","author":"MINESUP","created_at":"2026-09-29"},
    {"id":2,"title":"Bourse MoMo 2026 pour jeunes entrepreneurs","content":"MTN Cameroon lance bourse 5M FCFA pour startups jeunes.","category":"Bourse","region":"Littoral","author":"MTN","created_at":"2026-09-29"},
    {"id":3,"title":"Formation digitale gratuite à Buea","content":"Formation gratuite en dev web à Buea, SW Region.","category":"Formation","region":"Sud-Ouest","author":"ActuJeune","created_at":"2026-09-29"},
]

@app.get("/api/health")
def health(): return {"status":"ok"}

@app.get("/api/posts")
def get_posts():
    try:
        from app.database import SessionLocal
        from app.models import Post
        db = SessionLocal()
        posts = db.query(Post).all()
        db.close()
        if posts:
            result = []
            for p in posts:
                result.append({"id":p.id,"title":p.title,"content":p.content,"category":getattr(p,'category','Actualités'),"region":getattr(p,'region','Centre'),"author":getattr(p,'author','Admin'),"created_at":str(getattr(p,'created_at','2026-09-29'))})
            return result
    except Exception as e: print(f"DB fallback: {e}")
    return DEMO_POSTS

@app.get("/api/posts/{post_id}")
def get_one(post_id: int):
    for p in DEMO_POSTS:
        if p["id"]==post_id: return p
    return DEMO_POSTS[0]

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@app.get("/post/{post_id}", response_class=HTMLResponse)
def detail(request: Request, post_id: int):
    post = DEMO_POSTS[0]
    for p in DEMO_POSTS:
        if p["id"]==post_id: post=p
    return templates.TemplateResponse(request, "post_detail.html", {"request": request, "post": post})
