from flask import Blueprint, render_template, request, redirect, url_for
from database.connection import execute_db_query
from models import CommodityModel
from services import get_commodity_price
from utils import validate_name, validate_price
import sqlite3

commodities_bp = Blueprint('commodities', __name__, url_prefix='/commodities')

@commodities_bp.route('/')
def commodity_list():
    try:
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
        
        # Update prices
        for commodity in commodities:
            current_price = get_commodity_price(commodity.symbol)
            commodity.update_price(current_price)
        
        return render_template('commodities.html', commodities=commodities)
    except Exception as e:
        return render_template('commodities.html', commodities=[], error=str(e))

@commodities_bp.route('/add', methods=['GET', 'POST'])
def commodity_add():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '')
            symbol = request.form.get('symbol', '').upper()
            commodity_type = request.form.get('commodity_type', '')
            description = request.form.get('description', '')
            target_price = request.form.get('target_price', '')
            
            # Validate inputs
            errors = []
            if not validate_name(name):
                errors.append("Invalid commodity name")
            if not validate_price(target_price):
                errors.append("Invalid target price")
            
            if errors:
                return render_template('add_commodity.html', errors=errors)
            
            execute_db_query('''
                INSERT INTO commodities 
                (name, symbol, commodity_type, description, target_price) 
                VALUES (?, ?, ?, ?, ?)
            ''', (name, symbol, commodity_type, description, float(target_price)))
            
            return redirect(url_for('commodities.commodity_list'))
        
        except sqlite3.IntegrityError:
            return render_template('add_commodity.html', error="Commodity already exists")
        except Exception as e:
            return render_template('add_commodity.html', error=str(e))
    
    return render_template('add_commodity.html')

@commodities_bp.route('/delete/<int:commodity_id>', methods=['POST'])
def commodity_delete(commodity_id):
    try:
        execute_db_query('DELETE FROM commodities WHERE id = ?', (commodity_id,))
        return redirect(url_for('commodities.commodity_list'))
    except Exception as e:
        print(f"Error deleting commodity: {e}")
        return redirect(url_for('commodities.commodity_list'))
