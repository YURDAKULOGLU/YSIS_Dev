def count_vowels(input_string: str) -> int:
    """
    Counts the number of vowels in the given string.

    Args:
        input_string (str): The string to count vowels in.

    Returns:
        int: The number of vowels in the input string.
    """
    vowels = "aeiou"
    return sum(1 for char in input_string.lower() if char in vowels)
# Unit tests for count_vowels function
import unittest

class TestTextProcessor(unittest.TestCase):
    def test_count_vowels(self):
        self.assertEqual(count_vowels("hello"), 2)
        self.assertEqual(count_vowels("world"), 1)
        self.assertEqual(count_vowels("AEIOU"), 5)
        self.assertEqual(count_vowels(""), 0)
        self.assertEqual(count_vowels("bcdfg"), 0)
        self.assertEqual(count_vowels("aAeEiIoOuU"), 10)

if __name__ == "__main__":
    unittest.main()
