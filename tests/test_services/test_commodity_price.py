"""
Unit tests for commodity price service.
"""
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from services.commodity_price import get_commodity_price, get_commodity_details


class TestGetCommodityPrice:
    """Test get_commodity_price functionality."""
    
    @patch('yfinance.Ticker')
    def test_get_commodity_price_success(self, mock_ticker):
        """Test successful commodity price retrieval."""
        mock_history = pd.DataFrame({'Close': [2050.00]})
        mock_ticker.return_value.history.return_value = mock_history
        
        price = get_commodity_price('GOLD')
        
        assert price == 2050.00
        mock_ticker.assert_called_once_with('GC=F')  # Should use mapped symbol
    
    @patch('yfinance.Ticker')
    def test_get_commodity_price_with_direct_symbol(self, mock_ticker):
        """Test commodity price with direct Yahoo Finance symbol."""
        mock_history = pd.DataFrame({'Close': [25.50]})
        mock_ticker.return_value.history.return_value = mock_history
        
        price = get_commodity_price('GC=F')
        
        assert price == 25.50
    
    @patch('yfinance.Ticker')
    def test_get_commodity_price_empty_data(self, mock_ticker):
        """Test handling of empty price data."""
        mock_history = pd.DataFrame()
        mock_ticker.return_value.history.return_value = mock_history
        
        price = get_commodity_price('INVALID')
        
        assert price is None
    
    @patch('yfinance.Ticker')
    def test_get_commodity_price_exception(self, mock_ticker):
        """Test handling of exceptions."""
        mock_ticker.side_effect = Exception("Network error")
        
        price = get_commodity_price('GOLD')
        
        assert price is None
    
    @pytest.mark.parametrize("commodity,expected_symbol", [
        ('GOLD', 'GC=F'),
        ('SILVER', 'SI=F'),
        ('COPPER', 'HG=F'),
        ('CRUDE', 'CL=F'),
        ('NATGAS', 'NG=F'),
        ('WHEAT', 'ZW=F'),
        ('CORN', 'ZC=F'),
        ('COFFEE', 'KC=F'),
    ])
    @patch('yfinance.Ticker')
    def test_commodity_symbol_mapping(self, mock_ticker, commodity, expected_symbol):
        """Test that commodity symbols are correctly mapped."""
        mock_history = pd.DataFrame({'Close': [100.0]})
        mock_ticker.return_value.history.return_value = mock_history
        
        price = get_commodity_price(commodity)
        
        mock_ticker.assert_called_with(expected_symbol)
        assert price == 100.0
    
    @patch('yfinance.Ticker')
    def test_case_insensitive_mapping(self, mock_ticker):
        """Test that commodity mapping is case-insensitive."""
        mock_history = pd.DataFrame({'Close': [2050.0]})
        mock_ticker.return_value.history.return_value = mock_history
        
        # Test lowercase
        price = get_commodity_price('gold')
        assert price == 2050.0
        
        # Test mixed case
        price = get_commodity_price('Gold')
        assert price == 2050.0
    
    @patch('yfinance.Ticker')
    def test_multiple_prices_returns_latest(self, mock_ticker):
        """Test that latest price is returned when multiple exist."""
        mock_history = pd.DataFrame({'Close': [2000.0, 2025.0, 2050.0]})
        mock_ticker.return_value.history.return_value = mock_history
        
        price = get_commodity_price('GOLD')
        
        assert price == 2050.0


class TestGetCommodityDetails:
    """Test get_commodity_details functionality."""
    
    @patch('yfinance.Ticker')
    @patch('services.commodity_price.get_commodity_price')
    def test_get_commodity_details_success(self, mock_get_price, mock_ticker):
        """Test successful retrieval of commodity details."""
        mock_get_price.return_value = 2050.0
        mock_info = {
            'shortName': 'Gold Futures',
            'exchange': 'COMEX',
            'fiftyTwoWeekHigh': 2100.0,
            'fiftyTwoWeekLow': 1800.0
        }
        mock_ticker.return_value.info = mock_info
        
        details = get_commodity_details('GOLD')
        
        assert details['symbol'] == 'GOLD'
        assert details['name'] == 'Gold Futures'
        assert details['current_price'] == 2050.0
        assert details['exchange'] == 'COMEX'
        assert details['52_week_high'] == 2100.0
        assert details['52_week_low'] == 1800.0
    
    @patch('yfinance.Ticker')
    @patch('services.commodity_price.get_commodity_price')
    def test_get_commodity_details_missing_info(self, mock_get_price, mock_ticker):
        """Test commodity details with missing information."""
        mock_get_price.return_value = 2050.0
        mock_info = {}  # Empty info
        mock_ticker.return_value.info = mock_info
        
        details = get_commodity_details('GOLD')
        
        assert details['symbol'] == 'GOLD'
        assert details['name'] == 'GOLD'  # Falls back to symbol
        assert details['exchange'] == 'Futures'  # Default value
    
    @patch('yfinance.Ticker')
    def test_get_commodity_details_exception(self, mock_ticker):
        """Test handling of exceptions during details fetch."""
        mock_ticker.side_effect = Exception("API error")
        
        details = get_commodity_details('GOLD')
        
        assert details == {'symbol': 'GOLD'}
    
    @patch('yfinance.Ticker')
    @patch('services.commodity_price.get_commodity_price')
    def test_get_commodity_details_uses_mapping(self, mock_get_price, mock_ticker):
        """Test that get_commodity_details uses symbol mapping."""
        mock_get_price.return_value = 2050.0
        mock_info = {'shortName': 'Gold'}
        mock_ticker.return_value.info = mock_info
        
        details = get_commodity_details('GOLD')
        
        # Should call with mapped symbol
        mock_ticker.assert_called_with('GC=F')


class TestCommodityServiceEdgeCases:
    """Test edge cases and error scenarios."""
    
    @patch('yfinance.Ticker')
    def test_empty_symbol(self, mock_ticker):
        """Test handling of empty symbol."""
        mock_history = pd.DataFrame()
        mock_ticker.return_value.history.return_value = mock_history
        
        price = get_commodity_price('')
        
        assert price is None
    
    @patch('yfinance.Ticker')
    def test_unmapped_commodity(self, mock_ticker):
        """Test commodity that's not in the mapping."""
        mock_history = pd.DataFrame({'Close': [50.0]})
        mock_ticker.return_value.history.return_value = mock_history
        
        # Custom symbol not in the map
        price = get_commodity_price('CUSTOM=F')
        
        assert price == 50.0
        mock_ticker.assert_called_with('CUSTOM=F')  # Should use original symbol
    
    @patch('yfinance.Ticker')
    def test_logging_warnings(self, mock_ticker, caplog):
        """Test that warnings are logged appropriately."""
        import logging
        
        mock_history = pd.DataFrame()
        mock_ticker.return_value.history.return_value = mock_history
        
        with caplog.at_level(logging.WARNING):
            price = get_commodity_price('INVALID')
        
        assert price is None
        assert any('No price data found' in record.message for record in caplog.records)
    
    @patch('yfinance.Ticker')
    def test_logging_errors(self, mock_ticker, caplog):
        """Test that errors are logged appropriately."""
        import logging
        
        mock_ticker.side_effect = Exception("Test error")
        
        with caplog.at_level(logging.ERROR):
            price = get_commodity_price('GOLD')
        
        assert price is None
        assert any('Error fetching commodity price' in record.message for record in caplog.records)


class TestCommodityMapping:
    """Test complete commodity mapping functionality."""
    
    @pytest.mark.parametrize("display_name,yahoo_symbol", [
        ('GOLD', 'GC=F'),
        ('SILVER', 'SI=F'),
        ('COPPER', 'HG=F'),
        ('CRUDE', 'CL=F'),
        ('NATGAS', 'NG=F'),
        ('WHEAT', 'ZW=F'),
        ('CORN', 'ZC=F'),
        ('COFFEE', 'KC=F'),
    ])
    @patch('yfinance.Ticker')
    def test_all_commodity_mappings(self, mock_ticker, display_name, yahoo_symbol):
        """Test that all commodity mappings work correctly."""
        mock_history = pd.DataFrame({'Close': [100.0]})
        mock_ticker.return_value.history.return_value = mock_history
        
        price = get_commodity_price(display_name)
        
        # Verify correct symbol was used
        mock_ticker.assert_called_with(yahoo_symbol)
        assert price == 100.0
