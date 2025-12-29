"""
Database initialization script for creating tables in Neon PostgreSQL.

Usage:
    python -m models.init_db
"""

import asyncio
from .database import init_db, close_db


async def main():
    """Run database initialization."""
    print("Initializing database tables...")
    await init_db()
    print("Database tables created successfully!")
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
