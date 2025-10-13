"""
Activity Service
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime
from loguru import logger

from models.activity import Activity, ActivityType
from schemas.activity import ActivityCreate, ActivityUpdate


async def create_activity(
    db: AsyncSession,
    activity_data: ActivityCreate,
    creator_id: int
) -> Activity:
    """
    Create a new activity

    Args:
        db: Database session
        activity_data: Activity creation data
        creator_id: Creator user ID

    Returns:
        Created activity
    """
    # Create activity
    new_activity = Activity(
        title=activity_data.title,
        description=activity_data.description,
        activity_date=activity_data.activity_date,
        type=activity_data.type,
        participants=activity_data.participants,
        location=activity_data.location,
        images=activity_data.images or [],
        created_by=creator_id
    )

    db.add(new_activity)
    await db.commit()
    await db.refresh(new_activity)

    # Eagerly load creator relationship
    result = await db.execute(
        select(Activity).options(selectinload(Activity.creator)).where(Activity.id == new_activity.id)
    )
    activity_with_creator = result.scalar_one()

    logger.info(f"Activity created: {activity_with_creator.title} (ID: {activity_with_creator.id})")
    return activity_with_creator


async def get_activity_by_id(db: AsyncSession, activity_id: int) -> Optional[Activity]:
    """
    Get activity by ID

    Args:
        db: Database session
        activity_id: Activity ID

    Returns:
        Activity if found, None otherwise
    """
    result = await db.execute(
        select(Activity).options(selectinload(Activity.creator)).where(Activity.id == activity_id)
    )
    return result.scalar_one_or_none()


async def list_activities(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    activity_type: Optional[ActivityType] = None
) -> tuple[List[Activity], int]:
    """
    List activities with pagination

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        activity_type: Filter by activity type (optional)

    Returns:
        Tuple of (activity list, total count)
    """
    # Build query with eager loading
    query = select(Activity).options(selectinload(Activity.creator))

    if activity_type:
        query = query.where(Activity.type == activity_type)

    # Order by activity_date (descending)
    query = query.order_by(Activity.activity_date.desc())

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Get paginated results
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    activities = result.scalars().all()

    return list(activities), total


async def update_activity(
    db: AsyncSession,
    activity: Activity,
    activity_data: ActivityUpdate
) -> Activity:
    """
    Update an activity

    Args:
        db: Database session
        activity: Existing activity
        activity_data: Activity update data

    Returns:
        Updated activity
    """
    # Update fields
    if activity_data.title is not None:
        activity.title = activity_data.title

    if activity_data.description is not None:
        activity.description = activity_data.description

    if activity_data.activity_date is not None:
        activity.activity_date = activity_data.activity_date

    if activity_data.type is not None:
        activity.type = activity_data.type

    if activity_data.participants is not None:
        activity.participants = activity_data.participants

    if activity_data.location is not None:
        activity.location = activity_data.location

    if activity_data.images is not None:
        activity.images = activity_data.images

    await db.commit()
    await db.refresh(activity)

    logger.info(f"Activity updated: {activity.title} (ID: {activity.id})")
    return activity


async def delete_activity(db: AsyncSession, activity: Activity) -> None:
    """
    Delete an activity

    Args:
        db: Database session
        activity: Activity to delete
    """
    activity_id = activity.id
    activity_title = activity.title

    await db.delete(activity)
    await db.commit()

    logger.info(f"Activity deleted: {activity_title} (ID: {activity_id})")
