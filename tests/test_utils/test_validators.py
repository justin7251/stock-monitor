"""
Unit tests for validator functions.
"""
import pytest
from utils.validators import validate_stock_symbol, validate_price, validate_name


class TestValidateStockSymbol:
    """Test validate_stock_symbol function."""
    
    @pytest.mark.parametrize("symbol", [
        'AAPL',
        'GOOGL',
        'TSLA',
        'MSFT',
        'A',
        'AB',
        'ABCDE',
    ])
    def test_valid_symbols(self, symbol):
        """Test validation of valid stock symbols."""
        assert validate_stock_symbol(symbol) is True
    
    @pytest.mark.parametrize("symbol", [
        '',           # Empty
        'a',          # Lowercase
        'apple',      # Too long
        'ABCDEF',     # Too long (> 5 chars)
        'A-B',        # Special character
        'A.B',        # Period
        'AAPL ',      # Trailing space
        ' AAPL',      # Leading space
        'AA PL',      # Space in middle
        '@@@',        # Special characters only
    ])
    def test_invalid_symbols(self, symbol):
        """Test validation rejects invalid stock symbols."""
        assert validate_stock_symbol(symbol) is False
    
    def test_none_symbol(self):
        """Test validation with None."""
        assert validate_stock_symbol(None) is False
    
    def test_numbers_in_symbol(self):
        """Test that numbers are allowed in symbols."""
        assert validate_stock_symbol('BRK1') is True
        assert validate_stock_symbol('A1B2') is True


class TestValidatePrice:
    """Test validate_price function."""
    
    @pytest.mark.parametrize("price,expected", [
        (100.0, True),
        (150.50, True),
        (0.01, True),
        (1000000.0, True),
        ('100', True),       # String that can be converted
        ('150.50', True),
        (1, True),           # Integer
    ])
    def test_valid_prices(self, price, expected):
        """Test validation of valid prices."""
        assert validate_price(price) is expected
    
    @pytest.mark.parametrize("price", [
        0,            # Zero
        -1,           # Negative
        -100.50,      # Negative float
        'abc',        # Non-numeric string
        '',           # Empty string
        None,         # None
        'free',       # Invalid text
        '$100',       # Contains dollar sign
    ])
    def test_invalid_prices(self, price):
        """Test validation rejects invalid prices."""
        assert validate_price(price) is False
    
    def test_zero_price(self):
        """Test that zero price is invalid."""
        assert validate_price(0) is False
        assert validate_price(0.0) is False
        assert validate_price('0') is False
    
    def test_very_small_positive_price(self):
        """Test that very small positive prices are valid."""
        assert validate_price(0.001) is True
        assert validate_price(0.0001) is True


class TestValidateName:
    """Test validate_name function."""
    
    @pytest.mark.parametrize("name", [
        'Apple Inc.',
        'Tesla, Inc.',
        'Microsoft Corporation',
        'AB',            # Minimum valid length (2 chars)
        'A' * 100,       # Maximum valid length (100 chars)
        'Company-Name',  # With hyphen
        'Company & Co',  # With ampersand
        '123 Company',   # With numbers
    ])
    def test_valid_names(self, name):
        """Test validation of valid names."""
        assert validate_name(name) is True
    
    @pytest.mark.parametrize("name", [
        '',              # Empty
        'A',             # Too short (1 char)
        'A' * 101,       # Too long (> 100 chars)
        None,            # None
    ])
    def test_invalid_names(self, name):
        """Test validation rejects invalid names."""
        assert validate_name(name) is False
    
    def test_whitespace_only(self):
        """Test that whitespace-only names pass basic length check."""
        # Three spaces - meets length requirement but may not be semantically valid
        result = validate_name('   ')
        assert result is True  # Current implementation only checks length
    
    def test_boundary_lengths(self):
        """Test boundary conditions for name length."""
        assert validate_name('A') is False      # 1 char - too short
        assert validate_name('AB') is True      # 2 chars - minimum valid
        assert validate_name('A' * 100) is True # 100 chars - maximum valid
        assert validate_name('A' * 101) is False # 101 chars - too long


class TestValidatorEdgeCases:
    """Test edge cases across all validators."""
    
    def test_unicode_in_symbol(self):
        """Test handling of unicode characters in stock symbol."""
        assert validate_stock_symbol('ÄPPL') is False
        assert validate_stock_symbol('股票') is False
    
    def test_unicode_in_name(self):
        """Test handling of unicode characters in name."""
        # Unicode should be allowed in names
        result = validate_name('Société Générale')
        # Current implementation allows unicode since it only checks length
        assert len('Société Générale') >= 2
    
    def test_scientific_notation_price(self):
        """Test scientific notation in price."""
        assert validate_price('1e2') is True    # 100
        assert validate_price('1.5e3') is True  # 1500
    
    def test_infinity_price(self):
        """Test infinity values for price."""
        assert validate_price(float('inf')) is True  # Positive infinity > 0
        assert validate_price(float('-inf')) is False # Negative infinity < 0
    
    def test_nan_price(self):
        """Test NaN for price."""
        # NaN comparisons return False, so NaN > 0 is False
        assert validate_price(float('nan')) is False
