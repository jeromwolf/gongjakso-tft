"""
Blog Model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, Index, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from core.database import Base


class BlogStatus(str, enum.Enum):
    """Blog post status"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Blog(Base):
    """Blog post model"""
    __tablename__ = "blogs"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Content Fields
    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(250), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)  # Markdown content
    excerpt = Column(String(500), nullable=True)  # Short description

    # Metadata
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(SQLEnum(BlogStatus), nullable=False, default=BlogStatus.DRAFT, index=True)
    tags = Column(String(500), nullable=True)  # Comma-separated tags

    # Relationships
    author = relationship("User", back_populates="blogs")

    # Analytics
    view_count = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)

    # Indexes for performance
    __table_args__ = (
        Index('idx_blog_status_created', 'status', 'created_at'),
        Index('idx_blog_published_at', 'published_at'),
    )

    @property
    def author_name(self) -> str:
        """Get author name from relationship"""
        return self.author.name if self.author else "Unknown"

    @property
    def tags_list(self) -> list[str]:
        """Convert comma-separated tags to list"""
        return self.tags.split(",") if self.tags else []

    def __repr__(self):
        return f"<Blog(id={self.id}, title='{self.title}', status='{self.status}')>"

    def to_dict(self, include_author=True):
        """Convert model to dictionary"""
        data = {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "excerpt": self.excerpt,
            "author_id": self.author_id,
            "status": self.status.value,
            "tags": self.tags.split(",") if self.tags else [],
            "view_count": self.view_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
        }

        # Include author information if available
        if include_author and self.author:
            data["author"] = {
                "id": self.author.id,
                "name": self.author.name,
                "email": self.author.email
            }

        return data
