"""
Project Service
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime
from loguru import logger

from models.project import Project, ProjectStatus
from schemas.project import ProjectCreate, ProjectUpdate
from utils.slug import slugify


async def create_project(
    db: AsyncSession,
    project_data: ProjectCreate
) -> Project:
    """
    Create a new project

    Args:
        db: Database session
        project_data: Project creation data

    Returns:
        Created project
    """
    # Generate slug from name if not provided
    if project_data.slug:
        slug = project_data.slug
    else:
        slug = slugify(project_data.name)

    # Ensure slug is unique
    counter = 1
    original_slug = slug
    while True:
        result = await db.execute(
            select(Project).where(Project.slug == slug)
        )
        if result.scalar_one_or_none() is None:
            break
        slug = f"{original_slug}-{counter}"
        counter += 1

    # Create project
    new_project = Project(
        name=project_data.name,
        slug=slug,
        description=project_data.description,
        content=project_data.content,
        github_url=project_data.github_url,
        github_url_2=project_data.github_url_2,
        demo_url=project_data.demo_url,
        thumbnail_url=project_data.thumbnail_url,
        tech_stack=project_data.tech_stack,
        status=ProjectStatus(project_data.status) if project_data.status else ProjectStatus.ACTIVE,
        category=project_data.category,
        difficulty=project_data.difficulty,
        view_count=0,
        star_count=0
    )

    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)

    logger.info(f"Project created: {new_project.name} (ID: {new_project.id}, Slug: {new_project.slug})")
    return new_project


async def get_project_by_id(db: AsyncSession, project_id: int) -> Optional[Project]:
    """
    Get project by ID

    Args:
        db: Database session
        project_id: Project ID

    Returns:
        Project if found, None otherwise
    """
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    return result.scalar_one_or_none()


async def get_project_by_slug(db: AsyncSession, slug: str) -> Optional[Project]:
    """
    Get project by slug

    Args:
        db: Database session
        slug: Project slug

    Returns:
        Project if found, None otherwise
    """
    result = await db.execute(
        select(Project).where(Project.slug == slug)
    )
    return result.scalar_one_or_none()


async def list_projects(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    status: Optional[ProjectStatus] = None,
    category: Optional[str] = None
) -> tuple[List[Project], int]:
    """
    List projects with pagination

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Filter by status (optional)
        category: Filter by category (optional)

    Returns:
        Tuple of (project list, total count)
    """
    # Build query
    query = select(Project)

    if status:
        query = query.where(Project.status == status)

    if category:
        query = query.where(Project.category == category)

    # Order by created_at (descending) - newest first
    query = query.order_by(Project.created_at.desc())

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Get paginated results
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    projects = result.scalars().all()

    return list(projects), total


async def update_project(
    db: AsyncSession,
    project: Project,
    project_data: ProjectUpdate
) -> Project:
    """
    Update a project

    Args:
        db: Database session
        project: Existing project
        project_data: Project update data

    Returns:
        Updated project
    """
    # Update fields
    if project_data.name is not None:
        project.name = project_data.name

    if project_data.slug is not None:
        project.slug = project_data.slug

    if project_data.description is not None:
        project.description = project_data.description

    if project_data.content is not None:
        project.content = project_data.content

    if project_data.github_url is not None:
        project.github_url = project_data.github_url

    if project_data.github_url_2 is not None:
        project.github_url_2 = project_data.github_url_2

    if project_data.demo_url is not None:
        project.demo_url = project_data.demo_url

    if project_data.thumbnail_url is not None:
        project.thumbnail_url = project_data.thumbnail_url

    if project_data.tech_stack is not None:
        project.tech_stack = project_data.tech_stack

    if project_data.status is not None:
        project.status = ProjectStatus(project_data.status)

    if project_data.category is not None:
        project.category = project_data.category

    if project_data.difficulty is not None:
        project.difficulty = project_data.difficulty

    await db.commit()
    await db.refresh(project)

    logger.info(f"Project updated: {project.name} (ID: {project.id})")
    return project


async def delete_project(db: AsyncSession, project: Project) -> None:
    """
    Delete a project

    Args:
        db: Database session
        project: Project to delete
    """
    project_id = project.id
    project_name = project.name

    await db.delete(project)
    await db.commit()

    logger.info(f"Project deleted: {project_name} (ID: {project_id})")


async def increment_view_count(db: AsyncSession, project: Project) -> Project:
    """
    Increment project view count

    Args:
        db: Database session
        project: Project

    Returns:
        Updated project
    """
    project.view_count += 1
    await db.commit()
    await db.refresh(project)
    return project
