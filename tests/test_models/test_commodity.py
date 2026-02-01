"""
Unit tests for the CommodityModel class.
"""
import pytest
from datetime import datetime
from models.commodity import CommodityModel, validate_commodity_data, create_commodity


class TestCommodityModelInitialization:
    """Test CommodityModel initialization and default values."""
    
    def test_empty_initialization(self):
        """Test creating a commodity with default values."""
        commodity = CommodityModel()
        
        assert commodity.id is None
        assert commodity.name == ''
        assert commodity.symbol == ''
        assert commodity.commodity_type == ''
        assert commodity.description is None
        assert commodity.target_price == 0.0
        assert commodity.current_price is None
        assert commodity.price_difference is None
        assert commodity.price_percentage is None
        assert isinstance(commodity.created_at, datetime)
        assert commodity.updated_at is None
        assert commodity.historical_prices == []
    
    def test_initialization_with_data(self, sample_commodity_data):
        """Test creating a commodity with provided data."""
        commodity = CommodityModel(**sample_commodity_data)
        
        assert commodity.id == 1
        assert commodity.name == 'Gold'
        assert commodity.symbol == 'GC=F'
        assert commodity.commodity_type == 'Metals'
        assert commodity.description == 'Precious metal'
        assert commodity.target_price == 2000.00


class TestCommodityModelPriceUpdates:
    """Test price update functionality."""
    
    def test_update_price_basic(self, sample_commodity_data):
        """Test basic price update."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(2050.00)
        
        assert commodity.current_price == 2050.00
        assert commodity.updated_at is not None
        assert len(commodity.historical_prices) == 1
        assert commodity.historical_prices[0]['price'] == 2050.00
    
    def test_update_price_calculations(self, sample_commodity_data):
        """Test price difference and percentage calculations."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(2100.00)
        
        assert commodity.price_difference == 100.00
        assert commodity.price_percentage == 5.0
    
    def test_update_price_below_target(self, sample_commodity_data):
        """Test price update below target."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(1900.00)
        
        assert commodity.price_difference == -100.00
        assert commodity.price_percentage == -5.0
    
    def test_update_price_multiple_times(self, sample_commodity_data):
        """Test multiple price updates track history."""
        commodity = CommodityModel(**sample_commodity_data)
        
        commodity.update_price(2000.00)
        commodity.update_price(2050.00)
        commodity.update_price(2100.00)
        
        assert len(commodity.historical_prices) == 3
        assert commodity.current_price == 2100.00


class TestCommodityModelSerialization:
    """Test to_dict and from_dict methods."""
    
    def test_to_dict(self, sample_commodity_data):
        """Test converting commodity model to dictionary."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(2050.00)
        
        commodity_dict = commodity.to_dict()
        
        assert commodity_dict['id'] == 1
        assert commodity_dict['name'] == 'Gold'
        assert commodity_dict['symbol'] == 'GC=F'
        assert commodity_dict['commodity_type'] == 'Metals'
        assert commodity_dict['current_price'] == 2050.00
        assert 'created_at' in commodity_dict
        assert 'updated_at' in commodity_dict
    
    def test_from_dict(self, sample_commodity_data):
        """Test creating commodity model from dictionary."""
        commodity = CommodityModel.from_dict(sample_commodity_data)
        
        assert commodity.id == 1
        assert commodity.name == 'Gold'
        assert commodity.symbol == 'GC=F'
        assert commodity.target_price == 2000.00
    
    def test_round_trip_serialization(self, sample_commodity_data):
        """Test that to_dict and from_dict are reversible."""
        original = CommodityModel(**sample_commodity_data)
        original.update_price(2050.00)
        
        commodity_dict = original.to_dict()
        reconstructed = CommodityModel.from_dict(commodity_dict)
        
        assert reconstructed.name == original.name
        assert reconstructed.symbol == original.symbol
        assert reconstructed.current_price == original.current_price


class TestCommodityModelBusinessLogic:
    """Test business logic methods."""
    
    def test_is_above_target_true(self, sample_commodity_data):
        """Test is_above_target when price is above target."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(2100.00)
        
        assert commodity.is_above_target() is True
    
    def test_is_above_target_false(self, sample_commodity_data):
        """Test is_above_target when price is below target."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(1900.00)
        
        assert commodity.is_above_target() is False
    
    def test_is_above_target_equal(self, sample_commodity_data):
        """Test is_above_target when price equals target."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(2000.00)
        
        assert commodity.is_above_target() is False
    
    def test_get_price_status_above(self, sample_commodity_data):
        """Test get_price_status for above target."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(2100.00)
        
        assert commodity.get_price_status() == "Above Target"
    
    def test_get_price_status_below(self, sample_commodity_data):
        """Test get_price_status for below target."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(1900.00)
        
        assert commodity.get_price_status() == "Below Target"
    
    def test_get_price_status_at_target(self, sample_commodity_data):
        """Test get_price_status when at target."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(2000.00)
        
        assert commodity.get_price_status() == "At Target"
    
    def test_get_price_status_no_data(self, sample_commodity_data):
        """Test get_price_status with no price data."""
        commodity = CommodityModel(**sample_commodity_data)
        
        assert commodity.get_price_status() == "No Price Data"


class TestCommodityValidationFunctions:
    """Test validation helper functions."""
    
    def test_validate_commodity_data_valid(self, sample_commodity_data):
        """Test validation with valid data."""
        assert validate_commodity_data(sample_commodity_data) is True
    
    def test_validate_commodity_data_missing_name(self, sample_commodity_data):
        """Test validation with missing name."""
        data = sample_commodity_data.copy()
        data['name'] = ''
        
        assert validate_commodity_data(data) is False
    
    def test_validate_commodity_data_missing_symbol(self, sample_commodity_data):
        """Test validation with missing symbol."""
        data = sample_commodity_data.copy()
        data['symbol'] = ''
        
        assert validate_commodity_data(data) is False
    
    def test_validate_commodity_data_missing_type(self, sample_commodity_data):
        """Test validation with missing commodity type."""
        data = sample_commodity_data.copy()
        data['commodity_type'] = ''
        
        assert validate_commodity_data(data) is False
    
    def test_create_commodity_valid(self, sample_commodity_data):
        """Test factory method with valid data."""
        commodity = create_commodity(sample_commodity_data)
        
        assert commodity is not None
        assert isinstance(commodity, CommodityModel)
        assert commodity.name == 'Gold'
    
    def test_create_commodity_invalid(self):
        """Test factory method with invalid data."""
        invalid_data = {'name': '', 'symbol': '', 'commodity_type': ''}
        commodity = create_commodity(invalid_data)
        
        assert commodity is None


class TestCommodityTypes:
    """Test different commodity types."""
    
    @pytest.mark.parametrize("commodity_type", [
        "Energy",
        "Metals",
        "Agriculture",
        "Livestock"
    ])
    def test_different_commodity_types(self, commodity_type):
        """Test creating commodities with different types."""
        commodity = CommodityModel(
            name="Test Commodity",
            symbol="TEST",
            commodity_type=commodity_type,
            target_price=100.0
        )
        
        assert commodity.commodity_type == commodity_type
    
    def test_custom_commodity_type(self):
        """Test that custom commodity types are allowed."""
        commodity = CommodityModel(
            name="Bitcoin",
            symbol="BTC",
            commodity_type="Cryptocurrency",
            target_price=50000.0
        )
        
        assert commodity.commodity_type == "Cryptocurrency"


class TestCommodityModelEdgeCases:
    """Test edge cases and error handling."""
    
    def test_zero_price(self, sample_commodity_data):
        """Test handling of zero price."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(0.0)
        
        assert commodity.current_price == 0.0
    
    def test_very_high_commodity_price(self):
        """Test handling of extremely high prices (e.g., precious metals)."""
        commodity = CommodityModel(
            name="Rare Element",
            symbol="RARE",
            commodity_type="Metals",
            target_price=1000000.0
        )
        commodity.update_price(1050000.0)
        
        assert commodity.price_difference == 50000.0
        assert commodity.price_percentage == 5.0
    
    def test_none_price_update(self, sample_commodity_data):
        """Test updating with None price."""
        commodity = CommodityModel(**sample_commodity_data)
        commodity.update_price(None)
        
        assert commodity.current_price is None
        assert commodity.price_difference is None
        assert commodity.price_percentage is None
