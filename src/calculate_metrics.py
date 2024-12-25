import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# from arch import arch_model

def calculate_metrics(prices, fundamentals, investment_period_months):
    metrics = []
    for ticker in prices.columns:
        try:
            price_data = prices[ticker]
            returns = price_data.pct_change().dropna()
            ticker_fundamentals = fundamentals.loc[ticker]

            metrics.append({
                "Ticker": ticker,
                "PE_Ratio": ticker_fundamentals.get("trailingPE", np.nan),
                "Forward_PE": ticker_fundamentals.get("forwardPE", np.nan),
                "EPS": ticker_fundamentals.get("trailingEps", np.nan),
                "Forward_EPS": ticker_fundamentals.get("forwardEps", np.nan),
                "Dividend_Yield (%)": ticker_fundamentals.get("dividendYield", 0) * 100,
                "Price_to_Book": ticker_fundamentals.get("priceToBook", np.nan),
                "Debt_to_Equity": ticker_fundamentals.get("debtToEquity", np.nan),
                "Return_on_Equity (%)": ticker_fundamentals.get("returnOnEquity", np.nan) * 100,
                "Free_Cashflow": ticker_fundamentals.get("freeCashflow", np.nan),
                "Operating_Cashflow": ticker_fundamentals.get("operatingCashflow", np.nan),
                "Total_Cash": ticker_fundamentals.get("totalCash", np.nan),
                "Total_Debt": ticker_fundamentals.get("totalDebt", np.nan),
                "Current_Ratio": ticker_fundamentals.get("currentRatio", np.nan),
                "Quick_Ratio": ticker_fundamentals.get("quickRatio", np.nan),
                "Analyst_Recommendation": ticker_fundamentals.get("recommendationMean", np.nan),
                "Target_Mean_Price": ticker_fundamentals.get("targetMeanPrice", np.nan),
                "Market_Cap": ticker_fundamentals.get("marketCap", np.nan),
                "Momentum": calculate_momentum(price_data),
                "Volatility": calculate_annualized_volatility(returns),
                # "Projected_Profit_ARIMA (%)": calculate_projected_profit_arima(price_data, investment_period_months) * 100,
                # "Projected_Profit_GARCH (%)": calculate_projected_profit_garch(price_data, investment_period_months) * 100,
                "Trend_Strength": calculate_trend_strength(price_data)
            })
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    return pd.DataFrame(metrics)

def calculate_annualized_volatility(returns):
    return np.std(returns) * np.sqrt(252)

def calculate_momentum(price_data):
    return (price_data.iloc[-1] - price_data.mean()) / price_data.std()


# def make_stationary(price_data):
#     """
#     Make the time series stationary by differencing and checking stationarity.
#     """
#     diff_data = price_data.diff().dropna()
#     print("making data stationary")
#     result = adfuller(diff_data)
#     if result[1] < 0.05:  # p-value < 0.05 indicates stationary data
#         return diff_data
#     else:
#         raise ValueError("Data is not stationary even after differencing.")

# def calculate_projected_profit_arima(price_data, investment_period_months):
#     # Ensure the index is datetime
#     price_data.index = pd.to_datetime(price_data.index)
    
#     # Resample to daily frequency, forward-filling any missing values
#     price_data = price_data.resample('D').ffill()

#     # Make the data stationary
#     price_data_stationary = make_stationary(price_data)
    
#     # Create and fit the ARIMA model with specified frequency
#     model = ARIMA(price_data_stationary, order=(3, 2, 1))
#     model_fit = model.fit()
    
#     # Calculate the number of days to forecast
#     forecast_days = investment_period_months * 30  # Approximating months to days
    
#     # Generate forecast and reverse the differencing to get the projected prices
#     forecast = model_fit.forecast(steps=forecast_days)
#     last_observed_value = price_data.iloc[-1]
#     forecast_cumulative = forecast.cumsum() + last_observed_value

#     # Calculate projected profit
#     return (forecast_cumulative.iloc[-1] / price_data.iloc[-1]) - 1
# def calculate_projected_profit_garch(price_data, investment_period_months):
#     returns = price_data.pct_change().dropna()
#     # model = arch_model(returns, vol='GARCH', p=1, q=1)
#     model_fit = model.fit()
#     forecast = model_fit.forecast(horizon=investment_period_months)
#     return forecast.mean['h.{}'.format(investment_period_months)].values[-1]

def calculate_trend_strength(price_data):
    short_ma = price_data.rolling(window=50).mean()
    long_ma = price_data.rolling(window=200).mean()
    if short_ma.iloc[-1] > long_ma.iloc[-1]:
        return 'Bullish'
    elif short_ma.iloc[-1] < long_ma.iloc[-1]:
        return 'Bearish'
    return 'Neutral'
