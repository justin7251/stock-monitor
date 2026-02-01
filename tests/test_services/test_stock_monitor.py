"""
Unit tests for the StockMonitor service.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from services.stock_monitor import StockMonitor


class TestStockMonitorGetPrice:
    """Test get_stock_price functionality."""
    
    def test_get_stock_price_success(self, mock_yfinance_ticker):
        """Test successful stock price retrieval."""
        monitor = StockMonitor()
        price = monitor.get_stock_price('AAPL')
        
        assert price is not None
        assert price == 155.50
    
    @patch('yfinance.Ticker')
    def test_get_stock_price_with_mock(self, mock_ticker):
        """Test stock price retrieval with custom mock."""
        # Setup mock
        mock_history = pd.DataFrame({'Close': [150.25]})
        mock_ticker.return_value.history.return_value = mock_history
        
        monitor = StockMonitor()
        price = monitor.get_stock_price('GOOGL')
        
        assert price == 150.25
        mock_ticker.assert_called_once_with('GOOGL')
    
    @patch('yfinance.Ticker')
    def test_get_stock_price_empty_data(self, mock_ticker):
        """Test handling of empty price data."""
        # Setup mock with empty dataframe
        mock_history = pd.DataFrame()
        mock_ticker.return_value.history.return_value = mock_history
        
        monitor = StockMonitor()
        price = monitor.get_stock_price('INVALID')
        
        assert price is None
    
    @patch('yfinance.Ticker')
    def test_get_stock_price_exception(self, mock_ticker):
        """Test handling of exceptions during price fetch."""
        # Setup mock to raise exception
        mock_ticker.side_effect = Exception("Network error")
        
        monitor = StockMonitor()
        price = monitor.get_stock_price('AAPL')
        
        assert price is None
    
    @patch('yfinance.Ticker')
    def test_get_stock_price_invalid_symbol(self, mock_ticker):
        """Test handling of invalid stock symbol."""
        mock_history = pd.DataFrame()
        mock_ticker.return_value.history.return_value = mock_history
        
        monitor = StockMonitor()
        price = monitor.get_stock_price('NOTREAL123')
        
        assert price is None
    
    @patch('yfinance.Ticker')
    def test_get_stock_price_multiple_prices(self, mock_ticker):
        """Test that it returns the latest price when multiple prices exist."""
        # Multiple closing prices
        mock_history = pd.DataFrame({'Close': [150.0, 151.0, 152.5]})
        mock_ticker.return_value.history.return_value = mock_history
        
        monitor = StockMonitor()
        price = monitor.get_stock_price('AAPL')
        
        assert price == 152.5  # Should return the last price
    
    def test_get_stock_price_caching(self, mock_yfinance_ticker):
        """Test that LRU cache is working."""
        monitor = StockMonitor()
        
        # First call
        price1 = monitor.get_stock_price('AAPL')
        # Second call should use cache
        price2 = monitor.get_stock_price('AAPL')
        
        assert price1 == price2
        # Check cache info
        assert monitor.get_stock_price.cache_info().hits > 0


class TestStockMonitorGetDetails:
    """Test get_stock_details functionality."""
    
    def test_get_stock_details_success(self, mock_yfinance_ticker):
        """Test successful retrieval of stock details."""
        monitor = StockMonitor()
        details = monitor.get_stock_details('AAPL')
        
        assert details is not None
        assert details['symbol'] == 'AAPL'
        assert details['name'] == 'Apple Inc.'
        assert details['sector'] == 'Technology'
        assert 'current_price' in details
        assert 'market_cap' in details
    
    @patch('yfinance.Ticker')
    def test_get_stock_details_complete_info(self, mock_ticker):
        """Test stock details with complete information."""
        # Setup mock
        mock_info = {
            'longName': 'Tesla, Inc.',
            'sector': 'Automotive',
            'marketCap': 800000000000,
            'trailingPE': 65.5,
            'dividendYield': None,
            'fiftyTwoWeekHigh': 300.0,
            'fiftyTwoWeekLow': 150.0
        }
        mock_ticker.return_value.info = mock_info
        mock_history = pd.DataFrame({'Close': [250.0]})
        mock_ticker.return_value.history.return_value = mock_history
        
        monitor = StockMonitor()
        details = monitor.get_stock_details('TSLA')
        
        assert details['name'] == 'Tesla, Inc.'
        assert details['sector'] == 'Automotive'
        assert details['market_cap'] == 800000000000
        assert details['pe_ratio'] == 65.5
        assert details['52_week_high'] == 300.0
        assert details['52_week_low'] == 150.0
    
    @patch('yfinance.Ticker')
    def test_get_stock_details_missing_info(self, mock_ticker):
        """Test stock details with missing information."""
        # Setup mock with minimal info
        mock_info = {}
        mock_ticker.return_value.info = mock_info
        mock_history = pd.DataFrame({'Close': [100.0]})
        mock_ticker.return_value.history.return_value = mock_history
        
        monitor = StockMonitor()
        details = monitor.get_stock_details('TEST')
        
        assert details['symbol'] == 'TEST'
        assert details['sector'] == 'Unknown'
        assert details['name'] == 'TEST'  # Falls back to symbol
    
    @patch('yfinance.Ticker')
    def test_get_stock_details_exception(self, mock_ticker):
        """Test handling of exceptions during details fetch."""
        mock_ticker.side_effect = Exception("API error")
        
        monitor = StockMonitor()
        details = monitor.get_stock_details('AAPL')
        
        assert details == {'symbol': 'AAPL'}
    
    @patch('yfinance.Ticker')
    def test_get_stock_details_includes_current_price(self, mock_ticker):
        """Test that stock details includes current price."""
        mock_info = {'longName': 'Test Company'}
        mock_ticker.return_value.info = mock_info
        mock_history = pd.DataFrame({'Close': [123.45]})
        mock_ticker.return_value.history.return_value = mock_history
        
        monitor = StockMonitor()
        details = monitor.get_stock_details('TEST')
        
        assert details['current_price'] == 123.45


class TestStockMonitorEdgeCases:
    """Test edge cases and error scenarios."""
    
    @patch('yfinance.Ticker')
    def test_empty_symbol(self, mock_ticker):
        """Test handling of empty symbol."""
        monitor = StockMonitor()
        price = monitor.get_stock_price('')
        
        # Should handle gracefully
        assert price is None or isinstance(price, (float, type(None)))
    
    @patch('yfinance.Ticker')
    def test_special_characters_in_symbol(self, mock_ticker):
        """Test handling of special characters in symbol."""
        mock_history = pd.DataFrame({'Close': [50.0]})
        mock_ticker.return_value.history.return_value = mock_history
        
        monitor = StockMonitor()
        # Some symbols have special characters (e.g., "BRK.B")
        price = monitor.get_stock_price('BRK.B')
        
        assert price == 50.0
    
    @patch('yfinance.Ticker')
    def test_logger_warnings(self, mock_ticker, caplog):
        """Test that warnings are logged appropriately."""
        import logging
        
        # Setup mock with empty data
        mock_history = pd.DataFrame()
        mock_ticker.return_value.history.return_value = mock_history
        
        monitor = StockMonitor()
        
        with caplog.at_level(logging.WARNING):
            price = monitor.get_stock_price('INVALID')
        
        assert price is None
        # Check that warning was logged
        assert any('No price data found' in record.message for record in caplog.records)
    
    @patch('yfinance.Ticker')
    def test_logger_errors(self, mock_ticker, caplog):
        """Test that errors are logged appropriately."""
        import logging
        
        mock_ticker.side_effect = Exception("Test error")
        
        monitor = StockMonitor()
        
        with caplog.at_level(logging.ERROR):
            price = monitor.get_stock_price('AAPL')
        
        assert price is None
        # Check that error was logged
        assert any('Error fetching stock price' in record.message for record in caplog.records)


class TestStockMonitorIntegration:
    """Integration-style tests (may require network access)."""
    
    @pytest.mark.slow
    @pytest.mark.integration
    def test_real_api_call_skip(self):
        """Test with real API call (skipped by default)."""
        # This test would make a real API call
        # Mark it as slow/integration so it can be skipped in normal test runs
        pytest.skip("Skipping real API test to avoid network dependency")
        
        monitor = StockMonitor()
        price = monitor.get_stock_price('AAPL')
        
        assert price is not None
        assert isinstance(price, (float, int))
        assert price > 0
