# Stock Monitor 📈

A comprehensive Flask-based web application for monitoring stocks and commodities with real-time price tracking, target price alerts, and portfolio management capabilities.

## ✨ Features

- **Stock Monitoring**: Track multiple stocks with real-time price updates via Yahoo Finance API
- **Commodity Tracking**: Monitor commodities (Energy, Metals, Agriculture, Livestock)
- **Target Price Alerts**: Set target prices and view price differences and percentages
- **Portfolio Dashboard**: Visual overview of all monitored assets
- **Price History**: Track historical price data and volatility calculations
- **RESTful API**: Clean route structure for programmatic access
- **Responsive UI**: Modern web interface with HTML templates
- **Database Persistence**: SQLite database for data storage

## 🏗️ Architecture

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Database**: SQLite with custom connection pooling
- **External APIs**: Yahoo Finance (yfinance) for real-time stock data
- **Frontend**: HTML templates with Jinja2
- **Deployment**: Docker + Docker Compose support

### Project Structure
```
stock-monitor/
├── app.py                  # Application entry point and Flask app factory
├── config.py               # Configuration management (create from .env)
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Multi-container orchestration
│
├── routes/                # Route handlers (Controllers)
│   ├── __init__.py       # Blueprint registration
│   ├── home.py           # Dashboard and home routes
│   ├── stocks.py         # Stock CRUD operations
│   ├── commodities.py    # Commodity CRUD operations
│   └── debug.py          # Debug utilities
│
├── models/               # Data models
│   ├── stock.py         # StockModel with price calculations
│   └── commodity.py     # CommodityModel
│
├── services/            # Business logic layer
│   ├── stock_monitor.py # Stock price fetching service
│   ├── commodity_price.py # Commodity price service
│   └── api_debug.py     # API debugging utilities
│
├── database/            # Database layer
│   ├── connection.py   # Database connection management
│   └── init_db.py      # Schema initialization
│
├── utils/              # Utility functions
│   ├── validators.py  # Input validation
│   ├── helpers.py     # Helper functions
│   ├── error_handler.py # Error handling
│   ├── cache.py       # Caching utilities
│   └── logging_config.py # Logging setup
│
├── templates/          # HTML templates
│   ├── home.html
│   ├── stocks.html
│   ├── commodities.html
│   ├── add_stock.html
│   └── add_commodity.html
│
└── cron_jobs/         # Scheduled tasks
    └── cron_script.sh
```

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package installer
- **Virtual Environment**: Recommended for dependency isolation
- **API Keys**: Yahoo Finance (free via yfinance library)

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/stock-monitor.git
cd stock-monitor
```

### 2. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\Activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///stock_monitor.db
ALPHA_VANTAGE_API_KEY=your_api_key  # Optional for extended features
```

### 5. Initialize Database
The database is automatically initialized on first run. To manually reset:
```bash
rm -f stock_monitor.db  # Remove existing database
python app.py           # Recreates database with schema
```

### 6. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### 7. Run with Docker (Alternative)
```bash
docker-compose up --build
```

## 🔌 API Documentation

### Stock Endpoints

#### List All Stocks
```http
GET /stocks/
```
**Response**: HTML page displaying all tracked stocks with current prices

#### Add New Stock
```http
GET /stocks/add
POST /stocks/add
```
**POST Parameters**:
- `symbol` (string, required): Stock ticker symbol (e.g., "AAPL", "GOOGL")
- `name` (string, required): Company name
- `sector` (string, optional): Industry sector
- `description` (string, optional): Additional details
- `target_price` (float, required): Target price for alerts

**Example**:
```bash
curl -X POST http://localhost:5000/stocks/add \
  -F "symbol=AAPL" \
  -F "name=Apple Inc." \
  -F "sector=Technology" \
  -F "target_price=150.00"
```

#### Delete Stock
```http
POST /stocks/delete/<stock_id>
```
**Parameters**:
- `stock_id` (integer): ID of the stock to delete

### Commodity Endpoints

#### List All Commodities
```http
GET /commodities/
```

#### Add New Commodity
```http
POST /commodities/add
```
**POST Parameters**:
- `name` (string, required): Commodity name
- `symbol` (string, required): Commodity symbol
- `commodity_type` (string, required): Energy, Metals, Agriculture, or Livestock
- `description` (string, optional)
- `target_price` (float, required)

#### Delete Commodity
```http
POST /commodities/delete/<commodity_id>
```

### Home Dashboard
```http
GET /
```
Displays comprehensive dashboard with stocks and commodities overview

## 💡 Usage Examples

### Adding a Stock via Web Interface
1. Navigate to `http://localhost:5000/stocks/`
2. Click "Add New Stock"
3. Fill in the form:
   - Symbol: `TSLA`
   - Name: `Tesla, Inc.`
   - Sector: `Automotive`
   - Target Price: `250.00`
4. Click "Submit"

### Monitoring Price Changes
The application automatically fetches current prices from Yahoo Finance when viewing the stock list. Price differences are calculated and displayed:
- **Green**: Current price above target
- **Red**: Current price below target
- **Percentage Change**: Shows deviation from target price

### Using the Stock Model Programmatically
```python
from models import StockModel

# Create a stock instance
stock = StockModel(
    symbol="AAPL",
    name="Apple Inc.",
    sector="Technology",
    target_price=150.00
)

# Update with current price
stock.update_price(155.50)

# Check status
print(f"Status: {stock.get_price_status()}")  # "Above Target"
print(f"Difference: ${stock.price_difference:.2f}")  # "$5.50"
print(f"Change: {stock.price_percentage:.2f}%")  # "3.67%"
```

## 🧪 Running Tests

Execute the test suite:
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run specific test file
pytest tests/test_models/test_stock.py
```

## 🛠️ Development

### Adding a New Feature
1. Create model in `models/` if needed
2. Implement business logic in `services/`
3. Add routes in `routes/`
4. Create templates in `templates/`
5. Add tests in `tests/`

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function signatures
- Document classes and functions with docstrings

### Database Migrations
To modify the database schema:
1. Edit `database/init_db.py`
2. Delete `stock_monitor.db`
3. Restart the application

## 🐛 Troubleshooting

### Issue: "Module 'config' not found"
**Solution**: Create a `config.py` file:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    HOST = '0.0.0.0'
    PORT = int(os.getenv('PORT', 5000))
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///stock_monitor.db')
```

### Issue: Stock prices not updating
**Solution**: 
- Check internet connection
- Verify stock symbol is valid (use symbols from major exchanges)
- Yahoo Finance may rate-limit requests; wait a few minutes

### Issue: Database locked error
**Solution**:
- Ensure only one instance of the app is running
- Close any database browsers or tools accessing the SQLite file
- Restart the application

### Issue: Import errors
**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\Activate   # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## 📊 Configuration Reference

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_APP` | Application entry point | `app.py` | No |
| `FLASK_ENV` | Environment mode | `production` | No |
| `SECRET_KEY` | Flask secret key for sessions | Random | Yes |
| `DATABASE_URL` | Database connection string | `sqlite:///stock_monitor.db` | No |
| `ALPHA_VANTAGE_API_KEY` | API key for Alpha Vantage | None | No |
| `PORT` | Server port | `5000` | No |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ using Flask and Python**