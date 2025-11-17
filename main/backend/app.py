"""
Wind Power Prediction - Flask Backend API
==========================================
Server: Flask (lightweight, free, open-source)
Model: Random Forest Regressor
Features: 13 input parameters
Output: Normalized power prediction (0-1)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import logging
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# GLOBAL VARIABLES
# ============================================

model = None
scaler = None
feature_columns = None

# ============================================
# INITIALIZATION
# ============================================

def load_model():
    """Load pre-trained model and scaler"""
    global model, scaler
    
    try:
        # Load model
        model = joblib.load('model.pkl')
        logger.info("✅ Model loaded successfully")
        
        # Load scaler
        scaler = joblib.load('scaler.pkl')
        logger.info("✅ Scaler loaded successfully")
        
    except FileNotFoundError as e:
        logger.error(f"❌ Error loading model: {e}")
        logger.warning("Running in DEMO mode - predictions will be simulated")
        model = None
        scaler = None

def init_app():
    """Initialize application"""
    load_model()

# ============================================
# HEALTH CHECK ENDPOINT
# ============================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check API and model status"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': model is not None,
        'version': '1.0.0'
    }), 200

# ============================================
# PREDICTION ENDPOINT
# ============================================

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Make wind power prediction
    
    Expected JSON input:
    {
        "Location": int,
        "Temp_2m": float,
        "RelHum_2m": float,
        "DP_2m": float,
        "WS_10m": float,
        "WS_100m": float,
        "WD_10m": float,
        "WD_100m": float,
        "WG_10m": float,
        "hour": int,
        "day": int,
        "month": int,
        "dayofweek": int,
        "is_weekend": int
    }
    """
    
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = [
            'Location', 'Temp_2m', 'RelHum_2m', 'DP_2m',
            'WS_10m', 'WS_100m', 'WD_10m', 'WD_100m', 'WG_10m',
            'hour', 'day', 'month', 'dayofweek', 'is_weekend'
        ]
        
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing fields: {", ".join(missing_fields)}'
            }), 400
        
        # Create DataFrame for model
        input_df = pd.DataFrame([data])
        
        # Feature engineering (circular encoding for wind direction)
        input_df['WD_10m_sin'] = np.sin(np.deg2rad(input_df['WD_10m']))
        input_df['WD_10m_cos'] = np.cos(np.deg2rad(input_df['WD_10m']))
        input_df['WD_100m_sin'] = np.sin(np.deg2rad(input_df['WD_100m']))
        input_df['WD_100m_cos'] = np.cos(np.deg2rad(input_df['WD_100m']))
        
        # Polynomial features for wind speed
        input_df['WS_10m_sq'] = input_df['WS_10m'] ** 2
        input_df['WS_10m_cu'] = input_df['WS_10m'] ** 3
        input_df['WS_100m_sq'] = input_df['WS_100m'] ** 2
        input_df['WS_100m_cu'] = input_df['WS_100m'] ** 3
        
        # Interaction features
        input_df['temp_humidity'] = input_df['Temp_2m'] * input_df['RelHum_2m']
        input_df['temp_dew_diff'] = input_df['Temp_2m'] - input_df['DP_2m']
        input_df['wind_shear'] = input_df['WS_100m'] - input_df['WS_10m']
        
        # Select features in order (should match training)
        feature_list = [
            'Location', 'Temp_2m', 'RelHum_2m', 'DP_2m',
            'WS_10m', 'WS_100m', 'WD_10m', 'WD_100m', 'WG_10m',
            'hour', 'day', 'month', 'dayofweek', 'is_weekend',
            'WD_10m_sin', 'WD_10m_cos', 'WD_100m_sin', 'WD_100m_cos',
            'WS_10m_sq', 'WS_10m_cu', 'WS_100m_sq', 'WS_100m_cu',
            'temp_humidity', 'temp_dew_diff', 'wind_shear'
        ]
        
        X = input_df[feature_list]
        
        # Scale features
        if scaler is not None:
            X_scaled = scaler.transform(X)
        else:
            X_scaled = X.values
        
        # Make prediction
        if model is not None:
            prediction = model.predict(X_scaled)[0]
        else:
            # Demo prediction based on wind speed (for testing)
            wind_speed = data['WS_10m']
            prediction = min(0.9, (wind_speed / 15) ** 1.5)  # Simulated
        
        # Ensure prediction is in valid range
        prediction = float(np.clip(prediction, 0.0, 1.0))
        
        logger.info(f"Prediction made: {prediction:.4f}")
        
        return jsonify({
            'prediction': prediction,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'message': f'Predicted wind power output: {prediction:.4f} (normalized 0-1)'
        }), 200
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

# ============================================
# MODEL INFO ENDPOINT
# ============================================

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    return jsonify({
        'model_name': 'Wind Power Prediction - Random Forest',
        'version': '1.0.0',
        'algorithm': 'Random Forest Regressor',
        'n_estimators': 300,
        'r2_score': 0.8272,
        'mae': 0.0737,
        'rmse': 0.1054,
        'input_features': 13,
        'training_samples': 140160,
        'output_type': 'Normalized Power (0-1)'
    }), 200

# ============================================
# BATCH PREDICTION ENDPOINT
# ============================================

@app.route('/api/predict-batch', methods=['POST'])
def predict_batch():
    """
    Make batch predictions for multiple samples
    Expects: List of prediction requests
    """
    
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({'error': 'Expected list of prediction objects'}), 400
        
        predictions = []
        for item in data:
            # Reuse single prediction logic
            input_df = pd.DataFrame([item])
            
            # Feature engineering
            input_df['WD_10m_sin'] = np.sin(np.deg2rad(input_df['WD_10m']))
            input_df['WD_10m_cos'] = np.cos(np.deg2rad(input_df['WD_10m']))
            input_df['WD_100m_sin'] = np.sin(np.deg2rad(input_df['WD_100m']))
            input_df['WD_100m_cos'] = np.cos(np.deg2rad(input_df['WD_100m']))
            
            input_df['WS_10m_sq'] = input_df['WS_10m'] ** 2
            input_df['WS_10m_cu'] = input_df['WS_10m'] ** 3
            input_df['WS_100m_sq'] = input_df['WS_100m'] ** 2
            input_df['WS_100m_cu'] = input_df['WS_100m'] ** 3
            
            input_df['temp_humidity'] = input_df['Temp_2m'] * input_df['RelHum_2m']
            input_df['temp_dew_diff'] = input_df['Temp_2m'] - input_df['DP_2m']
            input_df['wind_shear'] = input_df['WS_100m'] - input_df['WS_10m']
            
            feature_list = [
                'Location', 'Temp_2m', 'RelHum_2m', 'DP_2m',
                'WS_10m', 'WS_100m', 'WD_10m', 'WD_100m', 'WG_10m',
                'hour', 'day', 'month', 'dayofweek', 'is_weekend',
                'WD_10m_sin', 'WD_10m_cos', 'WD_100m_sin', 'WD_100m_cos',
                'WS_10m_sq', 'WS_10m_cu', 'WS_100m_sq', 'WS_100m_cu',
                'temp_humidity', 'temp_dew_diff', 'wind_shear'
            ]
            
            X = input_df[feature_list]
            
            if scaler is not None:
                X_scaled = scaler.transform(X)
            else:
                X_scaled = X.values
            
            if model is not None:
                pred = model.predict(X_scaled)[0]
            else:
                wind_speed = item['WS_10m']
                pred = min(0.9, (wind_speed / 15) ** 1.5)
            
            predictions.append(float(np.clip(pred, 0.0, 1.0)))
        
        logger.info(f"Batch prediction made for {len(predictions)} samples")
        
        return jsonify({
            'predictions': predictions,
            'count': len(predictions),
            'status': 'success'
        }), 200
        
    except Exception as e:
        logger.error(f"Error during batch prediction: {str(e)}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    init_app()
    
    # Development server (change to False for production)
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )