"""
Rate limiting utilities for the AI chatbot application.
"""

import time
from typing import Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class RateLimitInfo:
    """Information about rate limiting for a user."""
    requests_made: int = 0
    window_start: datetime = field(default_factory=datetime.now)
    last_request: Optional[datetime] = None
    is_blocked: bool = False
    block_until: Optional[datetime] = None


class RateLimiter:
    """Rate limiter for controlling API usage."""
    
    def __init__(self, max_requests: int = 100, window_minutes: int = 60):
        self.max_requests = max_requests
        self.window_minutes = window_minutes
        self.users: Dict[str, RateLimitInfo] = {}
    
    def is_allowed(self, user_id: str) -> bool:
        """Check if user is allowed to make a request."""
        now = datetime.now()
        
        if user_id not in self.users:
            self.users[user_id] = RateLimitInfo()
        
        user_info = self.users[user_id]
        
        # Check if user is currently blocked
        if user_info.is_blocked and user_info.block_until:
            if now < user_info.block_until:
                return False
            else:
                # Unblock user
                user_info.is_blocked = False
                user_info.block_until = None
        
        # Check if we need to reset the window
        window_age = now - user_info.window_start
        if window_age >= timedelta(minutes=self.window_minutes):
            user_info.requests_made = 0
            user_info.window_start = now
        
        # Check if user has exceeded rate limit
        if user_info.requests_made >= self.max_requests:
            user_info.is_blocked = True
            user_info.block_until = now + timedelta(minutes=self.window_minutes)
            return False
        
        # Allow request and increment counter
        user_info.requests_made += 1
        user_info.last_request = now
        return True
    
    def get_remaining_requests(self, user_id: str) -> int:
        """Get remaining requests for user."""
        if user_id not in self.users:
            return self.max_requests
        
        user_info = self.users[user_id]
        return max(0, self.max_requests - user_info.requests_made)
    
    def get_reset_time(self, user_id: str) -> Optional[datetime]:
        """Get when the rate limit resets for user."""
        if user_id not in self.users:
            return None
        
        user_info = self.users[user_id]
        return user_info.window_start + timedelta(minutes=self.window_minutes)


def check_rate_limit(user_id: str, rate_limiter: RateLimiter) -> Dict[str, any]:
    """Check rate limit status for a user."""
    is_allowed = rate_limiter.is_allowed(user_id)
    remaining = rate_limiter.get_remaining_requests(user_id)
    reset_time = rate_limiter.get_reset_time(user_id)
    
    return {
        'allowed': is_allowed,
        'remaining': remaining,
        'reset_time': reset_time.isoformat() if reset_time else None
    }
