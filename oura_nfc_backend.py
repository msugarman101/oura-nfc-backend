"""
Oura NFC Tag Creator Backend
A simple Flask app that receives NFC tap data and creates tags in your Oura app
"""

from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Your Oura personal access token
# Replace this with your actual token from https://cloud.ouraring.com/personal-access-tokens
OURA_TOKEN = os.getenv('OURA_TOKEN', 'YOUR_OURA_TOKEN_HERE')

# Oura API endpoint for creating tags
OURA_API_URL = 'https://api.ouraring.com/v2/usercollection/enhanced_tag'

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'Backend is running!'}), 200

@app.route('/create-tag', methods=['POST', 'OPTIONS'])
def create_tag():
    """
    Create a tag in Oura
    
    Expected JSON body:
    {
        "tag_type_code": "workout",  # Required: tag type (e.g., "workout", "stress", "poor_sleep")
        "start_time": "2025-12-03",   # Required: ISO format date (YYYY-MM-DD)
        "end_time": "2025-12-03",     # Optional: defaults to start_time
        "comment": "My comment"       # Optional: add a note
    }
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response, 200
    
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No JSON body provided'}), 400
        
        tag_type_code = data.get('tag_type_code')
        start_time = data.get('start_time')
        end_time = data.get('end_time', start_time)
        comment = data.get('comment', '')
        
        if not tag_type_code or not start_time:
            return jsonify({
                'error': 'Missing required fields',
                'required': ['tag_type_code', 'start_time']
            }), 400
        
        # Validate token is set
        if OURA_TOKEN == 'YOUR_OURA_TOKEN_HERE':
            return jsonify({
                'error': 'OURA_TOKEN not configured. Set it in environment variables.'
            }), 500
        
        # Prepare request to Oura API
        headers = {
            'Authorization': f'Bearer {OURA_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'tag_type_code': tag_type_code,
            'start_time': start_time,
            'end_time': end_time,
            'comment': comment
        }
        
        # Make request to Oura API
        response = requests.post(OURA_API_URL, json=payload, headers=headers)
        
        # Check if successful
        if response.status_code in [200, 201]:
            return jsonify({
                'success': True,
                'message': f'Tag "{tag_type_code}" created successfully for {start_time}',
                'data': response.json()
            }), 201
        else:
            error_details = response.json() if response.text else 'No additional details'
            print(f"Oura API Error: {response.status_code}")
            print(f"Response: {error_details}")
            return jsonify({
                'error': 'Failed to create tag in Oura',
                'status_code': response.status_code,
                'details': error_details,
                'oura_error': error_details.get('error_description', '') if isinstance(error_details, dict) else ''
            }), response.status_code
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Failed to communicate with Oura API',
            'details': str(e)
        }), 503
    
    except Exception as e:
        return jsonify({
            'error': 'Server error',
            'details': str(e)
        }), 500

@app.route('/', methods=['GET'])
def home():
    """Root endpoint with HTML form"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Oura NFC Tag Creator</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 30px;
                max-width: 400px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 24px;
            }
            p {
                color: #666;
                margin-bottom: 30px;
                font-size: 14px;
            }
            .tag-buttons {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 20px;
            }
            button {
                padding: 12px;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                background: #f0f0f0;
                color: #333;
            }
            button:hover {
                background: #e0e0e0;
                transform: translateY(-2px);
            }
            button.active {
                background: #667eea;
                color: white;
            }
            .create-btn {
                width: 100%;
                padding: 15px;
                background: #667eea;
                color: white;
                font-size: 16px;
                margin-top: 20px;
                border-radius: 10px;
            }
            .create-btn:hover {
                background: #5568d3;
            }
            .create-btn:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                border-radius: 10px;
                display: none;
            }
            .result.success {
                background: #d4edda;
                color: #155724;
                display: block;
            }
            .result.error {
                background: #f8d7da;
                color: #721c24;
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📍 Oura Tag Creator</h1>
            <p>Tap a tag type, then create</p>
            
            <div class="tag-buttons">
                <button onclick="selectTag('workout')">Workout</button>
                <button onclick="selectTag('stress')">Stress</button>
                <button onclick="selectTag('poor_sleep')">Poor Sleep</button>
                <button onclick="selectTag('meditation')">Meditation</button>
                <button onclick="selectTag('recovery')">Recovery</button>
                <button onclick="selectTag('travel')">Travel</button>
                <button onclick="selectTag('sickness')">Sickness</button>
                <button onclick="selectTag('menstruation')">Menstruation</button>
            </div>
            
            <button class="create-btn" onclick="createTag()" id="createBtn" disabled>Create Tag</button>
            
            <div class="result" id="result"></div>
        </div>
        
        <script>
            let selectedTag = null;
            
            function selectTag(tag) {
                selectedTag = tag;
                // Update button styles
                document.querySelectorAll('.tag-buttons button').forEach(btn => {
                    btn.classList.remove('active');
                });
                event.target.classList.add('active');
                document.getElementById('createBtn').disabled = false;
            }
            
            async function createTag() {
                if (!selectedTag) {
                    showResult('Please select a tag type', 'error');
                    return;
                }
                
                const today = new Date().toISOString().split('T')[0];
                
                try {
                    const response = await fetch('/create-tag', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            tag_type_code: selectedTag,
                            start_time: today,
                            comment: 'Tagged via NFC'
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        showResult('✅ Tag created successfully!', 'success');
                        document.getElementById('createBtn').disabled = true;
                        selectedTag = null;
                    } else {
                        showResult('❌ Error: ' + data.error, 'error');
                    }
                } catch (error) {
                    showResult('❌ Error: ' + error.message, 'error');
                }
            }
            
            function showResult(message, type) {
                const resultDiv = document.getElementById('result');
                resultDiv.textContent = message;
                resultDiv.className = 'result ' + type;
            }
        </script>
    </body>
    </html>
    """
    return html, 200, {'Content-Type': 'text/html'}

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
