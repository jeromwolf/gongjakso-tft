"""
User Pydantic Schemas
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from models.user import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., min_length=1, max_length=100, description="User name")


class UserCreate(UserBase):
    """Schema for creating a new user (sign up)"""
    password: str = Field(..., min_length=8, max_length=100, description="User password (min 8 characters)")


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    id: int
    email: str
    name: str
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserProfile(BaseModel):
    """Schema for public user profile"""
    id: int
    name: str
    email: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Schema for JWT token payload"""
    user_id: int
    email: str
    role: UserRole


class PasswordChange(BaseModel):
    """Schema for changing password"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password (min 8 characters)")
