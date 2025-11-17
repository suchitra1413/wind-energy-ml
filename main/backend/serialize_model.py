"""
Model Serialization Script
Generate model.pkl and scaler.pkl from your Jupyter notebook
Run this in your Colab environment AFTER training the model
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# ============================================
# LOAD AND PREPROCESS DATA
# ============================================

# Update these paths to match your data location
train_path = '/content/drive/MyDrive/Train.csv'
test_path = '/content/drive/MyDrive/Test.csv'

train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

# Remove index column
train_df = train_df.drop(columns=['Unnamed: 0'])

# Handle missing values
train_df = train_df.fillna(train_df.mean(numeric_only=True))
test_df = test_df.fillna(test_df.mean(numeric_only=True))

# Encode categorical columns
label_enc = LabelEncoder()
for col in train_df.select_dtypes(include=['object']).columns:
    if col != 'Time':  # Don't encode Time column yet
        combined = pd.concat([train_df[col], test_df[col]], axis=0)
        label_enc.fit(combined.astype(str))
        train_df[col] = label_enc.transform(train_df[col].astype(str))
        test_df[col] = label_enc.transform(test_df[col].astype(str))

# ============================================
# FEATURE ENGINEERING
# ============================================

train_df['Time'] = pd.to_datetime(train_df['Time'], format="%d-%m-%Y %H:%M")

# Time features
train_df['hour'] = train_df['Time'].dt.hour
train_df['day'] = train_df['Time'].dt.day
train_df['month'] = train_df['Time'].dt.month
train_df['dayofweek'] = train_df['Time'].dt.dayofweek
train_df['is_weekend'] = train_df['dayofweek'].isin([5, 6]).astype(int)

# Circular wind direction encoding
for col in ['WD_10m', 'WD_100m']:
    train_df[col+'_sin'] = np.sin(np.deg2rad(train_df[col]))
    train_df[col+'_cos'] = np.cos(np.deg2rad(train_df[col]))

# Polynomial wind speed features
for col in ['WS_10m', 'WS_100m']:
    train_df[col+'_sq'] = train_df[col]**2
    train_df[col+'_cu'] = train_df[col]**3

# Interaction features
train_df['temp_humidity'] = train_df['Temp_2m'] * train_df['RelHum_2m']
train_df['temp_dew_diff'] = train_df['Temp_2m'] - train_df['DP_2m']
train_df['wind_shear'] = train_df['WS_100m'] - train_df['WS_10m']

# ============================================
# PREPARE DATA FOR TRAINING
# ============================================

X = train_df.drop(columns=['Power', 'Time'])
y = train_df['Power']

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ============================================
# TRAIN MODEL
# ============================================

print("Training Random Forest Model...")
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

model.fit(X_scaled, y)

print("✅ Model training completed!")

# ============================================
# SAVE MODEL AND SCALER
# ============================================

# Save to Google Drive for download
model_path = '/content/drive/MyDrive/model.pkl'
scaler_path = '/content/drive/MyDrive/scaler.pkl'

joblib.dump(model, model_path)
joblib.dump(scaler, scaler_path)

print(f"✅ Model saved to: {model_path}")
print(f"✅ Scaler saved to: {scaler_path}")

# Verify files
import os
print(f"\nModel file size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
print(f"Scaler file size: {os.path.getsize(scaler_path) / (1024):.2f} KB")

print("\n✨ Now download these files and place them in your backend folder!")