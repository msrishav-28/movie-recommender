"""
Structured logging configuration for production.
Supports JSON logging, log rotation, and multiple handlers.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger
import structlog
from datetime import datetime

from app.core.config import settings


def setup_logging():
    """
    Configure structured logging for the application.
    Uses structlog for structured logging with JSON output.
    """
    
    # Ensure log directory exists
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.LOG_FORMAT == "json" 
                else structlog.dev.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        handlers=[get_console_handler(), get_file_handler()]
    )
    
    # Get root logger
    logger = logging.getLogger()
    
    # Set log level
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    return logger


def get_console_handler():
    """Create console handler with appropriate formatter."""
    console_handler = logging.StreamHandler(sys.stdout)
    
    if settings.LOG_FORMAT == "json":
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    return console_handler


def get_file_handler():
    """Create file handler with rotation."""
    if settings.LOG_ROTATION == "daily":
        file_handler = TimedRotatingFileHandler(
            settings.LOG_FILE,
            when='midnight',
            interval=1,
            backupCount=settings.LOG_RETENTION_DAYS
        )
    else:
        # Rotating file handler (10MB per file, keep 10 files)
        file_handler = RotatingFileHandler(
            settings.LOG_FILE,
            maxBytes=10*1024*1024,
            backupCount=10
        )
    
    if settings.LOG_FORMAT == "json":
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    file_handler.setFormatter(formatter)
    return file_handler


def get_logger(name: str):
    """
    Get a structured logger instance.
    
    Usage:
        logger = get_logger(__name__)
        logger.info("message", user_id=123, action="login")
    """
    return structlog.get_logger(name)


class RequestLogger:
    """Middleware-compatible request logger."""
    
    @staticmethod
    def log_request(request_id: str, method: str, path: str, user_id: str = None):
        """Log incoming request."""
        logger = get_logger("api.request")
        logger.info(
            "incoming_request",
            request_id=request_id,
            method=method,
            path=path,
            user_id=user_id,
            timestamp=datetime.utcnow().isoformat()
        )
    
    @staticmethod
    def log_response(request_id: str, status_code: int, duration_ms: float):
        """Log response."""
        logger = get_logger("api.response")
        logger.info(
            "response_sent",
            request_id=request_id,
            status_code=status_code,
            duration_ms=duration_ms,
            timestamp=datetime.utcnow().isoformat()
        )
    
    @staticmethod
    def log_error(request_id: str, error: Exception, user_id: str = None):
        """Log error."""
        logger = get_logger("api.error")
        logger.error(
            "request_error",
            request_id=request_id,
            error_type=type(error).__name__,
            error_message=str(error),
            user_id=user_id,
            timestamp=datetime.utcnow().isoformat()
        )


class MLLogger:
    """Logger for ML operations."""
    
    @staticmethod
    def log_prediction(model_name: str, user_id: str, duration_ms: float, num_results: int):
        """Log ML prediction."""
        logger = get_logger("ml.prediction")
        logger.info(
            "prediction_made",
            model_name=model_name,
            user_id=user_id,
            duration_ms=duration_ms,
            num_results=num_results,
            timestamp=datetime.utcnow().isoformat()
        )
    
    @staticmethod
    def log_training(model_name: str, metrics: dict, duration_seconds: float):
        """Log model training."""
        logger = get_logger("ml.training")
        logger.info(
            "model_trained",
            model_name=model_name,
            metrics=metrics,
            duration_seconds=duration_seconds,
            timestamp=datetime.utcnow().isoformat()
        )
    
    @staticmethod
    def log_model_error(model_name: str, error: Exception):
        """Log ML model error."""
        logger = get_logger("ml.error")
        logger.error(
            "model_error",
            model_name=model_name,
            error_type=type(error).__name__,
            error_message=str(error),
            timestamp=datetime.utcnow().isoformat()
        )


class DatabaseLogger:
    """Logger for database operations."""
    
    @staticmethod
    def log_query(query_type: str, table: str, duration_ms: float):
        """Log database query."""
        logger = get_logger("db.query")
        logger.debug(
            "database_query",
            query_type=query_type,
            table=table,
            duration_ms=duration_ms,
            timestamp=datetime.utcnow().isoformat()
        )
    
    @staticmethod
    def log_slow_query(query_type: str, table: str, duration_ms: float, threshold_ms: float = 1000):
        """Log slow database query."""
        if duration_ms > threshold_ms:
            logger = get_logger("db.slow_query")
            logger.warning(
                "slow_database_query",
                query_type=query_type,
                table=table,
                duration_ms=duration_ms,
                threshold_ms=threshold_ms,
                timestamp=datetime.utcnow().isoformat()
            )


# Initialize logging on module import
setup_logging()
