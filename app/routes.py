from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db, init_db
from app import crud
from app.models import PostCreate

router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return {"status": "ok", "db": "connected"}

@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    try:
        init_db()
        posts = crud.get_posts(db)
        return posts if isinstance(posts, list) else posts.get("posts", []) if isinstance(posts, dict) else []
    except Exception as e:
        import traceback
        print(f"GET /posts error: {e}\n{traceback.format_exc()}")
        # Return empty list so frontend doesn't show "Erreur de chargement"
        return []

@router.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_post(db, post_id)
    except Exception as e:
        return {"error": str(e)}

@router.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_post(db, post)
    except Exception as e:
        return {"error": str(e)}
