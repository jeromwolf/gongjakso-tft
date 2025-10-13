"""
Activity Pydantic Schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from models.activity import ActivityType


class ActivityBase(BaseModel):
    """Base activity schema"""
    title: str = Field(..., min_length=1, max_length=200, description="Activity title")
    description: str = Field(..., min_length=1, description="Activity description (Markdown)")
    activity_date: datetime = Field(..., description="Date and time when the activity occurred")
    type: ActivityType = Field(..., description="Type of activity (meeting, seminar, study, project)")
    participants: Optional[int] = Field(None, ge=1, description="Number of participants")
    location: Optional[str] = Field(None, max_length=200, description="Location of activity")
    images: Optional[List[str]] = Field(default=None, description="List of image URLs")


class ActivityCreate(ActivityBase):
    """Schema for creating a new activity"""
    pass


class ActivityUpdate(BaseModel):
    """Schema for updating an activity"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    activity_date: Optional[datetime] = None
    type: Optional[ActivityType] = None
    participants: Optional[int] = Field(None, ge=1)
    location: Optional[str] = Field(None, max_length=200)
    images: Optional[List[str]] = None


class ActivityResponse(BaseModel):
    """Schema for activity response"""
    id: int
    title: str
    description: str
    activity_date: datetime
    type: ActivityType
    participants: Optional[int] = None
    location: Optional[str] = None
    images: List[str] = []
    created_by: int
    creator_name: str = Field(alias="creator_name")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ActivityListItem(BaseModel):
    """Schema for activity in list view"""
    id: int
    title: str
    activity_date: datetime
    type: ActivityType
    participants: Optional[int] = None
    location: Optional[str] = None
    images: List[str] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ActivityListResponse(BaseModel):
    """Schema for paginated activity list response"""
    items: List[ActivityListItem]
    total: int
    page: int
    page_size: int
    total_pages: int
