from .connection import get_db, execute_db_query
from .init_db import init_db, populate_default_commodities

# Export key database functions for easy importing
__all__ = [
    'get_db',
    'execute_db_query',
    'init_db',
    'populate_default_commodities'
]

# Optional: Add logging or initialization checks
def validate_database_connection():
    """
    Validate database connection and basic setup
    """
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Check if essential tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        required_tables = {'stocks', 'commodities'}
        existing_tables = {table[0] for table in tables}
        
        missing_tables = required_tables - existing_tables
        
        if missing_tables:
            print(f"Warning: Missing tables: {missing_tables}")
            return False
        
        return True
    except Exception as e:
        print(f"Database validation error: {e}")
        return False

# Perform validation on import
validate_database_connection()
