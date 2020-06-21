from app.ui import ui
import flask
import os


@ui.route('/',  methods=['GET'])
def index():
    """
    Delivers the home page of Nginx UI.

    :return: Rendered HTML document.
    :rtype: str
    """
    nginx_path = flask.current_app.config['NGINX_PATH']
    config = [f for f in os.listdir(nginx_path) if os.path.isfile(os.path.join(nginx_path, f))]
    return flask.render_template('index.html', config=config)
