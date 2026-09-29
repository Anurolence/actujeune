from fastapi import APIRouter
from app import crud
from app.models import PostCreate

router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/posts")
def get_posts():
    try:
        return crud.get_posts()
    except Exception as e:
        return {"posts": [], "error": str(e)}

@router.get("/posts/{post_id}")
def get_post(post_id: int):
    try:
        return crud.get_post(post_id)
    except Exception as e:
        return {"error": str(e)}

@router.post("/posts")
def create_post(post: PostCreate):
    try:
        return crud.create_post(post)
    except Exception as e:
        return {"error": str(e)}
