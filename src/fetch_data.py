import yfinance as yf
import pandas as pd

def fetch_stock_data(tickers, period='1y'):
    """
    Fetch historical stock prices and fundamental data.

    Args:
        tickers (list): List of stock tickers to fetch.
        period (str): Historical data period (e.g., '1y', '6mo', etc.).

    Returns:
        prices (pd.DataFrame): DataFrame of historical closing prices.
        fundamentals (dict): Dictionary of fundamental data for each ticker.
    """
    # Dictionary to store stock price data
    data = {}
    # Dictionary to store fundamental data
    fundamentals = {}

    for ticker in tickers:
        stock = yf.Ticker(ticker)

        # Fetch historical price data
        data[ticker] = stock.history(period=period)

        # Fetch fundamental data
        fundamentals[ticker] = stock.info

    # Create a DataFrame for closing prices
    prices = pd.DataFrame({ticker: df['Close'] for ticker, df in data.items()})

    return prices, fundamentals
