"""FastAPI Main Application for Actujeune - Youth of Cameroon Platform."""
import os
import shutil
import uuid
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Request, Depends, UploadFile, File, Form, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import init_db
from app.seed_data import seed_database
from app import crud
from app.models import PostCreate, PostUpdate, PostResponse, PostDetailResponse, CommentCreate, CommentResponse, LikeActionResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
UPLOADS_DIR = "/tmp/uploads" if os.environ.get("VERCEL") else os.path.join(STATIC_DIR, "uploads")

try:
    os.makedirs(UPLOADS_DIR, exist_ok=True)
except Exception:
    pass

app = FastAPI(
    title="Actujeune",
    description="Plateforme d'actualités et d'opportunités pour la jeunesse camerounaise / Cameroonian Youth Platform",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Templates engine
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.on_event("startup")
def on_startup():
    try:
        from app.database import init_db
        init_db()
    except Exception as e:
        print(f"init_db failed: {e}")
    try:
        seed_database()
    except Exception as e:
        print(f"seed failed: {e}")
    except:
        pass
    # original seed
    seed_database()

# ----------------- PAGE ROUTES ----------------- #

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Renders the main responsive web app."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def post_page(request: Request, post_id: int):
    """Renders the post detail page."""
    post = crud.get_post_by_id(post_id, increment_views=True)
    if not post:
        raise HTTPException(status_code=404, detail="Publication non trouvée / Post not found")
    comments = crud.get_comments(post_id)
    return templates.TemplateResponse(
        request=request,
        name="post_detail.html",
        context={"post": post, "comments": comments}
    )

# ----------------- REST API ROUTES ----------------- #

@app.get("/api/meta")
def get_metadata():
    """Returns platform metadata, categories, regions and counters."""
    return crud.get_categories_and_regions()

@app.get("/api/posts", response_model=List[PostResponse])
def list_posts(
    search: Optional[str] = Query(None, description="Search keyword in title, summary, or content"),
    category: Optional[str] = Query(None, description="Filter by category"),
    region: Optional[str] = Query(None, description="Filter by Cameroonian region"),
    opportunity_type: Optional[str] = Query(None, description="Filter by opportunity type (concours, bourse, emploi_stage, story)"),
    sort_by: str = Query("latest", pattern="^(latest|popular|views)$"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """List updates/posts with search, category/region filter, opportunity type, and sorting."""
    return crud.get_posts(
        search=search, category=category, region=region,
        opportunity_type=opportunity_type, sort_by=sort_by,
        limit=limit, offset=offset
    )

@app.get("/api/posts/{post_id}", response_model=PostDetailResponse)
def get_post(post_id: int):
    """Retrieve a single post along with comments, incrementing view count."""
    post = crud.get_post_by_id(post_id, increment_views=True)
    if not post:
        raise HTTPException(status_code=404, detail="Publication non trouvée / Post not found")
    comments = crud.get_comments(post_id)
    post_dict = dict(post)
    post_dict["comments"] = comments
    return post_dict

@app.post("/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_new_post(post: PostCreate):
    """Create a new youth update/story."""
    new_post = crud.create_post(post)
    return new_post

@app.put("/api/posts/{post_id}", response_model=PostResponse)
def update_existing_post(post_id: int, post_update: PostUpdate):
    """Update an existing update/post."""
    existing = crud.get_post_by_id(post_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Publication introuvable / Post not found")
    updated = crud.update_post(post_id, post_update)
    return updated

@app.delete("/api/posts/{post_id}")
def delete_existing_post(post_id: int):
    """Delete a post and its associated comments."""
    existing = crud.get_post_by_id(post_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Publication introuvable / Post not found")
    success = crud.delete_post(post_id)
    return {"success": success, "message": "Publication supprimée avec succès / Post deleted successfully"}

@app.post("/api/posts/{post_id}/like", response_model=LikeActionResponse)
def toggle_post_like(post_id: int, client_id: str = Form(...)):
    """Toggle like state for a post by client fingerprint."""
    existing = crud.get_post_by_id(post_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Publication introuvable / Post not found")
    result = crud.toggle_like(post_id, client_id)
    return result

@app.get("/api/posts/{post_id}/comments", response_model=List[CommentResponse])
def get_post_comments(post_id: int):
    """Get comments for a post."""
    return crud.get_comments(post_id)

@app.post("/api/posts/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def post_comment(post_id: int, comment: CommentCreate):
    """Add a community comment to an update."""
    existing = crud.get_post_by_id(post_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Publication introuvable / Post not found")
    created = crud.add_comment(post_id, comment)
    return created

@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    """Uploads an image for an update and returns its relative public URL."""
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Format d'image non supporté (autorisés: JPG, PNG, WEBP, GIF)")
    
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    destination_path = os.path.join(UPLOADS_DIR, unique_filename)
    
    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"url": f"/static/uploads/{unique_filename}"}
