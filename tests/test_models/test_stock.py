"""
Unit tests for the StockModel class.
"""
import pytest
from datetime import datetime
from models.stock import StockModel, validate_stock_data, create_stock


class TestStockModelInitialization:
    """Test StockModel initialization and default values."""
    
    def test_empty_initialization(self):
        """Test creating a stock with default values."""
        stock = StockModel()
        
        assert stock.id is None
        assert stock.symbol == ''
        assert stock.name == ''
        assert stock.sector == ''
        assert stock.description is None
        assert stock.target_price == 0.0
        assert stock.current_price is None
        assert stock.price_difference is None
        assert stock.price_percentage is None
        assert isinstance(stock.created_at, datetime)
        assert stock.updated_at is None
        assert stock.historical_prices == []
    
    def test_initialization_with_data(self, sample_stock_data):
        """Test creating a stock with provided data."""
        stock = StockModel(**sample_stock_data)
        
        assert stock.id == 1
        assert stock.symbol == 'AAPL'
        assert stock.name == 'Apple Inc.'
        assert stock.sector == 'Technology'
        assert stock.description == 'Consumer electronics company'
        assert stock.target_price == 150.00


class TestStockModelPriceUpdates:
    """Test price update functionality."""
    
    def test_update_price_basic(self, sample_stock_data):
        """Test basic price update."""
        stock = StockModel(**sample_stock_data)
        stock.update_price(155.50)
        
        assert stock.current_price == 155.50
        assert stock.updated_at is not None
        assert len(stock.historical_prices) == 1
        assert stock.historical_prices[0]['price'] == 155.50
    
    def test_update_price_calculations(self, sample_stock_data):
        """Test price difference and percentage calculations."""
        stock = StockModel(**sample_stock_data)
        stock.update_price(155.50)
        
        assert stock.price_difference == 5.50
        assert abs(stock.price_percentage - 3.67) < 0.01  # Allow small floating point error
    
    def test_update_price_multiple_times(self, sample_stock_data):
        """Test multiple price updates track history."""
        stock = StockModel(**sample_stock_data)
        
        stock.update_price(150.00)
        stock.update_price(155.00)
        stock.update_price(160.00)
        
        assert len(stock.historical_prices) == 3
        assert stock.current_price == 160.00
        assert stock.historical_prices[0]['price'] == 150.00
        assert stock.historical_prices[2]['price'] == 160.00
    
    def test_update_price_with_none(self, sample_stock_data):
        """Test updating with None price."""
        stock = StockModel(**sample_stock_data)
        stock.update_price(None)
        
        assert stock.current_price is None
        assert stock.price_difference is None
        assert stock.price_percentage is None
    
    def test_update_price_zero_target(self):
        """Test price update with zero target price."""
        stock = StockModel(symbol='TEST', target_price=0.0)
        stock.update_price(100.00)
        
        # Should handle division by zero gracefully
        assert stock.price_difference is None
        assert stock.price_percentage is None


class TestStockModelSerialization:
    """Test to_dict and from_dict methods."""
    
    def test_to_dict(self, sample_stock_data):
        """Test converting stock model to dictionary."""
        stock = StockModel(**sample_stock_data)
        stock.update_price(155.50)
        
        stock_dict = stock.to_dict()
        
        assert stock_dict['id'] == 1
        assert stock_dict['symbol'] == 'AAPL'
        assert stock_dict['name'] == 'Apple Inc.'
        assert stock_dict['current_price'] == 155.50
        assert 'created_at' in stock_dict
        assert 'updated_at' in stock_dict
    
    def test_from_dict(self, sample_stock_data):
        """Test creating stock model from dictionary."""
        stock = StockModel.from_dict(sample_stock_data)
        
        assert stock.id == 1
        assert stock.symbol == 'AAPL'
        assert stock.name == 'Apple Inc.'
        assert stock.target_price == 150.00
    
    def test_round_trip_serialization(self, sample_stock_data):
        """Test that to_dict and from_dict are reversible."""
        original = StockModel(**sample_stock_data)
        original.update_price(155.50)
        
        stock_dict = original.to_dict()
        reconstructed = StockModel.from_dict(stock_dict)
        
        assert reconstructed.symbol == original.symbol
        assert reconstructed.name == original.name
        assert reconstructed.current_price == original.current_price


class TestStockModelBusinessLogic:
    """Test business logic methods."""
    
    def test_is_above_target_true(self, sample_stock_data):
        """Test is_above_target when price is above target."""
        stock = StockModel(**sample_stock_data)
        stock.update_price(160.00)
        
        assert stock.is_above_target() is True
    
    def test_is_above_target_false(self, sample_stock_data):
        """Test is_above_target when price is below target."""
        stock = StockModel(**sample_stock_data)
        stock.update_price(140.00)
        
        assert stock.is_above_target() is False
    
    def test_is_above_target_equal(self, sample_stock_data):
        """Test is_above_target when price equals target."""
        stock = StockModel(**sample_stock_data)
        stock.update_price(150.00)
        
        assert stock.is_above_target() is False
    
    def test_is_above_target_no_price(self, sample_stock_data):
        """Test is_above_target when current price is None."""
        stock = StockModel(**sample_stock_data)
        
        assert stock.is_above_target() is False
    
    def test_get_price_status_above(self, sample_stock_data):
        """Test get_price_status for above target."""
        stock = StockModel(**sample_stock_data)
        stock.update_price(160.00)
        
        assert stock.get_price_status() == "Above Target"
    
    def test_get_price_status_below(self, sample_stock_data):
        """Test get_price_status for below target."""
        stock = StockModel(**sample_stock_data)
        stock.update_price(140.00)
        
        assert stock.get_price_status() == "Below Target"
    
    def test_get_price_status_at_target(self, sample_stock_data):
        """Test get_price_status when at target."""
        stock = StockModel(**sample_stock_data)
        stock.update_price(150.00)
        
        assert stock.get_price_status() == "At Target"
    
    def test_get_price_status_no_data(self, sample_stock_data):
        """Test get_price_status with no price data."""
        stock = StockModel(**sample_stock_data)
        
        assert stock.get_price_status() == "No Price Data"


class TestStockModelVolatility:
    """Test volatility calculation."""
    
    def test_calculate_volatility_sufficient_data(self, sample_stock_data):
        """Test volatility calculation with sufficient data."""
        stock = StockModel(**sample_stock_data)
        
        # Add 5 price points
        prices = [150.0, 152.0, 148.0, 151.0, 149.0]
        for price in prices:
            stock.update_price(price)
        
        volatility = stock.calculate_volatility(window=5)
        
        assert volatility is not None
        assert volatility > 0  # There is some volatility in the data
    
    def test_calculate_volatility_insufficient_data(self, sample_stock_data):
        """Test volatility calculation with insufficient data."""
        stock = StockModel(**sample_stock_data)
        stock.update_price(150.0)
        
        volatility = stock.calculate_volatility(window=5)
        
        assert volatility is None
    
    def test_calculate_volatility_no_data(self, sample_stock_data):
        """Test volatility calculation with no price data."""
        stock = StockModel(**sample_stock_data)
        
        volatility = stock.calculate_volatility()
        
        assert volatility is None
    
    def test_calculate_volatility_constant_prices(self, sample_stock_data):
        """Test volatility with constant prices (should be zero)."""
        stock = StockModel(**sample_stock_data)
        
        # All same price
        for _ in range(5):
            stock.update_price(150.0)
        
        volatility = stock.calculate_volatility(window=5)
        
        assert volatility == 0.0


class TestStockValidationFunctions:
    """Test validation helper functions."""
    
    def test_validate_stock_data_valid(self, sample_stock_data):
        """Test validation with valid data."""
        assert validate_stock_data(sample_stock_data) is True
    
    def test_validate_stock_data_missing_symbol(self, sample_stock_data):
        """Test validation with missing symbol."""
        data = sample_stock_data.copy()
        data['symbol'] = ''
        
        assert validate_stock_data(data) is False
    
    def test_validate_stock_data_missing_name(self, sample_stock_data):
        """Test validation with missing name."""
        data = sample_stock_data.copy()
        data['name'] = ''
        
        assert validate_stock_data(data) is False
    
    def test_validate_stock_data_invalid_price(self, sample_stock_data):
        """Test validation with invalid price type."""
        data = sample_stock_data.copy()
        data['target_price'] = 'not a number'
        
        assert validate_stock_data(data) is False
    
    def test_create_stock_valid(self, sample_stock_data):
        """Test factory method with valid data."""
        stock = create_stock(sample_stock_data)
        
        assert stock is not None
        assert isinstance(stock, StockModel)
        assert stock.symbol == 'AAPL'
    
    def test_create_stock_invalid(self):
        """Test factory method with invalid data."""
        invalid_data = {'symbol': '', 'name': '', 'sector': ''}
        stock = create_stock(invalid_data)
        
        assert stock is None


class TestStockModelEdgeCases:
    """Test edge cases and error handling."""
    
    def test_negative_prices(self):
        """Test handling of negative prices."""
        stock = StockModel(symbol='TEST', target_price=100.0)
        stock.update_price(-10.0)
        
        # Should still calculate, even though negative prices are unusual
        assert stock.current_price == -10.0
        assert stock.price_difference == -110.0
    
    def test_very_large_prices(self):
        """Test handling of very large prices."""
        stock = StockModel(symbol='TEST', target_price=1000000.0)
        stock.update_price(1000000.0)
        
        assert stock.current_price == 1000000.0
        assert stock.price_difference == 0.0
    
    def test_string_representations(self, sample_stock_data):
        """Test that object can be converted to string."""
        stock = StockModel(**sample_stock_data)
        
        # Should not raise an exception
        str_repr = str(stock)
        assert 'StockModel' in str_repr or 'AAPL' in str_repr
