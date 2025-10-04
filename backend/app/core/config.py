#!/usr/bin/env python3
"""
⚙️ Application Configuration
============================

Centralized configuration management using environment variables and defaults.
This allows easy deployment across different environments (dev, staging, prod).
"""

import os
from pathlib import Path
from typing import List, Optional
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    """📋 Application settings with environment variable support"""
    
    # Project Information
    PROJECT_NAME: str = "🌟 Exoplanet Discovery Dashboard API"
    PROJECT_DESCRIPTION: str = "Secure ML-powered exoplanet classification with interactive features"
    VERSION: str = "1.0.0"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Settings (for React frontend)
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # React development server
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite development server
        "http://127.0.0.1:5173"
    ]
    
    # File Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    MODEL_PATH: str = str(BASE_DIR / "trained_models")
    DATA_PATH: str = str(BASE_DIR / "data")
    LOGS_PATH: str = str(BASE_DIR / "logs")
    
    # Model Configuration
    RF_WEIGHT: float = 0.6
    XGB_WEIGHT: float = 0.4
    
    # API Limits
    MAX_BATCH_SIZE: int = 10000
    MAX_FILE_SIZE_MB: int = 50
    REQUEST_TIMEOUT_SECONDS: int = 300
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security
    ENABLE_SECURITY_HEADERS: bool = True
    ENABLE_RATE_LIMITING: bool = False  # Can be enabled with redis
    
    @validator('ALLOWED_ORIGINS', pre=True)
    def parse_origins(cls, v):
        """Parse CORS origins from environment variable"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @validator('MODEL_PATH')
    def validate_model_path(cls, v):
        """Ensure model path exists or can be created"""
        path = Path(v)
        if not path.exists():
            print(f"⚠️ Model directory not found: {path}")
            print("💡 Please train models first using Fine_Tuned_Training.ipynb")
        return str(path)
    
    @validator('LOGS_PATH')
    def create_logs_dir(cls, v):
        """Create logs directory if it doesn't exist"""
        path = Path(v)
        path.mkdir(exist_ok=True)
        return str(path)
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Global settings instance
settings = Settings()

# Environment-specific overrides
if settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.LOG_LEVEL = "WARNING"
    settings.ALLOWED_ORIGINS = [
        "https://yourdomain.com",  # Replace with actual production domain
        "https://www.yourdomain.com"
    ]
elif settings.ENVIRONMENT == "staging":
    settings.DEBUG = False
    settings.LOG_LEVEL = "INFO"
    settings.PORT = 8001

# Export commonly used paths
BASE_DIR = settings.BASE_DIR
MODEL_PATH = Path(settings.MODEL_PATH)
DATA_PATH = Path(settings.DATA_PATH)
LOGS_PATH = Path(settings.LOGS_PATH)