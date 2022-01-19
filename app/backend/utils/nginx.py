import io
import os.path
from app.backend.utils.tools import run_subprocess

import flask


def create_config(name, proxy_pass, disabled=True):
    config_path = flask.current_app.config['CONFIG_PATH']
    new_domain = flask.render_template('new_domain.j2', name=name,
                                       proxy=proxy_pass)
    name = name + '.conf'
    try:
        with io.open(os.path.join(config_path, name), 'w') as f:
            f.write(new_domain)
        return True, ""
    except Exception as ex:
        return False, ex


def disable_config(name):
    config_path = flask.current_app.config['CONFIG_PATH']

    for _ in os.listdir(config_path):
        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(name):
                if _.endswith('disabled'):
                    return
                else:
                    os.rename(os.path.join(config_path, _),
                              os.path.join(config_path, _ + '.disabled'))
                    return


def version():
    stdout = run_subprocess(["sudo", "nginx", "-v"])
    return stdout


def check():
    stdout = run_subprocess(["sudo", "nginx", "-T"])
    return stdout

def reload():
    stdout1 = run_subprocess(["sudo", "nginx", "-T"])
    stdout = run_subprocess(["sudo", "service", "nginx", "reload"])
    stdout1 = stdout1.decode("utf-8")
    stdout = stdout.decode("utf-8")
    stdout = stdout + "......\n\n" + stdout1
    return stdout
