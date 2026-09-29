import os
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE, "app", "templates")
STATIC_DIR = os.path.join(BASE, "app", "static")
if not os.path.exists(TEMPLATES_DIR): TEMPLATES_DIR = "app/templates"
if not os.path.exists(STATIC_DIR): STATIC_DIR = "app/static"

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# DB init
try:
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
    print("DB OK")
except Exception as e:
    print(f"DB fail: {e}")

# Mount static
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

DEMO_POSTS = [
    {"id": 1, "title": "Concours ENS Yaoundé 2026 - Inscriptions ouvertes", "content": "Le concours d'entrée à l'ENS Yaoundé est ouvert. Date limite 15 Octobre.", "category": "Concours", "region": "Centre", "author": "MINESUP", "created_at": "2026-09-29"},
    {"id": 2, "title": "Bourse MoMo 2026 pour jeunes entrepreneurs", "content": "MTN Cameroon lance bourse 5M FCFA pour startups jeunes.", "category": "Bourse", "region": "Littoral", "author": "MTN", "created_at": "2026-09-29"},
    {"id": 3, "title": "Opportunité à Buea - Formation digitale gratuite", "content": "Formation gratuite en développement web à Buea, SW Region.", "category": "Formation", "region": "Sud-Ouest", "author": "ActuJeune", "created_at": "2026-09-29"},
]

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/posts")
def get_posts():
    try:
        from app.database import SessionLocal
        from app.models import Post
        db = SessionLocal()
        posts = db.query(Post).all()
        db.close()
        if posts:
            return posts
        return DEMO_POSTS
    except Exception as e:
        print(f"api/posts error: {e}")
        return DEMO_POSTS

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    try:
        from app.database import SessionLocal
        from app.models import Post
        db = SessionLocal()
        post = db.query(Post).filter(Post.id == post_id).first()
        db.close()
        if post:
            return post
        return DEMO_POSTS[0]
    except:
        return DEMO_POSTS[0]

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@app.get("/post/{post_id}", response_class=HTMLResponse)
def detail(request: Request, post_id: int):
    try:
        from app.database import SessionLocal
        from app.models import Post
        db = SessionLocal()
        post = db.query(Post).filter(Post.id == post_id).first()
        db.close()
        post_data = post if post else DEMO_POSTS[0]
    except:
        post_data = DEMO_POSTS[0]
    return templates.TemplateResponse(request, "post_detail.html", {"request": request, "post": post_data})
