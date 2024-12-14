from .connection import get_db  # Assuming get_db now returns a MySQL connection
import mysql.connector

def init_db():
    """
    Initialize the MySQL database and create tables
    """
    db = get_db()
    cursor = db.cursor()

    # Create stocks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            sector VARCHAR(255) NOT NULL,
            description TEXT,
            target_price DECIMAL(10, 2) NOT NULL
        )
    ''')

    # Create commodities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commodities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            symbol VARCHAR(255) NOT NULL,
            commodity_type VARCHAR(255) NOT NULL,
            description TEXT,
            target_price DECIMAL(10, 2) NOT NULL
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
            VALUES (%s, %s, %s, %s, %s)
        ''', default_commodities)
        
        db.commit()