"""
Unit tests for commodity routes.
"""
import pytest
from unittest.mock import patch


class TestCommodityListRoute:
    """Test commodity list route."""
    
    @patch('routes.commodities.execute_db_query')
    @patch('routes.commodities.get_commodity_price')
    def test_commodity_list_success(self, mock_price, mock_db, client):
        """Test successful commodity list rendering."""
        mock_db.return_value = [
            {
                'id': 1,
                'name': 'Gold',
                'symbol': 'GC=F',
                'commodity_type': 'Metals',
                'description': 'Precious metal',
                'target_price': 2000.00
            }
        ]
        mock_price.return_value = 2050.00
        
        response = client.get('/commodities/')
        
        assert response.status_code == 200
        assert b'Gold' in response.data
    
    @patch('routes.commodities.execute_db_query')
    def test_commodity_list_empty(self, mock_db, client):
        """Test commodity list with no commodities."""
        mock_db.return_value = []
        
        response = client.get('/commodities/')
        
        assert response.status_code == 200


class TestCommodityAddRoute:
    """Test commodity add route."""
    
    def test_commodity_add_get(self, client):
        """Test GET request to add commodity form."""
        response = client.get('/commodities/add')
        
        assert response.status_code == 200
    
    @patch('routes.commodities.execute_db_query')
    def test_commodity_add_post_success(self, mock_db, client):
        """Test successful commodity addition."""
        mock_db.return_value = None
        
        response = client.post('/commodities/add', data={
            'name': 'Gold',
            'symbol': 'GC=F',
            'commodity_type': 'Metals',
            'description': 'Precious metal',
            'target_price': '2000.00'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    @patch('routes.commodities.execute_db_query')
    def test_commodity_add_invalid_price(self, mock_db, client):
        """Test adding commodity with invalid price."""
        response = client.post('/commodities/add', data={
            'name': 'Gold',
            'symbol': 'GC=F',
            'commodity_type': 'Metals',
            'target_price': 'invalid'
        })
        
        assert response.status_code == 200
        assert b'Invalid target price' in response.data or b'error' in response.data.lower()


class TestCommodityDeleteRoute:
    """Test commodity delete route."""
    
    @patch('routes.commodities.execute_db_query')
    def test_commodity_delete_success(self, mock_db, client):
        """Test successful commodity deletion."""
        mock_db.return_value = None
        
        response = client.post('/commodities/delete/1', follow_redirects=True)
        
        assert response.status_code == 200
