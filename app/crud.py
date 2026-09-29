from sqlalchemy.orm import Session
from app.models import Post

DEMO_POSTS = [
    {"id": 1, "title": "Concours ENS Yaoundé 2026 - Inscriptions ouvertes", "content": "Le concours d'entrée à l'ENS Yaoundé est ouvert. Date limite 15 Octobre.", "category": "Concours", "region": "Centre", "author": "MINESUP"},
    {"id": 2, "title": "Bourse MoMo 2026 pour jeunes entrepreneurs", "content": "MTN Cameroon lance bourse 5M FCFA pour startups jeunes.", "category": "Bourse", "region": "Littoral", "author": "MTN"},
    {"id": 3, "title": "Opportunité à Buea - Formation digitale gratuite", "content": "Formation gratuite en développement web à Buea, SW Region.", "category": "Formation", "region": "Sud-Ouest", "author": "ActuJeune"},
]

def get_posts(db: Session):
    try:
        posts = db.query(Post).all()
        if posts:
            return posts
        # No posts in DB - return demo
        return DEMO_POSTS
    except Exception as e:
        print(f"crud.get_posts fallback: {e}")
        return DEMO_POSTS

def get_post(db: Session, post_id: int):
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        return post or (DEMO_POSTS[0] if DEMO_POSTS else None)
    except:
        return DEMO_POSTS[0]

def create_post(db: Session, post):
    try:
        db_post = Post(**post.dict())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception as e:
        print(f"create error: {e}")
        return {"id": 999, **post.dict()}
