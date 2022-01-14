from dataclasses import dataclass
import consul


@dataclass
class ServiceInstance(object):
    service_id: str
    host: str
    port: int
    secure: bool = False
    metadata: dict = None
    instance_id: str = None


class ConsulServiceRegistry(object):
    _consul = None

    def __init__(self, host: str = "consul.service.consul.stage",
                 port: int = 80, token: str = None):
        self.host = host
        self.port = port
        self.token = token
        self._consul = consul.Consul(host, port, token=token)

    def register(self, service_instance: ServiceInstance):
        schema = "http"
        uri = f'{schema}://{service_instance.host}:{service_instance.port}/api/health'
        print(uri)
        # check = consul.Check.http(uri, "1s", "3s", "10s")
        self._consul.agent.service.register(service_instance.service_id,
                                            service_id=service_instance.instance_id,
                                            address=service_instance.host,
                                            port=service_instance.port,
                                            # check=check,
                                            tags=["local"])
        self._instance_id = service_instance.instance_id

    def deregister(self, instance_id):
        self._consul.agent.service.deregister(service_id=instance_id)
