from src.api_handler import create_app

# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)
