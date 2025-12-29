"""
Authentication configuration for Better Auth.

This module provides Better Auth configuration settings for
user authentication with session management.
"""

import os
from typing import Optional

from pydantic import BaseModel


class AuthConfig(BaseModel):
    """Better Auth configuration settings."""

    # Database URL for Better Auth
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@ep-xyz.region.neon.tech/dbname?sslmode=require"
    )

    # Secret key for signing tokens (generate with: openssl rand -base64 32)
    secret: str = os.getenv("BETTER_AUTH_SECRET", "default-secret-change-in-production")

    # Frontend URL for CORS and redirects
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Session max age in seconds (default: 24 hours)
    session_max_age: int = int(os.getenv("SESSION_MAX_AGE", "86400"))

    # JWT expiration in hours
    jwt_expiration_hours: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

    # Cookie settings
    cookie_name: str = "auth_session"
    cookie_secure: bool = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    cookie_same_site: str = "lax"

    # Email verification (disabled for MVP)
    email_verification_enabled: bool = False


# Global auth configuration instance
auth_config = AuthConfig()

# Export settings as alias for convenience
settings = auth_config
