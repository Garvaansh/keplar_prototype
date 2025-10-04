#!/usr/bin/env python3
"""
🧪 Backend Test Script
======================

Quick test to verify models are loaded and FastAPI server can start.
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

def test_models():
    """Test if models can be loaded"""
    print("🔍 Testing model loading...")
    
    try:
        from app.models.predictor import SecureExoplanetPredictor
        from app.core.config import Settings
        
        settings = Settings()
        print(f"📂 Model path: {settings.MODEL_PATH}")
        
        # Check if model files exist
        model_path = Path(settings.MODEL_PATH)
        if not model_path.exists():
            print(f"❌ Model directory not found: {model_path}")
            return False
            
        model_files = list(model_path.glob("*.model"))
        print(f"📋 Found {len(model_files)} model files:")
        for file in model_files:
            print(f"   - {file.name}")
        
        # Try to initialize predictor
        predictor = SecureExoplanetPredictor(str(model_path))
        print("✅ Predictor initialized successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return False

def test_fastapi():
    """Test if FastAPI can start"""
    print("\n🚀 Testing FastAPI startup...")
    
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully!")
        
        # Test import of all routes
        from app.api.routes import health, prediction, batch
        print("✅ All API routes imported successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error with FastAPI: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 BACKEND INTEGRATION TEST")
    print("=" * 40)
    
    models_ok = test_models()
    fastapi_ok = test_fastapi()
    
    print("\n📊 TEST RESULTS")
    print("=" * 20)
    print(f"Models:  {'✅ PASS' if models_ok else '❌ FAIL'}")
    print(f"FastAPI: {'✅ PASS' if fastapi_ok else '❌ FAIL'}")
    
    if models_ok and fastapi_ok:
        print("\n🎉 Backend is ready!")
        print("💡 Next step: Start server with 'python run.py'")
        return True
    else:
        print("\n⚠️  Backend needs fixes before starting")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)