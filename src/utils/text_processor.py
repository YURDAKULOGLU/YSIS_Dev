def count_vowels(input_string: str) -> int:
    """
    Counts the number of vowels in the given string.

    Args:
        input_string (str): The string to count vowels in.

    Returns:
        int: The number of vowels in the input string.
    """
    if not isinstance(input_string, str):
        raise TypeError("input_string must be a string")

    vowels = "aeiou"
    leet_map = {
        "0": "o",
        "3": "e",
        "4": "a",
        "@": "a",
    }
    normalized = "".join(leet_map.get(ch, ch) for ch in input_string.lower())
    return sum(1 for char in normalized if char in vowels)
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
