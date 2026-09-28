"""CRUD operations for Acujeune SQLite database."""
import sqlite3
from typing import List, Optional, Dict, Any
from app.database import get_db
from app.models import PostCreate, PostUpdate, CommentCreate

def get_posts(
    search: Optional[str] = None,
    category: Optional[str] = None,
    region: Optional[str] = None,
    opportunity_type: Optional[str] = None,
    sort_by: str = "latest",
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """Retrieves posts with search, filter, and sorting support."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        query = """
        SELECT p.*, 
               (SELECT COUNT(*) FROM comments c WHERE c.post_id = p.id) as comments_count
        FROM posts p
        WHERE p.status = 'published'
        """
        params: List[Any] = []
        
        if search:
            query += " AND (p.title LIKE ? OR p.summary LIKE ? OR p.content LIKE ? OR p.tags LIKE ?)"
            term = f"%{search.strip()}%"
            params.extend([term, term, term, term])
            
        if category and category != "all":
            query += " AND p.category = ?"
            params.append(category)
            
        if region and region != "all":
            query += " AND p.region = ?"
            params.append(region)

        if opportunity_type and opportunity_type != "all":
            query += " AND p.opportunity_type = ?"
            params.append(opportunity_type)
            
        if sort_by == "popular":
            query += " ORDER BY p.likes_count DESC, p.created_at DESC"
        elif sort_by == "views":
            query += " ORDER BY p.views_count DESC, p.created_at DESC"
        else:
            query += " ORDER BY p.is_featured DESC, p.created_at DESC"
            
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        return cursor.fetchall()

def get_post_by_id(post_id: int, increment_views: bool = False) -> Optional[Dict[str, Any]]:
    """Fetches a single post by ID and optionally increments view count."""
    with get_db() as conn:
        cursor = conn.cursor()
        if increment_views:
            cursor.execute("UPDATE posts SET views_count = views_count + 1 WHERE id = ?", (post_id,))
            
        cursor.execute("""
        SELECT p.*,
               (SELECT COUNT(*) FROM comments c WHERE c.post_id = p.id) as comments_count
        FROM posts p
        WHERE p.id = ?
        """, (post_id,))
        return cursor.fetchone()

def create_post(post: PostCreate) -> Dict[str, Any]:
    """Inserts a new youth update post with Cameroonian opportunity details."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO posts (
            title, summary, content, category, region, author_name, author_role,
            image_url, tags, opportunity_type, deadline, remuneration_fcfa,
            contact_whatsapp, apply_link, is_featured, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            post.title, post.summary, post.content, post.category, post.region,
            post.author_name, post.author_role or 'Jeune Leader',
            post.image_url, post.tags,
            post.opportunity_type or 'story',
            post.deadline, post.remuneration_fcfa,
            post.contact_whatsapp, post.apply_link,
            post.is_featured or 0, post.status or 'published'
        ))
        post_id = cursor.lastrowid
        cursor.execute("SELECT *, 0 as comments_count FROM posts WHERE id = ?", (post_id,))
        return cursor.fetchone()

def update_post(post_id: int, post_update: PostUpdate) -> Optional[Dict[str, Any]]:
    """Updates an existing post by ID."""
    update_data = post_update.model_dump(exclude_unset=True)
    if update_data:
        with get_db() as conn:
            cursor = conn.cursor()
            set_clauses = []
            params = []
            for key, value in update_data.items():
                set_clauses.append(f"{key} = ?")
                params.append(value)
                
            set_clauses.append("updated_at = CURRENT_TIMESTAMP")
            params.append(post_id)
            
            query = f"UPDATE posts SET {', '.join(set_clauses)} WHERE id = ?"
            cursor.execute(query, params)
            
    return get_post_by_id(post_id)

def delete_post(post_id: int) -> bool:
    """Deletes a post and cascades to comments and likes."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        return cursor.rowcount > 0

def toggle_like(post_id: int, client_id: str) -> Dict[str, Any]:
    """Toggles like for a given client_id (anonymous or authenticated)."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM post_likes WHERE post_id = ? AND client_id = ?", (post_id, client_id))
        existing = cursor.fetchone()
        
        if existing:
            # Unlike
            cursor.execute("DELETE FROM post_likes WHERE id = ?", (existing["id"],))
            cursor.execute("UPDATE posts SET likes_count = MAX(0, likes_count - 1) WHERE id = ?", (post_id,))
            has_liked = False
        else:
            # Like
            cursor.execute("INSERT INTO post_likes (post_id, client_id) VALUES (?, ?)", (post_id, client_id))
            cursor.execute("UPDATE posts SET likes_count = likes_count + 1 WHERE id = ?", (post_id,))
            has_liked = True
            
        cursor.execute("SELECT likes_count FROM posts WHERE id = ?", (post_id,))
        row = cursor.fetchone()
        likes_count = row["likes_count"] if row else 0
        return {"post_id": post_id, "likes_count": likes_count, "has_liked": has_liked}

def check_has_liked(post_id: int, client_id: str) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM post_likes WHERE post_id = ? AND client_id = ?", (post_id, client_id))
        return cursor.fetchone() is not None

def add_comment(post_id: int, comment: CommentCreate) -> Dict[str, Any]:
    """Adds a new comment to a post."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO comments (post_id, author_name, content)
        VALUES (?, ?, ?)
        """, (post_id, comment.author_name, comment.content))
        comment_id = cursor.lastrowid
        cursor.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
        return cursor.fetchone()

def get_comments(post_id: int) -> List[Dict[str, Any]]:
    """Gets all comments for a post ordered by latest first."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM comments WHERE post_id = ? ORDER BY created_at DESC
        """, (post_id,))
        return cursor.fetchall()

def get_categories_and_regions() -> Dict[str, Any]:
    """Provides current distinct categories, regions, opportunity types with counts."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT category, COUNT(*) as count 
        FROM posts WHERE status = 'published' 
        GROUP BY category ORDER BY count DESC
        """)
        categories = cursor.fetchall()
        
        cursor.execute("""
        SELECT region, COUNT(*) as count 
        FROM posts WHERE status = 'published' 
        GROUP BY region ORDER BY count DESC
        """)
        regions = cursor.fetchall()

        cursor.execute("""
        SELECT opportunity_type, COUNT(*) as count 
        FROM posts WHERE status = 'published' 
        GROUP BY opportunity_type ORDER BY count DESC
        """)
        opportunity_types = cursor.fetchall()
        
        cursor.execute("""
        SELECT 
            COUNT(*) as total_posts,
            COALESCE(SUM(likes_count), 0) as total_likes,
            COALESCE(SUM(views_count), 0) as total_views,
            (SELECT COUNT(*) FROM comments) as total_comments
        FROM posts WHERE status = 'published'
        """)
        stats = cursor.fetchone()
        
        return {
            "categories": categories,
            "regions": regions,
            "opportunity_types": opportunity_types,
            "stats": stats
        }
