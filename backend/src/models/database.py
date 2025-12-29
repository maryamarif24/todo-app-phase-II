"""
Database connection and session management for SQLModel.

Optimized for Neon PostgreSQL with sync driver for stability.
"""

import os
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@ep-xyz.region.neon.tech/dbname?sslmode=require"
)

# Create sync engine for SQLModel (more stable with Neon)
sync_engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600,
)


def get_db() -> Generator[Session, None, None]:
    """Dependency for getting database sessions."""
    with Session(sync_engine) as session:
        try:
            yield session
        finally:
            session.close()


def init_db() -> None:
    """Initialize database tables."""
    SQLModel.metadata.create_all(sync_engine)


def close_db() -> None:
    """Close database connections."""
    sync_engine.dispose()


class TimestampMixin:
    """Mixin for adding created_at and updated_at timestamps."""

    created_at: str = ""
    updated_at: str = ""
