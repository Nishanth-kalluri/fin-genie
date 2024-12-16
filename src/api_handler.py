from flask import Flask, request, jsonify
from src.fetch_data import fetch_nifty_data
from src.calculate_metrics import calculate_metrics
from src.screen_stocks import StockScreener

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    @app.route('/screen', methods=['POST'])
    def screen_stocks_api():
        try:
            data = request.json
            investment_amount = data['investment_amount']
            risk_tolerance = data['risk_tolerance']
            investment_period = data['investment_period']
            index = data.get('index', 'nifty50')  # Default to Nifty 50 if not specified

            # Fetch stock data
            prices, fundamentals = fetch_nifty_data(index, '1y')
            metrics_df = calculate_metrics(prices, fundamentals, investment_period)

            # Screen stocks based on user preferences
            result = StockScreener.screen_stocks(
                metrics_df,
                investment_amount,
                risk_tolerance,
                investment_period
            )

            return jsonify(result)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app
