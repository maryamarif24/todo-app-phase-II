"""
Authentication API endpoints.

Optimized for Neon PostgreSQL with sync database operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import datetime, timedelta

from src.models import User
from src.services import get_user_by_email, create_user, verify_password
from src.api import get_db, get_current_user
from src.auth.schemas import (
    SignupRequest,
    SignupResponse,
    SigninRequest,
    SigninResponse,
    SignoutResponse,
)
from src.auth.config import settings


router = APIRouter()


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new user account.

    Args:
        request: Signup request with email and password
        db: Database session

    Returns:
        Created user data

    Raises:
        HTTPException: 400 if email already registered or validation fails
    """
    # Check if email already exists
    existing_user = get_user_by_email(db, request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user (password is hashed in create_user)
    user = create_user(db, request.email, request.password)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create session for auto-login after signup
    session_token = str(user.id)
    expires_at = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)

    return SignupResponse(
        user={
            "id": str(user.id),
            "email": user.email,
        },
        session={
            "token": session_token,
            "expires_at": expires_at.isoformat(),
        },
    )


@router.post("/signin", response_model=SigninResponse)
async def signin(
    request: SigninRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate an existing user.

    Args:
        request: Signin request with email and password
        db: Database session

    Returns:
        User data and session information

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Verify credentials
    user = verify_password(db, request.email, request.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create session (simplified - using user ID as token for demo)
    session_token = str(user.id)

    return SigninResponse(
        user={
            "id": str(user.id),
            "email": user.email,
        },
        session={
            "token": session_token,
            "expires_at": datetime.utcnow().isoformat(),
        },
    )


@router.post("/signout", response_model=SignoutResponse)
async def signout(
    current_user: User = Depends(get_current_user),
):
    """
    Sign out the current user.

    Args:
        current_user: Authenticated user

    Returns:
        Success message
    """
    # In a real implementation, this would invalidate the session
    return SignoutResponse()
