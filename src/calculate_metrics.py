import pandas as pd
import numpy as np

def calculate_metrics(prices, fundamentals, investment_period):
    metrics = []
    for ticker in prices.columns:
        try:
            price_data = prices[ticker]
            returns = price_data.pct_change().dropna()
            
            annualized_volatility = np.std(returns) * np.sqrt(252)
            momentum = (price_data.iloc[-1] - price_data.mean()) / price_data.std()
            
            # Calculate projected profit
            historical_return = (price_data.iloc[-1] / price_data.iloc[0]) - 1
            projected_annual_return = (1 + historical_return) ** (1 / (len(price_data) / 252)) - 1
            projected_profit = (1 + projected_annual_return) ** investment_period - 1

            pe_ratio = fundamentals[ticker].get("trailingPE", np.nan)
            eps = fundamentals[ticker].get("trailingEps", np.nan)
            dividend_yield = fundamentals[ticker].get("dividendYield", 0) * 100

            metrics.append({
                "Ticker": ticker,
                "PE_Ratio": pe_ratio,
                "EPS": eps,
                "Dividend_Yield (%)": dividend_yield,
                "Momentum": momentum,
                "Volatility": annualized_volatility,
                "Projected_Profit (%)": projected_profit * 100
            })
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    return pd.DataFrame(metrics)
