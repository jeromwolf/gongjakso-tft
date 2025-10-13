"""
Activity Model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, Index, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from core.database import Base


class ActivityType(str, enum.Enum):
    """Activity type"""
    MEETING = "meeting"
    SEMINAR = "seminar"
    STUDY = "study"
    PROJECT = "project"


class Activity(Base):
    """Activity model for team meetings, seminars, studies, and projects"""
    __tablename__ = "activities"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Content Fields
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)  # Markdown content

    # Activity Details
    activity_date = Column(DateTime(timezone=True), nullable=False, index=True)  # When the activity happened
    type = Column(SQLEnum(ActivityType), nullable=False, index=True)

    # Optional Fields
    participants = Column(Integer, nullable=True)  # Number of participants
    location = Column(String(200), nullable=True)  # Location of activity
    images = Column(JSON, nullable=True, default=list)  # Array of image URLs

    # Metadata
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relationships
    creator = relationship("User", back_populates="activities")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Indexes for performance
    __table_args__ = (
        Index('idx_activity_type_date', 'type', 'activity_date'),
        Index('idx_activity_date', 'activity_date'),
    )

    @property
    def creator_name(self) -> str:
        """Get creator name from relationship"""
        return self.creator.name if self.creator else "Unknown"

    def __repr__(self):
        return f"<Activity(id={self.id}, title='{self.title}', type='{self.type}')>"

    def to_dict(self, include_creator=True):
        """Convert model to dictionary"""
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "activity_date": self.activity_date.isoformat() if self.activity_date else None,
            "type": self.type.value,
            "participants": self.participants,
            "location": self.location,
            "images": self.images or [],
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        # Include creator information if available
        if include_creator and self.creator:
            data["creator"] = {
                "id": self.creator.id,
                "name": self.creator.name,
                "email": self.creator.email
            }

        return data
