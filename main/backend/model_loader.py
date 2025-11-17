"""
model_loader.py
===============
Loads model.pkl and scaler.pkl from Google Drive instead of local filesystem
Perfect for large files (>3GB) that can't be stored on GitHub/Render
"""

import gdown
import joblib
import os
from functools import lru_cache

# ============================================
# GOOGLE DRIVE FILE IDS
# ============================================
# Replace these with your actual Google Drive file IDs

MODEL_FILE_ID = 'YOUR_MODEL_PKL_FILE_ID_HERE'
SCALER_FILE_ID = 'YOUR_SCALER_PKL_FILE_ID_HERE'

# Download destination (temp folder)
CACHE_DIR = '/tmp/ml_models'
MODEL_CACHE_PATH = os.path.join(CACHE_DIR, 'model.pkl')
SCALER_CACHE_PATH = os.path.join(CACHE_DIR, 'scaler.pkl')

# ============================================
# ENSURE CACHE DIRECTORY EXISTS
# ============================================
os.makedirs(CACHE_DIR, exist_ok=True)

# ============================================
# DOWNLOAD FROM GOOGLE DRIVE
# ============================================

def download_model_from_drive():
    """Download model.pkl from Google Drive if not cached"""
    if os.path.exists(MODEL_CACHE_PATH):
        print("✅ Model already cached locally")
        return True
    
    print("📥 Downloading model.pkl from Google Drive...")
    try:
        url = f'https://drive.google.com/uc?id={MODEL_FILE_ID}'
        gdown.download(url, MODEL_CACHE_PATH, quiet=False)
        print("✅ Model downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

def download_scaler_from_drive():
    """Download scaler.pkl from Google Drive if not cached"""
    if os.path.exists(SCALER_CACHE_PATH):
        print("✅ Scaler already cached locally")
        return True
    
    print("📥 Downloading scaler.pkl from Google Drive...")
    try:
        url = f'https://drive.google.com/uc?id={SCALER_FILE_ID}'
        gdown.download(url, SCALER_CACHE_PATH, quiet=False)
        print("✅ Scaler downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error downloading scaler: {e}")
        return False

# ============================================
# LOAD MODEL & SCALER (CACHED)
# ============================================

@lru_cache(maxsize=1)
def load_model():
    """Load model from cache or download from Drive"""
    if not os.path.exists(MODEL_CACHE_PATH):
        if not download_model_from_drive():
            raise RuntimeError("Failed to load model from Google Drive")
    
    print(f"Loading model from: {MODEL_CACHE_PATH}")
    model = joblib.load(MODEL_CACHE_PATH)
    return model

@lru_cache(maxsize=1)
def load_scaler():
    """Load scaler from cache or download from Drive"""
    if not os.path.exists(SCALER_CACHE_PATH):
        if not download_scaler_from_drive():
            raise RuntimeError("Failed to load scaler from Google Drive")
    
    print(f"Loading scaler from: {SCALER_CACHE_PATH}")
    scaler = joblib.load(SCALER_CACHE_PATH)
    return scaler

# ============================================
# UTILITY FUNCTIONS
# ============================================

def get_model_and_scaler():
    """Get both model and scaler in one call"""
    model = load_model()
    scaler = load_scaler()
    return model, scaler

def clear_cache():
    """Clear local cache (useful for testing)"""
    if os.path.exists(MODEL_CACHE_PATH):
        os.remove(MODEL_CACHE_PATH)
    if os.path.exists(SCALER_CACHE_PATH):
        os.remove(SCALER_CACHE_PATH)
    print("✅ Cache cleared")

# ============================================
# TEST FUNCTION
# ============================================

if __name__ == "__main__":
    print("Testing model loader...\n")
    
    try:
        model, scaler = get_model_and_scaler()
        print("\n✅ Successfully loaded model and scaler from Google Drive!")
        print(f"Model type: {type(model)}")
        print(f"Scaler type: {type(scaler)}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
