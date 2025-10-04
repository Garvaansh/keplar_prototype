#!/usr/bin/env python3
"""
🧪 API Testing Script
=====================

Quick script to test all API endpoints to ensure everything works.
Run this after starting the server to verify functionality.
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, files=None, description=""):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        print(f"🔍 Testing {method.upper()} {endpoint}")
        if description:
            print(f"   {description}")
        
        if method.lower() == "get":
            response = requests.get(url, timeout=30)
        elif method.lower() == "post":
            if files:
                response = requests.post(url, files=files, timeout=30)
            else:
                response = requests.post(url, json=data, timeout=30)
        
        if response.status_code in [200, 201]:
            print(f"   ✅ Success ({response.status_code})")
            return True
        else:
            print(f"   ❌ Failed ({response.status_code}): {response.text[:100]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   💥 Error: {str(e)[:100]}")
        return False

def main():
    """Run all API tests"""
    print("🧪 Testing Exoplanet Discovery Dashboard API")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Server not responding. Please start the server first:")
            print("   cd backend && python run.py")
            return
    except:
        print("❌ Server not running. Please start the server first:")
        print("   cd backend && python run.py")
        return
    
    print("✅ Server is running!")
    print()
    
    # Test endpoints
    tests = [
        ("GET", "/", None, None, "Root endpoint"),
        ("GET", "/api/v1/health", None, None, "Basic health check"),
        ("GET", "/api/v1/health/detailed", None, None, "Detailed health check"),
        ("GET", "/api/v1/model-info", None, None, "Model information"),
        ("GET", "/api/v1/feature-bounds", None, None, "Feature bounds"),
        ("GET", "/api/v1/batch-template", None, None, "Batch template info"),
        
        # Test prediction endpoint
        ("POST", "/api/v1/predict", {
            "transit": {
                "koi_period": 10.0,
                "koi_depth": 100.0,
                "koi_duration": 3.0,
                "koi_impact": 0.5,
                "koi_model_snr": 15.0
            },
            "planet": {
                "koi_prad": 1.2,
                "koi_teq": 300,
                "koi_insol": 1.5
            }
        }, None, "Single prediction"),
        
        # Test light curve generation
        ("GET", "/light-curve/10.0/100.0/3.0", None, None, "Light curve generation"),
    ]
    
    passed = 0
    total = len(tests)
    
    for method, endpoint, data, files, description in tests:
        if test_endpoint(method, endpoint, data, files, description):
            passed += 1
        print()
        time.sleep(0.5)  # Brief pause between tests
    
    # Summary
    print("=" * 50)
    print(f"🏁 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! API is ready for frontend integration.")
    else:
        print(f"⚠️  {total - passed} tests failed. Check the server logs.")
        
    print()
    print("🌐 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/api/v1/health")

if __name__ == "__main__":
    main()