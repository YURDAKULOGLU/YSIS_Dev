import unittest

from src.utils.string_reverser import reverse_string


class TestStringReverser(unittest.TestCase):
    def test_reverse_string(self):
        self.assertEqual(reverse_string(""), "")
        self.assertEqual(reverse_string("a"), "a")
        self.assertEqual(reverse_string("ab"), "ba")
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string("12345"), "54321")
        self.assertEqual(reverse_string("!@#$%"), "%$#@!")
        self.assertEqual(reverse_string("racecar"), "racecar")

if __name__ == '__main__':
    unittest.main()
