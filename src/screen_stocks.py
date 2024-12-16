import pandas as pd
import numpy as np

class StockScreener:
    @staticmethod
    def screen_stocks(metrics_df, investment_amount, risk_tolerance, investment_period):
        if risk_tolerance == 'low':
            screened_stocks = metrics_df[
                (metrics_df['Volatility'] < metrics_df['Volatility'].median()) &
                (metrics_df['Dividend_Yield (%)'] > metrics_df['Dividend_Yield (%)'].median())
            ]
        elif risk_tolerance == 'medium':
            screened_stocks = metrics_df[
                (metrics_df['Volatility'].between(
                    metrics_df['Volatility'].quantile(0.25),
                    metrics_df['Volatility'].quantile(0.75)
                )) &
                (metrics_df['PE_Ratio'] < metrics_df['PE_Ratio'].median())
            ]
        else:  # high risk tolerance
            screened_stocks = metrics_df[
                (metrics_df['Volatility'] > metrics_df['Volatility'].median()) &
                (metrics_df['Momentum'] > metrics_df['Momentum'].median())
            ]

        screened_stocks['Score'] = (
            screened_stocks['Momentum'] / screened_stocks['Volatility'] +
            screened_stocks['Dividend_Yield (%)'] / 100 +
            screened_stocks['Projected_Profit (%)'] / 100
        )
        screened_stocks = screened_stocks.sort_values('Score', ascending=False)

        num_stocks = min(5, len(screened_stocks))
        allocation_per_stock = investment_amount / num_stocks

        return {
            'screened_stocks': screened_stocks.head(num_stocks).to_dict(orient='records'),
            'allocation_per_stock': allocation_per_stock,
            'total_projected_profit': screened_stocks.head(num_stocks)['Projected_Profit (%)'].mean()
        }
