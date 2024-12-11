import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    """
    Configure logging for the application
    """
    # Ensure logs directory exists
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Create a file handler
    file_handler = RotatingFileHandler(
        'logs/market_monitor.log', 
        maxBytes=10240, 
        backupCount=10
    )
    
    # Create a formatter
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    
    # Set logging level
    file_handler.setLevel(logging.INFO)
    
    # Add handler to app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    # Log application startup
    app.logger.info('Market Monitor Application Startup')
