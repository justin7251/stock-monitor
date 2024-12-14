import mysql.connector
from mysql.connector import Error
from flask import g, current_app

def get_db():
    """
    Get or create a MySQL database connection
    """
    if 'db' not in g:
        try:
            # Connect to MySQL database
            g.db = mysql.connector.connect(
                host=current_app.config.get('DB_HOST'),
                user=current_app.config.get('DB_USER'),
                password=current_app.config.get('DB_PASSWORD'),
                database=current_app.config.get('DB_NAME')
            )
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            raise
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
    cursor = db.cursor(dictionary=True)  # This makes fetchall return dictionaries instead of tuples
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        db.commit()
        
        if fetch:
            return cursor.fetchall()
        
        return None
    
    except Error as e:
        print(f"Database error: {e}")
        db.rollback()
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        db.rollback()
        return None