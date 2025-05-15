from flask import Flask
import logging
from flask_migrate import Migrate

from .config import get_config
from .models import db
from .routes.rds_routes import api_blueprint

def create_app(config_name="development"):

    # Setting up the Flask app
    app = Flask(__name__)

    # Load configuration from the Config class
    app.config.from_object(get_config(config_name))

    # Setting up logging
    setup_logging(app)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register the blueprints (routes)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

def setup_logging(app):
    # setting up logging for the application
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    # log to the file as well
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)

    # Define formatter to structure logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # attach handler to app's logger
    app.logger.addHandler(handler)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)


