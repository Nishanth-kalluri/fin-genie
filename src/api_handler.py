from flask import Flask, request, jsonify
from src.fetch_data import FetchData
from src.calculate_metrics import calculate_metrics
from src.screen_stocks import ScreenStocks
from src.nifty_data import get_nifty_tickers
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    @app.route('/screen', methods=['POST'])
    def screen_stocks_api():
        try:
            # Validate input data
            data = request.json
            required_fields = ['investment_amount', 'risk_tolerance', 'investment_period']
            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400

            investment_amount = float(data['investment_amount'])
            risk_tolerance = data['risk_tolerance']
            investment_period = int(data['investment_period'])
            index = data.get('index', 'nifty50')

            # Validate risk tolerance
            if risk_tolerance not in ['low', 'medium', 'high']:
                return jsonify({"error": "Invalid risk tolerance. Must be 'low', 'medium', or 'high'"}), 400

            # Fetch stock data
            try:
                tickers = get_nifty_tickers(index)
                fetcher = FetchData(tickers=tickers)
                prices = fetcher.fetch_price_data()
                fundamentals = fetcher.fetch_fundamental_data()
            except Exception as e:
                logger.error(f"Error fetching data: {str(e)}")
                return jsonify({"error": "Failed to fetch stock data"}), 500

            # Calculate metrics
            try:
                metrics_df = calculate_metrics(prices, fundamentals, investment_period)
            except Exception as e:
                logger.error(f"Error calculating metrics: {str(e)}")
                return jsonify({"error": "Failed to calculate metrics"}), 500

            # Screen stocks
            try:
                result = ScreenStocks.screen_stocks(
                    metrics_df=metrics_df,
                    investment_amount=investment_amount,
                    risk_tolerance=risk_tolerance,
                    investment_period_months=investment_period,
                    historical_prices=prices,
                    index=index# Add missing required parameter
                )
            except Exception as e:
                logger.error(f"Error screening stocks: {str(e)}")
                return jsonify({"error": "Failed to screen stocks"}), 500

            return jsonify(result)

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)