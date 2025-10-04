@echo off
REM 🚀 Windows Development Setup Script
REM ===================================

echo 🌟 Setting up Exoplanet Discovery Dashboard Backend
echo ==================================================

REM Check Python version
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.9+
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing requirements...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ⚙️  Creating .env file...
    copy .env.example .env
    echo 📝 Please customize .env file as needed
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist "logs" mkdir logs
if not exist "..\model" mkdir ..\model
if not exist "..\data" mkdir ..\data

REM Check for trained models
echo 🔍 Checking for trained models...
if not exist "..\model\random-forest.model" (
    echo ⚠️  Trained models not found!
    echo 💡 Please train models first:
    echo    1. Open notebook/Fine_Tuned_Training.ipynb
    echo    2. Run all cells to train the 3-class models
    echo    3. Models will be saved to model/ directory
) else (
    echo ✅ Trained models found!
)

echo.
echo 🎉 Setup complete!
echo.
echo 🚀 To start the development server:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python run.py
echo.
echo 📚 API documentation will be available at:
echo    http://localhost:8000/docs

pause