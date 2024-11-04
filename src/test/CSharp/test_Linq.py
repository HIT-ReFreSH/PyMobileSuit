import unittest

from ReFreSH.CSharp.Linq import FirstOrDefault


class TestReFreSH(unittest.TestCase):


    def test_linq_first_or_default_found(self):
        """Test linq_first_or_default returns the first matching element."""
        l = [1, 2, 3, 4, 5]
        f = lambda x: x > 3
        result = FirstOrDefault(l, f)
        self.assertEqual(result, 4)

    def test_linq_first_or_default_not_found(self):
        """Test linq_first_or_default returns None when no matching element is found."""
        l = [1, 2, 3]
        f = lambda x: x > 5
        result = FirstOrDefault(l, f)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
