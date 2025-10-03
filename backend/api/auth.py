"""
Authentication API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from loguru import logger

from core.database import get_db
from models.user import User
from schemas.user import (
    UserCreate, UserLogin, UserResponse, Token,
    UserUpdate, PasswordChange
)
from utils.auth import hash_password, verify_password, create_access_token
from utils.dependencies import get_current_user, get_current_active_user


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Sign up a new user

    - **email**: User email address (must be unique)
    - **name**: User name
    - **password**: User password (min 8 characters)
    """
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hash_password(user_data.password),
        is_active=True,
        is_verified=False
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    logger.info(f"New user created: {new_user.email} (ID: {new_user.id})")

    # Create access token
    access_token = create_access_token(
        data={
            "user_id": new_user.id,
            "email": new_user.email,
            "role": new_user.role.value
        }
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(new_user)
    )


@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Log in a user

    - **email**: User email address
    - **password**: User password
    """
    # Get user by email
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    await db.refresh(user)

    logger.info(f"User logged in: {user.email} (ID: {user.id})")

    # Create access token
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value
        }
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user profile

    Requires authentication
    """
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user profile

    - **name**: New user name (optional)
    - **email**: New email address (optional)

    Requires authentication
    """
    # Update user fields
    if user_update.name is not None:
        current_user.name = user_update.name

    if user_update.email is not None:
        # Check if email already exists
        result = await db.execute(
            select(User).where(
                User.email == user_update.email,
                User.id != current_user.id
            )
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )

        current_user.email = user_update.email

    await db.commit()
    await db.refresh(current_user)

    logger.info(f"User profile updated: {current_user.email} (ID: {current_user.id})")

    return UserResponse.model_validate(current_user)


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Change user password

    - **current_password**: Current password
    - **new_password**: New password (min 8 characters)

    Requires authentication
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Update password
    current_user.password_hash = hash_password(password_data.new_password)
    await db.commit()

    logger.info(f"Password changed for user: {current_user.email} (ID: {current_user.id})")

    return {"message": "Password changed successfully"}
