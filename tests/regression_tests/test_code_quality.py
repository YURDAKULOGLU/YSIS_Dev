import unittest
from src.monitoring.code_quality_monitor import monitor_code_quality, check_for_regressions
import os
import json
import logging

class TestCodeQuality(unittest.TestCase):
    """
    Test cases for code quality monitoring.
    """

    def setUp(self):
        # Create a temporary directory and sample Python file for testing
        self.temp_dir = os.path.join(os.getcwd(), 'temp_test_dir')
        os.makedirs(self.temp_dir, exist_ok=True)
        self.sample_file_path = os.path.join(self.temp_dir, 'sample.py')

    def tearDown(self):
        # Clean up temporary directory
        if os.path.exists(self.sample_file_path):
            os.remove(self.sample_file_path)
        history_file = os.path.join(self.temp_dir, 'code_complexity_history.json')
        if os.path.exists(history_file):
            os.remove(history_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_monitor_code_quality_initial_run(self):
        """
        Örnek bir dizinde ilk çalıştırma durumunda monitor_code_quality fonksiyonunu test eder.
        """
        sample_content = "def test_function():\n    pass\n"
        with open(self.sample_file_path, 'w', encoding='utf-8') as f:
            f.write(sample_content)

        # Test the function
        with self.assertLogs('root', level='INFO') as log:
            monitor_code_quality(self.temp_dir)
            self.assertTrue(any(f"Parsing file: {self.sample_file_path}" in line for line in log.output))
            self.assertTrue(any("Code Complexity of sample.py: Lines=2, Functions=1, Classes=0" in line for line in log.output))

    def test_monitor_code_quality_with_regression(self):
        """
        Örnek bir dizinde gerilemeleri tespit etmek için monitor_code_quality fonksiyonunu test eder.
        """
        # Create initial history file
        history_file = os.path.join(self.temp_dir, 'code_complexity_history.json')
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump({"sample.py": {"lines": 4, "functions": 1, "classes": 0}}, f)

        # Modify the sample file to simulate a regression
        modified_content = (
            "def test_function():\n"
            "    pass\n"
            "\ndef another_test_function():\n"
            "    pass\n"
            "\nclass SampleClass:\n"
            "    pass\n"
        )
        with open(self.sample_file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)

        # Test for regression detection
        with self.assertLogs('root', level='INFO') as log:
            monitor_code_quality(self.temp_dir)
            self.assertTrue(any(f"Parsing file: {self.sample_file_path}" in line for line in log.output))
            expected_warning = (
                "sample.py dosyasında gerileme algılandı:\n"
                "  - Satırlar: 7 (önceki: 4)\n"
                "  - Fonksiyonlar: 2 (önceki: 1)\n"
                "  - Sınıflar: 1 (önceki: 0)"
            )
            self.assertIn(expected_warning, "\n".join(log.output))

    def test_monitor_code_quality_no_regression(self):
        """
        Örnek bir dizinde gerileme olmadığını doğrulamak için monitor_code_quality fonksiyonunu test eder.
        """
        # Create initial history file
        history_file = os.path.join(self.temp_dir, 'code_complexity_history.json')
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump({"sample.py": {"lines": 4, "functions": 1, "classes": 0}}, f)

        # No modification to simulate no regression
        sample_content = "def test_function():\n    pass\n"
        with open(self.sample_file_path, 'w', encoding='utf-8') as f:
            f.write(sample_content)

        # Test for no regression detection
        with self.assertLogs('root', level='INFO') as log:
            monitor_code_quality(self.temp_dir)
            self.assertTrue(any(f"Parsing file: {self.sample_file_path}" in line for line in log.output))
            self.assertIn("No regression detected in sample.py. Complexity remains the same.", "\n".join(log.output))

    def test_monitor_code_quality_with_no_change(self):
        """
        Örnek bir dizinde herhangi bir değişiklik olmadığı durumda monitor_code_quality fonksiyonunu test eder.
        """
        # Create initial history file
        history_file = os.path.join(self.temp_dir, 'code_complexity_history.json')
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump({"sample.py": {"lines": 4, "functions": 1, "classes": 0}}, f)

        # No modification to simulate no change
        sample_content = (
            "def test_function():\n"
            "    pass\n"
        )
        with open(self.sample_file_path, 'w', encoding='utf-8') as f:
            f.write(sample_content)

        # Test for no change detection
        with self.assertLogs('root', level='INFO') as log:
            monitor_code_quality(self.temp_dir)
            self.assertTrue(any(f"Parsing file: {self.sample_file_path}" in line for line in log.output))
            self.assertIn("No regression detected in sample.py. Complexity remains the same.", "\n".join(log.output))

    def test_monitor_code_quality_with_significant_regression(self):
        """
        Örnek bir dizinde önemli bir gerilemeyi tespit etmek için monitor_code_quality fonksiyonunu test eder.
        """
        # Create initial history file
        history_file = os.path.join(self.temp_dir, 'code_complexity_history.json')
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump({"sample.py": {"lines": 4, "functions": 1, "classes": 0}}, f)

        # Modify the sample file to simulate a significant regression
        modified_content = (
            "def test_function():\n"
            "    pass\n"
            "\ndef another_test_function():\n"
            "    pass\n"
            "\nclass SampleClass:\n"
            "    def method1(self):\n"
            "        pass\n"
            "    def method2(self):\n"
            "        pass\n"
        )
        with open(self.sample_file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)

        # Test for significant regression detection
        with self.assertLogs('root', level='INFO') as log:
            monitor_code_quality(self.temp_dir)
            self.assertTrue(any(f"Parsing file: {self.sample_file_path}" in line for line in log.output))
            expected_warning = (
                "sample.py dosyasında gerileme algılandı:\n"
                "  - Satırlar: 9 (önceki: 4)\n"
                "  - Fonksiyonlar: 2 (önceki: 1)\n"
                "  - Sınıflar: 1 (önceki: 0)"
            )
            self.assertIn(expected_warning, "\n".join(log.output))

if __name__ == '__main__':
    unittest.main()
