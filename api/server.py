from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory storage for the latest edge summary
latest_summary = None

@app.route('/api/summary', methods=['POST'])
def post_summary():
    """
    Accept POST requests with edge summary JSON and store the latest one in memory.
    """
    global latest_summary
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate required fields
        required_fields = ["date", "expected_power", "avg_loss_percent", "vision_label", "dust_detected", "health_score"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        latest_summary = data
        print(f"Received summary: {data}")
        return jsonify({"status": "Summary received and stored"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """
    Serve the latest edge summary via GET request.
    """
    if latest_summary is None:
        return jsonify({"status": "no_summary", "message": "No summary available yet."}), 200
    return jsonify(latest_summary), 200


@app.route('/', methods=['GET'])
def index():
    """Simple root endpoint to show API is running."""
    return jsonify({
        "status": "api_running",
        "available_endpoints": ["/api/summary (GET, POST)", "/api/clean (POST)"],
    }), 200

@app.route('/api/clean', methods=['POST'])
def clean_request():
    """
    Receive cleaning requests from dashboard.
    """
    data = request.get_json()
    if not data or 'method' not in data:
        return jsonify({"error": "Invalid cleaning request"}), 400
    
    method = data['method']
    message = data.get('message', f"Cleaning required via {method}")
    
    # Simulate sending to cleaning agent (log or send via different channel)
    print(f"Cleaning request: {method} - {message}")
    # Here, integrate with WhatsApp API or other messaging, but differentiated
    
    return jsonify({"status": f"Cleaning request sent to {method}"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)