import yfinance as yf
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_yahoo_finance_api():
    """
    Comprehensive test of Yahoo Finance data retrieval
    """
    test_scenarios = {
        'Stocks': ['AAPL', 'GOOGL', 'MSFT', 'AMZN'],
        'Commodities': ['GC=F', 'CL=F', 'NG=F', 'ZW=F']
    }
    
    results = []
    
    for category, symbols in test_scenarios.items():
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                
                # Fetch historical data
                history = ticker.history(period="1d")
                
                if not history.empty:
                    current_price = history['Close'].iloc[-1]
                    
                    results.append({
                        'category': category,
                        'symbol': symbol,
                        'status': 'PASSED',
                        'current_price': float(current_price)
                    })
                else:
                    results.append({
                        'category': category,
                        'symbol': symbol,
                        'status': 'FAILED',
                        'error': 'No price data available'
                    })
            
            except Exception as e:
                results.append({
                    'category': category,
                    'symbol': symbol,
                    'status': 'FAILED',
                    'error': str(e)
                })
    
    return results

def print_yahoo_finance_debug_results():
    """
    Print detailed Yahoo Finance API debugging results
    """
    print("\n--- Yahoo Finance API Debug ---")
    
    results = test_yahoo_finance_api()
    
    for result in results:
        print(f"\nCategory: {result['category']}")
        print(f"Symbol: {result['symbol']}")
        print(f"Status: {result['status']}")
        
        if result['status'] == 'PASSED':
            print(f"Current Price: {result['current_price']}")
        else:
            print(f"Error: {result.get('error', 'Unknown Error')}")

# Standalone debug runner
if __name__ == '__main__':
    print_yahoo_finance_debug_results()
