#!/usr/bin/env python3
"""
🔮 Prediction API Routes
========================

Single prediction endpoints for the React dashboard.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
import logging

from app.models.predictor import SecureExoplanetPredictor, create_predictor

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models for request validation
class TransitParameters(BaseModel):
    """📊 Transit observation parameters (for dashboard sliders)"""
    koi_period: float = Field(..., ge=0.1, le=10000, description="Orbital period (days)")
    koi_depth: float = Field(..., ge=0.1, le=100000, description="Transit depth (ppm)")
    koi_duration: float = Field(..., ge=0.1, le=48, description="Transit duration (hours)")
    koi_impact: float = Field(0.5, ge=0.0, le=1.5, description="Impact parameter")
    koi_model_snr: float = Field(..., ge=1.0, le=1000, description="Signal-to-noise ratio")
    
    @validator('koi_period')
    def validate_period(cls, v):
        if v <= 0:
            raise ValueError('Period must be positive')
        return v
    
    @validator('koi_depth')
    def validate_depth(cls, v):
        if v <= 0:
            raise ValueError('Transit depth must be positive')
        return v

class PlanetParameters(BaseModel):
    """🪐 Planet physical parameters"""
    koi_prad: Optional[float] = Field(1.0, ge=0.1, le=50, description="Planet radius (Earth radii)")
    koi_teq: Optional[float] = Field(288, ge=100, le=3000, description="Equilibrium temperature (K)")
    koi_insol: Optional[float] = Field(1.0, ge=0.01, le=10000, description="Insolation flux")

class StarParameters(BaseModel):
    """⭐ Stellar parameters"""
    koi_steff: Optional[float] = Field(5778, ge=2000, le=10000, description="Stellar temperature (K)")
    koi_slogg: Optional[float] = Field(4.44, ge=2.0, le=5.5, description="Surface gravity (log g)")
    koi_srad: Optional[float] = Field(1.0, ge=0.1, le=10, description="Stellar radius (Solar radii)")

class QualityFlags(BaseModel):
    """🚩 Data quality flags"""
    koi_fpflag_nt: int = Field(0, ge=0, le=1, description="Not transit-like flag")
    koi_fpflag_ss: int = Field(0, ge=0, le=1, description="Stellar eclipse flag")
    koi_fpflag_co: int = Field(0, ge=0, le=1, description="Centroid offset flag")
    koi_fpflag_ec: int = Field(0, ge=0, le=1, description="Ephemeris match flag")
    koi_score: Optional[float] = Field(0.5, ge=0.0, le=1.0, description="Disposition score")

class PredictionRequest(BaseModel):
    """🔮 Complete prediction request"""
    transit: TransitParameters
    planet: Optional[PlanetParameters] = None
    star: Optional[StarParameters] = None
    flags: Optional[QualityFlags] = None

class PredictionResponse(BaseModel):
    """📊 Prediction response with explanations"""
    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    feature_importance: Dict[str, float]
    validation_warnings: List[str]
    light_curve_params: Dict[str, float]
    explanation: str

# Dependency injection for predictor
async def get_predictor() -> SecureExoplanetPredictor:
    """Get predictor instance (singleton pattern)"""
    if not hasattr(get_predictor, '_predictor'):
        try:
            get_predictor._predictor = create_predictor()
            logger.info("Predictor initialized for predictions")
        except Exception as e:
            logger.error(f"Failed to initialize predictor: {e}")
            raise HTTPException(status_code=500, detail="Model initialization failed")
    return get_predictor._predictor

def _combine_parameters(request: PredictionRequest) -> Dict[str, float]:
    """Combine all parameter groups into single dict"""
    combined = {}
    
    # Add transit parameters (required)
    combined.update(request.transit.dict())
    
    # Add optional parameters
    if request.planet:
        combined.update(request.planet.dict())
    if request.star:
        combined.update(request.star.dict())
    if request.flags:
        combined.update(request.flags.dict())
    
    return combined

def _generate_explanation(result) -> str:
    """Generate human-readable explanation for the React dashboard"""
    pred = result.prediction
    conf = result.confidence * 100
    
    # Base explanation
    if pred == "CONFIRMED":
        explanation = f"This signal shows strong evidence of being a CONFIRMED exoplanet with {conf:.1f}% confidence. "
    elif pred == "CANDIDATE":
        explanation = f"This signal is classified as a CANDIDATE exoplanet with {conf:.1f}% confidence. More observations needed. "
    else:
        explanation = f"This signal appears to be a FALSE POSITIVE with {conf:.1f}% confidence. "
    
    # Add top contributing factors
    top_features = list(result.feature_importance.keys())[:3]
    if top_features:
        explanation += f"Key factors: {', '.join(top_features)}. "
    
    # Add warnings if present
    if result.validation_warnings:
        explanation += f"WARNING: {len(result.validation_warnings)} validation warnings detected."
    
    return explanation

@router.post("/predict", response_model=PredictionResponse)
async def predict_single(
    request: PredictionRequest,
    predictor: SecureExoplanetPredictor = Depends(get_predictor)
):
    """
    🔮 Single exoplanet prediction with full explanation
    
    This endpoint provides comprehensive predictions for the React dashboard:
    - Classification: CONFIRMED, CANDIDATE, or FALSE POSITIVE
    - Confidence score and class probabilities
    - Feature importance for explainable AI
    - Light curve parameters for Chart.js visualization
    - Input validation warnings
    - Human-readable explanation
    """
    try:
        # Combine all parameters
        input_data = _combine_parameters(request)
        
        # Make prediction
        result = predictor.predict(input_data)
        
        # Generate explanation
        explanation = _generate_explanation(result)
        
        logger.info(f"Prediction: {result.prediction} ({result.confidence:.3f})")
        
        return PredictionResponse(
            prediction=result.prediction,
            confidence=result.confidence,
            probabilities=result.probabilities,
            feature_importance=result.feature_importance,
            validation_warnings=result.validation_warnings,
            light_curve_params=result.light_curve_params,
            explanation=explanation
        )
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

@router.get("/light-curve/{period}/{depth}/{duration}")
async def generate_light_curve(
    period: float,
    depth: float, 
    duration: float,
    impact: float = 0.5
):
    """
    📈 Generate light curve data points for Chart.js visualization
    
    This endpoint generates realistic light curve data for the React dashboard.
    Returns time series data in Chart.js format for interactive plotting.
    """
    try:
        import numpy as np
        
        # Validate inputs
        if period <= 0 or depth <= 0 or duration <= 0:
            raise ValueError("All parameters must be positive")
        
        # Generate time points (2 periods for context)
        time_span = 2 * period
        time_points = np.linspace(-time_span/2, time_span/2, 1000)
        
        # Convert depth from ppm to fraction
        depth_fraction = depth / 1e6
        duration_days = duration / 24.0  # Convert hours to days
        
        # Simple box model for transit
        flux = np.ones_like(time_points)
        
        # Find transit times (including second period)
        for i in [-1, 0, 1]:  # Previous, current, next transit
            transit_center = i * period
            transit_start = transit_center - duration_days / 2
            transit_end = transit_center + duration_days / 2
            
            # Apply transit (box model)
            in_transit = (time_points >= transit_start) & (time_points <= transit_end)
            flux[in_transit] = 1 - depth_fraction
        
        # Add realistic noise
        noise_level = depth_fraction * 0.1  # 10% of transit depth
        noise = np.random.normal(0, noise_level, len(flux))
        flux += noise
        
        # Format for Chart.js
        data_points = [
            {"x": float(t), "y": float(f)} 
            for t, f in zip(time_points, flux)
        ]
        
        return {
            "data": data_points,
            "metadata": {
                "period": period,
                "depth_ppm": depth,
                "duration_hours": duration,
                "impact": impact,
                "num_points": len(data_points),
                "time_span_days": time_span,
                "depth_fraction": depth_fraction
            },
            "chart_config": {
                "type": "line",
                "xlabel": "Time (days)",
                "ylabel": "Normalized Flux",
                "title": f"Simulated Light Curve (P={period:.2f}d, Depth={depth:.0f}ppm)"
            }
        }
        
    except Exception as e:
        logger.error(f"Light curve generation failed: {e}")
        raise HTTPException(status_code=400, detail=f"Light curve generation failed: {str(e)}")