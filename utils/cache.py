from functools import wraps
from flask import current_app
import time

class SimpleCache:
    """
    Simple in-memory cache implementation
    """
    def __init__(self, timeout=300):  # 5 minutes default timeout
        self._cache = {}
        self._timeout = timeout
    
    def set(self, key, value):
        """
        Set a value in the cache
        """
        self._cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
    
    def get(self, key):
        """
        Get a value from the cache
        """
        cached_item = self._cache.get(key)
        
        if cached_item:
            # Check if cache has expired
            if time.time() - cached_item['timestamp'] < self._timeout:
                return cached_item['value']
            else:
                # Remove expired cache
                del self._cache[key]
        
        return None
    
    def clear(self, key=None):
        """
        Clear specific or all cache entries
        """
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()

def cached(timeout=300):
    """
    Decorator for caching function results
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache if not exists
            if not hasattr(current_app, 'simple_cache'):
                current_app.simple_cache = SimpleCache(timeout)
            
            # Generate a cache key
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            
            # Try to get from cache
            cached_result = current_app.simple_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Call the function
            result = func(*args, **kwargs)
            
            # Cache the result
            current_app.simple_cache.set(cache_key, result)
            
            return result
        return wrapper
    return decorator
