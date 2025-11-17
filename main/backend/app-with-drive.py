"""
Wind Power Prediction - Flask Backend with Google Drive Model Loading
=====================================================================
Uses model_loader.py to load model.pkl and scaler.pkl from Google Drive
No need to store large files locally!
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from model_loader import get_model_and_scaler
import logging
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and scaler
model = None
scaler = None

# ============================================
# INITIALIZATION
# ============================================

def init_app():
    """Initialize app - load model and scaler from Google Drive"""
    global model, scaler
    
    try:
        logger.info("Loading model and scaler from Google Drive...")
        model, scaler = get_model_and_scaler()
        logger.info("✅ Model and scaler loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        return False

# ============================================
# HEALTH CHECK
# ============================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API and model are healthy"""
    model_loaded = model is not None and scaler is not None
    
    return jsonify({
        'status': 'healthy' if model_loaded else 'unhealthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': model_loaded,
        'version': '1.0.0',
        'message': 'Model loaded from Google Drive' if model_loaded else 'Model not loaded'
    }), 200 if model_loaded else 503

# ============================================
# PREDICTION ENDPOINT
# ============================================

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Make prediction with meteorological data
    
    Expected JSON:
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
    
    if model is None or scaler is None:
        return jsonify({
            'error': 'Model not loaded. Please check server logs.',
            'status': 'error'
        }), 503
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Required fields
        required_fields = [
            'Location', 'Temp_2m', 'RelHum_2m', 'DP_2m',
            'WS_10m', 'WS_100m', 'WD_10m', 'WD_100m', 'WG_10m',
            'hour', 'day', 'month', 'dayofweek', 'is_weekend'
        ]
        
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400
        
        # Create DataFrame
        input_df = pd.DataFrame([data])
        
        # Feature Engineering
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
        
        # Select features in correct order
        feature_list = [
            'Location', 'Temp_2m', 'RelHum_2m', 'DP_2m',
            'WS_10m', 'WS_100m', 'WD_10m', 'WD_100m', 'WG_10m',
            'hour', 'day', 'month', 'dayofweek', 'is_weekend',
            'WD_10m_sin', 'WD_10m_cos', 'WD_100m_sin', 'WD_100m_cos',
            'WS_10m_sq', 'WS_10m_cu', 'WS_100m_sq', 'WS_100m_cu',
            'temp_humidity', 'temp_dew_diff', 'wind_shear'
        ]
        
        X = input_df[feature_list]
        X_scaled = scaler.transform(X)
        
        # Make prediction
        prediction = float(model.predict(X_scaled)[0])
        prediction = np.clip(prediction, 0.0, 1.0)
        
        logger.info(f"Prediction: {prediction:.4f}")
        
        return jsonify({
            'prediction': prediction,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'message': f'Predicted wind power: {prediction:.4f}'
        }), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

# ============================================
# MODEL INFO
# ============================================

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model details"""
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
        'output_type': 'Normalized Power (0-1)',
        'data_source': 'Google Drive'
    }), 200

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
    print("\n" + "="*60)
    print("Wind Power Prediction - Flask Backend")
    print("Loading model from Google Drive...")
    print("="*60 + "\n")
    
    if init_app():
        print("\n✅ Starting Flask server...\n")
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
    else:
        print("\n❌ Failed to initialize app. Check model files on Google Drive.")
        exit(1)
