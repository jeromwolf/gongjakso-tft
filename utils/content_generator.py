"""
Content Generator Utilities
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta, timezone
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from models.blog import Blog
from models.project import Project
from services.ai_service import generate_blog_content, generate_newsletter_content
from loguru import logger


async def fetch_github_project_info(github_url: str) -> Optional[Dict[str, Any]]:
    """
    Fetch project information from GitHub

    Args:
        github_url: GitHub repository URL

    Returns:
        Optional[Dict]: Project information or None
    """
    try:
        # Extract owner and repo from URL
        # Example: https://github.com/owner/repo
        parts = github_url.rstrip('/').split('/')
        if len(parts) < 2:
            logger.warning(f"Invalid GitHub URL: {github_url}")
            return None

        owner = parts[-2]
        repo = parts[-1]

        # Fetch from GitHub API
        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)

            if response.status_code != 200:
                logger.warning(f"GitHub API request failed: {response.status_code}")
                return None

            data = response.json()

            return {
                "name": data.get("name"),
                "full_name": data.get("full_name"),
                "description": data.get("description"),
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "language": data.get("language"),
                "topics": data.get("topics", []),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at"),
                "html_url": data.get("html_url"),
            }

    except Exception as e:
        logger.error(f"Failed to fetch GitHub project info: {str(e)}")
        return None


async def get_recent_blogs(
    db: AsyncSession,
    days: int = 7,
    limit: int = 10,
) -> List[Blog]:
    """
    Get recent published blog posts

    Args:
        db: Database session
        days: Number of days to look back
        limit: Maximum number of posts

    Returns:
        List[Blog]: Recent blog posts
    """
    from models.blog import BlogStatus

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    stmt = (
        select(Blog)
        .where(
            and_(
                Blog.status == BlogStatus.PUBLISHED,
                Blog.published_at >= cutoff_date
            )
        )
        .order_by(Blog.published_at.desc())
        .limit(limit)
    )

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_recent_projects(
    db: AsyncSession,
    days: int = 30,
    limit: int = 10,
) -> List[Project]:
    """
    Get recently updated projects

    Args:
        db: Database session
        days: Number of days to look back
        limit: Maximum number of projects

    Returns:
        List[Project]: Recent projects
    """
    from models.project import ProjectStatus

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    stmt = (
        select(Project)
        .where(
            and_(
                Project.status.in_([ProjectStatus.ACTIVE, ProjectStatus.IN_PROGRESS]),
                Project.updated_at >= cutoff_date
            )
        )
        .order_by(Project.updated_at.desc())
        .limit(limit)
    )

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def generate_blog_from_project(
    db: AsyncSession,
    project_id: int,
    style: str = "technical",
    length: str = "medium",
) -> Dict[str, str]:
    """
    Generate a blog post about a project

    Args:
        db: Database session
        project_id: Project ID
        style: Writing style
        length: Content length

    Returns:
        Dict: Generated blog content
    """
    # Get project
    stmt = select(Project).where(Project.id == project_id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()

    if not project:
        raise ValueError(f"Project not found: {project_id}")

    # Prepare project data
    project_data = {
        "name": project.name,
        "description": project.description,
        "tech_stack": project.tech_stack or [],
        "github_url": project.github_url,
        "demo_url": project.demo_url,
    }

    # Fetch GitHub info if available
    if project.github_url:
        github_info = await fetch_github_project_info(project.github_url)
        if github_info:
            project_data.update({
                "stars": github_info.get("stars"),
                "language": github_info.get("language"),
                "topics": github_info.get("topics", []),
            })

    # Generate blog content
    topic = f"{project.name} 프로젝트 소개"

    blog_content = await generate_blog_content(
        topic=topic,
        style=style,
        length=length,
        project_data=project_data,
    )

    return blog_content


async def generate_newsletter_from_recent_content(
    db: AsyncSession,
    period_days: int = 7,
) -> Dict[str, str]:
    """
    Generate newsletter from recent blog posts and projects

    Args:
        db: Database session
        period_days: Period in days (7 for weekly, 30 for monthly)

    Returns:
        Dict: Generated newsletter content
    """
    # Get recent blogs
    blogs = await get_recent_blogs(db, days=period_days, limit=5)
    blog_data = [
        {
            "title": blog.title,
            "excerpt": blog.excerpt,
            "slug": blog.slug,
        }
        for blog in blogs
    ]

    # Get recent projects
    projects = await get_recent_projects(db, days=period_days * 2, limit=5)
    project_data = [
        {
            "name": project.name,
            "description": project.description,
            "slug": project.slug,
        }
        for project in projects
    ]

    # Generate newsletter
    newsletter_content = await generate_newsletter_content(
        period_days=period_days,
        blog_posts=blog_data if blog_data else None,
        projects=project_data if project_data else None,
    )

    return newsletter_content


def format_markdown_content(content: str) -> str:
    """
    Format markdown content for better readability

    Args:
        content: Raw markdown content

    Returns:
        str: Formatted markdown
    """
    # Basic formatting
    lines = content.split('\n')
    formatted = []

    for line in lines:
        # Ensure proper spacing around headers
        if line.startswith('#'):
            if formatted and formatted[-1].strip():
                formatted.append('')
            formatted.append(line)
            formatted.append('')
        # Ensure proper spacing around code blocks
        elif line.startswith('```'):
            if formatted and formatted[-1].strip():
                formatted.append('')
            formatted.append(line)
        else:
            formatted.append(line)

    return '\n'.join(formatted)


def extract_summary_from_content(content: str, max_length: int = 200) -> str:
    """
    Extract a summary from content

    Args:
        content: Full content text
        max_length: Maximum summary length

    Returns:
        str: Extracted summary
    """
    # Remove markdown headers
    lines = [line for line in content.split('\n') if not line.startswith('#')]

    # Get first paragraph
    for line in lines:
        line = line.strip()
        if line and not line.startswith('```'):
            # Truncate if too long
            if len(line) > max_length:
                return line[:max_length].rsplit(' ', 1)[0] + '...'
            return line

    return content[:max_length] + '...'
