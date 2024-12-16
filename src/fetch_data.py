import yfinance as yf
import pandas as pd
from src.nifty_data import get_nifty_tickers  # Changed from get_nifty50_tickers

def fetch_stock_data(tickers, period='1y'):
    """Fetch historical stock prices and fundamental data."""
    data = {}
    fundamentals = {}

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data[ticker] = stock.history(period=period)
        fundamentals[ticker] = stock.info

    prices = pd.DataFrame({ticker: df['Close'] for ticker, df in data.items()})
    return prices, fundamentals

def fetch_nifty_data(index='nifty50', period='1y'):  # Changed from fetch_nifty50_data
    """Fetch data for Nifty stocks."""
    tickers = get_nifty_tickers(index)  # Pass the index parameter
    return fetch_stock_data(tickers, period)
