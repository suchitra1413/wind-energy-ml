# LOAD MODEL FROM GOOGLE DRIVE - COMPLETE SETUP GUIDE

## ✅ **YES, THIS IS PERFECTLY POSSIBLE!**

Your model.pkl and scaler.pkl files stay on Google Drive, and your Flask backend downloads them when needed. Perfect for large files!

---

## 🎯 **STEP-BY-STEP SETUP**

### **Step 1: Get Your Google Drive File IDs**

1. **Upload model.pkl to Google Drive:**
   - Go to Google Drive
   - Upload `model.pkl` file
   - Right-click → Share → Get link
   - Extract File ID from URL:
   ```
   https://drive.google.com/file/d/FILE_ID_HERE/view?usp=sharing
                              ^^^^^^^^^^^^^^^^
   ```

2. **Do the same for scaler.pkl**

3. **Make both files PUBLICLY SHARED** (important for download):
   - Right-click file → Share
   - Change to "Anyone with the link"

---

### **Step 2: Update model_loader.py**

Replace the placeholder IDs:

```python
# In model_loader.py, line 13-14:

MODEL_FILE_ID = 'YOUR_ACTUAL_MODEL_FILE_ID'      # Replace this
SCALER_FILE_ID = 'YOUR_ACTUAL_SCALER_FILE_ID'    # Replace this
```

Example:
```python
MODEL_FILE_ID = '1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p'
SCALER_FILE_ID = '9z8y7x6w5v4u3t2s1r0q9p8o7n6m5l4k'
```

---

### **Step 3: Update requirements.txt**

Add this line:
```
gdown==4.7.1
```

Your complete requirements.txt should have:
```
flask==2.3.3
flask-cors==4.0.0
pandas==2.1.1
numpy==1.24.3
scikit-learn==1.3.1
joblib==1.3.2
gdown==4.7.1
python-dotenv==1.0.0
gunicorn==21.2.0
```

---

### **Step 4: Replace app.py**

Replace your `app.py` with `app-with-drive.py`:
```bash
# Rename the new file
mv app-with-drive.py app.py
```

---

### **Step 5: Test Locally**

```bash
# Terminal 1: Start Backend
cd backend
pip install -r requirements.txt
python app.py
```

**First time will be SLOW** (downloading 3GB+ from Drive), but after that it will be cached locally!

Output will show:
```
Loading model and scaler from Google Drive...
📥 Downloading model.pkl from Google Drive...
✅ Model downloaded successfully
📥 Downloading scaler.pkl from Google Drive...
✅ Scaler downloaded successfully
✅ Model and scaler loaded successfully!
Running on http://0.0.0.0:5000
```

---

### **Step 6: Test Frontend**

In another terminal:
```bash
# Terminal 2: Start Frontend
cd frontend
python -m http.server 8000
```

Visit: `http://localhost:8000`

Make a prediction - it should work! ✅

---

## 🚀 **FOR PRODUCTION (Render.com, Railway, etc.)**

### **Deploy to Render:**

1. Push all files to GitHub (including model_loader.py and updated requirements.txt)
2. Create new Web Service on Render.com
3. Settings same as before:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`

4. **On first startup**, Render will download model + scaler from Google Drive (takes 5-10 minutes for 3GB)
5. After that, it's cached and runs fast!

### **Environment Variables (Optional):**
If you want to use different Drive IDs per environment:
```bash
# In Render dashboard, add:
MODEL_FILE_ID = your_id
SCALER_FILE_ID = your_id
```

Then update model_loader.py:
```python
import os
MODEL_FILE_ID = os.getenv('MODEL_FILE_ID', 'default_id')
SCALER_FILE_ID = os.getenv('SCALER_FILE_ID', 'default_id')
```

---

## ⚙️ **HOW IT WORKS**

1. **First Request:**
   - Flask app starts
   - Calls `get_model_and_scaler()`
   - `model_loader.py` downloads files from Google Drive
   - Saves to `/tmp/ml_models/` (temporary disk)
   - Uses for all predictions

2. **Subsequent Requests:**
   - Files already in `/tmp/`
   - No re-download needed
   - Fast predictions!

3. **Server Restart:**
   - `/tmp/` cleared on cloud restart
   - Re-downloads from Drive (but cached locally until restart)

---

## 📊 **FILE STRUCTURE**

```
backend/
├── app.py                 ← Updated Flask app (calls model_loader)
├── model_loader.py        ← NEW: Loads from Google Drive
├── requirements.txt       ← Updated with gdown
├── Procfile
└── runtime.txt
```

**No need for model.pkl or scaler.pkl in backend folder!** ✅

---

## 🔍 **TROUBLESHOOTING**

### **"File not found" Error:**
- Check Google Drive File ID is correct
- Make sure file is shared publicly ("Anyone with link")

### **Download Timeout (3GB+ file):**
- Normal on slow internet
- Takes 5-10 minutes first time
- Cloud servers download quickly (usually <2 minutes)

### **Cache Not Working:**
- `/tmp/` is automatically cleared on server restart
- First request after restart will re-download
- This is expected behavior

### **Test Without Render:**
```python
# In model_loader.py, test locally:
if __name__ == "__main__":
    model, scaler = get_model_and_scaler()
    print("Success!")
```

---

## ✨ **ADVANTAGES OF THIS APPROACH**

✅ No need to store 3GB files locally
✅ Works with GitHub (no file size limits)
✅ Works with Render/Railway/Heroku
✅ Models stay on Google Drive (centralized)
✅ Easy to update model - just re-upload to Drive
✅ Multiple versions can be kept on Drive

---

## 🎉 **YOU'RE ALL SET!**

This solution is **production-ready** and used by many ML engineers for deployment with large models!

**Do you need help with:**
1. Finding your Google Drive File IDs?
2. Setting up on Render/Railway?
3. Anything else?

Let me know! 🚀