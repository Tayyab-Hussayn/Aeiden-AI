"""
Logging utilities for the AI chatbot application.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


def setup_logger(name: str, log_file: str = 'chatbot.log', level: int = logging.INFO) -> logging.Logger:
    """Set up a logger with file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def log_chat_interaction(user_id: str, message: str, response: str, 
                        response_time: float, logger: logging.Logger) -> None:
    """Log a chat interaction."""
    interaction_data = {
        'user_id': user_id,
        'message': message,
        'response': response,
        'response_time': response_time,
        'timestamp': datetime.now().isoformat()
    }
    
    logger.info(f"Chat interaction: {json.dumps(interaction_data, ensure_ascii=False)}")


def log_error(error: Exception, context: Dict[str, Any], logger: logging.Logger) -> None:
    """Log an error with context information."""
    error_data = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'context': context,
        'timestamp': datetime.now().isoformat()
    }
    
    logger.error(f"Error occurred: {json.dumps(error_data, ensure_ascii=False)}")


def log_performance_metrics(metrics: Dict[str, float], logger: logging.Logger) -> None:
    """Log performance metrics."""
    metrics_data = {
        'metrics': metrics,
        'timestamp': datetime.now().isoformat()
    }
    
    logger.info(f"Performance metrics: {json.dumps(metrics_data)}")


def log_user_activity(user_id: str, activity: str, details: Optional[Dict[str, Any]] = None, 
                     logger: logging.Logger = None) -> None:
    """Log user activity."""
    if logger is None:
        logger = setup_logger('user_activity')
    
    activity_data = {
        'user_id': user_id,
        'activity': activity,
        'details': details or {},
        'timestamp': datetime.now().isoformat()
    }
    
    logger.info(f"User activity: {json.dumps(activity_data, ensure_ascii=False)}")


def log_system_event(event_type: str, event_data: Dict[str, Any], 
                    logger: logging.Logger = None) -> None:
    """Log system events."""
    if logger is None:
        logger = setup_logger('system_events')
    
    system_event = {
        'event_type': event_type,
        'event_data': event_data,
        'timestamp': datetime.now().isoformat()
    }
    
    logger.info(f"System event: {json.dumps(system_event, ensure_ascii=False)}")


def log_api_request(endpoint: str, method: str, status_code: int, 
                   response_time: float, logger: logging.Logger = None) -> None:
    """Log API requests."""
    if logger is None:
        logger = setup_logger('api_requests')
    
    request_data = {
        'endpoint': endpoint,
        'method': method,
        'status_code': status_code,
        'response_time': response_time,
        'timestamp': datetime.now().isoformat()
    }
    
    logger.info(f"API request: {json.dumps(request_data)}")


class ChatbotLogger:
    """Centralized logger for the chatbot application."""
    
    def __init__(self, log_dir: str = 'logs'):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.main_logger = setup_logger('chatbot', f'{log_dir}/chatbot.log')
        self.error_logger = setup_logger('errors', f'{log_dir}/errors.log', logging.ERROR)
        self.user_logger = setup_logger('users', f'{log_dir}/users.log')
        self.api_logger = setup_logger('api', f'{log_dir}/api.log')
        self.performance_logger = setup_logger('performance', f'{log_dir}/performance.log')
    
    def info(self, message: str, data: Dict[str, Any] = None) -> None:
        """Log info message."""
        if data:
            message = f"{message}: {json.dumps(data, ensure_ascii=False)}"
        self.main_logger.info(message)
    
    def error(self, message: str, error: Exception = None, context: Dict[str, Any] = None) -> None:
        """Log error message."""
        if error:
            log_error(error, context or {}, self.error_logger)
        else:
            self.error_logger.error(message)
    
    def user_activity(self, user_id: str, activity: str, details: Dict[str, Any] = None) -> None:
        """Log user activity."""
        log_user_activity(user_id, activity, details, self.user_logger)
    
    def api_request(self, endpoint: str, method: str, status_code: int, response_time: float) -> None:
        """Log API request."""
        log_api_request(endpoint, method, status_code, response_time, self.api_logger)
    
    def performance(self, metrics: Dict[str, float]) -> None:
        """Log performance metrics."""
        log_performance_metrics(metrics, self.performance_logger)
    
    def chat_interaction(self, user_id: str, message: str, response: str, response_time: float) -> None:
        """Log chat interaction."""
        log_chat_interaction(user_id, message, response, response_time, self.main_logger)
