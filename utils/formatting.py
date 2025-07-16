# Utility functions for formatting outputs

from datetime import datetime
from typing import Dict, Any


def format_response(response: Dict[str, Any]) -> str:
    """Format a response dictionary to a user-friendly string."""
    content = response.get("content", "")
    timestamp = response.get("created_at", "")
    return f"Response: {content} (at {timestamp})"


def format_timestamp(timestamp: datetime) -> str:
    """Format a datetime object to a string."""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def format_user_message(user_id: str, message: str) -> str:
    """Format a user message to include user ID."""
    return f"[User {user_id}]: {message}"

