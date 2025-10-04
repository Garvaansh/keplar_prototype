#!/usr/bin/env python3
"""
🔍 Health Check API Routes
=========================

Health monitoring endpoints for the FastAPI backend.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import logging

from app.models.predictor import SecureExoplanetPredictor, create_predictor
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Dependency injection for predictor
async def get_predictor() -> SecureExoplanetPredictor:
    """Get predictor instance (singleton pattern)"""
    if not hasattr(get_predictor, '_predictor'):
        try:
            get_predictor._predictor = create_predictor()
            logger.info("✅ Predictor initialized for health checks")
        except Exception as e:
            logger.error(f"❌ Failed to initialize predictor: {e}")
            raise HTTPException(status_code=500, detail="Model initialization failed")
    return get_predictor._predictor

@router.get("/health")
async def health_check():
    """🔍 Basic health check"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@router.get("/health/detailed")
async def detailed_health_check(predictor: SecureExoplanetPredictor = Depends(get_predictor)):
    """🔍 Detailed health check with model status"""
    return {
        "status": "healthy" if predictor.models_loaded else "degraded",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "models": {
            "loaded": predictor.models_loaded,
            "random_forest": predictor.rf_model is not None,
            "xgboost": predictor.xgb_model is not None,
            "feature_bounds": predictor.feature_bounds is not None
        },
        "features": {
            "total_features": len(predictor.all_features),
            "class_names": predictor.class_names
        },
        "model_path": str(predictor.model_path)
    }

@router.get("/feature-bounds")
async def get_feature_bounds(predictor: SecureExoplanetPredictor = Depends(get_predictor)):
    """📊 Get valid ranges for all features (for React dashboard sliders)"""
    if not predictor.feature_bounds:
        raise HTTPException(status_code=404, detail="Feature bounds not available")
    
    return {
        "feature_bounds": predictor.feature_bounds,
        "total_features": len(predictor.feature_bounds),
        "description": "Valid ranges for input features based on training data"
    }

@router.get("/model-info")
async def get_model_info(predictor: SecureExoplanetPredictor = Depends(get_predictor)):
    """ℹ️ Get comprehensive model information"""
    return {
        "model_type": "Random Forest + XGBoost Ensemble",
        "ensemble_weights": {
            "random_forest": predictor.rf_weight,
            "xgboost": predictor.xgb_weight
        },
        "classification": {
            "type": "multi-class",
            "num_classes": len(predictor.class_names),
            "class_names": predictor.class_names,
            "target_mapping": predictor.target_map
        },
        "features": {
            "total_features": len(predictor.all_features),
            "feature_names": predictor.all_features,
            "engineered_features": [
                "period_impact_ratio", "depth_duration_ratio", "snr_per_ppm",
                "planet_temp_ratio", "stellar_density", "transit_probability",
                "planet_density_proxy", "equilibrium_flux", "impact_depth_product",
                "period_snr_ratio", "duration_impact_ratio"
            ]
        },
        "capabilities": [
            "Multi-class classification (3 classes)",
            "Feature importance explanations for XAI", 
            "Light curve parameter generation",
            "Physics-based input validation",
            "Batch CSV processing",
            "Real-time predictions"
        ],
        "validation": {
            "input_bounds_checking": predictor.feature_bounds is not None,
            "physics_consistency_checks": True,
            "missing_value_handling": True
        }
    }