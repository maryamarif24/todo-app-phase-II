"""
Authentication middleware for session validation.

This module provides FastAPI dependencies for validating
authentication sessions on protected routes.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..models import User


# HTTP Bearer token security scheme
bearer_scheme = HTTPBearer(auto_error=False)


class AuthenticatedUser:
    """Represents an authenticated user from session."""

    def __init__(self, user: User):
        self.user = user
        self.id = user.id
        self.email = user.email


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
) -> User:
    """
    Dependency to get the current authenticated user.

    Raises:
        HTTPException: 401 if not authenticated
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # In a real implementation, this would validate the token/session
    # and retrieve the user from the database
    # For now, this is a placeholder that will be properly implemented
    # with Better Auth session validation

    # TODO: Implement proper session validation with Better Auth
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
) -> Optional[User]:
    """
    Dependency to get the current user if authenticated, None otherwise.

    Used for routes that work both with and without authentication.
    """
    if not credentials:
        return None

    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
