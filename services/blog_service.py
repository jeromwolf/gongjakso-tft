"""
Blog Service
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime
from loguru import logger

from models.blog import Blog, BlogStatus
from schemas.blog import BlogCreate, BlogUpdate
from utils.slug import generate_unique_slug


async def create_blog(
    db: AsyncSession,
    blog_data: BlogCreate,
    author_id: int
) -> Blog:
    """
    Create a new blog post

    Args:
        db: Database session
        blog_data: Blog creation data
        author_id: Author user ID

    Returns:
        Created blog post
    """
    # Generate slug from title
    slug = generate_unique_slug(blog_data.title, datetime.utcnow())

    # Ensure slug is unique
    counter = 1
    original_slug = slug
    while True:
        result = await db.execute(
            select(Blog).where(Blog.slug == slug)
        )
        if result.scalar_one_or_none() is None:
            break
        slug = f"{original_slug}-{counter}"
        counter += 1

    # Create blog
    new_blog = Blog(
        title=blog_data.title,
        slug=slug,
        content=blog_data.content,
        excerpt=blog_data.excerpt,
        author_id=author_id,
        status=blog_data.status,
        tags=",".join(blog_data.tags) if blog_data.tags else None
    )

    # Set published_at if status is PUBLISHED
    if blog_data.status == BlogStatus.PUBLISHED:
        new_blog.published_at = datetime.utcnow()

    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)

    # Eagerly load author relationship
    result = await db.execute(
        select(Blog).options(selectinload(Blog.author)).where(Blog.id == new_blog.id)
    )
    blog_with_author = result.scalar_one()

    logger.info(f"Blog created: {blog_with_author.title} (ID: {blog_with_author.id}, Slug: {blog_with_author.slug})")
    return blog_with_author


async def get_blog_by_id(db: AsyncSession, blog_id: int) -> Optional[Blog]:
    """
    Get blog post by ID

    Args:
        db: Database session
        blog_id: Blog ID

    Returns:
        Blog post if found, None otherwise
    """
    result = await db.execute(
        select(Blog).options(selectinload(Blog.author)).where(Blog.id == blog_id)
    )
    return result.scalar_one_or_none()


async def get_blog_by_slug(db: AsyncSession, slug: str) -> Optional[Blog]:
    """
    Get blog post by slug

    Args:
        db: Database session
        slug: Blog slug

    Returns:
        Blog post if found, None otherwise
    """
    result = await db.execute(
        select(Blog).options(selectinload(Blog.author)).where(Blog.slug == slug)
    )
    return result.scalar_one_or_none()


async def list_blogs(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    status: Optional[BlogStatus] = None,
    author_id: Optional[int] = None
) -> tuple[List[Blog], int]:
    """
    List blog posts with pagination

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Filter by status (optional)
        author_id: Filter by author ID (optional)

    Returns:
        Tuple of (blog list, total count)
    """
    # Build query with eager loading
    query = select(Blog).options(selectinload(Blog.author))

    if status:
        query = query.where(Blog.status == status)

    if author_id:
        query = query.where(Blog.author_id == author_id)

    # Order by published_at or created_at (descending)
    query = query.order_by(
        Blog.published_at.desc().nulls_last(),
        Blog.created_at.desc()
    )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Get paginated results
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    blogs = result.scalars().all()

    return list(blogs), total


async def update_blog(
    db: AsyncSession,
    blog: Blog,
    blog_data: BlogUpdate
) -> Blog:
    """
    Update a blog post

    Args:
        db: Database session
        blog: Existing blog post
        blog_data: Blog update data

    Returns:
        Updated blog post
    """
    # Update fields
    if blog_data.title is not None:
        blog.title = blog_data.title
        # Regenerate slug
        blog.slug = generate_unique_slug(blog_data.title, datetime.utcnow())

    if blog_data.content is not None:
        blog.content = blog_data.content

    if blog_data.excerpt is not None:
        blog.excerpt = blog_data.excerpt

    if blog_data.author is not None:
        # Note: This updates the author STRING field (deprecated, should use author_id)
        pass

    if blog_data.status is not None:
        old_status = blog.status
        blog.status = blog_data.status

        # Set published_at when status changes to PUBLISHED
        if old_status != BlogStatus.PUBLISHED and blog_data.status == BlogStatus.PUBLISHED:
            blog.published_at = datetime.utcnow()

    if blog_data.tags is not None:
        blog.tags = ",".join(blog_data.tags) if blog_data.tags else None

    await db.commit()
    await db.refresh(blog)

    logger.info(f"Blog updated: {blog.title} (ID: {blog.id})")
    return blog


async def delete_blog(db: AsyncSession, blog: Blog) -> None:
    """
    Delete a blog post

    Args:
        db: Database session
        blog: Blog post to delete
    """
    blog_id = blog.id
    blog_title = blog.title

    await db.delete(blog)
    await db.commit()

    logger.info(f"Blog deleted: {blog_title} (ID: {blog_id})")


async def increment_view_count(db: AsyncSession, blog: Blog) -> Blog:
    """
    Increment blog view count

    Args:
        db: Database session
        blog: Blog post

    Returns:
        Updated blog post
    """
    blog.view_count += 1
    await db.commit()
    await db.refresh(blog)
    return blog


async def publish_blog(db: AsyncSession, blog: Blog) -> Blog:
    """
    Publish a blog post

    Args:
        db: Database session
        blog: Blog post to publish

    Returns:
        Published blog post
    """
    if blog.status != BlogStatus.PUBLISHED:
        blog.status = BlogStatus.PUBLISHED
        blog.published_at = datetime.utcnow()
        await db.commit()
        await db.refresh(blog)
        logger.info(f"Blog published: {blog.title} (ID: {blog.id})")

    return blog


async def unpublish_blog(db: AsyncSession, blog: Blog) -> Blog:
    """
    Unpublish a blog post (set to DRAFT)

    Args:
        db: Database session
        blog: Blog post to unpublish

    Returns:
        Unpublished blog post
    """
    if blog.status == BlogStatus.PUBLISHED:
        blog.status = BlogStatus.DRAFT
        await db.commit()
        await db.refresh(blog)
        logger.info(f"Blog unpublished: {blog.title} (ID: {blog.id})")

    return blog
