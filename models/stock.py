from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class StockModel:
    """
    Detailed Stock Model with comprehensive attributes
    """
    id: Optional[int] = None
    symbol: str = ''
    name: str = ''
    sector: str = ''
    description: Optional[str] = None
    
    # Price-related attributes
    target_price: float = 0.0
    current_price: Optional[float] = None
    price_difference: Optional[float] = None
    price_percentage: Optional[float] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    # Additional tracking
    historical_prices: List[Dict[str, Any]] = field(default_factory=list)
    
    def update_price(self, current_price: float):
        """
        Update current price and calculate price metrics
        """
        self.current_price = current_price
        self.updated_at = datetime.now()
        
        # Track historical prices
        if current_price:
            self.historical_prices.append({
                'price': current_price,
                'timestamp': self.updated_at
            })
        
        # Calculate price metrics safely
        if self.target_price and current_price:
            try:
                self.price_difference = current_price - self.target_price
                self.price_percentage = (self.price_difference / self.target_price) * 100
            except (TypeError, ZeroDivisionError):
                self.price_difference = None
                self.price_percentage = None
        else:
            self.price_difference = None
            self.price_percentage = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert stock model to dictionary
        """
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'sector': self.sector,
            'description': self.description,
            'target_price': self.target_price,
            'current_price': self.current_price,
            'price_difference': self.price_difference,
            'price_percentage': self.price_percentage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StockModel':
        """
        Create a stock model from a dictionary
        """
        return cls(
            id=data.get('id'),
            symbol=data.get('symbol', ''),
            name=data.get('name', ''),
            sector=data.get('sector', ''),
            description=data.get('description'),
            target_price=data.get('target_price', 0.0),
            current_price=data.get('current_price'),
            price_difference=data.get('price_difference'),
            price_percentage=data.get('price_percentage')
        )
    
    def is_above_target(self) -> bool:
        """
        Check if current price is above target price
        """
        return (
            self.current_price is not None and 
            self.target_price is not None and 
            self.current_price > self.target_price
        )
    
    def get_price_status(self) -> str:
        """
        Get a textual representation of price status
        """
        if self.current_price is None:
            return "No Price Data"
        
        if self.is_above_target():
            return "Above Target"
        elif self.current_price < self.target_price:
            return "Below Target"
        else:
            return "At Target"
    
    def calculate_volatility(self, window: int = 5) -> Optional[float]:
        """
        Calculate price volatility based on historical prices
        
        :param window: Number of recent prices to consider
        :return: Volatility percentage or None
        """
        if len(self.historical_prices) < window:
            return None
        
        recent_prices = [entry['price'] for entry in self.historical_prices[-window:]]
        
        try:
            mean_price = sum(recent_prices) / len(recent_prices)
            variance = sum((price - mean_price) ** 2 for price in recent_prices) / len(recent_prices)
            volatility = (variance ** 0.5 / mean_price) * 100
            return volatility
        except (TypeError, ZeroDivisionError):
            return None

# Utility functions
def validate_stock_data(data: Dict[str, Any]) -> bool:
    """
    Validate stock data before model creation
    """
    required_fields = ['symbol', 'name', 'sector']
    return all(data.get(field) for field in required_fields)

def create_stock(data: Dict[str, Any]) -> Optional[StockModel]:
    """
    Factory method to create a stock model with validation
    """
    if validate_stock_data(data):
        return StockModel.from_dict(data)
    return None

# Export key components
__all__ = [
    'StockModel', 
    'validate_stock_data', 
    'create_stock'
]
