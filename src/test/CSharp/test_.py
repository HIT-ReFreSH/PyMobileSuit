import unittest
from ReFreSH.CSharp import NullCollapse


class TestCSharp(unittest.TestCase):

    def test_null_collapse_with_none(self):
        """Test null_collapse returns default value when obj is None."""
        default_value = "default"
        result = NullCollapse(None, default_value)
        self.assertEqual(result, default_value)

    def test_null_collapse_with_value(self):
        """Test null_collapse returns the original value when obj is not None."""
        result = NullCollapse("some_value", "default")
        self.assertEqual(result, "some_value")


if __name__ == '__main__':
    unittest.main()
