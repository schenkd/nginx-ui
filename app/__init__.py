from flask import Flask
from config import config
from flask_moment import Moment

from werkzeug.middleware.proxy_fix import ProxyFix
import os

moment = Moment()


def create_app(config_name):
    app = Flask(__name__)

    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    moment.init_app(app)

    from app.ui import ui as ui_blueprint
    app.register_blueprint(ui_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
