# Wind Power Prediction - Frontend & Backend Deployment Guide

## Project Structure

```
wind-power-prediction/
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── assets/
│       └── (images, icons)
│
├── backend/
│   ├── app.py
│   ├── serialize_model.py
│   ├── model.pkl (generate from notebook)
│   ├── scaler.pkl (generate from notebook)
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   └── .env
│
├── model/
│   └── Wind-Power-Prediction.ipynb
│
├── .gitignore
└── README.md
```

## Step 1: Prepare Your Model Files

### A. Export Model from Jupyter Notebook

1. **Run serialize_model.py in your Colab environment:**
   ```python
   # Copy the content from serialize_model.py
   # Run in Colab cell after training
   exec(open('/path/to/serialize_model.py').read())
   ```

2. **Download the generated files:**
   - `model.pkl` (Random Forest Regressor)
   - `scaler.pkl` (StandardScaler)
   
3. **Place these files in backend folder**

## Step 2: Setup Backend Locally

### A. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### B. Create .env file (optional)

```bash
# backend/.env
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000
```

### C. Test Backend Locally

```bash
python app.py
```

Visit: `http://localhost:5000/api/health`

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

## Step 3: Setup Frontend Locally

### A. Update API URL (if needed)

In `frontend/app.js`, update:
```javascript
const API_BASE_URL = 'http://localhost:5000/api'; // Local
// OR for production
const API_BASE_URL = 'https://your-backend-domain.com/api';
```

### B. Run Frontend

**Option 1: Simple HTTP Server**
```bash
cd frontend
python -m http.server 8000
```
Visit: `http://localhost:8000`

**Option 2: Live Server (VS Code)**
- Install "Live Server" extension
- Right-click index.html → "Open with Live Server"

## Step 4: Deploy to GitHub

### A. Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit: Wind Power Prediction app"
```

### B. Create GitHub Repository

1. Go to github.com and create new repository
2. Name: `wind-power-prediction`
3. Make it PUBLIC

### C. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/wind-power-prediction.git
git branch -M main
git push -u origin main
```

## Step 5: Deploy Frontend on GitHub Pages

### A. Enable GitHub Pages

1. Go to repository Settings
2. Navigate to "Pages" section
3. Set source to "Deploy from a branch"
4. Select branch: `main`
5. Select folder: `frontend` (or root)
6. Save

**Frontend will be live at:** `https://YOUR_USERNAME.github.io/wind-power-prediction/`

## Step 6: Deploy Backend (Choose One Option)

### Option A: Deploy on Render.com (Free, Recommended)

1. **Sign up at render.com**
2. **Create new Web Service**
   - Repository: Your GitHub repo
   - Branch: main
   - Runtime: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`

3. **Add Environment Variables** (if needed)
   - FLASK_ENV=production

4. **Deploy**

**Backend URL:** `https://your-service-name.onrender.com`

### Option B: Deploy on Railway.app (Free, No Credit Card)

1. **Sign up at railway.app**
2. **Create new project**
   - Connect GitHub repository
   - Select wind-power-prediction repo

3. **Configure**
   - Root Directory: `backend`
   - Add Procfile

4. **Deploy**

### Option C: Deploy on Heroku (Paid, but most reliable)

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Set buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

## Step 7: Update Frontend API URL

After backend deployment, update `frontend/app.js`:

```javascript
const API_BASE_URL = 'https://your-backend-url.com/api';
```

Then commit and push:
```bash
git add frontend/app.js
git commit -m "Update backend API URL for production"
git push origin main
```

## Step 8: Test Full Stack

1. **Visit Frontend:** https://YOUR_USERNAME.github.io/wind-power-prediction/
2. **Make a prediction** with sample data
3. **Check network tab** to verify API calls
4. **See predictions** from backend

## API Endpoints

### Health Check
```
GET /api/health
```

### Single Prediction
```
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
```

### Model Info
```
GET /api/model-info
```

### Batch Prediction
```
POST /api/predict-batch
Content-Type: application/json

[
  { /* prediction 1 */ },
  { /* prediction 2 */ },
  ...
]
```

## Troubleshooting

### Frontend not connecting to backend?
- Check CORS settings in `app.py` (already enabled)
- Verify API_BASE_URL in `app.js`
- Check browser console for errors

### Model not loading?
- Ensure `model.pkl` and `scaler.pkl` in backend folder
- Check file paths in `app.py`
- See logs for specific errors

### CORS errors?
Already handled with `CORS(app)` in app.py

### Port already in use?
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
python app.py --port 5001
```

## Performance Notes

- **Model Size:** ~50-100 MB (depending on trees)
- **Prediction Time:** <100ms
- **Concurrent Users:** Limited by backend service tier
- **Frontend:** Static files, instant loading

## Security Considerations

- Disable debug mode in production: `app.run(debug=False)`
- Add input validation (already in frontend)
- Use HTTPS in production (automatic on Render/Railway)
- Add rate limiting for production (optional)

## Next Steps

1. ✅ Set up local development
2. ✅ Deploy to GitHub
3. ✅ Deploy frontend on GitHub Pages
4. ✅ Deploy backend on Render/Railway
5. 📊 Monitor predictions and logs
6. 🔄 Iterate and improve model

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Render Deployment](https://render.com/docs)
- [GitHub Pages](https://pages.github.com/)
- [CORS Explained](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)