from flask import Blueprint, render_template, request, redirect, url_for
from database.connection import execute_db_query
from models import StockModel
from services import StockMonitor
from utils import validate_stock_symbol, validate_name, validate_price
import sqlite3

stocks_bp = Blueprint('stocks', __name__, url_prefix='/stocks')
stock_monitor = StockMonitor()

@stocks_bp.route('/')
def stock_list():
    try:
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
        
        # Update prices
        for stock in stocks:
            current_price = stock_monitor.get_stock_price(stock.symbol)
            stock.update_price(current_price)
        
        return render_template('stocks.html', stocks=stocks)
    except Exception as e:
        return render_template('stocks.html', stocks=[], error=str(e))

@stocks_bp.route('/add', methods=['GET', 'POST'])
def stock_add():
    if request.method == 'POST':
        try:
            symbol = request.form.get('symbol', '').upper()
            name = request.form.get('name', '')
            sector = request.form.get('sector', '')
            description = request.form.get('description', '')
            target_price = request.form.get('target_price', '')
            
            # Validate inputs
            errors = []
            if not validate_stock_symbol(symbol):
                errors.append("Invalid stock symbol")
            if not validate_name(name):
                errors.append("Invalid company name")
            if not validate_price(target_price):
                errors.append("Invalid target price")
            
            if errors:
                return render_template('add_stock.html', errors=errors)
            
            execute_db_query('''
                INSERT INTO stocks 
                (symbol, name, sector, description, target_price) 
                VALUES (?, ?, ?, ?, ?)
            ''', (symbol, name, sector, description, float(target_price)))
            
            return redirect(url_for('stocks.stock_list'))
        
        except sqlite3.IntegrityError:
            return render_template('add_stock.html', error="Stock symbol already exists")
        except Exception as e:
            return render_template('add_stock.html', error=str(e))
    
    return render_template('add_stock.html')

@stocks_bp.route('/delete/<int:stock_id>', methods=['POST'])
def stock_delete(stock_id):
    try:
        execute_db_query('DELETE FROM stocks WHERE id = ?', (stock_id,))
        return redirect(url_for('stocks.stock_list'))
    except Exception as e:
        print(f"Error deleting stock: {e}")
        return redirect(url_for('stocks.stock_list'))
