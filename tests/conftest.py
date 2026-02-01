"""
Pytest configuration and shared fixtures for the stock-monitor test suite.
"""
import sys
import os
import pytest
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from database.connection import get_db


@pytest.fixture(scope='session')
def app():
    """Create and configure a test Flask application instance."""
    # Create app with test config
    test_app = create_app()
    test_app.config.update({
        'TESTING': True,
        'DATABASE': ':memory:',  # Use in-memory database for tests
        'WTF_CSRF_ENABLED': False,
    })
    
    yield test_app


@pytest.fixture(scope='function')
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def test_db(app):
    """Create a fresh test database for each test function."""
    with app.app_context():
        db = get_db()
        # Database is already initialized in create_app
        yield db
        # Cleanup after test
        db.close()


# Sample test data fixtures
@pytest.fixture
def sample_stock_data():
    """Provide sample stock data for testing."""
    return {
        'id': 1,
        'symbol': 'AAPL',
        'name': 'Apple Inc.',
        'sector': 'Technology',
        'description': 'Consumer electronics company',
        'target_price': 150.00
    }


@pytest.fixture
def sample_commodity_data():
    """Provide sample commodity data for testing."""
    return {
        'id': 1,
        'name': 'Gold',
        'symbol': 'GC=F',
        'commodity_type': 'Metals',
        'description': 'Precious metal',
        'target_price': 2000.00
    }


@pytest.fixture
def sample_stock_prices():
    """Provide sample stock price data for testing."""
    return {
        'current': 155.50,
        'target': 150.00,
        'difference': 5.50,
        'percentage': 3.67
    }


@pytest.fixture
def mock_yfinance_ticker(monkeypatch):
    """Mock yfinance Ticker for testing without actual API calls."""
    class MockHistory:
        def __init__(self, price):
            self.price = price
            
        def __getitem__(self, key):
            import pandas as pd
            return pd.Series([self.price])
        
        @property
        def empty(self):
            return False
    
    class MockTicker:
        def __init__(self, symbol):
            self.symbol = symbol
            
        def history(self, period='1d'):
            # Return mock price data
            return MockHistory(155.50)
        
        @property
        def info(self):
            return {
                'longName': 'Apple Inc.',
                'sector': 'Technology',
                'marketCap': 2500000000000,
                'trailingPE': 28.5,
                'dividendYield': 0.005,
                'fiftyTwoWeekHigh': 180.00,
                'fiftyTwoWeekLow': 125.00
            }
    
    def mock_ticker(symbol):
        return MockTicker(symbol)
    
    import yfinance as yf
    monkeypatch.setattr(yf, 'Ticker', mock_ticker)
    
    return mock_ticker


@pytest.fixture
def freeze_time():
    """Fixture to freeze time for consistent datetime testing."""
    fixed_time = datetime(2024, 1, 1, 12, 0, 0)
    return fixed_time
