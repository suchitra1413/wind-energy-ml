# Wind Power Prediction - ML Model Web Application

## 📋 Overview

A complete **full-stack machine learning web application** for predicting hourly wind power output. Built with:

- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Flask (Python) - Free, lightweight, perfect for ML APIs
- **Model:** Random Forest Regressor (300 estimators, 82.7% R²)
- **Deployment:** GitHub + Render.com/Railway (free tiers available)

## 🎯 Features

✅ **Real-time Wind Power Prediction**
- Input 13 meteorological parameters
- Get normalized power output (0-1)
- Visual power level indicator

✅ **Advanced ML Model**
- Random Forest with 300 estimators
- Feature engineering: polynomial, circular, interaction features
- Trained on 140,160 wind power samples
- Performance: MAE=0.074, RMSE=0.105, R²=0.827

✅ **Professional UI/UX**
- Responsive design (mobile & desktop)
- Real-time form validation
- Loading states & error handling
- Beautiful gradient design with animations

✅ **Production-Ready Backend**
- RESTful API with CORS support
- Batch prediction endpoint
- Health check endpoint
- Model info endpoint
- Error handling & logging

✅ **Easy Deployment**
- GitHub Pages for frontend
- Render.com or Railway for backend (free)
- Comprehensive deployment guide included

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/wind-power-prediction.git
cd wind-power-prediction

# 2. Setup backend
cd backend
pip install -r requirements.txt
python app.py
# Backend running at: http://localhost:5000

# 3. In new terminal, setup frontend
cd ../frontend
python -m http.server 8000
# Frontend running at: http://localhost:8000
```

### Production Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions:

1. **Frontend:** Deploy to GitHub Pages (static files)
2. **Backend:** Deploy to Render.com or Railway (Python + Flask)
3. **Model:** Serialize and commit pickle files

## 📁 Project Structure

```
wind-power-prediction/
├── frontend/
│   ├── index.html          # HTML structure
│   ├── style.css           # Styling & animations
│   ├── app.js              # Frontend logic
│   └── assets/             # Images & icons (optional)
│
├── backend/
│   ├── app.py              # Flask API server
│   ├── serialize_model.py   # Model export script
│   ├── model.pkl            # Trained Random Forest (generated)
│   ├── scaler.pkl           # StandardScaler (generated)
│   ├── requirements.txt      # Python dependencies
│   ├── Procfile             # Heroku/Render deployment config
│   └── runtime.txt          # Python version specification
│
├── model/
│   └── Wind-Power-Prediction.ipynb  # Original training notebook
│
├── .gitignore              # Git ignore patterns
├── DEPLOYMENT_GUIDE.md     # Detailed deployment instructions
└── README.md              # This file
```

## 🧠 Model Architecture

### Input Features (13 parameters)
- **Meteorological:** Temperature, humidity, dew point, wind speed (10m & 100m), wind direction, wind gust
- **Temporal:** Hour, day, month, day-of-week, is-weekend flag

### Feature Engineering
- Circular encoding for wind direction (sine/cosine)
- Polynomial features for wind speed (squared & cubic terms)
- Interaction features (temp×humidity, wind shear)
- Total: 25 engineered features

### Model: Random Forest Regressor
- **Estimators:** 300 trees
- **Performance:** R² = 0.827 (82.7% accuracy)
- **MAE:** 0.074 (normalized units)
- **RMSE:** 0.105

## 🔌 API Endpoints

### Health Check
```http
GET /api/health
Response: { status: "healthy", model_loaded: true }
```

### Make Prediction
```http
POST /api/predict
Content-Type: application/json

{
  "Location": 1,
  "Temp_2m": 25.5,
  "RelHum_2m": 65,
  "DP_2m": 18.2,
  "WS_10m": 5.2,
  "WS_100m": 8.5,
  "WD_10m": 180,
  "WD_100m": 195,
  "WG_10m": 3.2,
  "hour": 14,
  "day": 15,
  "month": 6,
  "dayofweek": 2,
  "is_weekend": 0
}

Response: { prediction: 0.7234, status: "success" }
```

### Model Information
```http
GET /api/model-info
Response: { algorithm: "Random Forest", r2_score: 0.8272, ... }
```

### Batch Prediction
```http
POST /api/predict-batch
[{ ... }, { ... }, ...]
Response: { predictions: [0.45, 0.67, ...], count: 2 }
```

## 🛠 Technology Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | HTML5, CSS3, Vanilla JS | No build process, instant deployment |
| Backend | Flask + Gunicorn | Lightweight, perfect for ML APIs |
| ML Model | scikit-learn | Robust, production-proven library |
| Deployment | GitHub + Render/Railway | Free tiers, easy CI/CD |
| Version Control | Git + GitHub | Industry standard |

## 📊 Performance Metrics

- **Model Training:** ~2-3 minutes on 140K samples
- **Prediction Time:** <100ms per sample
- **Frontend Load:** <1 second
- **Backend Response:** <200ms (average)
- **Model File Size:** ~50-100 MB

## 🔐 Security Features

✅ CORS enabled for controlled cross-origin requests
✅ Input validation on frontend and backend
✅ No hardcoded credentials or API keys
✅ HTTPS support on production platforms
✅ Error messages sanitized (no internal details exposed)

## 📝 How to Generate Model Files

### From Your Colab Notebook:

```python
# 1. After training, run serialize_model.py
# Copy the code from backend/serialize_model.py

# 2. Execute in Colab cell
# This generates:
#   - model.pkl (trained Random Forest)
#   - scaler.pkl (StandardScaler)

# 3. Download both files
# Place in backend/ folder

# 4. Commit to GitHub
git add backend/model.pkl backend/scaler.pkl
git commit -m "Add serialized model files"
git push
```

## 🚢 Deployment Checklist

- [ ] Generated and saved `model.pkl` and `scaler.pkl`
- [ ] Updated API URL in `frontend/app.js` (for production)
- [ ] Created GitHub repository
- [ ] Pushed all files to GitHub
- [ ] Enabled GitHub Pages for frontend
- [ ] Deployed backend on Render/Railway
- [ ] Tested full-stack on production URLs
- [ ] Updated backend URL in frontend (if needed)

## 🐛 Troubleshooting

### Q: Model not loading?
A: Ensure `model.pkl` and `scaler.pkl` exist in backend folder. Check logs with `python app.py`.

### Q: Frontend can't connect to backend?
A: Verify API_BASE_URL in app.js matches your backend URL. Check CORS in browser console.

### Q: Predictions look wrong?
A: Ensure input validation passes. Check model performance metrics at `/api/model-info`.

### Q: Port already in use?
A: Change port in app.py or kill existing process: `lsof -ti:5000 | xargs kill -9`

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [scikit-learn Guide](https://scikit-learn.org/)
- [API Design Best Practices](https://restfulapi.net/)
- [Render Deployment](https://render.com/docs)
- [GitHub Pages Hosting](https://pages.github.com/)

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Add more meteorological features
- Try ensemble models (XGBoost, LightGBM)
- Add historical data visualization
- Implement time-series forecasting
- Add WebSocket for real-time predictions
- Create mobile app

## 📄 License

MIT License - Feel free to use this project for learning and deployment.

## 👤 Author

**Your Name** - Engineering Student | Cybersecurity Enthusiast | ML Developer

- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your Profile]
- Portfolio: [Your Website]

## 🙏 Acknowledgments

- Dataset: UCI Wind Power Dataset
- Framework: Flask & scikit-learn communities
- Inspiration: Renewable energy research

---

**Stars and forks appreciated!** ⭐

For questions or issues, open a GitHub issue or contact me directly.