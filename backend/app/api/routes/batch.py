#!/usr/bin/env python3
"""
📁 Batch Processing API Routes
==============================

Batch prediction endpoints for CSV file processing.
"""

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Dict, List, Any
import pandas as pd
import io
import logging

from app.models.predictor import SecureExoplanetPredictor, create_predictor

logger = logging.getLogger(__name__)
router = APIRouter()

class BatchResult(BaseModel):
    """📁 Batch processing result for React dashboard"""
    total_processed: int
    successful_predictions: int
    failed_predictions: int
    results: List[Dict[str, Any]]
    summary: Dict[str, Any]

# Dependency injection for predictor
async def get_predictor() -> SecureExoplanetPredictor:
    """Get predictor instance (singleton pattern)"""
    if not hasattr(get_predictor, '_predictor'):
        try:
            get_predictor._predictor = create_predictor()
            logger.info("✅ Predictor initialized for batch processing")
        except Exception as e:
            logger.error(f"❌ Failed to initialize predictor: {e}")
            raise HTTPException(status_code=500, detail="Model initialization failed")
    return get_predictor._predictor

@router.post("/batch-predict", response_model=BatchResult)
async def predict_batch(
    file: UploadFile = File(...),
    predictor: SecureExoplanetPredictor = Depends(get_predictor)
):
    """
    📁 Batch prediction from CSV file
    
    Upload a CSV file with multiple exoplanet candidates for batch processing.
    Returns results formatted for the React dashboard table with sorting/filtering.
    
    Expected CSV columns:
    - koi_period: Orbital period (days)
    - koi_depth: Transit depth (ppm)  
    - koi_duration: Transit duration (hours)
    - koi_model_snr: Signal-to-noise ratio
    - Other optional parameters...
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Read CSV
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        
        logger.info(f"📁 Processing batch file: {file.filename} ({len(df)} rows)")
        
        # Validate required columns
        required_cols = ['koi_period', 'koi_depth', 'koi_duration']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {missing_cols}"
            )
        
        # Convert to list of dicts
        batch_data = df.to_dict('records')
        
        # Process batch
        results = predictor.predict_batch(batch_data)
        
        # Format results for React dashboard table
        formatted_results = []
        successful = 0
        failed = 0
        class_counts = {"CONFIRMED": 0, "CANDIDATE": 0, "FALSE POSITIVE": 0, "ERROR": 0}
        
        for i, result in enumerate(results):
            if result.prediction != "ERROR":
                successful += 1
                class_counts[result.prediction] += 1
                
                # Get original data for context
                original_data = batch_data[i]
                
                formatted_results.append({
                    "id": i + 1,
                    "row": i + 1,
                    "prediction": result.prediction,
                    "confidence": round(result.confidence, 3),
                    "confidence_percent": f"{result.confidence * 100:.1f}%",
                    
                    # Class probabilities
                    "prob_confirmed": round(result.probabilities.get('CONFIRMED', 0), 3),
                    "prob_candidate": round(result.probabilities.get('CANDIDATE', 0), 3),
                    "prob_false_positive": round(result.probabilities.get('FALSE POSITIVE', 0), 3),
                    
                    # Key input parameters for reference
                    "period": round(original_data.get('koi_period', 0), 2),
                    "depth": round(original_data.get('koi_depth', 0), 1),
                    "duration": round(original_data.get('koi_duration', 0), 2),
                    "snr": round(original_data.get('koi_model_snr', 0), 1),
                    
                    # Feature importance (full dictionary for charts)
                    "feature_importance": {k: round(v, 4) for k, v in result.feature_importance.items()} if result.feature_importance else {},
                    
                    # Light curve parameters for visualization
                    "light_curve_params": result.light_curve_params,
                    
                    # Validation and explanations
                    "warnings": len(result.validation_warnings),
                    "warning_details": result.validation_warnings[:3],  # First 3 warnings
                    
                    # Status for UI
                    "status": "success",
                    "has_warnings": len(result.validation_warnings) > 0
                })
            else:
                failed += 1
                class_counts["ERROR"] += 1
                original_data = batch_data[i]
                
                formatted_results.append({
                    "id": i + 1,
                    "row": i + 1,
                    "prediction": "ERROR",
                    "confidence": 0.0,
                    "confidence_percent": "0.0%",
                    "prob_confirmed": 0.0,
                    "prob_candidate": 0.0,
                    "prob_false_positive": 0.0,
                    "period": original_data.get('koi_period', 0),
                    "depth": original_data.get('koi_depth', 0),
                    "duration": original_data.get('koi_duration', 0),
                    "snr": original_data.get('koi_model_snr', 0),
                    "warnings": len(result.validation_warnings),
                    "warning_details": result.validation_warnings[:3],
                    "top_feature": "Error",
                    "top_importance": 0.0,
                    "status": "error",
                    "has_warnings": True
                })
        
        # Generate summary statistics
        summary = {
            "file_name": file.filename,
            "processing_time": "< 1 minute",  # TODO: Add actual timing
            "success_rate": round((successful / len(batch_data)) * 100, 1) if batch_data else 0,
            "class_distribution": class_counts,
            "most_common_prediction": max(class_counts, key=class_counts.get),
            "average_confidence": round(
                sum(r["confidence"] for r in formatted_results if r["status"] == "success") / max(successful, 1),
                3
            ) if successful > 0 else 0,
            "high_confidence_count": sum(1 for r in formatted_results if r["confidence"] > 0.8),
            "warnings_count": sum(r["warnings"] for r in formatted_results)
        }
        
        logger.info(f"✅ Batch processing complete: {successful} successful, {failed} failed")
        
        return BatchResult(
            total_processed=len(batch_data),
            successful_predictions=successful,
            failed_predictions=failed,
            results=formatted_results,
            summary=summary
        )
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Empty CSV file")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Batch processing failed: {e}")
        raise HTTPException(status_code=400, detail=f"Batch processing failed: {str(e)}")

@router.get("/batch-template")
async def get_batch_template():
    """
    📋 Get CSV template for batch processing
    
    Returns information about the expected CSV format and download link
    for a template file that React dashboard can use.
    """
    return {
        "template_info": {
            "description": "CSV template for batch exoplanet prediction",
            "required_columns": [
                "koi_period", "koi_depth", "koi_duration", "koi_model_snr"
            ],
            "optional_columns": [
                "koi_impact", "koi_prad", "koi_teq", "koi_insol",
                "koi_steff", "koi_slogg", "koi_srad", "koi_score",
                "koi_fpflag_nt", "koi_fpflag_ss", "koi_fpflag_co", "koi_fpflag_ec"
            ]
        },
        "example_data": [
            {
                "koi_period": 10.0,
                "koi_depth": 100.0,
                "koi_duration": 3.0,
                "koi_model_snr": 15.0,
                "koi_impact": 0.5,
                "koi_prad": 1.2
            },
            {
                "koi_period": 365.25,
                "koi_depth": 84.0,
                "koi_duration": 4.5,
                "koi_model_snr": 25.0,
                "koi_impact": 0.3,
                "koi_prad": 1.0
            }
        ],
        "column_descriptions": {
            "koi_period": "Orbital period in days",
            "koi_depth": "Transit depth in parts per million (ppm)",
            "koi_duration": "Transit duration in hours",
            "koi_model_snr": "Signal-to-noise ratio of the detection",
            "koi_impact": "Impact parameter (0 = central transit, 1 = grazing)",
            "koi_prad": "Planet radius in Earth radii",
            "koi_teq": "Equilibrium temperature in Kelvin",
            "koi_insol": "Insolation flux (Earth = 1)",
            "koi_steff": "Stellar effective temperature in Kelvin",
            "koi_slogg": "Stellar surface gravity (log g)",
            "koi_srad": "Stellar radius in Solar radii"
        },
        "limits": {
            "max_rows": 10000,
            "max_file_size_mb": 50,
            "supported_formats": ["csv"]
        }
    }