# Kepler 2.0: Exoplanet Detection

## Abstract

The discovery of exoplanets has accelerated dramatically with space-based transit surveys like Kepler, K2, and TESS. However, the manual classification of thousands of planetary candidates remains a bottleneck in astronomical research. This project addresses NASA's challenge to develop an AI/ML system that automatically analyzes transit photometry data to identify and classify exoplanets.

Our solution combines ensemble machine learning with an interactive web dashboard, enabling researchers to efficiently process large datasets while maintaining scientific rigor. The system achieves high accuracy in distinguishing confirmed exoplanets from false positives (stellar eclipses, background binaries) and candidates requiring follow-up observations.

### Problem Statement

Data from several space-based exoplanet surveying missions have enabled discovery of thousands of new planets outside our solar system, but most of these exoplanets were identified manually. With advances in artificial intelligence and machine learning, it is possible to automatically analyze large sets of data collected by these missions to identify exoplanets. The challenge is to create an AI/ML model trained on NASA's open-source exoplanet datasets that can analyze new data to accurately identify exoplanets, supported by an intuitive web interface for researcher interaction.

## Our Solution

### Architecture Overview

We developed a full-stack exoplanet classification system consisting of:

1. **Ensemble Machine Learning Pipeline** - Combines Random Forest and XGBoost classifiers
2. **Deep Learning Model** - CNN trained on flux time-series data
3. **FastAPI Backend** - RESTful API serving model predictions
4. **React Dashboard** - Interactive visualization and batch processing interface

### Machine Learning Models

#### 1. Ensemble Model (Production)

Our primary classification system uses an ensemble of two complementary algorithms:

**Random Forest Classifier**

- 800 decision trees with bootstrap aggregating (bagging)
- Captures complex non-linear relationships in transit parameters
- Provides robust feature importance rankings
- Weight in ensemble: 60%

**XGBoost Classifier**

- Gradient boosting with regularization (L1/L2)
- Sequential learning corrects errors from previous iterations
- Handles imbalanced classes through scale_pos_weight
- Weight in ensemble: 40%

**Training Data**: Kepler Objects of Interest (KOI) and TESS Objects of Interest (TOI)

- KOI Dataset: [NASA Exoplanet Archive - Cumulative KOI Table](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=cumulative)
- TESS Dataset: [NASA Exoplanet Archive - TOI Table](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=TOI)

**Features Used** (27 total):

- Transit parameters: orbital period, depth, duration, impact parameter
- Stellar properties: effective temperature, radius, surface gravity
- Signal quality: signal-to-noise ratio, multiple event statistic
- Disposition metrics: planet/false positive scores
- Engineered features: planet density proxy, duration ratio, period-depth correlation

#### 2. Convolutional Neural Network (Research)

**Training Data**: Flux time-series from Kepler mission

- Dataset: [Kepler Exoplanet Hunting Dataset](https://www.kaggle.com/code/antonzv/exoplanet-hunting-top-score-using-smote-and-cnn/input)
- 3,197 flux measurements per light curve

**Architecture**:

```
Input (3197 flux values)
    ↓
Reshape → Normalization
    ↓
Conv1D (64 filters) + ReLU + BatchNorm
    ↓
Conv1D (32 filters) + ReLU + BatchNorm
    ↓
MaxPooling1D + Dropout(0.3)
    ↓
Flatten → Dense(128) → Dense(64) → Dense(32)
    ↓
Output (Sigmoid activation)
```

**Performance**: Trained with SMOTE oversampling to handle class imbalance, achieving high recall for exoplanet detection.

### Key Features

**Three-Class Classification**:

- **CONFIRMED**: High-confidence exoplanet detections
- **CANDIDATE**: Signals requiring follow-up observations
- **FALSE POSITIVE**: Stellar eclipses, instrumental artifacts, background binaries

**Explainable AI**:

- Feature importance visualization shows which parameters drive each prediction
- Physics-informed feature engineering ensures interpretability

**Batch Processing**:

- CSV upload for analyzing multiple candidates simultaneously
- Exportable results with confidence scores and validation warnings

**Real-time Predictions**:

- Interactive parameter sliders for single-object analysis
- Dynamic light curve generation
- Instant classification updates

## Project Structure

```
kepler2.0-dashboard-main/
├── backend/                    # FastAPI server
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/        # API endpoints
│   │   ├── core/              # Configuration
│   │   └── models/            # ML predictor logic
│   ├── trained_models/        # Serialized models
│   │   ├── random_forest.model
│   │   ├── xgboost.model
│   │   └── scaler.model       # StandardScaler for normalization
│   └── requirements.txt
│
├── frontend/                   # React dashboard
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── pages/             # Dashboard views
│   │   ├── lib/               # API client
│   │   └── hooks/             # React hooks
│   ├── package.json
│   └── vite.config.ts
│
├── Kepler-2.0-Dashboard/      # Reference implementation
│   └── Kepler-20-Dashboard/   # Original dashboard code
│
├── test.csv                    # Sample test data (25 cases)
└── readme.md
```

## Getting Started

### Prerequisites

- **Backend**: Python 3.8+, pip
- **Frontend**: Node.js 16+, yarn
- **System**: Windows/Linux/macOS

### Installation

#### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/Garvaansh/keplar_prototype/
cd keplar_prototype

# Run the cross-platform setup script
python setup.py
```

The setup script will automatically:

- Check Python 3.8+ and Node.js 16+ are installed
- Create a virtual environment for the backend
- Install all Python dependencies
- Install all frontend dependencies
- Verify trained models are present

#### Option 2: Manual Setup

**Step 1: Clone the Repository**

```bash
git clone https://github.com/Garvaansh/keplar_prototype/
cd keplar_prototype
```

**Step 2: Backend Setup**

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Step 3: Frontend Setup**

```bash
cd frontend

# Install dependencies (choose yarn or npm)
yarn install
# or
npm install
```

### Running the Application

#### Quick Start (Recommended)

From the root directory, run:

```bash
# Start both backend and frontend together
yarn dev
```

Or using npm:

```bash
npm run dev
```

This will start:

- **Backend** at `http://localhost:8000`
- **Frontend** at `http://localhost:5173`
- **API Documentation** at `http://localhost:8000/docs`

#### Manual Start (Two Terminals)

**Terminal 1 - Backend:**

```bash
cd backend
python run.py
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm run dev
```

The backend `run.py` script automatically:

- Detects your operating system
- Activates the virtual environment
- Starts the FastAPI server with hot reload
  yarn dev



Frontend will run at `http://localhost:5173`


### Usage

#### Single Object Analysis

1. Navigate to the main dashboard
2. Adjust the parameter sliders:
   - **Orbital Period**: Time between transits (days)
   - **Transit Depth**: Amount of starlight blocked (ppm)
   - **Transit Duration**: Length of transit event (hours)
3. View real-time predictions with confidence scores
4. Examine feature importance to understand the classification
5. Analyze the generated light curve

#### Batch Processing

1. Click "Batch Processing" in the dashboard header
2. Download the CSV template or prepare your own:
   ```csv
   koi_period,koi_depth,koi_duration,koi_impact,koi_snr,koi_steff,koi_srad,koi_score,koi_fpflag_nt,koi_fpflag_ss,koi_fpflag_co,koi_fpflag_ec
   365.25,84,13.0,0.2,150,5778,1.0,0.95,0,0,0,0
    ```

3. Upload your CSV file
4. Wait for processing (progress indicator shown)
5. Review results in the interactive table:
   - Sort by classification, confidence, or any parameter
   - Search and filter results
   - Click any row to see detailed analysis
6. Export results as CSV for further analysis

#### API Endpoints

**Predict Single Object**:

```bash
POST http://localhost:8000/api/v1/predict
Content-Type: application/json

{
  "period": 15.5,
  "depth": 5000,
  "duration": 3.5,
  "impact": 0.5
}
```

**Batch Predictions**:

```bash
POST http://localhost:8000/api/v1/batch-predict
Content-Type: multipart/form-data

file: exoplanet_data.csv
```

**Generate Light Curve**:

```bash
GET http://localhost:8000/api/v1/light-curve/{period}/{depth}/{duration}?impact=0.5
```

## Model Performance

### Ensemble Model Metrics

| Metric    | Random Forest | XGBoost | Ensemble |
| --------- | ------------- | ------- | -------- |
| Accuracy  | 94.2%         | 93.8%   | 95.1%    |
| Precision | 91.5%         | 90.8%   | 92.7%    |
| Recall    | 89.3%         | 88.6%   | 90.2%    |
| F1-Score  | 90.4%         | 89.7%   | 91.4%    |

### Real-World Results

From our 25-case test dataset:

- **6 CONFIRMED** planets identified (hot Jupiters, super-Earths)
- **3 FALSE POSITIVES** detected with 88-92% confidence (stellar eclipses with abnormal depths)
- **16 CANDIDATES** flagged for follow-up (scientifically accurate distribution)

The model correctly identifies edge cases:

- Ultra-short period planets (< 1 day)
- Ultra-long period planets (> 1000 days)
- Grazing transits (high impact parameter)
- Marginal detections (low SNR)

## Technical Highlights

### Data Preprocessing

1. **Feature Scaling**: StandardScaler normalization ensures all features contribute equally
2. **Outlier Handling**: Statistical methods remove instrumental artifacts
3. **Class Balancing**: SMOTE and class weights address inherent dataset imbalance
4. **Feature Engineering**: Physics-based derived features improve model understanding

### Why Ensemble Learning?

Random Forest and XGBoost complement each other:

- **Random Forest**: Parallel tree building, robust to overfitting, captures feature interactions
- **XGBoost**: Sequential error correction, handles complex patterns, optimized for speed

The weighted average (60% RF, 40% XGB) leverages the stability of bagging and the precision of boosting.

### Technology Stack

**Backend**:

- FastAPI 0.104.1 - Modern async web framework
- scikit-learn 1.3.2 - Random Forest implementation
- XGBoost 2.0.2 - Gradient boosting
- Pandas 2.1.3 - Data manipulation
- NumPy 1.26.2 - Numerical computing

**Frontend**:

- React 18 - UI framework
- TypeScript - Type safety
- Vite - Fast build tool
- Recharts - Data visualization
- Tailwind CSS - Styling
- radix-ui - Component library

## Acknowledgments

This project was developed in response to NASA's Space Apps Challenge 2025: "A World Away: Hunting for Exoplanets with AI"

**Data Sources**:

- NASA Exoplanet Archive
- Kepler Mission Science Team
- TESS Mission Team
- Kaggle Community

### Project URLs

| Service              | URL                                 |
| -------------------- | ----------------------------------- |
| Frontend Dashboard   | http://localhost:5173               |
| Backend API          | http://localhost:8000               |
| API Documentation    | http://localhost:8000/docs          |
| Interactive API      | http://localhost:8000/redoc         |
| Check backend health | http://localhost:8000/api/v1/health |
