"""
Authentication API router module.

This module exports the authentication router with all endpoints.
"""

from .signup import router as auth_router

__all__ = ["auth_router"]
