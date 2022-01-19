import json
from dataclasses import dataclass
import dataclasses
import os


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


@dataclass
class Config(object):
    service_config: dict
    local_service_config: dict
    external_ip: str


class ServiceConfig(object):
    def __init__(self):
        self.services = None
        with open('/home/app/nginx-ui/app/backend/config/config.json',
                  'r') as f:
            data = json.load(f)
            self.services = Config(**data)

        if self.services.external_ip == "":
            self.services.external_ip = os.getenv("EXTERNAL_ENV")

    def _save(self):
        with open('/home/app/nginx-ui/app/backend/config/config.json',
                  'w') as f:
            jsonstr = json.dumps(self.services, cls=EnhancedJSONEncoder)
            f.write(jsonstr)

    def save_service(self, name, instance):
        self.services.service_config[name] = instance
        self._save()

    def save_local_service(self, name, instance):
        self.services.local_service_config[name] = instance
        self._save()

    def save_external_ip(self, ip):
        self.services.external_ip = ip
        self._save()


sc = ServiceConfig()
