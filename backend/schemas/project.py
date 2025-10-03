"""
Project Schemas for API request/response
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class ProjectCreate(BaseModel):
    """Schema for creating a new project"""
    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    slug: str = Field(..., min_length=1, max_length=250, description="URL-friendly slug")
    description: Optional[str] = Field(None, max_length=500, description="Short description")
    content: Optional[str] = Field(None, description="Detailed description in Markdown")

    github_url: Optional[str] = Field(None, max_length=500, description="GitHub repository URL")
    demo_url: Optional[str] = Field(None, max_length=500, description="Live demo URL")
    thumbnail_url: Optional[str] = Field(None, max_length=500, description="Thumbnail image URL")

    tech_stack: Optional[List[str]] = Field(None, description="Technologies used (e.g., ['Python', 'FastAPI'])")
    status: Optional[str] = Field("active", description="Project status: active, in_progress, completed, archived")
    category: Optional[str] = Field(None, max_length=100, description="Category (e.g., 'Web', 'AI', 'Data')")
    difficulty: Optional[str] = Field(None, max_length=50, description="Difficulty: Beginner, Intermediate, Advanced")


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=250)
    description: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = None

    github_url: Optional[str] = Field(None, max_length=500)
    demo_url: Optional[str] = Field(None, max_length=500)
    thumbnail_url: Optional[str] = Field(None, max_length=500)

    tech_stack: Optional[List[str]] = None
    status: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    difficulty: Optional[str] = Field(None, max_length=50)


class ProjectResponse(BaseModel):
    """Schema for project response (full details)"""
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    content: Optional[str] = None

    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    tech_stack: Optional[List[str]] = None
    status: str
    category: Optional[str] = None
    difficulty: Optional[str] = None

    view_count: int
    star_count: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectListItem(BaseModel):
    """Schema for project list item (without full content)"""
    id: int
    name: str
    slug: str
    description: Optional[str] = None

    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    tech_stack: Optional[List[str]] = None
    status: str
    category: Optional[str] = None
    difficulty: Optional[str] = None

    view_count: int
    star_count: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectListResponse(BaseModel):
    """Schema for paginated project list response"""
    items: List[ProjectListItem]
    total: int
    page: int
    page_size: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)
