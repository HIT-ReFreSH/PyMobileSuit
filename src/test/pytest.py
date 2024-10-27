import unittest
from inspect import signature
from typing import Any, List
from unittest.mock import Mock

from ReFreSH.MobileSuit.Core.SuitBuildUtils import CreateConverterFactory, GetArg, GetArrayArg


class SuitContext:
    def GetRequiredService(self, service_type):
        # Mock implementation
        pass

    def GetService(self, service_type):
        # Mock implementation
        pass


class SuitArgParserInfo:
    def __init__(self, name: str, Converter: Any):
        self.Name = name
        self.Converter = Converter

class IParsingService:
    def Get(self, t, name: str):
        # Mock implementation
        pass

class SuitMethodParameterInfo:
    # Define necessary attributes and methods if any
    pass

def null_collapse(value, default):
    return value if value else default

def get_parser(function, param_name):
    # Mock function to return SuitArgParserInfo
    return SuitArgParserInfo('', None)
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.context = Mock(spec=SuitContext)
        self.parsing_service = Mock(spec=IParsingService)
        self.context.GetRequiredService.return_value = self.parsing_service

    def test_create_converter_factory_with_str_type(self):
        converter = CreateConverterFactory(str, None)(self.context)
        result = converter("test")
        self.assertEqual(result, "test")

    def test_create_converter_factory_with_list_type(self):
        list_str_converter = CreateConverterFactory(List[str], None)(self.context)
        self.parsing_service.Get.return_value = "parsed_string"
        result = list_str_converter("test")
        self.assertEqual(result, "parsed_string")

    def test_get_arg_with_none_arg(self):
        def func(arg: int):
            pass

        param = next(iter(signature(func).parameters.values()))
        result, step = GetArg(param, func, None, self.context)
        self.assertEqual(step, 0)
        self.assertIsNone(result)  # Assuming default is None for int

    def test_get_arg_with_context_type(self):
        def func(context: SuitContext):
            pass

        param = next(iter(signature(func).parameters.values()))
        result, step = GetArg(param, func, None, self.context)
        self.assertEqual(step, 0)
        self.assertEqual(result, self.context)

    def test_get_arg_with_service_type(self):
        class SomeService:
            pass

        def func(service: SomeService):
            pass

        param = next(iter(signature(func).parameters.values()))
        self.context.GetService.return_value = SomeService()
        result, step = GetArg(param, func, None, self.context)
        self.assertEqual(step, 0)
        self.assertIsInstance(result, SomeService)

    def test_get_array_arg(self):
        def func(args: List[int]):
            pass

        param = next(iter(signature(func).parameters.values()))
        self.parsing_service.Get.return_value = 42  # Mocking parsed integer
        result, step = GetArrayArg(param, func, ["1", "2", "3"], self.context)
        self.assertEqual(step, 3)
        self.assertEqual(result, [42, 42, 42])


if __name__ == '__main__':
    unittest.main()
