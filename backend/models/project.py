"""
Project Model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, JSON, Index
from sqlalchemy.sql import func
from datetime import datetime
import enum

from core.database import Base


class ProjectStatus(str, enum.Enum):
    """Project status"""
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(Base):
    """Project model for showcasing work"""
    __tablename__ = "projects"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Basic Info
    name = Column(String(200), nullable=False, index=True)
    slug = Column(String(250), unique=True, nullable=False, index=True)
    description = Column(String(500), nullable=True)  # Short description
    content = Column(Text, nullable=True)  # Detailed description (Markdown)

    # Links
    github_url = Column(String(500), nullable=True)
    github_url_2 = Column(String(500), nullable=True)  # Secondary GitHub repository
    demo_url = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)

    # Tech Stack
    tech_stack = Column(JSON, nullable=True)  # ["Python", "FastAPI", "React"]

    # Status
    status = Column(SQLEnum(ProjectStatus), nullable=False, default=ProjectStatus.ACTIVE, index=True)

    # Metadata
    category = Column(String(100), nullable=True)  # "Web", "AI", "Data"
    difficulty = Column(String(50), nullable=True)  # "Beginner", "Intermediate", "Advanced"

    # Analytics
    view_count = Column(Integer, default=0, nullable=False)
    star_count = Column(Integer, default=0, nullable=False)  # GitHub stars or bookmarks

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Indexes for performance
    __table_args__ = (
        Index('idx_project_status_created', 'status', 'created_at'),
        Index('idx_project_category', 'category'),
    )

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "content": self.content,
            "github_url": self.github_url,
            "github_url_2": self.github_url_2,
            "demo_url": self.demo_url,
            "thumbnail_url": self.thumbnail_url,
            "tech_stack": self.tech_stack,
            "status": self.status.value,
            "category": self.category,
            "difficulty": self.difficulty,
            "view_count": self.view_count,
            "star_count": self.star_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
