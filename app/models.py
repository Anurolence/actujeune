"""Pydantic schemas for data validation and API responses."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CommentBase(BaseModel):
    author_name: str = Field(..., min_length=2, max_length=100)
    content: str = Field(..., min_length=3, max_length=1000)

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    post_id: int
    created_at: str

class PostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    summary: str = Field(..., min_length=10, max_length=350)
    content: str = Field(..., min_length=20)
    category: str = Field(..., max_length=100)
    region: str = Field(..., max_length=100)
    author_name: str = Field(..., min_length=2, max_length=100)
    author_role: Optional[str] = "Jeune Leader"
    image_url: Optional[str] = None
    tags: Optional[str] = None
    opportunity_type: Optional[str] = "story"
    deadline: Optional[str] = None
    remuneration_fcfa: Optional[str] = None
    contact_whatsapp: Optional[str] = None
    apply_link: Optional[str] = None
    is_featured: Optional[int] = 0
    status: Optional[str] = "published"

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    author_name: Optional[str] = None
    author_role: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[str] = None
    opportunity_type: Optional[str] = None
    deadline: Optional[str] = None
    remuneration_fcfa: Optional[str] = None
    contact_whatsapp: Optional[str] = None
    apply_link: Optional[str] = None
    is_featured: Optional[int] = None
    status: Optional[str] = None

class PostResponse(PostBase):
    id: int
    likes_count: int = 0
    views_count: int = 0
    comments_count: Optional[int] = 0
    created_at: str
    updated_at: str

class PostDetailResponse(PostResponse):
    comments: List[CommentResponse] = []

class LikeActionResponse(BaseModel):
    post_id: int
    likes_count: int
    has_liked: bool
