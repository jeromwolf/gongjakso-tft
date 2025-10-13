"""
Activity API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from math import ceil

from core.database import get_db
from models.user import User
from models.activity import ActivityType
from schemas.activity import (
    ActivityCreate, ActivityUpdate, ActivityResponse,
    ActivityListItem, ActivityListResponse
)
from services import activity_service
from utils.dependencies import get_current_active_user


router = APIRouter(prefix="/api/activity", tags=["Activity"])


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_data: ActivityCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new activity

    - **title**: Activity title
    - **description**: Activity description (Markdown)
    - **activity_date**: Date and time when the activity occurred
    - **type**: Type of activity (meeting, seminar, study, project)
    - **participants**: Number of participants (optional)
    - **location**: Location of activity (optional)
    - **images**: List of image URLs (optional)

    Requires authentication
    """
    activity = await activity_service.create_activity(db, activity_data, current_user.id)
    return ActivityResponse.model_validate(activity)


@router.get("", response_model=ActivityListResponse)
async def list_activities(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    activity_type: Optional[ActivityType] = Query(None, description="Filter by activity type"),
    db: AsyncSession = Depends(get_db)
):
    """
    List activities with pagination

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    - **activity_type**: Filter by type (optional)

    Public endpoint (no authentication required)
    """
    skip = (page - 1) * page_size
    activities, total = await activity_service.list_activities(
        db,
        skip=skip,
        limit=page_size,
        activity_type=activity_type
    )

    # Convert to list items
    items = [ActivityListItem.model_validate(activity) for activity in activities]

    return ActivityListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=ceil(total / page_size) if total > 0 else 0
    )


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get activity by ID

    - **activity_id**: Activity ID

    Public endpoint (no authentication required)
    """
    activity = await activity_service.get_activity_by_id(db, activity_id)

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    return ActivityResponse.model_validate(activity)


@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: int,
    activity_data: ActivityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update an activity

    - **activity_id**: Activity ID
    - **title**: New title (optional)
    - **description**: New description (optional)
    - **activity_date**: New date (optional)
    - **type**: New type (optional)
    - **participants**: New participants count (optional)
    - **location**: New location (optional)
    - **images**: New images list (optional)

    Requires authentication
    Only the creator can update their own activities
    """
    activity = await activity_service.get_activity_by_id(db, activity_id)

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    # Check if user is the creator
    if activity.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this activity"
        )

    updated_activity = await activity_service.update_activity(db, activity, activity_data)
    return ActivityResponse.model_validate(updated_activity)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an activity

    - **activity_id**: Activity ID

    Requires authentication
    Only the creator can delete their own activities
    """
    activity = await activity_service.get_activity_by_id(db, activity_id)

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    # Check if user is the creator
    if activity.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this activity"
        )

    await activity_service.delete_activity(db, activity)
    return None
