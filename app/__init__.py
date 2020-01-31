# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    from app import models

    from .convert_api import convert_api as convert_api_blueprint
    app.register_blueprint(convert_api_blueprint, url_prefix='/api')

    return app
