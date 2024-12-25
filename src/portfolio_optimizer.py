import pandas as pd
import numpy as np

class PortfolioOptimizer:
    RISK_LEVELS = {
        'low': 0.02,    # 2% risk tolerance
        'medium': 0.05, # 5% risk tolerance
        'high': 0.10    # 10% risk tolerance
    }
    
    MIN_POSITION_SIZE = 1000  # Minimum investment in a single stock
    MAX_POSITION_PERCENTAGE = 0.4  # Maximum 40% in a single stock
    
    def __init__(self, prices_df, risk_tolerance, investment_amount):
        """
        Initialize the simple portfolio optimizer.
        
        Args:
            prices_df (pd.DataFrame): Historical price data for stocks
            risk_tolerance (str): 'low', 'medium', or 'high'
            investment_amount (float): Total investment amount
        """
        self.prices_df = prices_df
        self.returns_df = prices_df.pct_change().dropna()
        self.risk_tolerance = self.RISK_LEVELS.get(risk_tolerance.lower(), 0.05)
        self.num_assets = len(prices_df.columns)
        self.investment_amount = investment_amount
        
        # Calculate latest prices for position size constraints
        self.latest_prices = prices_df.iloc[-1]
        
        # Minimum and maximum weights based on investment amount
        self.min_weights = np.array([self.MIN_POSITION_SIZE / self.investment_amount] * self.num_assets)
        self.max_weights = np.array([self.MAX_POSITION_PERCENTAGE] * self.num_assets)
    
    def calculate_position_sizes(self, weights):
        """
        Calculate actual position sizes in currency terms.
        """
        return weights * self.investment_amount

    def optimize_portfolio(self, screened_stocks):
        """
        Optimize portfolio with equal weights while respecting position constraints.
        
        Args:
            screened_stocks (list): List of screened stock symbols
            
        Returns:
            dict: Optimized portfolio allocation and metrics
        """
        try:
            # Filter prices for screened stocks
            relevant_prices = self.prices_df[screened_stocks]
            self.num_assets = len(screened_stocks)
            
            # Equal weights for all assets
            equal_weight = 1 / self.num_assets
            
            # Ensure weights meet position size constraints
            weights = np.clip([equal_weight] * self.num_assets, self.min_weights, self.max_weights)
            
            # Calculate actual position sizes
            positions = self.calculate_position_sizes(weights)
            
            
            # Portfolio metrics (simplified: returns, risk)
            returns = self.prices_df.pct_change().dropna().mean() * 252  # Assuming 252 trading days in a year
            portfolio_return = np.sum(returns.loc[screened_stocks] * weights)
            
            # Calculate portfolio volatility using the risk tolerance
            cov_matrix = self.returns_df.cov() * 252  # Annualized covariance matrix
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix.loc[screened_stocks, screened_stocks], weights)))
            
            # Apply risk tolerance as a penalty on volatility
            adjusted_volatility = portfolio_volatility * (1 + self.risk_tolerance)
            
            # Sharpe ratio calculation (simplified)
            sharpe_ratio = portfolio_return / adjusted_volatility if adjusted_volatility != 0 else 0
            print("positions:",positions)
            
            # Return the optimized portfolio allocation
            return {
                'allocations': dict(zip(screened_stocks, positions)),
                'weights': dict(zip(screened_stocks, weights)),
                'expected_annual_return': portfolio_return * 100,
                'annual_volatility': adjusted_volatility * 100,
                'sharpe_ratio': sharpe_ratio,
                'position_metrics': {
                    'min_position': min(positions),
                    'max_position': max(positions),
                    'avg_position': np.mean(positions)
                }
            }
        
        except Exception as e:
            print(f"Error in optimization: {e}")
            return {}

