import unittest

from utils.math_helper import fibonacci


class TestMathHelper(unittest.TestCase):

    def test_fibonacci_zero_terms(self):
        self.assertEqual(fibonacci(0), [])

    def test_fibonacci_one_term(self):
        self.assertEqual(fibonacci(1), [0])

    def test_fibonacci_two_terms(self):
        self.assertEqual(fibonacci(2), [0, 1])

    def test_fibonacci_five_terms(self):
        self.assertEqual(fibonacci(5), [0, 1, 1, 2, 3])

    def test_fibonacci_ten_terms(self):
        self.assertEqual(fibonacci(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

if __name__ == '__main__':
    unittest.main()
