from flask import Flask
from src.api_handler import create_app
import logging
import sys
import os

def setup_logging():
    """Configure logging with proper formatting and handlers"""
    try:
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, "app.log")),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Add specific logger for the application
        logger = logging.getLogger('stock_screener')
        logger.setLevel(logging.INFO)
        
        return logger
    except Exception as e:
        print(f"Failed to setup logging: {str(e)}")
        sys.exit(1)

def main():
    """Initialize and run the application"""
    try:
        # Setup logging
        logger = setup_logging()
        logger.info("Starting Stock Screener Application")

        # Create the Flask app instance
        app = create_app()

        # Add basic configuration
        app.config.update(
            JSON_SORT_KEYS=False,  # Preserve the order of JSON keys
            MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # Max request size of 16MB
            PROPAGATE_EXCEPTIONS=True  # For better error tracking
        )

        # Log startup configuration
        logger.info(f"Application configured with DEBUG={app.debug}")
        
        return app

    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    app = main()
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the Flask app
    app.run(
        debug=True,  # Set to False in production
        host='0.0.0.0',
        port=port,
        use_reloader=True
    )