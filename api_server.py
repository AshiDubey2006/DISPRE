"""
API Server for DISPRE (Optional - for web deployment)
Provides REST API endpoints for disaster predictions
"""

from flask import Flask, request, jsonify
import sys
import os
import logging

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dispre_engine import DISPREEngine

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Initialize engine globally
engine = None


def init_engine():
    """Initialize DISPRE engine"""
    global engine
    if engine is None:
        engine = DISPREEngine()
        engine.train_all_models()
    return engine


@app.before_request
def before_request():
    """Initialize before first request"""
    init_engine()


@app.route('/', methods=['GET'])
def home():
    """API home endpoint"""
    return jsonify({
        'name': 'DISPRE API',
        'version': '1.0.0',
        'description': 'Disaster Prediction and Response Engine',
        'endpoints': {
            'GET /': 'API information',
            'POST /predict/earthquake': 'Get earthquake prediction',
            'POST /predict/flood': 'Get flood prediction',
            'POST /predict/tsunami': 'Get tsunami prediction',
            'POST /predict/all': 'Get all hazard predictions',
            'GET /health': 'Health check'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'})


@app.route('/predict/earthquake', methods=['POST'])
def predict_earthquake():
    """
    Predict earthquake risk
    
    Request body:
    {
        "latitude": float,
        "longitude": float,
        "depth_km": float (optional),
        "strain": float (optional, 0-1)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Missing latitude or longitude'}), 400
        
        result = engine.predict_earthquake(
            latitude=data['latitude'],
            longitude=data['longitude'],
            depth_km=data.get('depth_km', 10),
            strain=data.get('strain', 0.5)
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in earthquake prediction: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/predict/flood', methods=['POST'])
def predict_flood():
    """
    Predict flood risk
    
    Request body:
    {
        "latitude": float,
        "longitude": float,
        "rainfall_mm": float (optional),
        "soil_moisture": float (optional, 0-1)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Missing latitude or longitude'}), 400
        
        result = engine.predict_flood(
            latitude=data['latitude'],
            longitude=data['longitude'],
            rainfall_mm=data.get('rainfall_mm', 50),
            soil_moisture=data.get('soil_moisture', 0.5)
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in flood prediction: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/predict/tsunami', methods=['POST'])
def predict_tsunami():
    """
    Predict tsunami risk
    
    Request body:
    {
        "latitude": float,
        "longitude": float,
        "earthquake_magnitude": float (optional),
        "depth_km": float (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Missing latitude or longitude'}), 400
        
        result = engine.predict_tsunami(
            latitude=data['latitude'],
            longitude=data['longitude'],
            magnitude=data.get('earthquake_magnitude', 7.0),
            depth_km=data.get('depth_km', 10)
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in tsunami prediction: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/predict/all', methods=['POST'])
def predict_all():
    """
    Get all hazard predictions for a location
    
    Request body:
    {
        "latitude": float,
        "longitude": float,
        "rainfall_mm": float (optional),
        "earthquake_magnitude": float (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Missing latitude or longitude'}), 400
        
        result = engine.predict_all_hazards(
            latitude=data['latitude'],
            longitude=data['longitude'],
            rainfall_mm=data.get('rainfall_mm', 50),
            earthquake_magnitude=data.get('earthquake_magnitude', 6.0)
        )
        
        # Check for emergency alerts
        alerts = engine.run_emergency_alert(result)
        result['emergency_alerts'] = alerts
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in multi-hazard prediction: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("Starting DISPRE API Server...")
    logger.info("Initialize engine and train models (this may take a moment)...")
    
    # Initialize and train
    init_engine()
    
    logger.info("Engine ready. Starting Flask server on http://0.0.0.0:8000")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=8000, debug=False)
