#!/usr/bin/env python3
"""
📝 Logging Configuration
========================

Centralized logging setup for the FastAPI application.
"""

import logging
import logging.handlers
from pathlib import Path
from app.core.config import settings

def setup_logging():
    """Configure application logging"""
    
    # Create logs directory
    logs_dir = Path(settings.LOGS_PATH)
    logs_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=settings.LOG_FORMAT,
        handlers=[
            # Console handler
            logging.StreamHandler(),
            # File handler with rotation
            logging.handlers.RotatingFileHandler(
                logs_dir / "exoplanet_api.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    # Reduce noise from external libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sklearn").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured - Level: {settings.LOG_LEVEL}")
    logger.info(f"Log files: {logs_dir}")
    
    return logger