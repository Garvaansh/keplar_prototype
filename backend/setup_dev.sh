#!/bin/bash
# 🚀 Development Setup Script
# ===========================

echo "🌟 Setting up Exoplanet Discovery Dashboard Backend"
echo "=================================================="

# Check Python version
python_version=$(python --version 2>&1)
echo "🐍 Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "📝 Please customize .env file as needed"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p ../model
mkdir -p ../data

# Check for trained models
echo "🔍 Checking for trained models..."
if [ ! -f "../model/random-forest.model" ] || [ ! -f "../model/xgboost.model" ]; then
    echo "⚠️  Trained models not found!"
    echo "💡 Please train models first:"
    echo "   1. Open notebook/Fine_Tuned_Training.ipynb"
    echo "   2. Run all cells to train the 3-class models"
    echo "   3. Models will be saved to model/ directory"
else
    echo "✅ Trained models found!"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🚀 To start the development server:"
echo "   cd backend"
echo "   source venv/bin/activate  # (if not already activated)"
echo "   python run.py"
echo ""
echo "📚 API documentation will be available at:"
echo "   http://localhost:8000/docs"