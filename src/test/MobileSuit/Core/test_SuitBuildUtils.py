import sys
sys.path.insert(0, r'C:\kaiyuan_ex\PyMobileSuit\src')

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

        self.mock_context.GetService.return_value = None

        self.mock_parsing_service = Mock(spec=IParsingService)
        self.mock_function = Mock()
        #添加缺失的属性，避免get_injected函数出错
        self.mock_function.____suit_injected = []
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
        self.mock_function.__dict__["____suit_parser"] = {}
        result, length = GetArrayArg(self.mock_parameter, self.mock_function, arg_list, self.mock_context)
        self.assertEqual(result, arg_list)
        self.assertEqual(length, len(arg_list))

    def test_GetMethodParameterInfo_no_parameters(self):
        def test_func():
            pass

        #设置必要的属性
        test_func.____suit_injected = []
        test_func.__annotations__ = {}
        info = GetMethodParameterInfo(test_func)
        self.assertEqual(info.TailParameterType, TailParameterType.NoParameter)

    def test_CreateInstance_with_mock_service(self):
        self.mock_context.GetService.return_value = "mock_service"
        instance = CreateInstance(str, self.mock_context)
        self.assertEqual(instance, "mock_service")

    def test_CreateInstanceWithProvider(self):
        class MockType:
            def __init__(self):
                pass

        mock_provider = Mock()
        mock_provider.GetService.return_value = None
        instance = CreateInstanceWithProvider(MockType, mock_provider)
        self.assertIsNotNone(instance)

    def test_GetArgs_no_arguments(self):
        def test_func():
            pass
        #设置必要的属性
        test_func.____suit_injected = []
        test_func.__annotations__ = {}
        result = GetArgs(test_func, [], self.mock_context)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)

    def test_get_arg_with_none_arg(self):
        def func(arg: int):
            pass

        param = next(iter(signature(func).parameters.values()))
        result_step = GetArg(param, func, None, self.mock_context)
        if isinstance(result_step, tuple):
            result, step = result_step
        else:
            result, step = result_step, 0
        self.assertEqual(step, 0)
        from inspect import _empty
        self.assertIs(result, _empty)

    def test_get_arg_with_context_type(self):
        def func(context: SuitContext):
            pass

        param = next(iter(signature(func).parameters.values()))
        result, step = GetArg(param, func, None, self.mock_context)
        self.assertEqual(step, 0)
        self.assertEqual(result, self.mock_context)

    def test_get_arg_with_service_type(self):
        class SomeService:
            pass

        def func(service: SomeService):
            pass

        param = next(iter(signature(func).parameters.values()))

        # 确保 GetService 返回 SomeService 实例
        self.mock_context.GetService.return_value = SomeService()

        # 调用 GetArg 函数
        result = GetArg(param, func, None, self.mock_context)

        # 如果结果不是元组，则将其转换为 (result, 0)
        if not isinstance(result, tuple):
            result = (result, 0)

        # 解包结果
        service_instance, step = result

        # 断言检查
        self.assertEqual(step, 0)
        self.assertIsInstance(service_instance, SomeService)

    def test_get_array_arg(self):
        def func(args: List[int]):
            pass
        param = next(iter(signature(func).parameters.values()))
        self.mock_parsing_service.Get.side_effect = lambda myT, name: lambda s: 42
        self.mock_context.GetRequiredService.return_value = self.mock_parsing_service
        result, step = GetArrayArg(param, func, ["1", "2", "3"], self.mock_context)
        self.assertEqual(step, 3)
        self.assertEqual(result, [42, 42, 42])


if __name__ == '__main__':
    unittest.main()
