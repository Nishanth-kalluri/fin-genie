import pandas as pd
import numpy as np

def calculate_metrics(prices, fundamentals):
    """
    Calculate key metrics for stock analysis.

    Args:
        prices (pd.DataFrame): DataFrame of historical stock prices (columns: tickers, rows: dates).
        fundamentals (dict): Dictionary of fundamental data for each ticker.

    Returns:
        pd.DataFrame: A DataFrame with calculated metrics for each stock.
    """
    metrics = []

    for ticker in prices.columns:
        try:
            # Historical price data for the stock
            price_data = prices[ticker]
            returns = price_data.pct_change().dropna()

            # Calculate annualized volatility
            annualized_volatility = np.std(returns) * np.sqrt(252)

            # Calculate momentum (Z-score)
            momentum = (price_data.iloc[-1] - price_data.mean()) / price_data.std()

            # Extract fundamental data
            pe_ratio = fundamentals[ticker].get("trailingPE", np.nan)  # P/E Ratio
            eps = fundamentals[ticker].get("trailingEps", np.nan)      # Earnings Per Share
            dividend_yield = fundamentals[ticker].get("dividendYield", 0) * 100  # Convert to percentage

            # Append calculated metrics to list
            metrics.append({
                "Ticker": ticker,
                "PE_Ratio": pe_ratio,
                "EPS": eps,
                "Dividend_Yield (%)": dividend_yield,
                "Momentum": momentum,
                "Volatility": annualized_volatility,
            })
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    # Convert list of metrics to a DataFrame
    return pd.DataFrame(metrics)
