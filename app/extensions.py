# encoding: utf-8
"""
In this file all extensions are initialized. For registration in the app, these are imported in app/__init__.py and
added in the register_extensions method.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment


moment = Moment()
db = SQLAlchemy()
migrate = Migrate()
