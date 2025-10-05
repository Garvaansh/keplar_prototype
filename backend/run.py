#!/usr/bin/env python3
"""
Backend Server Runner
=====================

Simple script to run the FastAPI backend server with proper configuration.
This is the main entry point for development and production.
"""

import os
import sys
import logging
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.core.logging_config import setup_logging

def check_models():
    """Check if trained models are available"""
    model_path = Path(settings.MODEL_PATH)
    required_models = [
        "random-forest.model",
        "xgboost.model", 
        "ensemble_metadata.pkl"
    ]
    
    missing_models = []
    for model_file in required_models:
        if not (model_path / model_file).exists():
            missing_models.append(model_file)
    
    if missing_models:
        print("WARNING: Missing trained models:")
        for model in missing_models:
            print(f"   - {model}")
        print("\nPlease train models first:")
        print("   1. Open notebook/Fine_Tuned_Training.ipynb")
        print("   2. Run all cells to train the 3-class models")
        print("   3. Models will be saved to model/ directory")
        print("\nContinuing without models (API will show warnings)...")
    else:
        print("SUCCESS: All required models found!")
    
    return len(missing_models) == 0

def main():
    """Main entry point"""
    print("=" * 50)
    print("Starting Exoplanet Discovery Dashboard API")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Host: {settings.HOST}:{settings.PORT}")
    print(f"Model path: {settings.MODEL_PATH}")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Check models
    models_ready = check_models()
    
    # Import and run the app
    try:
        import uvicorn
        from app.main import app
        
        # Configure uvicorn
        config = {
            "app": "app.main:app",
            "host": settings.HOST,
            "port": settings.PORT,
            "reload": settings.DEBUG,
            "log_level": settings.LOG_LEVEL.lower(),
            "access_log": True
        }
        
        print(f"\nStarting server at http://{settings.HOST}:{settings.PORT}")
        print(f"API docs: http://{settings.HOST}:{settings.PORT}/docs")
        print(f"Health check: http://{settings.HOST}:{settings.PORT}/api/v1/health")
        
        if not models_ready:
            print("\nWARNING: Server starting without trained models!")
            print("   Some endpoints may not work until models are trained.")
        
        print("\n" + "=" * 50)
        
        # Run the server
        uvicorn.run(**config)
        
    except ImportError as e:
        print(f"ERROR: Import error: {e}")
        print("HINT: Please install requirements: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        print(f"ERROR: Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()