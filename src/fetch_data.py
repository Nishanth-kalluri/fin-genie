import yfinance as yf
import pandas as pd

def fetch_stock_data(tickers, period='1y'):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data[ticker] = stock.history(period=period)
    return pd.DataFrame({ticker: df['Close'] for ticker, df in data.items()})
