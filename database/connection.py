import sqlite3
from flask import g, current_app

def get_db():
    """
    Get or create a database connection
    """
    if 'db' not in g:
        # Use row_factory to allow column access by name
        g.db = sqlite3.connect(current_app.config.get('DATABASE', 'stock_prices.db'))
        g.db.row_factory = sqlite3.Row
    return g.db

def execute_db_query(query, params=None, fetch=False):
    """
    Execute a database query with optional parameters
    
    :param query: SQL query string
    :param params: Query parameters (optional)
    :param fetch: Whether to fetch results
    :return: Query results or None
    """
    db = get_db()
    cursor = db.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        db.commit()
        
        if fetch:
            # Convert sqlite3.Row to list of dictionaries
            return [dict(row) for row in cursor.fetchall()]
        
        return None
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        db.rollback()
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        db.rollback()
        return None
