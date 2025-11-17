# Wind Power Prediction - API Documentation

## Overview

Complete REST API documentation for the Wind Power Prediction ML model backend.

**Base URL:** `https://your-backend-domain.com/api` (production) or `http://localhost:5000/api` (local)

---

## 1. Health Check Endpoint

Check if the API and model are running correctly.

### Request
```http
GET /api/health
```

### Response (200 OK)
```json
{
  "status": "healthy",
  "timestamp": "2025-11-16T17:30:00.000Z",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### Errors
- **503 Service Unavailable:** Model not loaded or service down

---

## 2. Single Prediction Endpoint

Predict wind power output for a single meteorological observation.

### Request
```http
POST /api/predict
Content-Type: application/json

{
  "Location": 1,
  "Temp_2m": 25.5,
  "RelHum_2m": 65.0,
  "DP_2m": 18.2,
  "WS_10m": 5.2,
  "WS_100m": 8.5,
  "WD_10m": 180.0,
  "WD_100m": 195.0,
  "WG_10m": 3.2,
  "hour": 14,
  "day": 15,
  "month": 6,
  "dayofweek": 2,
  "is_weekend": 0
}
```

### Request Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| Location | int | 1-N | Location identifier |
| Temp_2m | float | -50 to 50 | Temperature at 2m (°C) |
| RelHum_2m | float | 0-100 | Relative humidity at 2m (%) |
| DP_2m | float | -50 to 50 | Dew point temperature (°C) |
| WS_10m | float | 0-30 | Wind speed at 10m (m/s) |
| WS_100m | float | 0-40 | Wind speed at 100m (m/s) |
| WD_10m | float | 0-360 | Wind direction at 10m (degrees) |
| WD_100m | float | 0-360 | Wind direction at 100m (degrees) |
| WG_10m | float | 0-20 | Wind gust at 10m (m/s) |
| hour | int | 0-23 | Hour of day (24-hour format) |
| day | int | 1-31 | Day of month |
| month | int | 1-12 | Month of year |
| dayofweek | int | 0-6 | Day of week (0=Monday, 6=Sunday) |
| is_weekend | int | 0-1 | 0=Weekday, 1=Weekend |

### Response (200 OK)
```json
{
  "prediction": 0.7234,
  "status": "success",
  "timestamp": "2025-11-16T17:30:15.000Z",
  "message": "Predicted wind power output: 0.7234 (normalized 0-1)"
}
```

### Response Fields
- **prediction** (float): Normalized power output (0-1)
  - 0.0 = No wind power generated
  - 0.5 = 50% of maximum power
  - 1.0 = Maximum power output
- **status** (string): "success" or "error"
- **timestamp** (string): ISO 8601 timestamp
- **message** (string): Human-readable description

### Errors
```json
{
  "error": "Missing fields: WS_10m, WS_100m",
  "status": "error"
}
```

Error codes:
- **400 Bad Request:** Missing or invalid fields
- **422 Unprocessable Entity:** Invalid data types or ranges
- **500 Internal Server Error:** Model prediction error

---

## 3. Model Information Endpoint

Get details about the trained ML model.

### Request
```http
GET /api/model-info
```

### Response (200 OK)
```json
{
  "model_name": "Wind Power Prediction - Random Forest",
  "version": "1.0.0",
  "algorithm": "Random Forest Regressor",
  "n_estimators": 300,
  "r2_score": 0.8272,
  "mae": 0.0737,
  "rmse": 0.1054,
  "input_features": 13,
  "training_samples": 140160,
  "output_type": "Normalized Power (0-1)"
}
```

### Model Performance Metrics
- **R² Score:** 82.72% - Variance explained by the model
- **MAE:** 0.0737 - Average absolute prediction error
- **RMSE:** 0.1054 - Root mean squared error

---

## 4. Batch Prediction Endpoint

Predict wind power for multiple observations in one request.

### Request
```http
POST /api/predict-batch
Content-Type: application/json

[
  {
    "Location": 1,
    "Temp_2m": 25.5,
    "RelHum_2m": 65.0,
    "DP_2m": 18.2,
    "WS_10m": 5.2,
    "WS_100m": 8.5,
    "WD_10m": 180.0,
    "WD_100m": 195.0,
    "WG_10m": 3.2,
    "hour": 14,
    "day": 15,
    "month": 6,
    "dayofweek": 2,
    "is_weekend": 0
  },
  {
    "Location": 1,
    "Temp_2m": 22.3,
    "RelHum_2m": 72.0,
    ...
  }
]
```

### Response (200 OK)
```json
{
  "predictions": [0.7234, 0.5621, 0.8901],
  "count": 3,
  "status": "success"
}
```

### Errors
```json
{
  "error": "Expected list of prediction objects",
  "status": "error"
}
```

Error codes:
- **400 Bad Request:** Not a list or invalid format
- **500 Internal Server Error:** Processing error

---

## HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Prediction made |
| 400 | Bad Request | Missing required fields |
| 404 | Not Found | Invalid endpoint |
| 500 | Server Error | Model loading failed |

---

## Example Usage

### JavaScript/Fetch
```javascript
const response = await fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    Location: 1,
    Temp_2m: 25.5,
    RelHum_2m: 65,
    DP_2m: 18.2,
    WS_10m: 5.2,
    WS_100m: 8.5,
    WD_10m: 180,
    WD_100m: 195,
    WG_10m: 3.2,
    hour: 14,
    day: 15,
    month: 6,
    dayofweek: 2,
    is_weekend: 0
  })
});

const result = await response.json();
console.log(result.prediction); // 0.7234
```

### Python/Requests
```python
import requests

url = 'http://localhost:5000/api/predict'
data = {
    'Location': 1,
    'Temp_2m': 25.5,
    'RelHum_2m': 65,
    # ... other parameters
}

response = requests.post(url, json=data)
prediction = response.json()['prediction']
print(f"Predicted Power: {prediction}")
```

### cURL
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## Rate Limiting

Currently no rate limiting. For production, consider:
- Implementing request throttling (Flask-Limiter)
- Adding API keys for authentication
- Setting max requests per minute/hour

---

## CORS Configuration

The API accepts requests from all origins (`*`). For production, restrict to specific domains:

```python
CORS(app, resources={r"/api/*": {"origins": ["https://yourdomain.com"]}})
```

---

## Error Response Format

All errors follow this format:

```json
{
  "error": "Error description",
  "status": "error",
  "timestamp": "2025-11-16T17:30:15.000Z"
}
```

---

## Feature Engineering Details

Input parameters are automatically transformed:

1. **Circular Encoding (Wind Direction)**
   - WD_10m → sin(WD_10m), cos(WD_10m)
   - WD_100m → sin(WD_100m), cos(WD_100m)

2. **Polynomial Features (Wind Speed)**
   - WS_10m → WS_10m², WS_10m³
   - WS_100m → WS_100m², WS_100m³

3. **Interaction Features**
   - temp_humidity = Temp_2m × RelHum_2m
   - temp_dew_diff = Temp_2m - DP_2m
   - wind_shear = WS_100m - WS_10m

Total input to model: **25 features**

---

## Performance Characteristics

- **Average Response Time:** 50-150ms
- **Model Inference Time:** <100ms
- **Throughput:** ~100-200 predictions/second
- **Concurrent Connections:** Depends on server configuration

---

## Support

For issues or questions:
1. Check the README.md
2. Review DEPLOYMENT_GUIDE.md
3. Open GitHub issue
4. Contact: your-email@example.com