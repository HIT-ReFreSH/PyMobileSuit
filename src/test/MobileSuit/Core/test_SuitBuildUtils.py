import unittest
from unittest.mock import Mock, MagicMock
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

class TestSuitBuildUtils(unittest.TestCase):

    def setUp(self):
        # Set up mock SuitContext and other necessary mocks
        self.mock_context = Mock(spec=SuitContext)
        self.mock_function = Mock()
        self.mock_parameter = Mock()
        self.mock_parameter.annotation = str
        self.mock_parameter.default = None

    def test_CreateConverterFactory_string_type(self):
        parser_info = Mock()
        converter_factory = CreateConverterFactory(str, parser_info)
        converter = converter_factory(self.mock_context)
        self.assertEqual(converter("test"), "test")

    def test_GetArg_with_string_type(self):
        result, step = GetArg(self.mock_parameter, self.mock_function, "test_arg", self.mock_context)
        self.assertEqual(result, "test_arg")
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

if __name__ == '__main__':
    unittest.main()
