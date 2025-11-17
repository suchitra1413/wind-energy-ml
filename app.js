const API_URL = 'http://localhost:5000/api/predict';

document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        showSpinner();
        
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

        console.log('Sending data:', formData);

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
            mode: 'cors'
        });

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const result = await response.json();
        console.log('Response:', result);

        displayResult(result.prediction);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        hideSpinner();
    }
});

function displayResult(prediction) {
    const pred = parseFloat(prediction);
    const percentage = (pred * 100).toFixed(2);

    document.getElementById('powerValue').textContent = pred.toFixed(4);
    document.getElementById('powerPercent').textContent = percentage + '%';
    document.getElementById('powerFill').style.width = percentage + '%';

    let status = '';
    if (pred < 0.33) {
        status = '🔴 LOW - Minimal Power Generation';
    } else if (pred < 0.66) {
        status = '🟡 MEDIUM - Moderate Power Generation';
    } else {
        status = '🟢 HIGH - Strong Power Generation';
    }

    document.getElementById('statusMessage').textContent = status;

    document.getElementById('successResult').classList.remove('hidden');
    document.getElementById('errorResult').classList.add('hidden');
    document.getElementById('resultBox').classList.remove('hidden');
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message || 'Failed to get prediction';
    document.getElementById('errorResult').classList.remove('hidden');
    document.getElementById('successResult').classList.add('hidden');
    document.getElementById('resultBox').classList.remove('hidden');
}

function showSpinner() {
    document.getElementById('loadingSpinner').classList.remove('hidden');
    document.getElementById('resultBox').classList.remove('hidden');
}

function hideSpinner() {
    document.getElementById('loadingSpinner').classList.add('hidden');
}

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('resultBox').classList.add('hidden');
    document.getElementById('successResult').classList.add('hidden');
    document.getElementById('errorResult').classList.add('hidden');
}

function scrollToPredict() {
    document.getElementById('predict').scrollIntoView({ behavior: 'smooth' });
}

console.log('App loaded');