"""
Wind Power Prediction - Backend Configuration & Utils
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Flask Configuration
DEBUG = os.getenv('FLASK_DEBUG', False)
TESTING = False
ENV = os.getenv('FLASK_ENV', 'production')

# API Configuration
API_TITLE = 'Wind Power Prediction API'
API_VERSION = '1.0.0'
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 5000))

# Model Configuration
MODEL_PATH = os.getenv('MODEL_PATH', 'model.pkl')
SCALER_PATH = os.getenv('SCALER_PATH', 'scaler.pkl')

# CORS Configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/api.log')

print(f"Flask App Configuration Loaded")
print(f"Environment: {ENV}")
print(f"Debug Mode: {DEBUG}")