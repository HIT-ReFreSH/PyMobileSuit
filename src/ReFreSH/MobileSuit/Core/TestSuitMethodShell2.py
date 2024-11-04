import unittest
from unittest.mock import Mock, AsyncMock
from ReFreSH.MobileSuit.Core.SuitContext import SuitContext
from ReFreSH.MobileSuit.Core.SuitMethodShell import SuitMethodShell
from ReFreSH.MobileSuit.Core.SuitBuildUtils import GetMethodParameterInfo
from ReFreSH.MobileSuit.RequestStatus import RequestStatus
from ReFreSH.MobileSuit.Core.SuitMethodParameterInfo import TailParameterType
import unittest
import asyncio
class TestSuitMethodShell(unittest.TestCase):

    def setUp(self):
        # 创建一个模拟方法，用于测试
        def mock_method(param1, param2='default'):
            return f"param1={param1}, param2={param2}"

        # 创建模拟的 factory 方法和其他依赖项
        self.factory_mock = Mock()
        self.method_shell = SuitMethodShell(
            method=mock_method,
            factory=self.factory_mock,
            absoluteName="mock_method"
        )

    def test_member_count(self):
        # 测试 MemberCount 属性
        self.assertEqual(self.method_shell.MemberCount, 2)

    def test_may_execute(self):
        # 测试 MayExecute 方法
        request = ["mock_method", "param1"]
        self.method_shell.FriendlyNames = ["mock_method"]
        self.assertTrue(self.method_shell.MayExecute(request))

        # 测试无效请求
        request_invalid = ["invalid_method", "param1"]
        self.assertFalse(self.method_shell.MayExecute(request_invalid))
    def test_execute_method(self):
        # 用 asyncio.run() 来调用异步测试方法
        asyncio.run(self.execute_method_async())

    async def execute_method_async(self):
        # 测试 Execute 方法
        # 创建一个模拟的 sp 参数（根据实际情况调整）
        sp_mock = Mock()

        sp_mock.GetRequiredService().Get().return_value = "value1"

        context = SuitContext(sp=sp_mock)  # 传入所需的 sp 参数

        context.Request = ["mock_method", "value1", "value2"]

        await self.method_shell.Execute(context)

        # 验证请求状态
        self.assertEqual(context.RequestStatus, RequestStatus.Handled)
        self.assertEqual(context.Response, "param1=value1, param2=value1")

if __name__ == '__main__':
    unittest.main()
