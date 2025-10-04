# 🌟 Exoplanet Discovery Dashboard - Backend

## 🚀 Quick Start

### For Development (Windows)

```bash
cd backend
setup_dev.bat
python run.py
```

### For Development (Linux/Mac)

```bash
cd backend
chmod +x setup_dev.sh
./setup_dev.sh
python run.py
```

### Using Docker

```bash
docker-compose up --build
```

## 📋 Prerequisites

1. **Python 3.9+** installed
2. **Trained Models** from `Fine_Tuned_Training.ipynb`
3. **Virtual Environment** (recommended)

## 🏗️ Architecture

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/routes/          # API endpoints
│   │   ├── health.py        # Health checks
│   │   ├── prediction.py    # Single predictions
│   │   └── batch.py         # Batch processing
│   ├── models/
│   │   └── predictor.py     # ML prediction logic
│   └── core/
│       ├── config.py        # Configuration management
│       └── logging_config.py # Logging setup
├── config/
├── requirements.txt
├── Dockerfile
├── run.py                   # Development server
└── test_api.py             # API testing
```

## 🔌 API Endpoints

### Core Endpoints

- `GET /` - API information
- `GET /api/v1/health` - Health check
- `GET /api/v1/health/detailed` - Detailed status

### Prediction Endpoints

- `POST /api/v1/predict` - Single prediction
- `POST /api/v1/batch-predict` - CSV batch processing
- `GET /api/v1/light-curve/{period}/{depth}/{duration}` - Light curve data

### Information Endpoints

- `GET /api/v1/model-info` - Model details
- `GET /api/v1/feature-bounds` - Feature ranges
- `GET /api/v1/batch-template` - CSV template info

## 🔧 Configuration

Environment variables (create `.env` from `.env.example`):

```bash
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🧪 Testing

Test all endpoints:

```bash
python test_api.py
```

## 📚 Documentation

Interactive API docs: http://localhost:8000/docs

## 🐳 Docker Deployment

Full stack with React frontend:

```bash
docker-compose --profile frontend up
```

Backend only:

```bash
docker-compose up exoplanet-api
```

## 🔗 Frontend Integration

The API is designed for seamless React integration:

- **CORS enabled** for common development ports
- **Structured responses** for easy component binding
- **Chart.js compatible** light curve data
- **Validation warnings** for user feedback
- **Batch processing** with sortable results

### Sample React API Call

```javascript
const response = await fetch("http://localhost:8000/api/v1/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    transit: {
      koi_period: 10.0,
      koi_depth: 100.0,
      koi_duration: 3.0,
      koi_model_snr: 15.0,
    },
  }),
});
const prediction = await response.json();
```

## ⚙️ Production Notes

1. **Models Required**: Train models first using `Fine_Tuned_Training.ipynb`
2. **Environment**: Set `ENVIRONMENT=production` in `.env`
3. **CORS**: Update `ALLOWED_ORIGINS` for your domain
4. **Security**: Enable HTTPS in production
5. **Monitoring**: Check `/api/v1/health/detailed` for status

## 🆘 Troubleshooting

**Models not found?**

```bash
# Train models first
jupyter notebook ../notebook/Fine_Tuned_Training.ipynb
```

**Port already in use?**

```bash
# Change port in .env
PORT=8001
```

**Import errors?**

```bash
# Reinstall requirements
pip install -r requirements.txt
```
