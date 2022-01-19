from app.backend.utils.service_config import sc
import flask
from flask import request
from app.backend.consul.register import ConsulServiceRegistry, ServiceInstance
from app.backend.consul.service import ConsulServiceDiscovery
from app.backend.consul.utils import get_instance_id, get_ingress
from app.backend.utils.nginx import create_config, reload
from app.backend.api import api
from app.backend.utils.hosts import add_host
from app.backend.utils.const import HOST


@api.route('/service/register', methods=['POST'])
def register_service():
    # 1. 将服务注册到 consul
    service_name = request.form.get('service_name')
    host = sc.services.external_ip
    port = int(request.form.get('port'))
    user_name = request.form.get('user_name')
    # print(service_name, host, port, user_name, type(service_name))
    instance = ServiceInstance(service_name, host, 80,
                               instance_id=get_instance_id(service_name,
                                                           user_name))
    registry = ConsulServiceRegistry()
    registry.register(instance)

    # 2. 添加 nginx 代理
    ingress_name = get_ingress(service_name)
    result, msg = create_config(ingress_name, f'http://{service_name}:{port}',
                                disabled=False)

    # 3. 把 service 的 port 记起来
    sc.save_local_service(service_name, {"port": port})
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
    registry = ConsulServiceRegistry()
    registry.deregister(instance_id)

    return flask.make_response({'success': True}), 200


@api.route('/services/<name>', methods=['GET'])
def get_service(name: str):
    discovery = ConsulServiceDiscovery()
    instances = discovery.get_instance(name)

    response = []
    for i in instances:
        response.append(
            {
                'instance_id': i.instance_id,
                'endpoint': i.endpoint,
                'metadata': i.metadata,
                'service_name': i.service_name,
                'tags': i.tags,
            }
        )

    return flask.make_response({'success': True, 'endpoints': response})


@api.route('/services/<name>', methods=['PUT'])
def put_services(name: str):
    request = flask.request.get_json()
    # 1. save in sc
    sc.save_service(name, request['endpoint'])
    # 2. update config
    ingress_name = get_ingress(name)

    if f'http://{sc.services.external_ip}:{sc.services.local_service_config[name]["port"]}' == \
            request['endpoint']['endpoint']:
        create_config(ingress_name,
                      f'http://{name}:{sc.services.local_service_config[name]["port"]}',
                      disabled=False)
    else:
        create_config(ingress_name, request['endpoint']['endpoint'])

    # 3. write hosts in /etc/hosts
    add_host(HOST, ingress_name)
    # 3. reload nginx
    reload()
    return flask.make_response({'success': True})


@api.route('/services', methods=['GET'])
def get_services():
    # 1. get all service name
    discovery = ConsulServiceDiscovery()
    all_services_name = discovery.get_services()

    # 2. get all service config
    response = []
    for name in all_services_name:
        service = {
            'service_name': name
        }
        if name in sc.services.service_config:
            service['instance_id'] = sc.services.service_config[name]['instance_id']
            service['endpoint'] = sc.services.service_config[name]['endpoint']
            service['tags'] = sc.services.service_config[name]['tags']
        else:
            service['instance_id'] = ''
            service['endpoint'] = ''
            service['tags'] = []
        response.append(service)
    return flask.make_response({'success': True, 'data': response}), 200
