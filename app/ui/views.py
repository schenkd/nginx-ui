from app.ui import ui
from pathlib import Path
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

    reload_nginx = False
    docker_sock = Path('/var/run/docker.sock')
    if docker_sock.is_socket() and 'NGINX_CONTAINER_NAME' in os.environ:
        reload_nginx = True

    return flask.render_template('index.html', config=config, reload_nginx=reload_nginx)
