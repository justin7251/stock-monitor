from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class CommodityModel:
    """
    Detailed Commodity Model with comprehensive attributes
    """
    id: Optional[int] = None
    name: str = ''
    symbol: str = ''
    commodity_type: str = ''
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
        Convert commodity model to dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'commodity_type': self.commodity_type,
            'description': self.description,
            'target_price': self.target_price,
            'current_price': self.current_price,
            'price_difference': self.price_difference,
            'price_percentage': self.price_percentage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CommodityModel':
        """
        Create a commodity model from a dictionary
        """
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            symbol=data.get('symbol', ''),
            commodity_type=data.get('commodity_type', ''),
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

# Utility functions
def validate_commodity_data(data: Dict[str, Any]) -> bool:
    """
    Validate commodity data before model creation
    """
    required_fields = ['name', 'symbol', 'commodity_type']
    return all(data.get(field) for field in required_fields)

def create_commodity(data: Dict[str, Any]) -> Optional[CommodityModel]:
    """
    Factory method to create a commodity model with validation
    """
    if validate_commodity_data(data):
        return CommodityModel.from_dict(data)
    return None

# Export key components
__all__ = [
    'CommodityModel', 
    'validate_commodity_data', 
    'create_commodity'
]
