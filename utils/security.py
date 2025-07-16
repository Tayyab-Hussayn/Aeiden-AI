"""
Security utilities for the application.
"""

import hashlib
import secrets
from typing import str


def generate_session_token() -> str:
    """Generate a secure session token."""
    return secrets.token_urlsafe(32)


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == hashed_password
