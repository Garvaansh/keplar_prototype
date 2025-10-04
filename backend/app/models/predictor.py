#!/usr/bin/env python3
"""
🛡️ Secure Exoplanet Predictor
=============================

Production-ready ML predictor with comprehensive validation and security measures.
Designed for FastAPI integration with React dashboard frontend.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Any
import pandas as pd
import numpy as np
import pickle
import joblib
import logging
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from app.core.config import settings

logger = logging.getLogger(__name__)

@dataclass
class PredictionResult:
    """📊 Structured prediction result with full context"""
    prediction: str
    confidence: float
    probabilities: Dict[str, float]
    feature_importance: Dict[str, float]
    validation_warnings: List[str]
    light_curve_params: Dict[str, float]

class SecureExoplanetPredictor:
    """
    🛡️ Production-grade exoplanet predictor with security safeguards
    
    Features:
    - Multi-class classification (CONFIRMED, CANDIDATE, FALSE POSITIVE)
    - Comprehensive input validation and bounds checking
    - Physics-based consistency validation
    - Feature importance explanations for XAI
    - Light curve parameter generation for dashboard
    - Batch processing capabilities
    """
    
    def __init__(self, model_path: str):
        """Initialize predictor with models and validation data"""
        self.model_path = Path(model_path)
        self.models_loaded = False
        
        # Model components
        self.rf_model = None
        self.xgb_model = None
        self.ensemble_metadata = None
        self.feature_bounds = None
        
        # Model configuration
        self.rf_weight = 0.6
        self.xgb_weight = 0.4
        self.class_names = ["FALSE POSITIVE", "CANDIDATE", "CONFIRMED"]
        self.target_map = {0: "FALSE POSITIVE", 1: "CANDIDATE", 2: "CONFIRMED"}
        
        # Load models and metadata
        self._load_models()
        
        # Define all required features (must match training exactly)
        self.all_features = [
            'koi_period', 'koi_depth', 'koi_duration', 'koi_impact', 'koi_model_snr',
            'koi_prad', 'koi_teq', 'koi_insol', 'koi_steff', 'koi_slogg', 'koi_srad',
            'koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec', 
            'koi_score',
            # Engineered features (calculated during prediction)
            'period_impact_ratio', 'depth_duration_ratio', 'snr_per_ppm', 
            'planet_temp_ratio', 'stellar_density', 'transit_probability',
            'planet_density_proxy', 'equilibrium_flux', 'impact_depth_product',
            'period_snr_ratio', 'duration_impact_ratio'
        ]
    
    def _load_models(self):
        """Load trained models and metadata"""
        try:
            # Load Random Forest
            rf_path = self.model_path / "random_forest.model"
            if rf_path.exists():
                self.rf_model = joblib.load(rf_path)
                logger.info("Random Forest model loaded")
            
            # Load XGBoost
            xgb_path = self.model_path / "xgboost.model"
            if xgb_path.exists():
                with open(xgb_path, 'rb') as f:
                    self.xgb_model = pickle.load(f)
                logger.info("XGBoost model loaded")
            
            # Load ensemble metadata
            metadata_path = self.model_path / "ensemble_metadata.model"
            if metadata_path.exists():
                with open(metadata_path, 'rb') as f:
                    self.ensemble_metadata = pickle.load(f)
                if 'target_map' in self.ensemble_metadata:
                    # The target_map may be inverted (string->int), so we need to invert it to (int->string)
                    loaded_map = self.ensemble_metadata['target_map']
                    new_target_map = {}
                    
                    # Check if keys are strings or integers
                    first_key = next(iter(loaded_map.keys()))
                    if isinstance(first_key, str):
                        # Map is string->int, invert it to int->string
                        for k, v in loaded_map.items():
                            new_target_map[int(v)] = k
                    else:
                        # Map is already int->string or int->int
                        for k, v in loaded_map.items():
                            new_target_map[int(k)] = str(v)
                    
                    self.target_map = new_target_map
                if 'class_names' in self.ensemble_metadata:
                    self.class_names = self.ensemble_metadata['class_names']
                logger.info("Ensemble metadata loaded")
            
            # Load feature bounds for validation
            bounds_path = self.model_path / "features.model"
            if bounds_path.exists():
                with open(bounds_path, 'rb') as f:
                    self.feature_bounds = pickle.load(f)
                logger.info("Feature bounds loaded")
            else:
                # Fallback: create reasonable bounds for basic validation
                self.feature_bounds = {
                    'koi_period': {'min': 0.1, 'max': 10000},
                    'koi_depth': {'min': 0.1, 'max': 100000},
                    'koi_duration': {'min': 0.1, 'max': 48},
                    'koi_model_snr': {'min': 1.0, 'max': 1000}
                }
                logger.warning("Using fallback feature bounds")
            
            # Check if models are ready
            self.models_loaded = (self.rf_model is not None and 
                                self.xgb_model is not None)
            
            if self.models_loaded:
                logger.info("All models loaded successfully - Ready for predictions!")
            else:
                logger.warning("Some models missing - Please train models first")
                
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            self.models_loaded = False
    
    def validate_input(self, data: Dict[str, Any]) -> List[str]:
        """🔍 Comprehensive input validation with physics checks"""
        warnings = []
        
        try:
            # Required feature validation
            required_features = ['koi_period', 'koi_depth', 'koi_duration']
            for feature in required_features:
                if feature not in data or data[feature] is None:
                    warnings.append(f"Missing required feature: {feature}")
                elif data[feature] <= 0:
                    warnings.append(f"{feature} must be positive, got {data[feature]}")
            
            # Bounds checking (if available)
            if self.feature_bounds:
                for feature, value in data.items():
                    if feature in self.feature_bounds and value is not None:
                        bounds = self.feature_bounds[feature]
                        if value < bounds['min'] or value > bounds['max']:
                            warnings.append(f"{feature} outside training bounds [{bounds['min']:.3f}, {bounds['max']:.3f}]: {value}")
            
            # Physics-based validation
            period = data.get('koi_period', 0)
            depth = data.get('koi_depth', 0)
            duration = data.get('koi_duration', 0)
            
            if period > 0 and duration > 0:
                # Transit duration should be reasonable fraction of period
                duration_days = duration / 24.0
                duration_fraction = duration_days / period
                if duration_fraction > 0.1:  # More than 10% of period
                    warnings.append(f"Transit duration ({duration:.2f}h) unusually long for period ({period:.2f}d)")
            
            if depth > 0:
                # Planet radius vs transit depth consistency
                prad = data.get('koi_prad', 1.0)
                if prad and prad > 0:
                    # Approximate expected depth (ppm) = (Rp/Rs)^2 * 1e6
                    srad = data.get('koi_srad', 1.0) or 1.0
                    expected_depth = (prad / srad) ** 2 * 1e6
                    if abs(depth - expected_depth) > expected_depth * 2:  # Factor of 2 tolerance
                        warnings.append(f"Transit depth ({depth:.0f}ppm) inconsistent with planet size")
            
            # SNR validation
            snr = data.get('koi_model_snr', 0)
            if snr < 7:  # Typical threshold for reliable detection
                warnings.append(f"Low SNR ({snr:.1f}) - detection may be unreliable")
            
        except Exception as e:
            warnings.append(f"Validation error: {str(e)}")
        
        return warnings
    
    def engineer_features(self, data: Dict[str, Any]) -> pd.DataFrame:
        """⚙️ Feature engineering matching training pipeline exactly"""
        try:
            # Convert to DataFrame for consistent processing
            df = pd.DataFrame([data])
            
            # Ensure required columns exist with defaults
            feature_defaults = {
                'koi_period': 10.0, 'koi_depth': 100.0, 'koi_duration': 3.0,
                'koi_impact': 0.5, 'koi_model_snr': 10.0, 'koi_prad': 1.0,
                'koi_teq': 288.0, 'koi_insol': 1.0, 'koi_steff': 5778.0,
                'koi_slogg': 4.44, 'koi_srad': 1.0, 'koi_fpflag_nt': 0,
                'koi_fpflag_ss': 0, 'koi_fpflag_co': 0, 'koi_fpflag_ec': 0,
                'koi_score': 0.5
            }
            
            for feature, default_value in feature_defaults.items():
                if feature not in df.columns:
                    df[feature] = default_value
                df[feature] = df[feature].fillna(default_value)
            
            # Engineered features (EXACT match to training)
            df['period_impact_ratio'] = df['koi_period'] / np.maximum(df['koi_impact'], 0.01)
            df['depth_duration_ratio'] = df['koi_depth'] / np.maximum(df['koi_duration'], 0.1)
            df['snr_per_ppm'] = df['koi_model_snr'] / np.maximum(df['koi_depth'], 1.0)
            df['planet_temp_ratio'] = df['koi_teq'] / np.maximum(df['koi_steff'], 1000.0)
            df['stellar_density'] = 10 ** df['koi_slogg'] / np.maximum(df['koi_srad'], 0.1) ** 2
            df['transit_probability'] = np.minimum(df['koi_srad'] / np.maximum(df['koi_period'] ** (2/3), 0.1), 1.0)
            df['planet_density_proxy'] = df['koi_prad'] ** 3 / np.maximum(df['koi_period'], 0.1) ** 2
            df['equilibrium_flux'] = df['koi_insol'] * (df['koi_steff'] / 5778) ** 4
            df['impact_depth_product'] = df['koi_impact'] * np.sqrt(df['koi_depth'])
            df['period_snr_ratio'] = df['koi_period'] / np.maximum(df['koi_model_snr'], 1.0)
            df['duration_impact_ratio'] = df['koi_duration'] / np.maximum(df['koi_impact'], 0.01)
            
            # Handle infinities and NaNs
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.fillna(0)
            
            # Select only required features in correct order
            feature_df = df[self.all_features].copy()
            
            return feature_df
            
        except Exception as e:
            logger.error(f"Feature engineering failed: {e}")
            # Return DataFrame with zeros as fallback
            return pd.DataFrame(np.zeros((1, len(self.all_features))), columns=self.all_features)
    
    def generate_light_curve_params(self, data: Dict[str, Any]) -> Dict[str, float]:
        """📈 Generate parameters for dashboard light curve visualization"""
        try:
            period = data.get('koi_period', 10.0)
            depth = data.get('koi_depth', 100.0)
            duration = data.get('koi_duration', 3.0)
            impact = data.get('koi_impact', 0.5)
            
            return {
                'period_days': float(period),
                'depth_ppm': float(depth),
                'duration_hours': float(duration),
                'impact_parameter': float(impact),
                'ingress_duration': float(duration * 0.15),  # ~15% of total
                'egress_duration': float(duration * 0.15),
                'baseline_flux': 1.0,
                'minimum_flux': 1.0 - (depth / 1e6),
                'phase_offset': 0.0
            }
        except Exception as e:
            logger.error(f"Light curve parameter generation failed: {e}")
            return {
                'period_days': 10.0, 'depth_ppm': 100.0, 'duration_hours': 3.0,
                'impact_parameter': 0.5, 'ingress_duration': 0.45, 'egress_duration': 0.45,
                'baseline_flux': 1.0, 'minimum_flux': 0.9999, 'phase_offset': 0.0
            }
    
    def predict(self, data: Dict[str, Any]) -> PredictionResult:
        """🔮 Make secure prediction with full validation and explanations"""
        if not self.models_loaded:
            return PredictionResult(
                prediction="ERROR",
                confidence=0.0,
                probabilities={"ERROR": 1.0},
                feature_importance={},
                validation_warnings=["Models not loaded"],
                light_curve_params={}
            )
        
        try:
            # Validate input
            warnings = self.validate_input(data)
            
            # Engineer features
            features_df = self.engineer_features(data)
            
            # Make predictions
            rf_probs = self.rf_model.predict_proba(features_df)[0]
            xgb_probs = self.xgb_model.predict_proba(features_df)[0]
            
            # Ensemble prediction (weighted average)
            ensemble_probs = (self.rf_weight * rf_probs + self.xgb_weight * xgb_probs)
            predicted_class_raw = np.argmax(ensemble_probs)
            predicted_class = int(predicted_class_raw)  # Ensure regular Python int
            
            # Debug logging
            logger.debug(f"Predicted class raw: {predicted_class_raw} (type: {type(predicted_class_raw)})")
            logger.debug(f"Predicted class: {predicted_class} (type: {type(predicted_class)})")
            logger.debug(f"Target map keys: {list(self.target_map.keys())}")
            
            prediction_name = self.target_map[predicted_class]
            confidence = float(ensemble_probs[predicted_class])
            
            # Class probabilities
            probabilities = {
                self.class_names[i]: float(prob) 
                for i, prob in enumerate(ensemble_probs)
            }
            
            # Feature importance (from Random Forest)
            feature_importance = dict(zip(
                self.all_features,
                [float(importance) for importance in self.rf_model.feature_importances_]
            ))
            # Sort by importance and take top 10
            feature_importance = dict(sorted(
                feature_importance.items(), 
                key=lambda x: x[1], reverse=True
            )[:10])
            
            # Generate light curve parameters
            light_curve_params = self.generate_light_curve_params(data)
            
            return PredictionResult(
                prediction=prediction_name,
                confidence=confidence,
                probabilities=probabilities,
                feature_importance=feature_importance,
                validation_warnings=warnings,
                light_curve_params=light_curve_params
            )
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return PredictionResult(
                prediction="ERROR",
                confidence=0.0,
                probabilities={"ERROR": 1.0},
                feature_importance={},
                validation_warnings=[f"Prediction error: {str(e)}"],
                light_curve_params={}
            )
    
    def predict_batch(self, batch_data: List[Dict[str, Any]]) -> List[PredictionResult]:
        """📁 Process multiple predictions efficiently"""
        results = []
        
        for i, data in enumerate(batch_data):
            try:
                result = self.predict(data)
                results.append(result)
                
                if (i + 1) % 100 == 0:
                    logger.info(f"Processed {i + 1}/{len(batch_data)} predictions")
                    
            except Exception as e:
                logger.error(f"Batch prediction {i+1} failed: {e}")
                results.append(PredictionResult(
                    prediction="ERROR",
                    confidence=0.0,
                    probabilities={"ERROR": 1.0},
                    feature_importance={},
                    validation_warnings=[f"Batch processing error: {str(e)}"],
                    light_curve_params={}
                ))
        
        logger.info(f"Batch processing complete: {len(results)} predictions")
        return results

def create_predictor(model_path: Optional[str] = None) -> SecureExoplanetPredictor:
    """🏭 Factory function to create predictor instance"""
    if model_path is None:
        model_path = settings.MODEL_PATH
    
    predictor = SecureExoplanetPredictor(model_path)
    return predictor