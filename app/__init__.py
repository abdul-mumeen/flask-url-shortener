from config import config
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


bootstrap = Bootstrap()
moment = Moment()
migrate = Migrate()
db = SQLAlchemy()
from .main import main as main_blueprint
from .api_1_0 import api as api_1_0_blueprint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
