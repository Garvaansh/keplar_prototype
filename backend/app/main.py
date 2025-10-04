#!/usr/bin/env python3
"""
🌟 FastAPI Main Application
===========================

Main FastAPI application entry point for the Exoplanet Discovery Dashboard.
This is the central hub that connects all API routes and middleware.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from pathlib import Path

from app.api.routes import prediction, health, batch
from app.core.config import settings
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(prediction.router, prefix="/api/v1", tags=["prediction"])
app.include_router(batch.router, prefix="/api/v1", tags=["batch"])

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        logger.info(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
        logger.info(f"📊 Environment: {settings.ENVIRONMENT}")
        logger.info(f"🔧 Debug mode: {settings.DEBUG}")
        logger.info(f"📁 Model path: {settings.MODEL_PATH}")
        
        # Verify model directory exists
        model_path = Path(settings.MODEL_PATH)
        if not model_path.exists():
            logger.warning(f"⚠️ Model directory not found: {model_path}")
            logger.info("💡 Please train models first using Fine_Tuned_Training.ipynb")
        
    except Exception as e:
        logger.error(f"💥 Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down Exoplanet Discovery Dashboard API")

@app.get("/")
async def root():
    """🏠 API root endpoint"""
    return {
        "message": f"🌟 {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health",
        "prediction": "/api/v1/predict",
        "batch": "/api/v1/batch-predict"
    }

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    logger.error(f"❌ ValueError: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": f"Invalid input: {str(exc)}"}
    )

@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(request, exc):
    logger.error(f"❌ FileNotFoundError: {exc}")
    return JSONResponse(
        status_code=404,
        content={"detail": f"Required file not found: {str(exc)}"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"💥 Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )