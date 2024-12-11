import yfinance as yf
import logging
from typing import Optional, Dict, Any
from functools import lru_cache

class StockMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    @lru_cache(maxsize=100)
    def get_stock_price(self, symbol: str) -> Optional[float]:
        """
        Retrieve current stock price using Yahoo Finance
        
        :param symbol: Stock ticker symbol
        :return: Current stock price or None
        """
        try:
            # Fetch stock data
            stock = yf.Ticker(symbol)
            
            # Get current price
            current_price = stock.history(period="1d")['Close']
            
            if not current_price.empty:
                return float(current_price.iloc[-1])
            
            self.logger.warning(f"No price data found for {symbol}")
            return None
        
        except Exception as e:
            self.logger.error(f"Error fetching stock price for {symbol}: {e}")
            return None
    
    def get_stock_details(self, symbol: str) -> Dict[str, Any]:
        """
        Retrieve comprehensive stock details
        
        :param symbol: Stock ticker symbol
        :return: Dictionary of stock details
        """
        try:
            stock = yf.Ticker(symbol)
            
            # Fetch key information
            info = stock.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'current_price': self.get_stock_price(symbol),
                'sector': info.get('sector', 'Unknown'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'dividend_yield': info.get('dividendYield'),
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow')
            }
        
        except Exception as e:
            self.logger.error(f"Error fetching stock details for {symbol}: {e}")
            return {'symbol': symbol}
