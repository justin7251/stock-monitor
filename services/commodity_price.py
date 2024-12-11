import yfinance as yf
import logging
from typing import Optional, Dict, Any
from functools import lru_cache

def get_commodity_price(symbol: str) -> Optional[float]:
    """
    Retrieve commodity price using Yahoo Finance
    
    :param symbol: Commodity ticker symbol
    :return: Current commodity price or None
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Mapping for common commodity symbols
        commodity_map = {
            'GOLD': 'GC=F',    # Gold Futures
            'SILVER': 'SI=F',  # Silver Futures
            'COPPER': 'HG=F',  # Copper Futures
            'CRUDE': 'CL=F',   # Crude Oil Futures
            'NATGAS': 'NG=F',  # Natural Gas Futures
            'WHEAT': 'ZW=F',   # Wheat Futures
            'CORN': 'ZC=F',    # Corn Futures
            'COFFEE': 'KC=F'   # Coffee Futures
        }
        
        # Use mapped symbol or original symbol
        yahoo_symbol = commodity_map.get(symbol.upper(), symbol)
        
        # Fetch commodity data
        commodity = yf.Ticker(yahoo_symbol)
        price_history = commodity.history(period="1d")
        
        if not price_history.empty:
            return float(price_history['Close'].iloc[-1])
        
        logger.warning(f"No price data found for {symbol}")
        return None
    
    except Exception as e:
        logger.error(f"Error fetching commodity price for {symbol}: {e}")
        return None

def get_commodity_details(symbol: str) -> Dict[str, Any]:
    """
    Retrieve comprehensive commodity details
    
    :param symbol: Commodity ticker symbol
    :return: Dictionary of commodity details
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Mapping for common commodity symbols
        commodity_map = {
            'GOLD': 'GC=F',    # Gold Futures
            'SILVER': 'SI=F',  # Silver Futures
            'COPPER': 'HG=F',  # Copper Futures
            'CRUDE': 'CL=F',   # Crude Oil Futures
            'NATGAS': 'NG=F',  # Natural Gas Futures
            'WHEAT': 'ZW=F',   # Wheat Futures
            'CORN': 'ZC=F',    # Corn Futures
            'COFFEE': 'KC=F'   # Coffee Futures
        }
        
        # Use mapped symbol or original symbol
        yahoo_symbol = commodity_map.get(symbol.upper(), symbol)
        
        commodity = yf.Ticker(yahoo_symbol)
        info = commodity.info
        
        return {
            'symbol': symbol,
            'name': info.get('shortName', symbol),
            'current_price': get_commodity_price(symbol),
            'exchange': info.get('exchange', 'Futures'),
            '52_week_high': info.get('fiftyTwoWeekHigh'),
            '52_week_low': info.get('fiftyTwoWeekLow')
        }
    
    except Exception as e:
        logger.error(f"Error fetching commodity details for {symbol}: {e}")
        return {'symbol': symbol}
