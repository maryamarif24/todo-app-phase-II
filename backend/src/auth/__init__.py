"""
Authentication module exports.

This module provides authentication utilities for user authentication,
including password hashing and verification.
"""

from .config import auth_config, AuthConfig
from .server import verify_password, hash_password
from .middleware import get_current_user, get_optional_user, AuthenticatedUser
from .schemas import (
    SignupRequest,
    SignupResponse,
    SigninRequest,
    SigninResponse,
    SignoutResponse,
    ErrorResponse,
    TokenResponse,
)

__all__ = [
    "auth_config",
    "AuthConfig",
    "verify_password",
    "hash_password",
    "get_current_user",
    "get_optional_user",
    "AuthenticatedUser",
    "SignupRequest",
    "SignupResponse",
    "SigninRequest",
    "SigninResponse",
    "SignoutResponse",
    "ErrorResponse",
    "TokenResponse",
]
