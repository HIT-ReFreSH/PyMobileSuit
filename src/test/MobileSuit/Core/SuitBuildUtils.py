import unittest
from inspect import signature
from typing import List
from unittest.mock import Mock

from ReFreSH.MobileSuit.Core.Services.ParsingService import IParsingService
from ReFreSH.MobileSuit.Core.SuitBuildUtils import (
    CreateConverterFactory,
    GetArg,
    GetArrayArg,
    GetMethodParameterInfo,
    CreateInstance,
    CreateInstanceWithProvider,
    GetArgs,
    SuitMethodParameterInfo,
    TailParameterType
)
from ReFreSH.MobileSuit.Core.SuitContext import SuitContext
from ReFreSH.MobileSuit.Decorators import SuitArgParserInfo


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Set up mock SuitContext and other necessary mocks
        self.mock_context = Mock(spec=SuitContext)
        self.mock_parsing_service = Mock(spec=IParsingService)
        self.mock_function = Mock()
        self.mock_parameter = Mock()
        self.mock_parameter.annotation = str
        self.mock_parameter.default = None

    def test_CreateConverterFactory_with_str_type(self):
        converter = CreateConverterFactory(str, None)(self.mock_context)
        result = converter("test")
        self.assertEqual(result, "test")

    def test_CreateConverterFactory_with_list_type(self):
        list_str_converter = CreateConverterFactory(List[str], None)(self.mock_context)
        result = list_str_converter("parsed_string")
        self.assertEqual(result, "parsed_string")

    def test_GetArg_with_string_type(self):
        def func(arg: str):
            pass
        result, step = GetArg(self.mock_parameter, func, "arg", self.mock_context)
        self.assertEqual(result, "arg")
        self.assertEqual(step, 1)

    def test_GetArrayArg_with_string_list(self):
        self.mock_parameter.annotation = list[str]
        arg_list = ["arg1", "arg2"]
        result, length = GetArrayArg(self.mock_parameter, self.mock_function, arg_list, self.mock_context)
        self.assertEqual(result, arg_list)
        self.assertEqual(length, len(arg_list))

    def test_GetMethodParameterInfo_no_parameters(self):
        self.mock_function.__annotations__ = {}
        info = GetMethodParameterInfo(self.mock_function)
        self.assertEqual(info.TailParameterType, TailParameterType.NoParameter)

    def test_CreateInstance_with_mock_service(self):
        self.mock_context.GetService.return_value = "mock_service"
        instance = CreateInstance(str, self.mock_context)
        self.assertEqual(instance, "mock_service")

    def test_CreateInstanceWithProvider(self):
        mock_provider = Mock()
        mock_provider.GetService.return_value = None
        mock_type = Mock()
        instance = CreateInstanceWithProvider(mock_type, mock_provider)
        self.assertIsNone(instance)

    def test_GetArgs_no_arguments(self):
        self.mock_function.__annotations__ = {}
        result = GetArgs(self.mock_function, [], self.mock_context)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)

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
        self.mock_parsing_service.Get.return_value = 42  # Mocking parsed integer
        result, step = GetArrayArg(param, func, ["1", "2", "3"], self.context)
        self.assertEqual(step, 3)
        self.assertEqual(result, [42, 42, 42])


if __name__ == '__main__':
    unittest.main()
