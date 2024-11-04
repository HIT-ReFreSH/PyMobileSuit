import unittest

from ReFreSH.MobileSuit.Core.SuitMethodParameterInfo import SuitMethodParameterInfo, TailParameterType # type: ignore

class TestSuitMethodParameterInfo(unittest.TestCase):

    def test_default_values(self):
        param_info = SuitMethodParameterInfo()
        self.assertEqual(param_info.TailParameterType, TailParameterType.NoParameter)
        self.assertEqual(param_info.MinParameterCount, 0)
        self.assertEqual(param_info.NonArrayParameterCount, 0)
        self.assertEqual(param_info.MaxParameterCount, 0)

    def test_tail_parameter_type(self):
        param_info = SuitMethodParameterInfo()
        param_info.TailParameterType = TailParameterType.Normal
        self.assertEqual(param_info.TailParameterType, TailParameterType.Normal)

    def test_parameter_counts(self):
        param_info = SuitMethodParameterInfo()
        param_info.MinParameterCount = 5
        self.assertEqual(param_info.MinParameterCount, 5)
        param_info.NonArrayParameterCount = 3
        self.assertEqual(param_info.NonArrayParameterCount, 3)
        param_info.MaxParameterCount = 10
        self.assertEqual(param_info.MaxParameterCount, 10)

if __name__ == '__main__':
    unittest.main()