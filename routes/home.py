from flask import Blueprint, render_template
from database.connection import execute_db_query
from models import StockModel, CommodityModel
from services import StockMonitor, get_commodity_price

home_bp = Blueprint('home', __name__)
stock_monitor = StockMonitor()

@home_bp.route('/')
def home():
    try:
        # Fetch stocks
        stock_data = execute_db_query('SELECT * FROM stocks', fetch=True)
        stocks = [
            StockModel(
                id=row['id'],
                symbol=row['symbol'],
                name=row['name'],
                sector=row['sector'],
                description=row['description'],
                target_price=row['target_price']
            ) for row in stock_data
        ]
        
        # Fetch commodities
        commodity_data = execute_db_query('SELECT * FROM commodities', fetch=True)
        commodities = [
            CommodityModel(
                id=row['id'],
                name=row['name'],
                symbol=row['symbol'],
                commodity_type=row['commodity_type'],
                description=row['description'],
                target_price=row['target_price']
            ) for row in commodity_data
        ]
        
        # Process stocks and commodities
        for stock in stocks:
            current_price = stock_monitor.get_stock_price(stock.symbol)
            stock.update_price(current_price)
        
        for commodity in commodities:
            current_price = get_commodity_price(commodity.symbol)
            commodity.update_price(current_price)
        
        # Calculate summary metrics
        summary = {
            'total_stocks': len(stocks),
            'total_commodities': len(commodities),
            'stocks_above_target': len([s for s in stocks if s.is_above_target()]),
            'commodities_above_target': len([c for c in commodities if c.is_above_target()])
        }
        
        return render_template('home.html', 
                               stocks=stocks, 
                               commodities=commodities,
                               summary=summary)
    
    except Exception as e:
        print(f"Error in home route: {e}")
        return render_template('home.html', 
                               stocks=[], 
                               commodities=[],
                               summary={
                                   'total_stocks': 0,
                                   'total_commodities': 0,
                                   'stocks_above_target': 0,
                                   'commodities_above_target': 0
                               },
                               error=str(e))
