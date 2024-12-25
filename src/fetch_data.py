import pandas as pd
import yfinance as yf

class FetchData:
    def __init__(self, tickers):
        self.tickers = tickers

    def fetch_price_data(self):
        df = yf.download(self.tickers, period="max")["Adj Close"]
        return df.dropna()

    def fetch_fundamental_data(self):
        fundamental_data = {}
        for ticker in self.tickers:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info
            fundamental_data[ticker] = {
                "trailingPE": info.get("trailingPE"),
                "forwardPE": info.get("forwardPE"),
                "marketCap": info.get("marketCap"),
                "priceToBook": info.get("priceToBook"),
                "dividendYield": info.get("dividendYield"),
                "trailingEps": info.get("trailingEps"),
                "forwardEps": info.get("forwardEps"),
                "bookValue": info.get("bookValue"),
                "debtToEquity": info.get("debtToEquity"),
                "returnOnEquity": info.get("returnOnEquity"),
                "freeCashflow": info.get("freeCashflow"),
                "operatingCashflow": info.get("operatingCashflow"),
                "totalCash": info.get("totalCash"),
                "totalDebt": info.get("totalDebt"),
                "currentRatio": info.get("currentRatio"),
                "quickRatio": info.get("quickRatio"),
                "recommendationMean": info.get("recommendationMean"),
                "targetMeanPrice": info.get("targetMeanPrice")
            }
        return pd.DataFrame.from_dict(fundamental_data, orient='index')
