    # Stock Monitor

## Project Description
A Python-based stock monitoring application that tracks and analyzes stock prices.

## Prerequisites
- Python 3.8+
- pip
- Virtual Environment

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/stock-monitor.git
```

### 2. Create Virtual Environment
```bash
python -m venv venv 
```

### 3. Activate Virtual Environment 
```bash
source venv/bin/activate
.\venv\Scripts\Activate
```


### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables
Create a `.env` file and add the following variables:
```
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient_email@example.com
```


### 6. Test the API
```bash
curl -Method Post -Uri "http://localhost:5000/webhook" -Body '{"symbol": "GOOGL", "threshold": 120.75}' -ContentType "application/json"
```

 python -m services.api_debug