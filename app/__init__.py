from flask import Flask
from config import config
from app.extensions import moment, db, migrate


def create_app(config_name: str) -> Flask:
    """
    App factory method, that initializes the app context using the configuration.

    :param config_name: Name of the configuration
    :type config_name: str

    :return: Flask app context
    :rtype: Flask
    """
    app = Flask(__name__)
    app.config.from_object(obj=config[config_name])

    register_extensions(app=app)

    from app.ui import ui as ui_blueprint
    app.register_blueprint(ui_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


def register_extensions(app: Flask) -> None:
    """
    Initializes the extensions to be registered with the app context.

    :param app: Flask app context
    :type app: Flask
    """
    moment.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
