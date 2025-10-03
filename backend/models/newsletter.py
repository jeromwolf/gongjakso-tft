"""
Newsletter Models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
import uuid

from core.database import Base


class NewsletterStatus(str, enum.Enum):
    """Newsletter status"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENT = "sent"
    FAILED = "failed"


class RequestStatus(str, enum.Enum):
    """Newsletter request status"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Subscriber(Base):
    """Newsletter subscriber (회원가입 불필요)"""
    __tablename__ = "subscribers"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Contact Info
    email = Column(String(255), unique=True, nullable=False, index=True)

    # User Connection (optional)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Subscription Status
    is_active = Column(Boolean, default=False, nullable=False)
    unsubscribe_token = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    confirmation_token = Column(String(36), unique=True, nullable=True, default=lambda: str(uuid.uuid4()))
    confirmed_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    subscribed_at = Column(DateTime(timezone=True), nullable=True)
    unsubscribed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="newsletter_subscription")

    def __repr__(self):
        return f"<Subscriber(id={self.id}, email='{self.email}', is_active={self.is_active})>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "subscribed_at": self.subscribed_at.isoformat() if self.subscribed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Newsletter(Base):
    """Newsletter content (AI 자동 생성)"""
    __tablename__ = "newsletters"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Content
    title = Column(String(200), nullable=False)
    summary = Column(String(500), nullable=True)  # Short summary
    content = Column(Text, nullable=False)  # HTML content

    # Status
    status = Column(SQLEnum(NewsletterStatus), nullable=False, default=NewsletterStatus.DRAFT, index=True)

    # Period (데이터 집계 기간)
    period_start = Column(DateTime(timezone=True), nullable=True)
    period_end = Column(DateTime(timezone=True), nullable=True)

    # Sources (JSON)
    source_blog_ids = Column(JSON, nullable=True)  # List of blog IDs
    source_projects = Column(JSON, nullable=True)  # GitHub project updates

    # AI Generation
    is_auto_generated = Column(Boolean, default=False, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Scheduling
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    recipient_count = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<Newsletter(id={self.id}, title='{self.title}', status='{self.status}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "content": self.content,
            "status": self.status.value,
            "period_start": self.period_start.isoformat() if self.period_start else None,
            "period_end": self.period_end.isoformat() if self.period_end else None,
            "is_auto_generated": self.is_auto_generated,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "recipient_count": self.recipient_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class NewsletterRequest(Base):
    """Newsletter topic request (게스트 가능)"""
    __tablename__ = "newsletter_requests"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Requester Info
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    email = Column(String(255), nullable=False, index=True)  # For guests
    name = Column(String(100), nullable=True)  # For guests

    # Request
    topic = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Integer, default=0, nullable=False)  # Higher = more important
    votes = Column(Integer, default=0, nullable=False)

    # Status
    status = Column(SQLEnum(RequestStatus), nullable=False, default=RequestStatus.PENDING, index=True)

    # Newsletter Inclusion
    is_included = Column(Boolean, default=False, nullable=False)
    included_at = Column(DateTime(timezone=True), nullable=True)
    newsletter_id = Column(Integer, ForeignKey("newsletters.id", ondelete="SET NULL"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="newsletter_requests")
    newsletter = relationship("Newsletter")

    def __repr__(self):
        return f"<NewsletterRequest(id={self.id}, topic='{self.topic}', status='{self.status}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "topic": self.topic,
            "description": self.description,
            "votes": self.votes,
            "status": self.status.value,
            "is_included": self.is_included,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
