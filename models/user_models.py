"""
User-related data models for the AI chatbot application.
"""

from datetime import datetime
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
from enum import Enum


class UserRole(Enum):
    """Enumeration for user roles."""
    GUEST = "guest"
    REGISTERED = "registered"
    PREMIUM = "premium"
    ADMIN = "admin"


class Theme(Enum):
    """Enumeration for UI themes."""
    DARK = "dark"
    LIGHT = "light"
    AUTO = "auto"


class Language(Enum):
    """Enumeration for supported languages."""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    ARABIC = "ar"
    HINDI = "hi"


@dataclass
class UserPreferences:
    """
    User preferences for the chatbot application.
    
    Attributes:
        theme: Preferred UI theme
        language: Preferred language
        notifications: Whether to show notifications
        sound_effects: Whether to play sound effects
        auto_scroll: Whether to auto-scroll chat
        message_preview: Whether to show message previews
        typing_indicators: Whether to show typing indicators
        message_timestamps: Whether to show message timestamps
        compact_mode: Whether to use compact UI mode
        accessibility_mode: Whether to enable accessibility features
    """
    theme: Theme = Theme.DARK
    language: Language = Language.ENGLISH
    notifications: bool = True
    sound_effects: bool = False
    auto_scroll: bool = True
    message_preview: bool = True
    typing_indicators: bool = True
    message_timestamps: bool = True
    compact_mode: bool = False
    accessibility_mode: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert preferences to dictionary format."""
        return {
            'theme': self.theme.value,
            'language': self.language.value,
            'notifications': self.notifications,
            'sound_effects': self.sound_effects,
            'auto_scroll': self.auto_scroll,
            'message_preview': self.message_preview,
            'typing_indicators': self.typing_indicators,
            'message_timestamps': self.message_timestamps,
            'compact_mode': self.compact_mode,
            'accessibility_mode': self.accessibility_mode
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        """Create UserPreferences from dictionary."""
        return cls(
            theme=Theme(data.get('theme', Theme.DARK.value)),
            language=Language(data.get('language', Language.ENGLISH.value)),
            notifications=data.get('notifications', True),
            sound_effects=data.get('sound_effects', False),
            auto_scroll=data.get('auto_scroll', True),
            message_preview=data.get('message_preview', True),
            typing_indicators=data.get('typing_indicators', True),
            message_timestamps=data.get('message_timestamps', True),
            compact_mode=data.get('compact_mode', False),
            accessibility_mode=data.get('accessibility_mode', False)
        )


@dataclass
class UserStats:
    """
    User statistics for the chatbot application.
    
    Attributes:
        total_messages: Total number of messages sent
        total_sessions: Total number of chat sessions
        total_time_spent: Total time spent in minutes
        favorite_topics: List of favorite discussion topics
        most_active_hours: Hours when user is most active
        average_session_length: Average session length in minutes
        last_activity: Last activity timestamp
    """
    total_messages: int = 0
    total_sessions: int = 0
    total_time_spent: int = 0  # in minutes
    favorite_topics: List[str] = field(default_factory=list)
    most_active_hours: List[int] = field(default_factory=list)
    average_session_length: float = 0.0
    last_activity: Optional[datetime] = None
    
    def add_message(self) -> None:
        """Increment message count."""
        self.total_messages += 1
    
    def add_session(self, duration_minutes: float) -> None:
        """Add a new session and update statistics."""
        self.total_sessions += 1
        self.total_time_spent += int(duration_minutes)
        self.average_session_length = self.total_time_spent / self.total_sessions
        self.last_activity = datetime.now()
    
    def add_topic(self, topic: str) -> None:
        """Add a topic to favorites (if not already present)."""
        if topic not in self.favorite_topics:
            self.favorite_topics.append(topic)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary format."""
        return {
            'total_messages': self.total_messages,
            'total_sessions': self.total_sessions,
            'total_time_spent': self.total_time_spent,
            'favorite_topics': self.favorite_topics,
            'most_active_hours': self.most_active_hours,
            'average_session_length': self.average_session_length,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None
        }


@dataclass
class User:
    """
    Represents a user of the chatbot application.
    
    Attributes:
        user_id: Unique identifier for the user
        username: User's chosen username
        email: User's email address
        role: User's role in the system
        preferences: User's preferences
        stats: User's statistics
        created_at: When the user account was created
        last_login: Last login timestamp
        is_active: Whether the user account is active
        session_token: Current session token
        metadata: Additional user metadata
    """
    user_id: str
    username: str
    email: Optional[str] = None
    role: UserRole = UserRole.GUEST
    preferences: UserPreferences = field(default_factory=UserPreferences)
    stats: UserStats = field(default_factory=UserStats)
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    is_active: bool = True
    session_token: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def login(self, session_token: str) -> None:
        """Update user login information."""
        self.last_login = datetime.now()
        self.session_token = session_token
        self.is_active = True
    
    def logout(self) -> None:
        """Clear user session information."""
        self.session_token = None
    
    def update_preferences(self, preferences: UserPreferences) -> None:
        """Update user preferences."""
        self.preferences = preferences
    
    def can_access_feature(self, feature: str) -> bool:
        """Check if user can access a specific feature."""
        feature_permissions = {
            'basic_chat': [UserRole.GUEST, UserRole.REGISTERED, UserRole.PREMIUM, UserRole.ADMIN],
            'chat_history': [UserRole.REGISTERED, UserRole.PREMIUM, UserRole.ADMIN],
            'advanced_features': [UserRole.PREMIUM, UserRole.ADMIN],
            'admin_panel': [UserRole.ADMIN],
            'unlimited_messages': [UserRole.PREMIUM, UserRole.ADMIN],
            'priority_support': [UserRole.PREMIUM, UserRole.ADMIN],
            'custom_themes': [UserRole.PREMIUM, UserRole.ADMIN],
            'export_data': [UserRole.REGISTERED, UserRole.PREMIUM, UserRole.ADMIN]
        }
        
        allowed_roles = feature_permissions.get(feature, [])
        return self.role in allowed_roles
    
    def get_display_name(self) -> str:
        """Get the display name for the user."""
        if self.username:
            return self.username
        elif self.email:
            return self.email.split('@')[0]
        else:
            return f"User {self.user_id[:8]}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary format."""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'preferences': self.preferences.to_dict(),
            'stats': self.stats.to_dict(),
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'session_token': self.session_token,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create a User from dictionary."""
        return cls(
            user_id=data['user_id'],
            username=data['username'],
            email=data.get('email'),
            role=UserRole(data['role']),
            preferences=UserPreferences.from_dict(data['preferences']),
            stats=UserStats(**data['stats']),
            created_at=datetime.fromisoformat(data['created_at']),
            last_login=datetime.fromisoformat(data['last_login']) if data.get('last_login') else None,
            is_active=data.get('is_active', True),
            session_token=data.get('session_token'),
            metadata=data.get('metadata', {})
        )


@dataclass
class UserManager:
    """
    Manages user accounts and sessions.
    
    Attributes:
        users: Dictionary of user_id -> User
        active_sessions: Dictionary of session_token -> user_id
        max_users: Maximum number of users to keep in memory
    """
    users: Dict[str, User] = field(default_factory=dict)
    active_sessions: Dict[str, str] = field(default_factory=dict)
    max_users: int = 10000
    
    def create_user(self, user_id: str, username: str, email: Optional[str] = None, 
                   role: UserRole = UserRole.GUEST) -> User:
        """Create a new user."""
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            role=role
        )
        self.users[user_id] = user
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return self.users.get(user_id)
    
    def get_user_by_session(self, session_token: str) -> Optional[User]:
        """Get a user by session token."""
        user_id = self.active_sessions.get(session_token)
        if user_id:
            return self.get_user(user_id)
        return None
    
    def authenticate_user(self, user_id: str, session_token: str) -> bool:
        """Authenticate a user and create session."""
        user = self.get_user(user_id)
        if user and user.is_active:
            user.login(session_token)
            self.active_sessions[session_token] = user_id
            return True
        return False
    
    def logout_user(self, session_token: str) -> bool:
        """Logout a user by session token."""
        user = self.get_user_by_session(session_token)
        if user:
            user.logout()
            del self.active_sessions[session_token]
            return True
        return False
    
    def get_active_users(self) -> List[User]:
        """Get all active users."""
        return [user for user in self.users.values() if user.is_active]
    
    def get_user_count(self) -> int:
        """Get total number of users."""
        return len(self.users)
    
    def cleanup_inactive_sessions(self, max_age_hours: int = 24) -> None:
        """Clean up inactive sessions older than specified hours."""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        sessions_to_remove = []
        for session_token, user_id in self.active_sessions.items():
            user = self.get_user(user_id)
            if user and user.last_login and user.last_login < cutoff_time:
                sessions_to_remove.append(session_token)
        
        for session_token in sessions_to_remove:
            self.logout_user(session_token)
