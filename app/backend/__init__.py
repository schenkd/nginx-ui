from flask import Flask
from app.backend.config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    from app.backend.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
