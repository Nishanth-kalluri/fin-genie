from src.fetch_data import fetch_stock_data
from src.calculate_metrics import calculate_metrics
from src.screen_stocks import screen_stocks

# Define parameters
tickers = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']
period = '1y'
risk_tolerance = 'medium'

# Fetch and process data
prices = fetch_stock_data(tickers, period)
metrics = calculate_metrics(prices)

# Screen stocks
selected_stocks = screen_stocks(metrics, risk_tolerance)

print("Selected Stocks:")
print(selected_stocks)
