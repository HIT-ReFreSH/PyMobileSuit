import unittest
from ReFreSH.ConsoleColor import ConsoleColor
from ReFreSH.CSharp import null_collapse,linq_first_or_default
from ReFreSH.DependencyInjection import ServiceDescriptor, ServiceType, ServiceProvider, ServiceInstantiationFailure

class TestReFreSH(unittest.TestCase):

    def test_null_collapse_with_none(self):
        """Test null_collapse returns default value when obj is None."""
        default_value = "default"
        result = null_collapse(None, default_value)
        self.assertEqual(result, default_value)

    def test_null_collapse_with_value(self):
        """Test null_collapse returns the original value when obj is not None."""
        result = null_collapse("some_value", "default")
        self.assertEqual(result, "some_value")

    def test_linq_first_or_default_found(self):
        """Test linq_first_or_default returns the first matching element."""
        l = [1, 2, 3, 4, 5]
        f = lambda x: x > 3
        result = linq_first_or_default(l, f)
        self.assertEqual(result, 4)

    def test_linq_first_or_default_not_found(self):
        """Test linq_first_or_default returns None when no matching element is found."""
        l = [1, 2, 3]
        f = lambda x: x > 5
        result = linq_first_or_default(l, f)
        self.assertIsNone(result)

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
