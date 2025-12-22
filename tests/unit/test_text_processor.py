import unittest
from src.utils.text_processor import count_vowels

class TestTextProcessor(unittest.TestCase):
    def test_count_vowels_normal_cases(self):
        self.assertEqual(count_vowels("hello"), 2)
        self.assertEqual(count_vowels("world"), 1)
        self.assertEqual(count_vowels("python"), 1)

    def test_count_vowels_edge_cases(self):
        self.assertEqual(count_vowels(""), 0)  # Empty string
        self.assertEqual(count_vowels("bcdfg"), 0)  # No vowels

    def test_count_vowels_uppercase(self):
        self.assertEqual(count_vowels("HELLO"), 2)
        self.assertEqual(count_vowels("WORLD"), 1)

    def test_count_vowels_mixed_case(self):
        self.assertEqual(count_vowels("HeLLo WoRLd"), 3)

    def test_count_vowels_with_numbers(self):
        self.assertEqual(count_vowels("h3ll0"), 2)
        self.assertEqual(count_vowels("w0rld"), 1)

    def test_count_vowels_with_special_characters(self):
        self.assertEqual(count_vowels("h@ll!o"), 2)
        self.assertEqual(count_vowels("w#or$ld%"), 1)

    def test_count_vowels_invalid_input(self):
        with self.assertRaises(TypeError):
            count_vowels(None)  # None input
        with self.assertRaises(TypeError):
            count_vowels(12345)  # Integer input
        with self.assertRaises(TypeError):
            count_vowels([1, 2, 3])  # List input
