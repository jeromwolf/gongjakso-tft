"""
Blog Pydantic Schemas
"""
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional, List
from datetime import datetime
from models.blog import BlogStatus


class BlogBase(BaseModel):
    """Base blog schema"""
    title: str = Field(..., min_length=1, max_length=200, description="Blog post title")
    content: str = Field(..., min_length=1, description="Blog post content (Markdown)")
    excerpt: Optional[str] = Field(None, max_length=500, description="Short description")
    author: str = Field(default="Gongjakso TFT", max_length=100)
    tags: Optional[List[str]] = Field(default=None, description="Tags for the blog post")


class BlogCreate(BlogBase):
    """Schema for creating a new blog post"""
    status: BlogStatus = Field(default=BlogStatus.DRAFT, description="Blog post status")


class BlogUpdate(BaseModel):
    """Schema for updating a blog post"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    excerpt: Optional[str] = Field(None, max_length=500)
    author: Optional[str] = Field(None, max_length=100)
    status: Optional[BlogStatus] = None
    tags: Optional[List[str]] = None


class BlogResponse(BaseModel):
    """Schema for blog post response"""
    id: int
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    author: str = Field(alias="author_name", serialization_alias="author")
    tags: Optional[List[str]] = Field(alias="tags_list", serialization_alias="tags")
    status: BlogStatus
    view_count: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class BlogListItem(BaseModel):
    """Schema for blog post in list view (without full content)"""
    id: int
    title: str
    slug: str
    excerpt: Optional[str]
    author: str = Field(alias="author_name", serialization_alias="author")
    status: BlogStatus
    tags: Optional[List[str]] = Field(alias="tags_list", serialization_alias="tags")
    view_count: int
    created_at: datetime
    published_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class BlogListResponse(BaseModel):
    """Schema for paginated blog list response"""
    items: List[BlogListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


class BlogPublishRequest(BaseModel):
    """Schema for publishing a blog post"""
    publish: bool = Field(..., description="True to publish, False to unpublish")
