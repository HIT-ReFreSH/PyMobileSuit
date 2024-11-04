import unittest
from service_management import ServiceType, ServiceDescriptor, ServiceBag, ServiceProvider, ServiceNotFound, \
    ScopedServiceProvider
# 测试ServiceDescriptor类
class TestServiceDescriptor(unittest.TestCase):
    def test_create_instance(self):
        def factory(dependency):
            return dependency * 2
        descriptor = ServiceDescriptor(ServiceType.Singleton, factory, [int])
        service_bag = ServiceBag()
        service_bag.addDescriptor(descriptor)
        provider = service_bag.build()
        instance = descriptor.CreateInstance(provider)
        input_value = 5
        result = instance(input_value)
        self.assertEqual(result, input_value * 2)
# 测试ServiceBag类
class TestServiceBag(unittest.TestCase):
    def test_build(self):
        service_bag = ServiceBag()
        def factory1(dependency):
            return dependency * 2
        descriptor1 = ServiceDescriptor(ServiceType.Singleton, factory1, [int])
        service_bag.addDescriptor(descriptor1)
        provider = service_bag.build()
        self.assertEqual(type(provider), ServiceProvider)
# 测试ServiceProvider类
class TestServiceProvider(unittest.TestCase):
    def test_get_required_service(self):
        service_bag = ServiceBag()
        def factory1(dependency):
            return dependency * 2
        descriptor1 = ServiceDescriptor(ServiceType.Singleton, factory1, [int])
        service_bag.addDescriptor(descriptor1)
        provider = service_bag.build()
        service = provider.getRequiredService(factory1)
        input_value = 3
        result = service(input_value)
        self.assertEqual(result, input_value * 2)
    def test_service_not_found(self):
        service_bag = ServiceBag()
        def factory1(dependency):
            return dependency * 2
        descriptor1 = ServiceDescriptor(ServiceType.Singleton, factory1, [int])
        service_bag.addDescriptor(descriptor1)
        provider = service_bag.build()
        with self.assertRaises(ServiceNotFound):
            provider.getRequiredService(lambda x: x + 1)
# 测试ScopedServiceProvider类
class TestScopedServiceProvider(unittest.TestCase):
    def test_create_scope(self):
        service_bag = ServiceBag()
        def factory1(dependency):
            return dependency * 2
        descriptor1 = ServiceDescriptor(ServiceType.Singleton, factory1, [int])
        service_bag.addDescriptor(descriptor1)
        provider = service_bag.build()
        scope = provider.createScope()
        self.assertEqual(type(scope), ScopedServiceProvider)
if __name__ == '__main__':
    unittest.main()