#!/usr/bin/env python3
"""
🌟 FastAPI Main Application
===========================

Main FastAPI application entry point for the Exoplanet Discovery Dashboard.
This is the central hub that connects all API routes and middleware.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
import logging
from pathlib import Path
import time
from contextlib import asynccontextmanager

from app.api.routes import prediction, health, batch
from app.core.config import settings
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Model path: {settings.MODEL_PATH}")
    
    # Verify model directory exists
    model_path = Path(settings.MODEL_PATH)
    if not model_path.exists():
        logger.warning(f"Model directory not found: {model_path}")
        logger.info("Please train models first using Fine_Tuned_Training.ipynb")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Exoplanet Discovery Dashboard API")

# Initialize FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Security middleware
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["yourdomain.com", "*.yourdomain.com"]  # Update with actual domains
    )

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    if settings.ENABLE_SECURITY_HEADERS:
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        if settings.ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# CORS middleware for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"]
)

# Include API routes
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(prediction.router, prefix="/api/v1", tags=["prediction"])
app.include_router(batch.router, prefix="/api/v1", tags=["batch"])

# Startup/shutdown logic moved to lifespan context manager above

@app.get("/")
async def root():
    """🏠 API root endpoint"""
    return {
        "message": f"{settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health",
        "prediction": "/api/v1/predict",
        "batch": "/api/v1/batch-predict"
    }

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.error(f"ValueError from {request.url}: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "validation_error",
            "message": f"Invalid input: {str(exc)}",
            "status_code": 400,
            "timestamp": time.time()
        }
    )

@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(request: Request, exc: FileNotFoundError):
    logger.error(f"FileNotFoundError from {request.url}: {exc}")
    return JSONResponse(
        status_code=404,
        content={
            "error": "file_not_found",
            "message": f"Required file not found: {str(exc)}",
            "status_code": 404,
            "timestamp": time.time()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP {exc.status_code} from {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error from {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred. Please try again later.",
            "status_code": 500,
            "timestamp": time.time()
        }
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