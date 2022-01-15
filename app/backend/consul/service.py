import consul
from app.backend.consul.register import ServiceInstance


class ConsulServiceDiscovery(object):
    _consul = None

    def __init__(self, host: str = "consul.service.consul.stage",
                 port: int = 80, token: str = None):
        self.host = host
        self.port = port
        self.token = token
        self._consul = consul.Consul(host, port, token=token)

    def get_services(self) -> list:
        return self._consul.catalog.services()[1].keys()

    def get_instance(self, service_id: str) -> list:
        origin_instances = self._consul.catalog.service(service_id)[1]
        result = []
        for oi in origin_instances:
            result.append(ServiceInstance(
                oi.get("ServiceName"),
                oi.get("ServiceAddress"),
                oi.get("ServicePort"),
                oi.get("ServiceMeta"),
                oi.get("ServiceID"),
                oi.get("ServiceTags")
            ))
        return result
