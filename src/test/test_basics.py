import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


from ReFreSH.MobileSuit import Suit, SuitInfo, SuitAlias, SuitIgnore, SuitConfig

class TestMobileSuitBasics(unittest.TestCase):
    """
    PyMobileSuit 的基础冒烟测试 (Smoke Test)
    """

    def test_config_modification(self):
        """测试 Config 配置能否被正常修改"""
        original_locale = SuitConfig.LOCALE
        try:
            SuitConfig.LOCALE = 'zh'
            self.assertEqual(SuitConfig.LOCALE, 'zh')
            SuitConfig.LOCALE = 'en'
            self.assertEqual(SuitConfig.LOCALE, 'en')
        finally:
            SuitConfig.LOCALE = original_locale

    def test_app_decorators(self):
        """测试装饰器能否正常应用在类方法上"""
        try:
            class DemoApp:
                @SuitInfo("test_command")
                def cmd_func(self): pass
                
                @SuitAlias("alias_cmd")
                def alias_func(self): pass

            app = DemoApp()
            self.assertTrue(hasattr(app, 'cmd_func'))
        except Exception as e:
            self.fail(f"应用 MobileSuit 装饰器时抛出了异常: {e}")

if __name__ == '__main__':
    unittest.main()