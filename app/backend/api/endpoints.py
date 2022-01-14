import datetime
import io
import os
import flask
from flask import request
from app.backend.consul.register import ConsulServiceRegistry, ServiceInstance
from app.backend.consul.service import ConsulServiceDiscovery
from app.backend.consul.utils import get_instance_id, get_ingress, \
    get_service_name_by_ingress
from app.backend.utils.nginx import create_config, disable_config, version, check, \
    reload
from app.backend.api import api


@api.route('/config/<name>', methods=['GET'])
def get_config(name: str):
    """
    Reads the file with the corresponding name that was passed.

    :param name: Configuration file name
    :type name: str

    :return: Rendered HTML document with content of the configuration file.
    :rtype: str
    """
    nginx_path = flask.current_app.config['NGINX_PATH']

    with io.open(os.path.join(nginx_path, name), 'r') as f:
        _file = f.read()

    return flask.render_template('config.html', name=name, file=_file), 200


@api.route('/config/<name>', methods=['POST'])
def post_config(name: str):
    """
    Accepts the customized configuration and saves it in the configuration file with the supplied name.

    :param name: Configuration file name
    :type name: str

    :return:
    :rtype: werkzeug.wrappers.Response
    """
    content = flask.request.get_json()
    nginx_path = flask.current_app.config['NGINX_PATH']

    with io.open(os.path.join(nginx_path, name), 'w') as f:
        f.write(content['file'])

    return flask.make_response({'success': True}), 200


@api.route('/domains', methods=['GET'])
def get_domains():
    """
    Reads all files from the configuration file directory and checks the state of the site configuration.

    :return: Rendered HTML document with the domains
    :rtype: str
    """
    config_path = flask.current_app.config['CONFIG_PATH']
    sites_available = []
    sites_enabled = []

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            domain, state = _.rsplit('.', 1)

            if state == 'conf':
                time = datetime.datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(config_path, _)))

                sites_available.append({
                    'name': domain,
                    'time': time
                })
                sites_enabled.append(domain)
            elif state == 'disabled':
                time = datetime.datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(config_path, _)))

                sites_available.append({
                    'name': domain.rsplit('.', 1)[0],
                    'time': time
                })

    # mock service
    services = []
    # services.append({
    #     'service_name': 'wishpost',
    #     'endpoint': 'http://www.wishpost2.com',
    #     'instances': [
    #         {
    #             'endpoint': 'http://www.wishpost1.com',
    #             'instance_id': 'conan-wishpost'
    #         },
    #         {
    #             'endpoint': 'http://www.wishpost2.com',
    #             'instance_id': 'wishpost'
    #         }
    #     ]
    # })

    discovery = ConsulServiceDiscovery()
    service_names = discovery.get_services()
    for name in service_names:
        tmp_services = discovery.get_instance(name)
        if len(tmp_services) == 0:
            continue

        instances = []
        for svc in tmp_services:
            svc: ServiceInstance
            instances.append({
                'endpoint': f'http://{svc.host}:{svc.port}',
                'instance_id': svc.instance_id
            })

        services.append({
            'service_name': name,
            'endpoint': '',
            'instances': instances,
        })

    print("zzz", services)

    # sort sites by name
    # sites_available = sorted(sites_available, key=lambda _: _['name'])
    return flask.render_template('domains.html',
                                 # sites_available=sites_available,
                                 # sites_enabled=sites_enabled,
                                 services=services), 200


@api.route('/domain/<name>', methods=['GET'])
def get_domain(name: str):
    """
    Takes the name of the domain configuration file and
    returns a rendered HTML with the current configuration of the domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Rendered HTML document with the domain
    :rtype: str
    """
    config_path = flask.current_app.config['CONFIG_PATH']
    _file = ''
    enabled = True

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(name):
                domain, state = _.rsplit('.', 1)

                if state == 'disabled':
                    enabled = False

                with io.open(os.path.join(config_path, _), 'r') as f:
                    data = f.readlines()
                    for idx, item in enumerate(data):
                        if "proxy_pass" in item:
                            start_pos = data[idx].find("proxy_pass")
                            start_pos += len("proxy_pass") + 1
                            host = data[idx][start_pos:-2]
                            break

                break

    discovery = ConsulServiceDiscovery()
    result, service_name = get_service_name_by_ingress(name)
    instances = []
    if result:
        instances = discovery.get_instance(service_name)

    return flask.render_template('domain.html', name=name, host=host,
                                 enabled=enabled, instances=instances), 200


@api.route('/domain/<name>', methods=['POST'])
def post_domain(name: str):
    """
    Creates the configuration file of the domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    result, msg = create_config(name, "")
    if result:
        response = flask.jsonify({'success': True}), 201
    else:
        response = flask.jsonify({'success': False, 'error_msg': msg}), 500
    return response


@api.route('/domain/<name>', methods=['DELETE'])
def delete_domain(name: str):
    """
    Deletes the configuration file of the corresponding domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    config_path = flask.current_app.config['CONFIG_PATH']
    removed = False

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(name):
                os.remove(os.path.join(config_path, _))
                removed = not os.path.exists(os.path.join(config_path, _))
                break

    if removed:
        return flask.jsonify({'success': True}), 200
    else:
        return flask.jsonify({'success': False}), 400


@api.route('/domain/<name>', methods=['PUT'])
def put_domain(name: str):
    """
    Updates the configuration file with the corresponding domain name.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    content = flask.request.get_json()
    config_path = flask.current_app.config['CONFIG_PATH']

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(name):
                with io.open(os.path.join(config_path, _), 'r') as f:
                    data = f.readlines()
                for idx, item in enumerate(data):
                    if "proxy_pass" in item:
                        data[idx] = "       proxy_pass {};\n".format(
                            content["host"])
                        break
                with io.open(os.path.join(config_path, _), 'w') as f:
                    f.writelines(data)

    return flask.make_response({'success': True}), 200


@api.route('/domain/<name>/enable', methods=['POST'])
def enable_domain(name: str):
    """
    Activates the domain in Nginx so that the configuration is applied.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    content = flask.request.get_json()
    config_path = flask.current_app.config['CONFIG_PATH']

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(name):
                if content['enable']:
                    new_filename, disable = _.rsplit('.', 1)
                    os.rename(os.path.join(config_path, _),
                              os.path.join(config_path, new_filename))
                else:
                    os.rename(os.path.join(config_path, _),
                              os.path.join(config_path, _ + '.disabled'))

    return flask.make_response({'success': True}), 200


@api.route('/action/<name>', methods=['POST'])
def do_action(name: str):
    """
    :param name:
    :return:
    """
    if name == "version":
        stdout = version()
    elif name == "check":
        stdout = check()
    else:
        stdout = reload()
    return flask.render_template('action_info.html', header="LOG",
                                 file=stdout), 200


@api.route('/service/register', methods=['POST'])
def register_service():
    # 1. 将服务注册到 consul
    service_name = request.form.get('service_name')
    host = request.form.get('host')
    port = int(request.form.get('port'))
    user_name = request.form.get('user_name')
    print(service_name, host, port, user_name, type(service_name))
    instance = ServiceInstance(service_name, host, 80,
                               instance_id=get_instance_id(service_name,
                                                           user_name))
    registry = ConsulServiceRegistry()
    registry.register(instance)

    # 2. 添加 nginx 代理
    ingress_name = get_ingress(service_name)
    result, msg = create_config(ingress_name, f'http://{service_name}:{port}',
                                disabled=False)

    # 3. reload
    reload()

    if result:
        response = flask.jsonify({'success': True}), 201
    else:
        response = flask.jsonify({'success': False, 'error_msg': msg}), 500
    return response


@api.route('/service/deregister', methods=['POST'])
def deregister_service():
    service_name = request.form.get("service_name")
    user_name = request.form.get("user_name")
    instance_id = get_instance_id(service_name, user_name)
    print(instance_id)
    registry = ConsulServiceRegistry()
    registry.deregister(instance_id)

    # 2. 把 nginx 代理 close 掉
    ingress_name = get_ingress(service_name)
    disable_config(ingress_name)

    # 3. reload
    reload()

    return flask.make_response({'success': True}), 200


@api.route('/service/<name>', methods=['GET'])
def get_service(name: str):
    discovery = ConsulServiceDiscovery()
    result, service_name = get_service_name_by_ingress(name)
    if result:
        instance = discovery.get_instance(service_name)
    else:
        pass
