"""
Validation utilities.
"""

from typing import Dict, Any
import re


def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection vulnerabilities."""
    # Escape special characters
    return re.escape(user_input)


def validate_message(message: Dict[str, Any]) -> bool:
    """Validate a chat message structure."""
    required_keys = {'id', 'role', 'content', 'timestamp', 'status'}
    return all(key in message for key in required_keys)


def validate_user_input(input_data: Dict[str, Any]) -> bool:
    """Validate expected structure of user input."""
    required_keys = {'message', 'history'}
    return all(key in input_data for key in required_keys)

