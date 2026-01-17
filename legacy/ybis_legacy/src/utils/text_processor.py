def count_vowels(input_string: str) -> int:
    """
    Counts the number of vowels in the provided text.

    Args:
        input_string (str): The string in which to count vowels.

    Returns:
        int: The total number of vowels found in the input string.
    """
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    vowels = "aeiou"
    leet_map = {
        "0": "o",
        "3": "e",
        "4": "a",
        "@": "a",
    }
    normalized_text = "".join(leet_map.get(char, char) for char in input_string.lower())
    return sum(1 for character in normalized_text if character in vowels)

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
