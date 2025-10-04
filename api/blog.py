"""
Blog API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from math import ceil

from core.database import get_db
from models.user import User
from models.blog import BlogStatus
from schemas.blog import (
    BlogCreate, BlogUpdate, BlogResponse, BlogListItem,
    BlogListResponse, BlogPublishRequest
)
from services import blog_service
from utils.dependencies import get_current_active_user, get_optional_user


router = APIRouter(prefix="/api/blog", tags=["Blog"])


@router.post("", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog_data: BlogCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new blog post

    - **title**: Blog post title
    - **content**: Blog post content (Markdown)
    - **excerpt**: Short description (optional)
    - **status**: Blog post status (draft/published/archived)
    - **tags**: List of tags (optional)

    Requires authentication
    """
    blog = await blog_service.create_blog(db, blog_data, current_user.id)
    return BlogResponse.model_validate(blog)


@router.get("", response_model=BlogListResponse)
async def list_blogs(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    status: Optional[BlogStatus] = Query(None, description="Filter by status"),
    author_id: Optional[int] = Query(None, description="Filter by author ID"),
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List blog posts with pagination

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    - **status**: Filter by status (optional)
    - **author_id**: Filter by author ID (optional)

    Public endpoint (no authentication required)
    Only shows PUBLISHED posts unless user is authenticated
    """
    # If user is not authenticated, only show published posts
    if current_user is None and status != BlogStatus.PUBLISHED:
        status = BlogStatus.PUBLISHED

    skip = (page - 1) * page_size
    blogs, total = await blog_service.list_blogs(
        db,
        skip=skip,
        limit=page_size,
        status=status,
        author_id=author_id
    )

    # Convert to list items
    items = [BlogListItem.model_validate(blog) for blog in blogs]

    return BlogListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=ceil(total / page_size) if total > 0 else 0
    )


@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(
    blog_id: int,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get blog post by ID

    - **blog_id**: Blog post ID

    Public endpoint (no authentication required)
    Only shows PUBLISHED posts unless user is authenticated
    """
    blog = await blog_service.get_blog_by_id(db, blog_id)

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )

    # Check if user can view this blog
    if blog.status != BlogStatus.PUBLISHED:
        if not current_user or (current_user.id != blog.author_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view this blog post"
            )

    # Increment view count
    await blog_service.increment_view_count(db, blog)

    return BlogResponse.model_validate(blog)


@router.get("/slug/{slug}", response_model=BlogResponse)
async def get_blog_by_slug(
    slug: str,
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get blog post by slug

    - **slug**: Blog post slug (URL-friendly identifier)

    Public endpoint (no authentication required)
    Only shows PUBLISHED posts unless user is authenticated
    """
    blog = await blog_service.get_blog_by_slug(db, slug)

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )

    # Check if user can view this blog
    if blog.status != BlogStatus.PUBLISHED:
        if not current_user or (current_user.id != blog.author_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view this blog post"
            )

    # Increment view count
    await blog_service.increment_view_count(db, blog)

    return BlogResponse.model_validate(blog)


@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: int,
    blog_data: BlogUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a blog post

    - **blog_id**: Blog post ID
    - **title**: New title (optional)
    - **content**: New content (optional)
    - **excerpt**: New excerpt (optional)
    - **status**: New status (optional)
    - **tags**: New tags (optional)

    Requires authentication
    Only the author can update their own blog posts
    """
    blog = await blog_service.get_blog_by_id(db, blog_id)

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )

    # Check if user is the author
    if blog.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this blog post"
        )

    updated_blog = await blog_service.update_blog(db, blog, blog_data)
    return BlogResponse.model_validate(updated_blog)


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a blog post

    - **blog_id**: Blog post ID

    Requires authentication
    Only the author can delete their own blog posts
    """
    blog = await blog_service.get_blog_by_id(db, blog_id)

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )

    # Check if user is the author
    if blog.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this blog post"
        )

    await blog_service.delete_blog(db, blog)
    return None


@router.post("/{blog_id}/publish", response_model=BlogResponse)
async def publish_blog(
    blog_id: int,
    publish_data: BlogPublishRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Publish or unpublish a blog post

    - **blog_id**: Blog post ID
    - **publish**: True to publish, False to unpublish

    Requires authentication
    Only the author can publish/unpublish their own blog posts
    """
    blog = await blog_service.get_blog_by_id(db, blog_id)

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found"
        )

    # Check if user is the author
    if blog.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to publish this blog post"
        )

    if publish_data.publish:
        updated_blog = await blog_service.publish_blog(db, blog)
    else:
        updated_blog = await blog_service.unpublish_blog(db, blog)

    return BlogResponse.model_validate(updated_blog)
