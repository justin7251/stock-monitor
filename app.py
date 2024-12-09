from flask import Flask, g
from flask_cors import CORS
from config import Config
from database.connection import get_db
from database.init_db import init_db, populate_default_commodities
from routes import register_blueprints
from utils.logging_config import setup_logging
from utils.error_handler import register_error_handlers

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configuration
    app.config.from_object(Config)
    
    # Setup logging
    setup_logging(app)
    
    # Register Blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Database initialization
    with app.app_context():
        init_db()
        populate_default_commodities()
    
    @app.teardown_appcontext
    def close_db(error):
        """Closes the database at the end of the request."""
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=Config.DEBUG, 
        host=Config.HOST, 
        port=Config.PORT
    )
