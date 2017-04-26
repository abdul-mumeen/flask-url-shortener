from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config
# This objects are initialized here to prevent circular dependencies
moment = Moment()
migrate = Migrate()
db = SQLAlchemy()
from app.api_1_0 import api as api_1_0_blueprint


def create_app(config_name):
    """
    This function is used to create the application using the supplied
    configuration name by initializing the app's blueprint.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
