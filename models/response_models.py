"""
Response-related data models for the AI chatbot application.
"""

from datetime import datetime
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
from enum import Enum


class ResponseType(Enum):
    """Enumeration for response types."""
    TEXT = "text"
    CODE = "code"
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"
    ERROR = "error"
    SYSTEM = "system"


class ResponseStatus(Enum):
    """Enumeration for response status."""
    SUCCESS = "success"
    PARTIAL = "partial"
    ERROR = "error"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    PROCESSING = "processing"


class ResponsePriority(Enum):
    """Enumeration for response priority."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class ResponseMetadata:
    """
    Metadata for AI responses.
    
    Attributes:
        model_name: Name of the AI model used
        model_version: Version of the AI model
        response_time: Time taken to generate response (in milliseconds)
        token_count: Number of tokens in the response
        temperature: Temperature setting used
        max_tokens: Maximum tokens allowed
        finish_reason: Reason why generation stopped
        safety_ratings: Safety ratings for the response
        citations: List of citations if any
        confidence_score: Confidence score of the response
    """
    model_name: str = "gemini-1.5-flash"
    model_version: str = "1.0"
    response_time: float = 0.0
    token_count: int = 0
    temperature: float = 0.7
    max_tokens: int = 1000
    finish_reason: str = "stop"
    safety_ratings: Dict[str, str] = field(default_factory=dict)
    citations: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary format."""
        return {
            'model_name': self.model_name,
            'model_version': self.model_version,
            'response_time': self.response_time,
            'token_count': self.token_count,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'finish_reason': self.finish_reason,
            'safety_ratings': self.safety_ratings,
            'citations': self.citations,
            'confidence_score': self.confidence_score
        }


@dataclass
class AIResponse:
    """
    Represents a response from the AI system.
    
    Attributes:
        response_id: Unique identifier for the response
        content: The actual response content
        response_type: Type of response (text, code, etc.)
        status: Status of the response
        priority: Priority level of the response
        metadata: Additional metadata about the response
        created_at: When the response was created
        user_id: ID of the user who received the response
        session_id: ID of the session this response belongs to
        parent_message_id: ID of the message this is responding to
        suggested_actions: List of suggested follow-up actions
        feedback_score: User feedback score for the response
        is_helpful: Whether the response was marked as helpful
        error_message: Error message if status is ERROR
    """
    response_id: str
    content: str
    response_type: ResponseType = ResponseType.TEXT
    status: ResponseStatus = ResponseStatus.SUCCESS
    priority: ResponsePriority = ResponsePriority.NORMAL
    metadata: ResponseMetadata = field(default_factory=ResponseMetadata)
    created_at: datetime = field(default_factory=datetime.now)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    parent_message_id: Optional[str] = None
    suggested_actions: List[str] = field(default_factory=list)
    feedback_score: Optional[int] = None
    is_helpful: Optional[bool] = None
    error_message: Optional[str] = None
    
    def add_suggested_action(self, action: str) -> None:
        """Add a suggested action to the response."""
        if action not in self.suggested_actions:
            self.suggested_actions.append(action)
    
    def set_feedback(self, score: int, is_helpful: bool = None) -> None:
        """Set user feedback for the response."""
        self.feedback_score = score
        if is_helpful is not None:
            self.is_helpful = is_helpful
    
    def mark_as_error(self, error_message: str) -> None:
        """Mark the response as an error."""
        self.status = ResponseStatus.ERROR
        self.error_message = error_message
    
    def get_formatted_content(self) -> str:
        """Get formatted content based on response type."""
        if self.response_type == ResponseType.CODE:
            return f"```\n{self.content}\n```"
        elif self.response_type == ResponseType.JSON:
            return f"```json\n{self.content}\n```"
        elif self.response_type == ResponseType.HTML:
            return f"```html\n{self.content}\n```"
        elif self.response_type == ResponseType.ERROR:
            return f"❌ Error: {self.content}"
        elif self.response_type == ResponseType.SYSTEM:
            return f"ℹ️ System: {self.content}"
        else:
            return self.content
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary format."""
        return {
            'response_id': self.response_id,
            'content': self.content,
            'response_type': self.response_type.value,
            'status': self.status.value,
            'priority': self.priority.value,
            'metadata': self.metadata.to_dict(),
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id,
            'session_id': self.session_id,
            'parent_message_id': self.parent_message_id,
            'suggested_actions': self.suggested_actions,
            'feedback_score': self.feedback_score,
            'is_helpful': self.is_helpful,
            'error_message': self.error_message
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIResponse':
        """Create an AIResponse from dictionary."""
        return cls(
            response_id=data['response_id'],
            content=data['content'],
            response_type=ResponseType(data['response_type']),
            status=ResponseStatus(data['status']),
            priority=ResponsePriority(data['priority']),
            metadata=ResponseMetadata(**data['metadata']),
            created_at=datetime.fromisoformat(data['created_at']),
            user_id=data.get('user_id'),
            session_id=data.get('session_id'),
            parent_message_id=data.get('parent_message_id'),
            suggested_actions=data.get('suggested_actions', []),
            feedback_score=data.get('feedback_score'),
            is_helpful=data.get('is_helpful'),
            error_message=data.get('error_message')
        )


@dataclass
class ResponseCache:
    """
    Caches AI responses for improved performance.
    
    Attributes:
        cache: Dictionary of content_hash -> AIResponse
        max_size: Maximum number of responses to cache
        hit_count: Number of cache hits
        miss_count: Number of cache misses
    """
    cache: Dict[str, AIResponse] = field(default_factory=dict)
    max_size: int = 1000
    hit_count: int = 0
    miss_count: int = 0
    
    def _hash_content(self, content: str, user_id: str = None) -> str:
        """Create a hash for caching purposes."""
        import hashlib
        cache_key = f"{content}:{user_id or 'anonymous'}"
        return hashlib.md5(cache_key.encode()).hexdigest()
    
    def get(self, content: str, user_id: str = None) -> Optional[AIResponse]:
        """Get a cached response."""
        cache_key = self._hash_content(content, user_id)
        if cache_key in self.cache:
            self.hit_count += 1
            return self.cache[cache_key]
        else:
            self.miss_count += 1
            return None
    
    def set(self, content: str, response: AIResponse, user_id: str = None) -> None:
        """Cache a response."""
        cache_key = self._hash_content(content, user_id)
        
        # Remove oldest entries if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[cache_key] = response
    
    def clear(self) -> None:
        """Clear the cache."""
        self.cache.clear()
        self.hit_count = 0
        self.miss_count = 0
    
    def get_cache_ratio(self) -> float:
        """Get cache hit ratio."""
        total_requests = self.hit_count + self.miss_count
        if total_requests == 0:
            return 0.0
        return self.hit_count / total_requests
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_ratio': self.get_cache_ratio()
        }


@dataclass
class ResponseAnalytics:
    """
    Analytics for AI responses.
    
    Attributes:
        total_responses: Total number of responses generated
        success_count: Number of successful responses
        error_count: Number of error responses
        average_response_time: Average response time in milliseconds
        response_types: Count of different response types
        user_feedback: Dictionary of feedback scores
        popular_topics: List of popular discussion topics
        peak_usage_hours: Hours with highest usage
    """
    total_responses: int = 0
    success_count: int = 0
    error_count: int = 0
    average_response_time: float = 0.0
    response_types: Dict[str, int] = field(default_factory=dict)
    user_feedback: Dict[str, int] = field(default_factory=dict)
    popular_topics: List[str] = field(default_factory=list)
    peak_usage_hours: List[int] = field(default_factory=list)
    
    def add_response(self, response: AIResponse) -> None:
        """Add a response to analytics."""
        self.total_responses += 1
        
        if response.status == ResponseStatus.SUCCESS:
            self.success_count += 1
        elif response.status == ResponseStatus.ERROR:
            self.error_count += 1
        
        # Update average response time
        total_time = (self.average_response_time * (self.total_responses - 1) + 
                     response.metadata.response_time)
        self.average_response_time = total_time / self.total_responses
        
        # Update response types count
        response_type = response.response_type.value
        self.response_types[response_type] = self.response_types.get(response_type, 0) + 1
        
        # Update user feedback
        if response.feedback_score is not None:
            score_key = str(response.feedback_score)
            self.user_feedback[score_key] = self.user_feedback.get(score_key, 0) + 1
    
    def get_success_rate(self) -> float:
        """Get success rate of responses."""
        if self.total_responses == 0:
            return 0.0
        return self.success_count / self.total_responses
    
    def get_error_rate(self) -> float:
        """Get error rate of responses."""
        if self.total_responses == 0:
            return 0.0
        return self.error_count / self.total_responses
    
    def get_most_common_response_type(self) -> str:
        """Get the most common response type."""
        if not self.response_types:
            return "text"
        return max(self.response_types, key=self.response_types.get)
    
    def get_average_feedback_score(self) -> float:
        """Get average user feedback score."""
        if not self.user_feedback:
            return 0.0
        
        total_score = sum(int(score) * count for score, count in self.user_feedback.items())
        total_count = sum(self.user_feedback.values())
        
        return total_score / total_count if total_count > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analytics to dictionary format."""
        return {
            'total_responses': self.total_responses,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'success_rate': self.get_success_rate(),
            'error_rate': self.get_error_rate(),
            'average_response_time': self.average_response_time,
            'response_types': self.response_types,
            'most_common_response_type': self.get_most_common_response_type(),
            'user_feedback': self.user_feedback,
            'average_feedback_score': self.get_average_feedback_score(),
            'popular_topics': self.popular_topics,
            'peak_usage_hours': self.peak_usage_hours
        }
