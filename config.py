import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.urandom(64).hex()

    NGINX_PATH = os.environ.get('NGINX_PATH', '/etc/nginx')
    CONFIG_PATH = os.path.join(NGINX_PATH, 'conf.d')

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(f'{basedir}/db', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True


class WorkingConfig(Config):
    DEBUG = False


config = {
    'dev': DevConfig,
    'default': WorkingConfig
}
