"""
Todo API router module.

This module exports the todo router with all CRUD endpoints.
"""

from .list import router as todos_router

__all__ = ["todos_router"]
