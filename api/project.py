"""
Project API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from math import ceil

from core.database import get_db
from models.user import User, UserRole
from models.project import ProjectStatus
from schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListItem,
    ProjectListResponse
)
from services import project_service
from utils.dependencies import get_current_active_user


router = APIRouter(prefix="/api/projects", tags=["Projects"])


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency to require admin role
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new project

    - **name**: Project name
    - **slug**: URL-friendly identifier (must be unique)
    - **description**: Short description (optional)
    - **content**: Detailed description in Markdown (optional)
    - **github_url**: GitHub repository URL (optional)
    - **demo_url**: Live demo URL (optional)
    - **thumbnail_url**: Thumbnail image URL (optional)
    - **tech_stack**: List of technologies (optional)
    - **status**: Project status (optional, default: active)
    - **category**: Project category (optional)
    - **difficulty**: Difficulty level (optional)

    Requires admin authentication
    """
    project = await project_service.create_project(db, project_data)
    return ProjectResponse.model_validate(project)


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    status: Optional[ProjectStatus] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db)
):
    """
    List projects with pagination

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    - **status**: Filter by status (optional)
    - **category**: Filter by category (optional)

    Public endpoint (no authentication required)
    """
    skip = (page - 1) * page_size
    projects, total = await project_service.list_projects(
        db,
        skip=skip,
        limit=page_size,
        status=status,
        category=category
    )

    # Convert to list items
    items = [ProjectListItem.model_validate(project) for project in projects]

    return ProjectListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=ceil(total / page_size) if total > 0 else 0
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get project by ID

    - **project_id**: Project ID

    Public endpoint (no authentication required)
    Increments view count
    """
    project = await project_service.get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Increment view count
    await project_service.increment_view_count(db, project)

    return ProjectResponse.model_validate(project)


@router.get("/slug/{slug}", response_model=ProjectResponse)
async def get_project_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get project by slug

    - **slug**: Project slug (URL-friendly identifier)

    Public endpoint (no authentication required)
    Increments view count
    """
    project = await project_service.get_project_by_slug(db, slug)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Increment view count
    await project_service.increment_view_count(db, project)

    return ProjectResponse.model_validate(project)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a project

    - **project_id**: Project ID
    - All fields are optional (only provided fields will be updated)

    Requires admin authentication
    """
    project = await project_service.get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    updated_project = await project_service.update_project(db, project, project_data)
    return ProjectResponse.model_validate(updated_project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a project

    - **project_id**: Project ID

    Requires admin authentication
    """
    project = await project_service.get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    await project_service.delete_project(db, project)
    return None
