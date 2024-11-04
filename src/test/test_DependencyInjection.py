import unittest
from ReFreSH.DependencyInjection import ServiceDescriptor, ServiceType, ServiceProvider, ServiceInstantiationFailure

class TestDependencyInjection(unittest.TestCase):
    def test_service_descriptor_initialization(self):
        """Test initialization of ServiceDescriptor."""
        # 这里定义一个简单的工厂函数，返回一个字符串实例
        factory_function = lambda: "default_string"
        descriptor = ServiceDescriptor(str, ServiceType.Singleton, factory=factory_function)

        # 验证服务类型和实际类型
        self.assertEqual(descriptor.TService, str)
        self.assertEqual(descriptor.TActual, str)

        # 通过工厂函数创建服务实例
        instance = descriptor.Factory()
        self.assertEqual(instance, "default_string")

    def test_service_descriptor_factory_function(self):
        """Test ServiceDescriptor can use a factory function."""
        def factory_function():
            return "created_instance"

        descriptor = ServiceDescriptor(str, ServiceType.Singleton, factory=factory_function)
        service = descriptor.CreateInstance(ServiceProvider({}))
        self.assertEqual(service, "created_instance")

    def test_service_instantiation_failure(self):
        """Test ServiceInstantiationFailure raises correctly."""
        with self.assertRaises(ServiceInstantiationFailure):
            raise ServiceInstantiationFailure(str, None)

if __name__ == '__main__':
    unittest.main()
