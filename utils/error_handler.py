from flask import jsonify

def handle_error(error, status_code=500):
    """
    Generic error handler
    """
    response = {
        'error': str(error),
        'status': status_code
    }
    return jsonify(response), status_code

def register_error_handlers(app):
    """
    Register error handlers for the Flask app
    """
    @app.errorhandler(404)
    def not_found_error(error):
        return handle_error(error, 404)

    @app.errorhandler(500)
    def internal_error(error):
        return handle_error(error, 500)
