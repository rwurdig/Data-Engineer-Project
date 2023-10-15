from app import create_app
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    try:
        logger.info("Starting the application.")
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
