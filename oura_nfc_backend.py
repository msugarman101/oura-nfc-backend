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

# Oura API endpoint
OURA_API_URL = 'https://api.ouraring.com/v2/usercollection/daily_tags'

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'Backend is running!'}), 200

@app.route('/create-tag', methods=['POST'])
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
            return jsonify({
                'error': 'Failed to create tag in Oura',
                'status_code': response.status_code,
                'details': response.json() if response.text else 'No additional details'
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
    """Root endpoint with instructions"""
    return jsonify({
        'message': 'Oura NFC Tag Creator Backend',
        'endpoints': {
            'POST /create-tag': 'Create a tag in Oura',
            'GET /health': 'Health check'
        },
        'usage': {
            'endpoint': 'POST /create-tag',
            'body': {
                'tag_type_code': 'workout (or: stress, poor_sleep, meditation, travel, sickness, recovery, etc)',
                'start_time': '2025-12-03 (YYYY-MM-DD format)',
                'end_time': '2025-12-03 (optional, defaults to start_time)',
                'comment': 'Optional note'
            }
        }
    }), 200

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
