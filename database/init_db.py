from .connection import get_db  # Assuming get_db now returns a MySQL connection
import mysql.connector

def init_db():
    """
    Initialize the MySQL database and create tables
    """
    db = get_db()
    cursor = db.cursor()

    try:
        # Create stocks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                symbol VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                sector VARCHAR(255) NOT NULL,
                description TEXT,
                target_price DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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
                target_price DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')

        db.commit()
    except mysql.connector.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        cursor.close()


def populate_default_commodities():
    """
    Populate default commodities if table is empty
    """
    db = get_db()
    cursor = db.cursor()

    default_commodities = [
        ('Gold', 'GOLD', 'Metal', 'Precious metal', 1800.00),
        ('Silver', 'SILVER', 'Metal', 'Industrial metal', 25.00),
        ('Copper', 'COPPER', 'Metal', 'Industrial metal', 4.00),
        ('Oil', 'OIL', 'Energy', 'Crude oil', 70.00),
        ('Gas', 'GAS', 'Energy', 'Natural gas', 3.00),
        ('Wheat', 'WHEAT', 'Agriculture', 'Grain', 250.00),
        ('Corn', 'CORN', 'Agriculture', 'Grain', 230.00),
        ('Soybeans', 'SOYBEANS', 'Agriculture', 'Oilseed', 1300.00),
    ]

    try:
        cursor.execute('SELECT COUNT(*) FROM commodities')
        if cursor.fetchone()[0] == 0:
            for commodity in default_commodities:
                cursor.execute('''
                    INSERT IGNORE INTO commodities 
                    (name, symbol, commodity_type, description, target_price) 
                    VALUES (%s, %s, %s, %s, %s)
                ''', commodity)
            
            db.commit()
            print("Default commodities populated successfully.")
        else:
            print("Commodities table already populated.")
    except mysql.connector.Error as e:
        print(f"Error populating commodities: {e}")
    finally:
        cursor.close()
