import pandas as pd
import numpy as np
from src.portfolio_optimizer import PortfolioOptimizer
import logging

class ScreenStocks:
    
    @staticmethod
    def screen_stocks(metrics_df, investment_amount, risk_tolerance, investment_period_months, historical_prices, index):
        """
        Screen and optimize portfolio allocation for stocks based on multiple criteria.
        
        Args:
            metrics_df (pd.DataFrame): DataFrame containing stock metrics
            investment_amount (float): Total amount to invest
            risk_tolerance (str): 'low', 'medium', or 'high'
            investment_period_months (int): Investment timeframe in months
            historical_prices (pd.DataFrame): Historical price data for stocks
        
        Returns:
            dict: Screening results and optimized portfolio allocation
        """
        try:
            # Define weights for each time category based on investment period
            weights = ScreenStocks._get_time_based_weights(investment_period_months)
            metrics_df.fillna(0, inplace=True)

            print(metrics_df)
            # Calculate component scores
            fundamental_score = ScreenStocks.normalize_scores(
                ScreenStocks.get_fundamental_score(metrics_df, investment_period_months)
            )
            print("fundamental scores")
            print(fundamental_score)
            statistical_score = ScreenStocks.normalize_scores(
                ScreenStocks.get_statistical_score(metrics_df, investment_period_months)
            )
             #remove the below code while integrating real statistical scores
            if(index=='nifty50'):
                statistical_score = np.full(50, statistical_score)
            else:
                statistical_score = np.full(100, statistical_score)
            
            print("statistical scores")
            print(statistical_score)
            technical_score = ScreenStocks.normalize_scores(
                ScreenStocks.get_technical_score(metrics_df, investment_period_months)
            )
            print("technical_score")
            print(technical_score)
           
            print("normalized scores")
            # Combine scores using weights
            metrics_df['Score'] = (
                weights['fundamental'] * fundamental_score +
                weights['statistical'] * statistical_score +
                weights['technical'] * technical_score
            )

            # Sort stocks by score and select top ones
            metrics_df.sort_values('Score', ascending=False, inplace=True)
            print(metrics_df)
            print("sorted stocks")
            # Select top stocks based on scores
            num_stocks = min(5, len(metrics_df))
            top_stocks = metrics_df.head(num_stocks)['Ticker'].tolist() 
            print("Top stocks list:", top_stocks)
            # Filter historical prices for selected stocks
            selected_prices = historical_prices[top_stocks]
            
            print("Selected prices columns:", selected_prices)
            print("filtered stocks")
            # Create portfolio optimizer
            optimizer = PortfolioOptimizer(
                prices_df=selected_prices,
                risk_tolerance=risk_tolerance,
                investment_amount=investment_amount
            )
            print("optimized stocks")
            # Get optimized portfolio allocation
            portfolio = optimizer.optimize_portfolio(top_stocks)
            
            # Calculate risk metrics for the portfolio
            # risk_metrics = optimizer.get_risk_metrics(portfolio['weights'], top_stocks)
            print("risk metrics fetched")
            
            # Prepare detailed metrics for selected stocks
            detailed_metrics = metrics_df.head(num_stocks).copy()
            
            # Add allocation and weight information to detailed metrics
            for stock in top_stocks:
                detailed_metrics.loc[stock, 'Allocated_Amount'] = portfolio['allocations'][stock]
                detailed_metrics.loc[stock, 'Portfolio_Weight'] = portfolio['weights'][stock]
            
            return {
                'screened_stocks': detailed_metrics.to_dict(orient='records'),
                'portfolio_allocation': portfolio['allocations'],
                'position_metrics': portfolio['position_metrics'],
                'expected_return': portfolio['expected_annual_return'],
                'portfolio_volatility': portfolio['annual_volatility'],
                'sharpe_ratio': portfolio['sharpe_ratio'],
                # 'risk_metrics': risk_metrics,
                'screening_metrics': {
                    'total_stocks_analyzed': len(metrics_df),
                    'selected_stocks': num_stocks,
                    'investment_period': investment_period_months,
                    'risk_tolerance': risk_tolerance
                }
            }
            
        except Exception as e:
            logging.error(f"Stock screening failed: {str(e)}")
            return {
                'error': str(e),
                'status': 'failed'
            }

    @staticmethod
    def _get_time_based_weights(investment_period_months):
        """Get weights based on investment period."""
        if investment_period_months <= 3:
            return {'fundamental': 0.4, 'statistical': 0.4, 'technical': 0.2}
        elif 3 < investment_period_months <= 6:
            return {'fundamental': 0.3, 'statistical': 0.5, 'technical': 0.2}
        elif 6 < investment_period_months <= 12:
            return {'fundamental': 0.4, 'statistical': 0.3, 'technical': 0.3}
        elif 12 < investment_period_months <= 36:
            return {'fundamental': 0.5, 'statistical': 0.25, 'technical': 0.25}
        else:
            return {'fundamental': 0.6, 'statistical': 0.2, 'technical': 0.2}

    @staticmethod
    def normalize_scores(series):
        """Normalize scores to range [0, 1]."""
        print("trying to normalize")
        if not isinstance(series, pd.Series):
            series = pd.Series(series)
        if series.max() == series.min():
            return pd.Series(0.5, index=series.index)
        return (series - series.min()) / (series.max() - series.min())

    @staticmethod
    def get_fundamental_score(metrics_df, investment_period_months):
        """Calculate fundamental scores based on investment period."""
        try:
            if investment_period_months <= 3:
                return (
                    metrics_df['Dividend_Yield (%)'] * 0.4 + 
                    metrics_df['EPS'] * 0.6
                ).fillna(0)
            elif 3 < investment_period_months <= 6:
                return (
                    metrics_df['PE_Ratio'].apply(lambda x: -0.5 * x if x > 0 else 0) + 
                    metrics_df['EPS'] * 0.5
                ).fillna(0)
            elif 6 < investment_period_months <= 12:
                return (
                    metrics_df['Return_on_Equity (%)'] * 0.5 + 
                    metrics_df['Cash_Flow_Sustainability'] * 0.5
                ).fillna(0)
            elif 12 < investment_period_months <= 36:
                return (
                    metrics_df['Long_Term_Growth'] * 0.6 + 
                    metrics_df['Debt_to_Equity_Ratio'].apply(lambda x: -0.4 * x if x > 0 else 0)
                ).fillna(0)
            else:
                return metrics_df['Price_to_Book_Ratio'].apply(lambda x: -1 * x if x > 0 else 0).fillna(0)
        except Exception as e:
            logging.error(f"Error calculating fundamental score: {str(e)}")
            return pd.Series(0, index=metrics_df.index)
    #issue with ARIMA modeling should fix it
    @staticmethod
    def get_statistical_score(metrics_df, investment_period_months):
        return 0
        """Calculate statistical scores based on ARIMA projections."""
        # try:
        #     return metrics_df['Projected_Profit_ARIMA (%)'].fillna(0)
        # except Exception as e:
        #     logging.error(f"Error calculating statistical score: {str(e)}")
        #     return pd.Series(0, index=metrics_df.index)

    @staticmethod
    def get_technical_score(metrics_df, investment_period_months):
        """Calculate technical scores based on investment period."""
        try:
            if investment_period_months <= 3:
                momentum_score = metrics_df['Momentum'] * 0.4
                volatility_score = (metrics_df['Volatility'].quantile(0.5) - metrics_df['Volatility']) * 0.6
                return (momentum_score + volatility_score).fillna(0)
            elif 3 < investment_period_months <= 6:
                momentum_score = metrics_df['Momentum'] * 0.5
                volatility_score = (metrics_df['Volatility'].quantile(0.75) - metrics_df['Volatility']) * 0.5
                return (momentum_score + volatility_score).fillna(0)
            else:
                return metrics_df['Trend_Strength'].apply(
                    lambda x: 1 if x == 'Bullish' else (-1 if x == 'Bearish' else 0)
                ).fillna(0)
        except Exception as e:
            logging.error(f"Error calculating technical score: {str(e)}")
            return pd.Series(0, index=metrics_df.index)