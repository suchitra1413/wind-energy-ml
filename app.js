// ============================================
// WIND POWER PREDICTION - FRONTEND APP.JS
// ============================================

const API_BASE_URL = 'http://localhost:5000/api'; // Change for production

// ============================================
// FORM SUBMISSION HANDLER
// ============================================

document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading state
    showLoading();
    
    try {
        // Collect form data
        const formData = {
            Location: parseInt(document.getElementById('location').value),
            Temp_2m: parseFloat(document.getElementById('temp_2m').value),
            RelHum_2m: parseFloat(document.getElementById('relhum_2m').value),
            DP_2m: parseFloat(document.getElementById('dp_2m').value),
            WS_10m: parseFloat(document.getElementById('ws_10m').value),
            WS_100m: parseFloat(document.getElementById('ws_100m').value),
            WD_10m: parseFloat(document.getElementById('wd_10m').value),
            WD_100m: parseFloat(document.getElementById('wd_100m').value),
            WG_10m: parseFloat(document.getElementById('wg_10m').value),
            hour: parseInt(document.getElementById('hour').value),
            day: parseInt(document.getElementById('day').value),
            month: parseInt(document.getElementById('month').value),
            dayofweek: parseInt(document.getElementById('dayofweek').value),
            is_weekend: parseInt(document.getElementById('is_weekend').value)
        };

        // Validate data
        validateInputData(formData);

        // Make API call to backend
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        const result = await response.json();

        // Display results
        displayResults(result.prediction, formData);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to get prediction. Please check your input and try again.');
    } finally {
        hideLoading();
    }
});

// ============================================
// VALIDATION FUNCTION
// ============================================

function validateInputData(data) {
    const errors = [];

    if (data.RelHum_2m < 0 || data.RelHum_2m > 100) {
        errors.push('Relative Humidity must be between 0-100%');
    }

    if (data.WD_10m < 0 || data.WD_10m > 360) {
        errors.push('Wind Direction at 10m must be between 0-360°');
    }

    if (data.WD_100m < 0 || data.WD_100m > 360) {
        errors.push('Wind Direction at 100m must be between 0-360°');
    }

    if (data.hour < 0 || data.hour > 23) {
        errors.push('Hour must be between 0-23');
    }

    if (data.day < 1 || data.day > 31) {
        errors.push('Day must be between 1-31');
    }

    if (data.month < 1 || data.month > 12) {
        errors.push('Month must be between 1-12');
    }

    if (data.dayofweek < 0 || data.dayofweek > 6) {
        errors.push('Day of week must be between 0-6');
    }

    if (errors.length > 0) {
        throw new Error(errors.join('\n'));
    }
}

// ============================================
// DISPLAY RESULTS
// ============================================

function displayResults(prediction, inputData) {
    const resultContainer = document.getElementById('resultContainer');
    const predictedPowerEl = document.getElementById('predictedPower');
    const powerStatusEl = document.getElementById('powerStatus');
    const powerFillEl = document.getElementById('powerFill');
    const percentTextEl = document.getElementById('percentText');

    // Ensure prediction is between 0 and 1
    const normalizedPrediction = Math.max(0, Math.min(1, parseFloat(prediction)));
    const percentage = (normalizedPrediction * 100).toFixed(2);

    // Display predicted power
    predictedPowerEl.textContent = normalizedPrediction.toFixed(4);
    percentTextEl.textContent = percentage + '%';

    // Update power bar visualization
    powerFillEl.style.width = percentage + '%';
    powerFillEl.textContent = percentage + '%';

    // Determine power status
    let status, statusClass;
    if (normalizedPrediction < 0.33) {
        status = '🔴 LOW - Minimal Power Generation';
        statusClass = 'low';
    } else if (normalizedPrediction < 0.66) {
        status = '🟡 MEDIUM - Moderate Power Generation';
        statusClass = 'medium';
    } else {
        status = '🟢 HIGH - Strong Power Generation';
        statusClass = 'high';
    }

    powerStatusEl.textContent = status;
    powerStatusEl.className = `status ${statusClass}`;

    // Hide other panels and show results
    document.getElementById('loadingSpinner').classList.add('hidden');
    document.getElementById('errorContainer').classList.add('hidden');
    resultContainer.classList.remove('hidden');

    // Log prediction details
    console.log('Prediction Details:', {
        prediction: normalizedPrediction,
        percentage: percentage,
        inputData: inputData
    });
}

// ============================================
// ERROR HANDLING
// ============================================

function showError(message) {
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');

    errorMessage.textContent = message;
    document.getElementById('resultContainer').classList.add('hidden');
    document.getElementById('loadingSpinner').classList.add('hidden');
    errorContainer.classList.remove('hidden');
}

// ============================================
// LOADING STATE
// ============================================

function showLoading() {
    document.getElementById('loadingSpinner').classList.remove('hidden');
    document.getElementById('resultContainer').classList.add('hidden');
    document.getElementById('errorContainer').classList.add('hidden');
}

function hideLoading() {
    document.getElementById('loadingSpinner').classList.add('hidden');
}

// ============================================
// FORM RESET
// ============================================

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('resultContainer').classList.add('hidden');
    document.getElementById('errorContainer').classList.add('hidden');
    document.getElementById('loadingSpinner').classList.add('hidden');
}

// ============================================
// SAMPLE DATA LOADER (Optional)
// ============================================

function loadSampleData() {
    const sampleData = {
        location: 1,
        temp_2m: 25.5,
        relhum_2m: 65,
        dp_2m: 18.2,
        ws_10m: 5.2,
        ws_100m: 8.5,
        wd_10m: 180,
        wd_100m: 195,
        wg_10m: 3.2,
        hour: 14,
        day: 15,
        month: 6,
        dayofweek: 2,
        is_weekend: 0
    };

    document.getElementById('location').value = sampleData.location;
    document.getElementById('temp_2m').value = sampleData.temp_2m;
    document.getElementById('relhum_2m').value = sampleData.relhum_2m;
    document.getElementById('dp_2m').value = sampleData.dp_2m;
    document.getElementById('ws_10m').value = sampleData.ws_10m;
    document.getElementById('ws_100m').value = sampleData.ws_100m;
    document.getElementById('wd_10m').value = sampleData.wd_10m;
    document.getElementById('wd_100m').value = sampleData.wd_100m;
    document.getElementById('wg_10m').value = sampleData.wg_10m;
    document.getElementById('hour').value = sampleData.hour;
    document.getElementById('day').value = sampleData.day;
    document.getElementById('month').value = sampleData.month;
    document.getElementById('dayofweek').value = sampleData.dayofweek;
    document.getElementById('is_weekend').value = sampleData.is_weekend;
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Wind Power Prediction App Loaded');
    
    // Check if backend is available
    checkBackendHealth();
});

function checkBackendHealth() {
    fetch(`${API_BASE_URL}/health`)
        .then(response => response.json())
        .then(data => {
            console.log('✅ Backend Status:', data.status);
        })
        .catch(error => {
            console.warn('⚠️ Backend not available. Using demo mode.');
            console.warn('Error:', error.message);
        });
}