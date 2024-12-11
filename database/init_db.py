from .connection import get_db
import sqlite3

def init_db():
    """
    Initialize the database and create tables
    """
    db = get_db()
    cursor = db.cursor()
    
    # Create stocks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            sector TEXT NOT NULL,
            description TEXT,
            target_price REAL NOT NULL
        )
    ''')
    
    # Create commodities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commodities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            symbol TEXT NOT NULL,
            commodity_type TEXT NOT NULL,
            description TEXT,
            target_price REAL NOT NULL
        )
    ''')
    
    db.commit()

def populate_default_commodities():
    """
    Populate default commodities if table is empty
    """
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM commodities')
    if cursor.fetchone()[0] == 0:
        default_commodities = [
            ('Gold', 'GOLD', 'Metal', 'Precious metal', 0.00),
            ('Silver', 'SILVER', 'Metal', 'Industrial metal', 0.00),
            ('Copper', 'COPPER', 'Metal', 'Industrial metal', 0.00),
            ('Oil', 'OIL', 'Energy', 'Crude oil', 0.00),
            ('Gas', 'GAS', 'Energy', 'Natural gas', 0.00),
            ('Wheat', 'WHEAT', 'Agriculture', 'Grain', 0.00),
            ('Corn', 'CORN', 'Agriculture', 'Grain', 0.00),
            ('Soybeans', 'SOYBEANS', 'Agriculture', 'Oilseed', 0.00),
            # Add more default commodities
        ]
        
        cursor.executemany('''
            INSERT INTO commodities 
            (name, symbol, commodity_type, description, target_price) 
            VALUES (?, ?, ?, ?, ?)
        ''', default_commodities)
        
        db.commit()
