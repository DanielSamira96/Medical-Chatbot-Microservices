"""
Comprehensive logging system for the Medical Chatbot application.
"""

import logging
import logging.handlers
import json
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from config.settings import settings


class StructuredLogger:
    """Structured logger with JSON formatting and multiple handlers."""
    
    def __init__(self, name: str = "medical_chatbot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplication
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Create formatters
        self.console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Setup handlers
        self._setup_console_handler()
        self._setup_file_handler()
        
        # Prevent duplicate logs
        self.logger.propagate = False
    
    def _setup_console_handler(self):
        """Setup console handler for development."""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self):
        """Setup rotating file handler."""
        # Ensure logs directory exists
        log_dir = Path(settings.LOG_FILE).parent
        log_dir.mkdir(exist_ok=True)
        
        # Create rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            filename=settings.LOG_FILE,
            maxBytes=settings.LOG_MAX_SIZE_MB * 1024 * 1024,  # Convert MB to bytes
            backupCount=settings.LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # JSON formatter for structured logs
        file_handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(file_handler)
    
    def _create_log_entry(self, level: str, message: str, **kwargs) -> Dict[str, Any]:
        """Create structured log entry."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "logger": self.logger.name
        }
        
        # Add additional context
        if kwargs:
            entry["context"] = kwargs
            
        return entry
    
    def info(self, message: str, **kwargs):
        """Log info level message."""
        entry = self._create_log_entry("INFO", message, **kwargs)
        self.logger.info(json.dumps(entry, ensure_ascii=False))
    
    def warning(self, message: str, **kwargs):
        """Log warning level message."""
        entry = self._create_log_entry("WARNING", message, **kwargs)
        self.logger.warning(json.dumps(entry, ensure_ascii=False))
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log error level message with optional exception details."""
        entry = self._create_log_entry("ERROR", message, **kwargs)
        
        if exception:
            entry["exception"] = {
                "type": type(exception).__name__,
                "message": str(exception),
                "traceback": traceback.format_exc()
            }
        
        self.logger.error(json.dumps(entry, ensure_ascii=False))
    
    def debug(self, message: str, **kwargs):
        """Log debug level message."""
        entry = self._create_log_entry("DEBUG", message, **kwargs)
        self.logger.debug(json.dumps(entry, ensure_ascii=False))
    
    def api_request(self, endpoint: str, method: str, user_info: Optional[Dict] = None, **kwargs):
        """Log API request."""
        self.info(
            f"API Request: {method} {endpoint}",
            endpoint=endpoint,
            method=method,
            user_info=user_info,
            **kwargs
        )
    
    def api_response(self, endpoint: str, status_code: int, response_time_ms: float, **kwargs):
        """Log API response."""
        self.info(
            f"API Response: {endpoint} - {status_code}",
            endpoint=endpoint,
            status_code=status_code,
            response_time_ms=response_time_ms,
            **kwargs
        )
    
    def user_interaction(self, phase: str, action: str, user_language: str, **kwargs):
        """Log user interactions."""
        self.info(
            f"User Interaction: {phase} - {action}",
            phase=phase,
            action=action,
            user_language=user_language,
            **kwargs
        )
    
    def azure_openai_request(self, model: str, tokens_used: Optional[int] = None, **kwargs):
        """Log Azure OpenAI API calls."""
        self.info(
            f"Azure OpenAI Request: {model}",
            model=model,
            tokens_used=tokens_used,
            **kwargs
        )
    
    def system_health(self, component: str, status: str, **kwargs):
        """Log system health checks."""
        self.info(
            f"System Health: {component} - {status}",
            component=component,
            status=status,
            **kwargs
        )


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logs."""
    
    def format(self, record):
        # The message is already JSON formatted from StructuredLogger
        return record.getMessage()


# Global logger instance
logger = StructuredLogger()


# Convenience functions for common operations
def log_api_call(endpoint: str, method: str = "POST", **kwargs):
    """Log API call with timing context manager."""
    class APICallContext:
        def __init__(self, endpoint: str, method: str, **kwargs):
            self.endpoint = endpoint
            self.method = method
            self.kwargs = kwargs
            self.start_time = None
        
        def __enter__(self):
            self.start_time = datetime.now()
            logger.api_request(self.endpoint, self.method, **self.kwargs)
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            end_time = datetime.now()
            response_time = (end_time - self.start_time).total_seconds() * 1000
            
            if exc_type:
                logger.error(
                    f"API call failed: {self.endpoint}",
                    exception=exc_val,
                    endpoint=self.endpoint,
                    method=self.method,
                    response_time_ms=response_time
                )
            else:
                logger.api_response(
                    self.endpoint, 
                    200, 
                    response_time,
                    **self.kwargs
                )
    
    return APICallContext(endpoint, method, **kwargs)


def log_user_action(phase: str, action: str, language: str = "he", **kwargs):
    """Log user action."""
    logger.user_interaction(phase, action, language, **kwargs)


def log_error(message: str, exception: Optional[Exception] = None, **kwargs):
    """Log error with context."""
    logger.error(message, exception, **kwargs)


def log_system_startup():
    """Log system startup."""
    config_result = settings.validate_azure_config()
    logger.system_health(
        "application", 
        "startup",
        azure_configured=config_result['valid'],
        log_level=settings.LOG_LEVEL,
        default_language=settings.DEFAULT_LANGUAGE
    )