"""
AI Content Generation API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

from core.database import get_db
from models.user import User
from models.blog import Blog, BlogStatus
from models.newsletter import Newsletter, NewsletterStatus
from utils.dependencies import get_current_admin_user
from utils.slug import generate_unique_slug
from utils import content_generator
from loguru import logger


router = APIRouter(prefix="/api/ai", tags=["ai"])


# ============ Request Schemas ============

class GenerateBlogRequest(BaseModel):
    """Request schema for blog generation"""
    project_id: Optional[int] = Field(None, description="Project ID to write about")
    topic: Optional[str] = Field(None, description="Custom topic (if no project)")
    style: str = Field("technical", description="Writing style: technical, casual, tutorial")
    length: str = Field("medium", description="Content length: short, medium, long")
    save_as_draft: bool = Field(True, description="Save as draft instead of publishing")


class GenerateNewsletterRequest(BaseModel):
    """Request schema for newsletter generation"""
    period_days: int = Field(7, ge=1, le=30, description="Period in days (7=weekly, 30=monthly)")
    save_as_draft: bool = Field(True, description="Save as draft instead of sending")


class ContentPreviewRequest(BaseModel):
    """Request schema for content preview"""
    topic: str = Field(..., min_length=1, description="Topic for preview")
    style: str = Field("technical", description="Writing style")


# ============ Response Schemas ============

class GeneratedBlogResponse(BaseModel):
    """Response schema for generated blog"""
    blog_id: Optional[int] = None
    title: str
    excerpt: str
    content: str
    tags: list[str]
    status: str


class GeneratedNewsletterResponse(BaseModel):
    """Response schema for generated newsletter"""
    newsletter_id: Optional[int] = None
    title: str
    content: str
    status: str


# ============ Endpoints ============

@router.post("/generate-blog", response_model=GeneratedBlogResponse)
async def generate_blog(
    request: GenerateBlogRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Generate blog content using AI (Admin only)

    - If project_id is provided, generate blog about that project
    - Otherwise, use custom topic
    - Optionally save as draft in database
    """
    try:
        # Generate content
        if request.project_id:
            # Generate from project
            blog_content = await content_generator.generate_blog_from_project(
                db=db,
                project_id=request.project_id,
                style=request.style,
                length=request.length,
            )
        elif request.topic:
            # Generate from topic
            from services.ai_service import generate_blog_content

            blog_content = await generate_blog_content(
                topic=request.topic,
                style=request.style,
                length=request.length,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="project_id 또는 topic 중 하나를 제공해야 합니다.",
            )

        blog_id = None
        blog_status = "preview"

        # Save as draft if requested
        if request.save_as_draft:
            # Generate unique slug
            slug = await generate_unique_slug(db, Blog, blog_content["title"])

            # Create blog
            blog = Blog(
                title=blog_content["title"],
                slug=slug,
                content=blog_content["content"],
                excerpt=blog_content["excerpt"],
                tags=blog_content["tags"],
                status=BlogStatus.DRAFT,
                author_id=current_user.id,
            )

            db.add(blog)
            await db.commit()
            await db.refresh(blog)

            blog_id = blog.id
            blog_status = blog.status.value

            logger.info(f"Generated blog saved as draft: {blog.title} (ID: {blog.id})")

        return GeneratedBlogResponse(
            blog_id=blog_id,
            title=blog_content["title"],
            excerpt=blog_content["excerpt"],
            content=blog_content["content"],
            tags=blog_content["tags"],
            status=blog_status,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Failed to generate blog: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="블로그 생성에 실패했습니다.",
        )


@router.post("/generate-newsletter", response_model=GeneratedNewsletterResponse)
async def generate_newsletter(
    request: GenerateNewsletterRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Generate newsletter content using AI (Admin only)

    - Automatically collects recent blog posts and project updates
    - Generates newsletter content based on period
    - Optionally save as draft in database
    """
    try:
        # Generate newsletter
        newsletter_content = await content_generator.generate_newsletter_from_recent_content(
            db=db,
            period_days=request.period_days,
        )

        newsletter_id = None
        newsletter_status = "preview"

        # Save as draft if requested
        if request.save_as_draft:
            newsletter = Newsletter(
                title=newsletter_content["title"],
                content=newsletter_content["content"],
                status=NewsletterStatus.DRAFT,
                created_by=current_user.id,
                is_auto_generated=True,
            )

            db.add(newsletter)
            await db.commit()
            await db.refresh(newsletter)

            newsletter_id = newsletter.id
            newsletter_status = newsletter.status.value

            logger.info(f"Generated newsletter saved as draft: {newsletter.title} (ID: {newsletter.id})")

        return GeneratedNewsletterResponse(
            newsletter_id=newsletter_id,
            title=newsletter_content["title"],
            content=newsletter_content["content"],
            status=newsletter_status,
        )

    except Exception as e:
        logger.error(f"Failed to generate newsletter: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="뉴스레터 생성에 실패했습니다.",
        )


@router.post("/preview", response_model=dict)
async def preview_content(
    request: ContentPreviewRequest,
    current_user: User = Depends(get_current_admin_user),
):
    """
    Generate a preview of AI-generated content without saving (Admin only)
    """
    try:
        from services.ai_service import generate_blog_content

        blog_content = await generate_blog_content(
            topic=request.topic,
            style=request.style,
            length="short",  # Always use short for preview
        )

        return {
            "title": blog_content["title"],
            "excerpt": blog_content["excerpt"],
            "content_preview": blog_content["content"][:500] + "...",
            "tags": blog_content["tags"],
        }

    except Exception as e:
        logger.error(f"Failed to generate preview: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="미리보기 생성에 실패했습니다.",
        )
