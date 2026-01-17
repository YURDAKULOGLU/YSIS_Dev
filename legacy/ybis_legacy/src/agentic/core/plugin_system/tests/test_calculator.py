import unittest
from src.agentic.core.plugins.builtin.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        result = self.calculator.execute("add", 1, 2)
        self.assertEqual(result, 3)

    def test_subtract(self):
        result = self.calculator.execute("subtract", 5, 3)
        self.assertEqual(result, 2)

    def test_multiply(self):
        result = self.calculator.execute("multiply", 4, 6)
        self.assertEqual(result, 24)

    def test_divide(self):
        result = self.calculator.execute("divide", 10, 2)
        self.assertEqual(result, 5)

if __name__ == "__main__":
    unittest.main()
