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

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/user')

    from .calendar import calendar as cal_blueprint
    app.register_blueprint(cal_blueprint, url_prefix='/api')

    from .event import event as event_blueprint
    app.register_blueprint(event_blueprint, url_prefix='/api')

    return app
