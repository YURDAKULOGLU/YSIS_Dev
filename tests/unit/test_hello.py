import unittest
from src.hello_world import main

class TestHelloWorld(unittest.TestCase):
    def test_main(self):
        """
        main fonksiyonunu test eder.
        
        'Hello World' mesajının ekrana yazdırıldığını doğrular.
        """
        from io import StringIO
        import sys

        # Redirect stdout to capture the print statement
        captured_output = StringIO()
        sys.stdout = captured_output

        main()

        # Reset redirect.
        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue().strip(), 'Hello World')
