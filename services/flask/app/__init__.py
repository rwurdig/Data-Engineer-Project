from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Globally accessible libraries
db = SQLAlchemy()
socketio = SocketIO()

def create_app():
    """Initialize the core application."""
    try:
        # Create Flask application
        app = Flask(__name__, instance_relative_config=False)
        
        # Load configurations
        app.config.from_object('config.Config')

        # Initialize Plugins
        db.init_app(app)
        socketio.init_app(app)  # Initialize SocketIO

        with app.app_context():
            # Include our Routes
            from . import routes

            # Initialize database migration utility
            migrate = Migrate(app, db)

        logger.info("Application initialized successfully.")
        return app

    except Exception as e:
        logger.error(f"An error occurred during application initialization: {e}")
        return None
