
import unittest

class MathWhiz:
    """
    A simple math utility class for system stress testing.
    """
    
    @staticmethod
    def fibonacci(n: int) -> int:
        """Returns the nth Fibonacci number."""
        if n < 0:
            raise ValueError("n must be non-negative")
        if n <= 1:
            return n
        return MathWhiz.fibonacci(n-1) + MathWhiz.fibonacci(n-2)

    @staticmethod
    def factorial(n: int) -> int:
        """Returns the factorial of n."""
        if n < 0:
            raise ValueError("n must be non-negative")
        if n == 0:
            return 1
        return n * MathWhiz.factorial(n-1)

    @staticmethod
    def is_prime(n: int) -> bool:
        """Checks if n is a prime number."""
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

class TestMathWhiz(unittest.TestCase):
    def test_fibonacci(self):
        self.assertEqual(MathWhiz.fibonacci(0), 0)
        self.assertEqual(MathWhiz.fibonacci(1), 1)
        self.assertEqual(MathWhiz.fibonacci(5), 5) # 0,1,1,2,3,5

    def test_factorial(self):
        self.assertEqual(MathWhiz.factorial(0), 1)
        self.assertEqual(MathWhiz.factorial(5), 120)

    def test_is_prime(self):
        self.assertTrue(MathWhiz.is_prime(7))
        self.assertFalse(MathWhiz.is_prime(4))
        self.assertFalse(MathWhiz.is_prime(1))

if __name__ == '__main__':
    unittest.main()
