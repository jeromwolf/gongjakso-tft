"""
Newsletter Service
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional, List
from datetime import datetime, timezone
import uuid

from models.newsletter import Subscriber, Newsletter, NewsletterRequest, NewsletterStatus
from schemas.newsletter import (
    SubscriberCreate,
    NewsletterCreate,
    NewsletterRequestCreate,
)
from services.email_service import send_newsletter, send_subscription_confirmation
from loguru import logger


# ============ Subscriber Functions ============

async def subscribe(
    db: AsyncSession,
    email: str,
) -> Subscriber:
    """
    Subscribe to newsletter

    Args:
        db: Database session
        email: Subscriber email

    Returns:
        Subscriber: Created or updated subscriber
    """
    # Check if subscriber already exists
    stmt = select(Subscriber).where(Subscriber.email == email)
    result = await db.execute(stmt)
    subscriber = result.scalar_one_or_none()

    if subscriber:
        # Reactivate if unsubscribed
        if not subscriber.is_active:
            subscriber.is_active = True
            subscriber.subscribed_at = datetime.now(timezone.utc)
            subscriber.unsubscribed_at = None
            await db.commit()
            await db.refresh(subscriber)
            logger.info(f"Reactivated subscription for {email}")
        else:
            logger.info(f"Already subscribed: {email}")
        return subscriber

    # Create new subscriber
    confirmation_token = str(uuid.uuid4())
    subscriber = Subscriber(
        email=email,
        is_active=True,  # Auto-activate (or require confirmation if needed)
        subscribed_at=datetime.now(timezone.utc),
        confirmation_token=confirmation_token,
    )

    db.add(subscriber)
    await db.commit()
    await db.refresh(subscriber)

    logger.info(f"New subscriber: {email}")

    # Send confirmation email (optional)
    # await send_subscription_confirmation(email, confirmation_token)

    return subscriber


async def unsubscribe(
    db: AsyncSession,
    email: str,
) -> bool:
    """
    Unsubscribe from newsletter

    Args:
        db: Database session
        email: Subscriber email

    Returns:
        bool: True if unsubscribed successfully
    """
    stmt = select(Subscriber).where(Subscriber.email == email)
    result = await db.execute(stmt)
    subscriber = result.scalar_one_or_none()

    if not subscriber:
        logger.warning(f"Subscriber not found: {email}")
        return False

    if not subscriber.is_active:
        logger.info(f"Already unsubscribed: {email}")
        return True

    subscriber.is_active = False
    subscriber.unsubscribed_at = datetime.now(timezone.utc)
    await db.commit()

    logger.info(f"Unsubscribed: {email}")
    return True


async def get_active_subscribers(db: AsyncSession) -> List[Subscriber]:
    """
    Get all active subscribers

    Args:
        db: Database session

    Returns:
        List[Subscriber]: Active subscribers
    """
    stmt = select(Subscriber).where(Subscriber.is_active == True)
    result = await db.execute(stmt)
    subscribers = result.scalars().all()
    return list(subscribers)


async def get_subscriber_by_email(
    db: AsyncSession,
    email: str,
) -> Optional[Subscriber]:
    """
    Get subscriber by email

    Args:
        db: Database session
        email: Subscriber email

    Returns:
        Optional[Subscriber]: Subscriber or None
    """
    stmt = select(Subscriber).where(Subscriber.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# ============ Newsletter Functions ============

async def create_newsletter(
    db: AsyncSession,
    title: str,
    content: str,
    created_by_id: Optional[int] = None,
) -> Newsletter:
    """
    Create a new newsletter

    Args:
        db: Database session
        title: Newsletter title
        content: Newsletter content
        created_by_id: User ID of creator (optional)

    Returns:
        Newsletter: Created newsletter
    """
    newsletter = Newsletter(
        title=title,
        content=content,
        status=NewsletterStatus.DRAFT,
        created_by=created_by_id,
        is_auto_generated=False,
    )

    db.add(newsletter)
    await db.commit()
    await db.refresh(newsletter)

    logger.info(f"Created newsletter: {title}")
    return newsletter


async def get_newsletter_by_id(
    db: AsyncSession,
    newsletter_id: int,
) -> Optional[Newsletter]:
    """
    Get newsletter by ID

    Args:
        db: Database session
        newsletter_id: Newsletter ID

    Returns:
        Optional[Newsletter]: Newsletter or None
    """
    stmt = select(Newsletter).where(Newsletter.id == newsletter_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def send_newsletter_to_all(
    db: AsyncSession,
    newsletter_id: int,
) -> int:
    """
    Send newsletter to all active subscribers

    Args:
        db: Database session
        newsletter_id: Newsletter ID

    Returns:
        int: Number of emails sent
    """
    # Get newsletter
    newsletter = await get_newsletter_by_id(db, newsletter_id)
    if not newsletter:
        logger.error(f"Newsletter not found: {newsletter_id}")
        raise ValueError("Newsletter not found")

    if newsletter.status == NewsletterStatus.SENT:
        logger.warning(f"Newsletter already sent: {newsletter_id}")
        return newsletter.recipient_count

    # Get active subscribers
    subscribers = await get_active_subscribers(db)
    if not subscribers:
        logger.warning("No active subscribers")
        return 0

    # Send emails in batches
    batch_size = 50
    sent_count = 0
    subscriber_emails = [sub.email for sub in subscribers]

    for i in range(0, len(subscriber_emails), batch_size):
        batch = subscriber_emails[i:i + batch_size]
        success = await send_newsletter(
            to=batch,
            title=newsletter.title,
            content=newsletter.content,
        )
        if success:
            sent_count += len(batch)
            logger.info(f"Sent newsletter to {len(batch)} subscribers (batch {i // batch_size + 1})")
        else:
            logger.error(f"Failed to send newsletter batch {i // batch_size + 1}")

    # Update newsletter status
    newsletter.status = NewsletterStatus.SENT
    newsletter.sent_at = datetime.now(timezone.utc)
    newsletter.recipient_count = sent_count
    await db.commit()
    await db.refresh(newsletter)

    logger.info(f"Newsletter sent to {sent_count} subscribers")
    return sent_count


# ============ Newsletter Request Functions ============

async def create_newsletter_request(
    db: AsyncSession,
    email: str,
    topic: str,
    description: Optional[str] = None,
    name: Optional[str] = None,
    user_id: Optional[int] = None,
) -> NewsletterRequest:
    """
    Create a newsletter topic request

    Args:
        db: Database session
        email: Requester email
        topic: Requested topic
        description: Detailed description (optional)
        name: Requester name (optional)
        user_id: User ID if authenticated (optional)

    Returns:
        NewsletterRequest: Created request
    """
    request = NewsletterRequest(
        email=email,
        topic=topic,
        description=description,
        name=name,
        user_id=user_id,
    )

    db.add(request)
    await db.commit()
    await db.refresh(request)

    logger.info(f"Newsletter request created: {topic} by {email}")
    return request


async def get_pending_requests(
    db: AsyncSession,
    limit: int = 100,
) -> List[NewsletterRequest]:
    """
    Get pending newsletter requests

    Args:
        db: Database session
        limit: Maximum number of requests to return

    Returns:
        List[NewsletterRequest]: Pending requests
    """
    from models.newsletter import RequestStatus

    stmt = (
        select(NewsletterRequest)
        .where(NewsletterRequest.status == RequestStatus.PENDING)
        .order_by(NewsletterRequest.priority.desc(), NewsletterRequest.votes.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())
