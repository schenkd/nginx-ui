import json

class ServiceConfig(object):
    def __init__(self):
        self.services = None
        with open('/home/app/nginx-ui/app/backend/config/config.json', 'r') as f:
            data = json.load(f)
            self.services = data

    def save_service(self, name, instance):
        self.services[name] = instance

        with open('/home/app/nginx-ui/app/backend/config/config.json', 'w') as f:
            jsonstr = json.dumps(self.services)
            f.write(jsonstr)

sc = ServiceConfig()
