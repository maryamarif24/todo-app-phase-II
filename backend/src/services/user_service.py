"""
User service for database operations.

Optimized for Neon PostgreSQL with sync database operations.
"""

import uuid
from typing import Optional
from sqlmodel import select
from sqlmodel import Session
import bcrypt

from ..models import User


def create_user(session: Session, email: str, password: str) -> User:
    """
    Create a new user with hashed password.

    Args:
        session: Database session
        email: User's email address
        password: Plain text password (will be hashed)

    Returns:
        Created User instance
    """
    # Hash the password with lower rounds for faster hashing during development
    salt = bcrypt.gensalt(rounds=4)
    password_hash = bcrypt.hashpw(password.encode(), salt).decode()

    # Create user instance
    user = User(email=email, password_hash=password_hash)
    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by their email address.

    Args:
        session: Database session
        email: User's email address

    Returns:
        User instance if found, None otherwise
    """
    statement = select(User).where(User.email == email)
    result = session.execute(statement)
    return result.scalar_one_or_none()


def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
    """
    Retrieve a user by their ID.

    Args:
        session: Database session
        user_id: User's UUID

    Returns:
        User instance if found, None otherwise
    """
    statement = select(User).where(User.id == user_id)
    result = session.execute(statement)
    return result.scalar_one_or_none()


def verify_password(session: Session, email: str, password: str) -> Optional[User]:
    """
    Verify user credentials.

    Args:
        session: Database session
        email: User's email address
        password: Plain text password to verify

    Returns:
        User if credentials valid, None otherwise
    """
    user = get_user_by_email(session, email)
    if user is None:
        return None

    if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return user

    return None


def get_or_create_user(session: Session, email: str, password: str) -> User:
    """
    Get existing user or create new one.

    Args:
        session: Database session
        email: User's email address
        password: Password for new user

    Returns:
        User instance (existing or newly created)
    """
    user = get_user_by_email(session, email)
    if user:
        return user

    return create_user(session, email, password)
