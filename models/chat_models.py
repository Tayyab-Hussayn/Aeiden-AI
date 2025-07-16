"""
Chat-related data models for the AI chatbot application.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class MessageRole(Enum):
    """Enumeration for message roles in the chat."""
    USER = "user"
    MODEL = "model"
    SYSTEM = "system"


class MessageStatus(Enum):
    """Enumeration for message status."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"


@dataclass
class ChatMessage:
    """
    Represents a single message in the chat conversation.
    
    Attributes:
        id: Unique identifier for the message
        role: Role of the message sender (user, model, system)
        content: The actual message content
        timestamp: When the message was created
        status: Current status of the message
        metadata: Additional metadata about the message
    """
    id: str
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: MessageStatus = MessageStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the message to a dictionary format."""
        return {
            'id': self.id,
            'role': self.role.value,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status.value,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatMessage':
        """Create a ChatMessage from a dictionary."""
        return cls(
            id=data['id'],
            role=MessageRole(data['role']),
            content=data['content'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            status=MessageStatus(data['status']),
            metadata=data.get('metadata', {})
        )
    
    def to_gemini_format(self) -> Dict[str, Any]:
        """Convert message to Gemini API format."""
        return {
            "role": self.role.value,
            "parts": [{"text": self.content}]
        }


@dataclass
class ChatSession:
    """
    Represents a chat session with the AI.
    
    Attributes:
        session_id: Unique identifier for the session
        user_id: ID of the user (if authenticated)
        messages: List of messages in the session
        created_at: When the session was created
        last_activity: Last activity timestamp
        is_active: Whether the session is currently active
        settings: Session-specific settings
    """
    session_id: str
    user_id: Optional[str] = None
    messages: List[ChatMessage] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    settings: Dict[str, Any] = field(default_factory=dict)
    
    def add_message(self, message: ChatMessage) -> None:
        """Add a message to the session."""
        self.messages.append(message)
        self.last_activity = datetime.now()
    
    def get_messages_for_gemini(self) -> List[Dict[str, Any]]:
        """Get messages in Gemini API format."""
        return [msg.to_gemini_format() for msg in self.messages]
    
    def get_recent_messages(self, limit: int = 10) -> List[ChatMessage]:
        """Get recent messages from the session."""
        return self.messages[-limit:] if len(self.messages) > limit else self.messages
    
    def clear_messages(self) -> None:
        """Clear all messages from the session."""
        self.messages.clear()
        self.last_activity = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary format."""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'messages': [msg.to_dict() for msg in self.messages],
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'is_active': self.is_active,
            'settings': self.settings
        }


@dataclass
class ChatHistory:
    """
    Manages the history of chat sessions.
    
    Attributes:
        sessions: Dictionary of session_id -> ChatSession
        max_sessions: Maximum number of sessions to keep
        max_messages_per_session: Maximum messages per session
    """
    sessions: Dict[str, ChatSession] = field(default_factory=dict)
    max_sessions: int = 100
    max_messages_per_session: int = 1000
    
    def create_session(self, session_id: str, user_id: Optional[str] = None) -> ChatSession:
        """Create a new chat session."""
        session = ChatSession(session_id=session_id, user_id=user_id)
        self.sessions[session_id] = session
        self._cleanup_old_sessions()
        return session
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID."""
        return self.sessions.get(session_id)
    
    def get_or_create_session(self, session_id: str, user_id: Optional[str] = None) -> ChatSession:
        """Get existing session or create new one."""
        session = self.get_session(session_id)
        if session is None:
            session = self.create_session(session_id, user_id)
        return session
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def get_active_sessions(self) -> List[ChatSession]:
        """Get all active sessions."""
        return [session for session in self.sessions.values() if session.is_active]
    
    def _cleanup_old_sessions(self) -> None:
        """Clean up old sessions to maintain max_sessions limit."""
        if len(self.sessions) > self.max_sessions:
            # Sort by last activity and remove oldest sessions
            sorted_sessions = sorted(
                self.sessions.items(),
                key=lambda x: x[1].last_activity
            )
            
            # Keep only the most recent sessions
            sessions_to_keep = sorted_sessions[-self.max_sessions:]
            self.sessions = dict(sessions_to_keep)
    
    def cleanup_messages(self, session_id: str) -> None:
        """Clean up messages in a session to maintain max_messages_per_session limit."""
        session = self.get_session(session_id)
        if session and len(session.messages) > self.max_messages_per_session:
            # Keep only the most recent messages
            session.messages = session.messages[-self.max_messages_per_session:]
    
    def get_session_count(self) -> int:
        """Get the total number of sessions."""
        return len(self.sessions)
    
    def get_total_messages(self) -> int:
        """Get the total number of messages across all sessions."""
        return sum(len(session.messages) for session in self.sessions.values())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert history to dictionary format."""
        return {
            'sessions': {sid: session.to_dict() for sid, session in self.sessions.items()},
            'max_sessions': self.max_sessions,
            'max_messages_per_session': self.max_messages_per_session
        }
