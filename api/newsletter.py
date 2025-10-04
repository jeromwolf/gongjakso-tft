"""
Newsletter API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional

from core.database import get_db
from models.user import User
from models.newsletter import Subscriber, Newsletter, NewsletterRequest, NewsletterStatus
from schemas.newsletter import (
    SubscriberCreate,
    SubscriberResponse,
    SubscriptionStatus,
    NewsletterCreate,
    NewsletterResponse,
    NewsletterListItem,
    NewsletterRequestCreate,
    NewsletterRequestResponse,
)
from utils.dependencies import get_current_admin_user, get_optional_user
from services import newsletter_service
from loguru import logger


router = APIRouter(prefix="/api/newsletter", tags=["newsletter"])


# ============ Public Endpoints ============

@router.post("/subscribe", response_model=SubscriptionStatus, status_code=status.HTTP_201_CREATED)
async def subscribe_to_newsletter(
    data: SubscriberCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Subscribe to newsletter (public)
    """
    try:
        subscriber = await newsletter_service.subscribe(db, data.email)
        return SubscriptionStatus(
            subscribed=subscriber.is_active,
            email=subscriber.email,
            subscribed_at=subscriber.subscribed_at,
        )
    except Exception as e:
        logger.error(f"Failed to subscribe: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="구독에 실패했습니다. 다시 시도해주세요.",
        )


@router.post("/unsubscribe", status_code=status.HTTP_200_OK)
async def unsubscribe_from_newsletter(
    email: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Unsubscribe from newsletter (public)
    """
    success = await newsletter_service.unsubscribe(db, email)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="구독 정보를 찾을 수 없습니다.",
        )
    return {"message": "구독이 취소되었습니다."}


@router.post("/request", response_model=NewsletterRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_newsletter_request(
    data: NewsletterRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    """
    Create a newsletter topic request (public or authenticated)
    """
    try:
        request = await newsletter_service.create_newsletter_request(
            db=db,
            email=data.email,
            topic=data.topic,
            description=data.description,
            name=data.name,
            user_id=current_user.id if current_user else None,
        )
        return request
    except Exception as e:
        logger.error(f"Failed to create newsletter request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="뉴스레터 요청 생성에 실패했습니다.",
        )


# ============ Admin Endpoints ============

@router.get("/subscribers", response_model=dict)
async def get_subscribers(
    page: int = 1,
    page_size: int = 100,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Get subscriber list (Admin only)
    """
    # Build query
    stmt = select(Subscriber)

    # Filter by status
    if status:
        if status == "active":
            stmt = stmt.where(Subscriber.is_active == True)
        elif status == "unsubscribed":
            stmt = stmt.where(Subscriber.is_active == False)

    # Count total
    count_stmt = select(func.count()).select_from(Subscriber)
    if status:
        if status == "active":
            count_stmt = count_stmt.where(Subscriber.is_active == True)
        elif status == "unsubscribed":
            count_stmt = count_stmt.where(Subscriber.is_active == False)

    total_result = await db.execute(count_stmt)
    total = total_result.scalar()

    # Pagination
    offset = (page - 1) * page_size
    stmt = stmt.order_by(Subscriber.subscribed_at.desc()).offset(offset).limit(page_size)

    result = await db.execute(stmt)
    subscribers = result.scalars().all()

    # Convert to response format with status field
    items = []
    for subscriber in subscribers:
        item_dict = {
            "id": subscriber.id,
            "email": subscriber.email,
            "is_active": subscriber.is_active,
            "created_at": subscriber.subscribed_at,
            "subscribed_at": subscriber.subscribed_at,
            "unsubscribed_at": subscriber.unsubscribed_at,
        }
        items.append(item_dict)

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.get("", response_model=dict)
async def get_newsletter_list(
    page: int = 1,
    page_size: int = 20,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Get newsletter list with pagination
    """
    # Build query
    stmt = select(Newsletter)

    # Filter by status
    if status:
        try:
            status_enum = NewsletterStatus(status)
            stmt = stmt.where(Newsletter.status == status_enum)
        except ValueError:
            pass

    # Count total
    count_stmt = select(func.count()).select_from(Newsletter)
    if status:
        try:
            status_enum = NewsletterStatus(status)
            count_stmt = count_stmt.where(Newsletter.status == status_enum)
        except ValueError:
            pass

    total_result = await db.execute(count_stmt)
    total = total_result.scalar()

    # Pagination
    offset = (page - 1) * page_size
    stmt = stmt.order_by(Newsletter.created_at.desc()).offset(offset).limit(page_size)

    result = await db.execute(stmt)
    newsletters = result.scalars().all()

    # Convert to list items with sent_count field
    items = []
    for newsletter in newsletters:
        item_dict = {
            "id": newsletter.id,
            "title": newsletter.title,
            "status": newsletter.status.value,
            "sent_at": newsletter.sent_at,
            "sent_count": newsletter.recipient_count,  # Map recipient_count to sent_count
            "created_at": newsletter.created_at,
        }
        items.append(item_dict)

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.get("/{newsletter_id}", response_model=dict)
async def get_newsletter(
    newsletter_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get newsletter by ID
    """
    newsletter = await newsletter_service.get_newsletter_by_id(db, newsletter_id)
    if not newsletter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="뉴스레터를 찾을 수 없습니다.",
        )

    # Return with sent_count field
    return {
        "id": newsletter.id,
        "title": newsletter.title,
        "content": newsletter.content,
        "status": newsletter.status.value,
        "sent_at": newsletter.sent_at,
        "sent_count": newsletter.recipient_count,
        "created_at": newsletter.created_at,
        "updated_at": newsletter.updated_at,
    }


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_newsletter(
    data: NewsletterCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Create a new newsletter (Admin only)
    """
    try:
        newsletter = await newsletter_service.create_newsletter(
            db=db,
            title=data.title,
            content=data.content,
            created_by_id=current_user.id,
        )

        return {
            "id": newsletter.id,
            "title": newsletter.title,
            "content": newsletter.content,
            "status": newsletter.status.value,
            "sent_at": newsletter.sent_at,
            "sent_count": newsletter.recipient_count,
            "created_at": newsletter.created_at,
            "updated_at": newsletter.updated_at,
        }
    except Exception as e:
        logger.error(f"Failed to create newsletter: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="뉴스레터 생성에 실패했습니다.",
        )


@router.post("/{newsletter_id}/send", status_code=status.HTTP_200_OK)
async def send_newsletter(
    newsletter_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Send newsletter to all subscribers (Admin only)
    """
    try:
        sent_count = await newsletter_service.send_newsletter_to_all(db, newsletter_id)
        return {
            "message": f"{sent_count}명의 구독자에게 뉴스레터를 발송했습니다.",
            "sent_count": sent_count,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Failed to send newsletter: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="뉴스레터 발송에 실패했습니다.",
        )


