"""
Unit tests for stock routes.
"""
import pytest
from unittest.mock import patch, MagicMock


class TestStockListRoute:
    """Test stock list route."""
    
    @patch('routes.stocks.execute_db_query')
    @patch('routes.stocks.stock_monitor')
    def test_stock_list_success(self, mock_monitor, mock_db, client):
        """Test successful stock list rendering."""
        # Mock database response
        mock_db.return_value = [
            {
                'id': 1,
                'symbol': 'AAPL',
                'name': 'Apple Inc.',
                'sector': 'Technology',
                'description': 'Tech company',
                'target_price': 150.00
            }
        ]
        
        # Mock stock monitor
        mock_monitor.get_stock_price.return_value = 155.50
        
        response = client.get('/stocks/')
        
        assert response.status_code == 200
        assert b'AAPL' in response.data
    
    @patch('routes.stocks.execute_db_query')
    def test_stock_list_empty(self, mock_db, client):
        """Test stock list with no stocks."""
        mock_db.return_value = []
        
        response = client.get('/stocks/')
        
        assert response.status_code == 200
    
    @patch('routes.stocks.execute_db_query')
    def test_stock_list_error(self, mock_db, client):
        """Test stock list with database error."""
        mock_db.side_effect = Exception("Database error")
        
        response = client.get('/stocks/')
        
        assert response.status_code == 200  # Should still render with error message


class TestStockAddRoute:
    """Test stock add route."""
    
    def test_stock_add_get(self, client):
        """Test GET request to add stock form."""
        response = client.get('/stocks/add')
        
        assert response.status_code == 200
    
    @patch('routes.stocks.execute_db_query')
    def test_stock_add_post_success(self, mock_db, client):
        """Test successful stock addition."""
        mock_db.return_value = None  # Successful insert
        
        response = client.post('/stocks/add', data={
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'sector': 'Technology',
            'description': 'Tech company',
            'target_price': '150.00'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    @patch('routes.stocks.execute_db_query')
    def test_stock_add_invalid_symbol(self, mock_db, client):
        """Test adding stock with invalid symbol."""
        response = client.post('/stocks/add', data={
            'symbol': 'invalid',  # Lowercase
            'name': 'Test Company',
            'sector': 'Technology',
            'target_price': '150.00'
        })
        
        assert response.status_code == 200
        assert b'Invalid stock symbol' in response.data or b'error' in response.data.lower()
    
    @patch('routes.stocks.execute_db_query')
    def test_stock_add_invalid_price(self, mock_db, client):
        """Test adding stock with invalid price."""
        response = client.post('/stocks/add', data={
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'sector': 'Technology',
            'target_price': 'invalid'
        })
        
        assert response.status_code == 200
        assert b'Invalid target price' in response.data or b'error' in response.data.lower()
    
    @patch('routes.stocks.execute_db_query')
    def test_stock_add_duplicate(self, mock_db, client):
        """Test adding duplicate stock."""
        import sqlite3
        mock_db.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
        
        response = client.post('/stocks/add', data={
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'sector': 'Technology',
            'target_price': '150.00'
        })
        
        assert response.status_code == 200
        assert b'already exists' in response.data


class TestStockDeleteRoute:
    """Test stock delete route."""
    
    @patch('routes.stocks.execute_db_query')
    def test_stock_delete_success(self, mock_db, client):
        """Test successful stock deletion."""
        mock_db.return_value = None
        
        response = client.post('/stocks/delete/1', follow_redirects=True)
        
        assert response.status_code == 200
    
    @patch('routes.stocks.execute_db_query')
    def test_stock_delete_error(self, mock_db, client):
        """Test stock deletion with error."""
        mock_db.side_effect = Exception("Database error")
        
        response = client.post('/stocks/delete/1', follow_redirects=True)
        
        assert response.status_code == 200  # Should redirect even on error
