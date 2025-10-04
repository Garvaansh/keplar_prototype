#!/usr/bin/env python3
"""
⚙️ Application Configuration
============================

Centralized configuration management using environment variables and defaults.
This allows easy deployment across different environments (dev, staging, prod).
"""

import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """📋 Application settings with environment variable support"""
    
    # Project Information
    PROJECT_NAME: str = "Exoplanet Discovery Dashboard API"
    PROJECT_DESCRIPTION: str = "Secure ML-powered exoplanet classification with interactive features"
    VERSION: str = "1.0.0"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Settings (for React frontend) - will be parsed from string in env
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173"
    
    # File Paths
    MODEL_PATH: str = ""
    DATA_PATH: str = ""  
    LOGS_PATH: str = ""
    
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
    ENABLE_RATE_LIMITING: bool = False
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore"
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set up paths
        base_dir = Path(__file__).parent.parent.parent
        if not self.MODEL_PATH:
            self.MODEL_PATH = str(base_dir / "trained_models")
        if not self.DATA_PATH:
            self.DATA_PATH = str(base_dir / "data")
        if not self.LOGS_PATH:
            self.LOGS_PATH = str(base_dir / "logs")
            
        # Create logs directory
        Path(self.LOGS_PATH).mkdir(exist_ok=True)
        
        # Check model path
        if not Path(self.MODEL_PATH).exists():
            print(f"WARNING: Model directory not found: {self.MODEL_PATH}")
            print("INFO: Please train models first using Fine_Tuned_Training.ipynb")
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',')]

# Global settings instance
settings = Settings()

# Export commonly used paths
MODEL_PATH = Path(settings.MODEL_PATH)
DATA_PATH = Path(settings.DATA_PATH)
LOGS_PATH = Path(settings.LOGS_PATH)