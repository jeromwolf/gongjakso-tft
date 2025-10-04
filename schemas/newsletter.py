"""
Newsletter Pydantic Schemas
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from models.newsletter import NewsletterStatus, RequestStatus


# ============ Subscriber Schemas ============

class SubscriberCreate(BaseModel):
    """Schema for newsletter subscription (게스트)"""
    email: EmailStr = Field(..., description="Subscription email")


class SubscriberResponse(BaseModel):
    """Schema for subscriber response"""
    id: int
    email: str
    is_active: bool
    subscribed_at: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SubscriptionStatus(BaseModel):
    """Schema for subscription status check"""
    subscribed: bool
    email: str
    subscribed_at: Optional[datetime] = None


# ============ Newsletter Schemas ============

class NewsletterCreate(BaseModel):
    """Schema for creating newsletter (Admin/Manual)"""
    title: str = Field(..., min_length=1, max_length=200)
    summary: Optional[str] = Field(None, max_length=500)
    content: str = Field(..., min_length=1, description="HTML content")


class NewsletterUpdate(BaseModel):
    """Schema for updating newsletter"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    summary: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = None
    status: Optional[NewsletterStatus] = None


class NewsletterResponse(BaseModel):
    """Schema for newsletter response"""
    id: int
    title: str
    summary: Optional[str]
    content: str
    status: NewsletterStatus
    period_start: Optional[datetime]
    period_end: Optional[datetime]
    is_auto_generated: bool
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    recipient_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NewsletterListItem(BaseModel):
    """Schema for newsletter in list view"""
    id: int
    title: str
    summary: Optional[str]
    status: NewsletterStatus
    is_auto_generated: bool
    sent_at: Optional[datetime]
    recipient_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NewsletterGenerateRequest(BaseModel):
    """Schema for AI newsletter generation request"""
    period_days: int = Field(1, ge=1, le=30, description="Period in days (1=daily, 7=weekly)")


class NewsletterSendRequest(BaseModel):
    """Schema for sending newsletter"""
    test_email: Optional[EmailStr] = Field(None, description="Send test email instead of all subscribers")


# ============ Newsletter Request Schemas ============

class NewsletterRequestCreate(BaseModel):
    """Schema for topic request (게스트)"""
    email: EmailStr = Field(..., description="Requester email")
    name: Optional[str] = Field(None, max_length=100, description="Requester name")
    topic: str = Field(..., min_length=1, max_length=200, description="Requested topic")
    description: Optional[str] = Field(None, description="Detailed description")


class NewsletterRequestCreateAuth(BaseModel):
    """Schema for topic request (회원)"""
    topic: str = Field(..., min_length=1, max_length=200, description="Requested topic")
    description: Optional[str] = Field(None, description="Detailed description")


class NewsletterRequestUpdate(BaseModel):
    """Schema for updating request status (Admin)"""
    status: RequestStatus
    priority: Optional[int] = Field(None, ge=0, le=100)


class NewsletterRequestResponse(BaseModel):
    """Schema for newsletter request response"""
    id: int
    topic: str
    description: Optional[str]
    votes: int
    status: RequestStatus
    is_included: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NewsletterRequestVote(BaseModel):
    """Schema for voting on a request"""
    vote: int = Field(1, ge=-1, le=1, description="Vote value: 1 (upvote), -1 (downvote)")


# ============ Statistics Schemas ============

class NewsletterStats(BaseModel):
    """Schema for newsletter statistics"""
    total_subscribers: int
    active_subscribers: int
    total_newsletters: int
    total_sent: int
    pending_requests: int
    this_month_sent: int
