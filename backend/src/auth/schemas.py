"""
Pydantic schemas for authentication requests and responses.

This module provides validation schemas for authentication
endpoints including signup, signin, and signout.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class SignupRequest(BaseModel):
    """Request schema for user registration."""

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=128, description="Password (min 8 characters)")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class SignupResponse(BaseModel):
    """Response schema for successful registration."""

    user: dict
    session: dict


class SigninRequest(BaseModel):
    """Request schema for user sign in."""

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class SigninResponse(BaseModel):
    """Response schema for successful sign in."""

    user: dict
    session: dict


class SignoutResponse(BaseModel):
    """Response schema for successful sign out."""

    message: str = "Successfully signed out"


class ErrorResponse(BaseModel):
    """Generic error response schema."""

    detail: str


class TokenResponse(BaseModel):
    """Response schema for token-based authentication."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
