from flask import Blueprint, jsonify
from services import test_alpha_vantage_api_key

debug_bp = Blueprint('debug', __name__, url_prefix='/debug')

@debug_bp.route('/api-key')
def debug_api_key():
    """
    API endpoint to check Alpha Vantage API key
    """
    results = test_alpha_vantage_api_key()
    return jsonify(results)
