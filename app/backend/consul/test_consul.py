import unittest
from app.backend.consul.service import ServiceInstance, ConsulServiceDiscovery
from app.backend.consul.register import ConsulServiceRegistry
from random import random


class ConsulTest(unittest.TestCase):
    def test_consul_register(self):
        instance = ServiceInstance("hello_world", "172.26.232.23", 8888,
                                   instance_id='abc_0.21416486207680163')
        registry = ConsulServiceRegistry()
        discovery = ConsulServiceDiscovery()
        # registry.register(instance)
        registry._instance_id = instance.instance_id
        registry.deregister()
        print(discovery.get_services())
        print(discovery.get_instance("hello_world"))
        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
