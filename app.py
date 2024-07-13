# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
import requests
import uuid
import base64

app = Flask(__name__)

COPYLEAKS_API_KEY = '53626d4e-a6fc-4f74-ab5d-2e05ff114e48'
COPYLEAKS_EMAIL = 'kib23-a.kulish@nubip.edu.ua'

# Function to get access token
def get_access_token():
    url = 'https://id.copyleaks.com/v3/account/login/api'
    data = {
        'email': COPYLEAKS_EMAIL,
        'key': COPYLEAKS_API_KEY
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=data, headers=headers)
    print("Access Token Response:", response.text)  # Debug information
    response.raise_for_status()  # Raise an error for bad status codes
    response_data = response.json()
    return response_data['access_token']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_plagiarism', methods=['POST'])
def check_plagiarism_route():
    if 'file' in request.files:
        file = request.files['file']
        text = file.read().decode('utf-8')
        filename = file.filename
    else:
        text = request.form['text']
        filename = 'uploaded_text.txt'  # A default filename for text input

    text_base64 = base64.b64encode(text.encode('utf-8')).decode('utf-8')

    try:
        access_token = get_access_token()
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        scan_id = str(uuid.uuid4())  # Generate unique scan ID
        data = {
            'base64': text_base64,  # Text for plagiarism check in Base64 format
            'filename': filename,  # Include the filename in the request
            'properties': {
                'sandbox': True,
                'webhooks': {
                    'status': 'https://your-public-domain.com/webhook'  # Use a public domain for webhook
                }
            }
        }
        response = requests.put(f'https://api.copyleaks.com/v3/scans/submit/file/{scan_id}', headers=headers, json=data)
        print("Create Scan Response:", response.text)  # Debug information
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
    except requests.exceptions.RequestException as e:
        print("Error Response:", e.response.text)  # Print full server response
        return render_template('error.html', error=str(e))  # Return error template if request fails

    return render_template('result.html', result=result)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Webhook data received:", data)  # Debug information
    # Handle webhook data as needed
    # You can save it to a database or display directly

    # Example: Rendering a template to display results
    return render_template('webhook_result.html', result=data)

if __name__ == '__main__':
    app.run(debug=True)
