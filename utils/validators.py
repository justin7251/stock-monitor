import re

def validate_stock_symbol(symbol):
    """
    Validate stock symbol format
    """
    if not symbol:
        return False
    
    # Alphanumeric characters, 1-5 characters long
    return bool(re.match(r'^[A-Z0-9]{1,5}$', symbol))

def validate_price(price):
    """
    Validate price input
    """
    try:
        price_float = float(price)
        return price_float > 0
    except (ValueError, TypeError):
        return False

def validate_name(name):
    """
    Validate name input
    """
    if not name:
        return False
    
    # Ensure name is not too short or too long
    return 2 <= len(name) <= 100
