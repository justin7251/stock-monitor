"""
Unit tests for home route.
"""
import pytest
from unittest.mock import patch


class TestHomeRoute:
    """Test home/dashboard route."""
    
    @patch('routes.home.execute_db_query')
    def test_home_route_success(self, mock_db, client):
        """Test successful home page rendering."""
        # Mock returning some data
        mock_db.return_value = []
        
        response = client.get('/')
        
        assert response.status_code == 200
    
    def test_home_route_loads(self, client):
        """Test that home route loads without errors."""
        response = client.get('/')
        
        # Should at least return a valid response
        assert response.status_code in [200, 302]  # 200 or redirect
