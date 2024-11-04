import unittest
from ReFreSH.MobileSuit.Core.Services.AppInfo import SuitAppInfo  # 假设 SuitAppInfo 类定义在名为 your_module 的模块中

class TestSuitAppInfo(unittest.TestCase):
    def setUp(self):
        # 在每个测试方法之前调用，设置测试环境
        self.app_info = SuitAppInfo()

    def test_initial_state(self):
        # 测试初始化状态
        self.assertEqual(self.app_info.AppName, "")#检查 AppName 是否为空字符串
        self.assertEqual(self.app_info.StartArgs, [])#检查 StartArgs 是否为空列表

    def test_set_app_name(self):
        # 测试设置应用名称
        self.app_info.AppName = "TestApp"
        self.assertEqual(self.app_info.AppName, "TestApp")#检查 AppName 是否成功设置为 "TestApp"

    def test_set_start_args(self):
        # 测试设置启动参数
        args = ["-a", "--b", "value"]
        self.app_info.StartArgs = args
        self.assertEqual(self.app_info.StartArgs, args)#检查 StartArgs 是否成功设置为 ["-a", "--b", "value"]

    def test_set_and_get_properties(self):
        # 综合测试属性的设置与获取
        self.app_info.AppName = "MyApp"
        self.app_info.StartArgs = ["--flag", "param1", "param2"]

        self.assertEqual(self.app_info.AppName, "MyApp")#检查 AppName 是否成功设置为 "MyApp"
        self.assertListEqual(self.app_info.StartArgs, ["--flag", "param1", "param2"])#检查 StartArgs 是否成功设置为 ["--flag", "param1", "param2"]

if __name__ == '__main__':
    unittest.main()
