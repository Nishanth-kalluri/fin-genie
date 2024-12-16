from flask import Flask, request, jsonify
from src.fetch_data import fetch_stock_data
from src.calculate_metrics import calculate_metrics
from src.screen_stocks import StockScreener

app = Flask(__name__)

class APIHandler:
    @staticmethod
    @app.route('/screen', methods=['POST'])
    def screen_stocks():
        try:
            data = request.json
            
            # Validate input
            required_fields = ['tickers', 'investment_amount', 'risk_tolerance', 'time_horizon']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing {field}"}), 400

            tickers = data['tickers']
            investment_amount = data['investment_amount']
            risk_tolerance = data['risk_tolerance']
            time_horizon = data['time_horizon']

            # Fetch and process data
            prices, fundamentals = fetch_stock_data(tickers, time_horizon)
            metrics_df = calculate_metrics(prices, fundamentals)

            # Screen stocks
            result = StockScreener.screen_stocks(
                metrics_df, 
                investment_amount, 
                risk_tolerance, 
                time_horizon
            )

            return jsonify(result)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

def create_app():
    return app
