import ast
import json
import os
import unittest

from src.monitoring.code_quality_monitor import monitor_code_quality


def _complexity(content: str) -> dict:
    tree = ast.parse(content)
    return {
        "lines": len(content.splitlines()),
        "functions": sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree)),
        "classes": sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree)),
    }


class TestCodeQuality(unittest.TestCase):
    def setUp(self):
        self.temp_dir = os.path.join(os.getcwd(), "temp_test_dir")
        os.makedirs(self.temp_dir, exist_ok=True)
        self.sample_file_path = os.path.join(self.temp_dir, "sample.py")

    def tearDown(self):
        if os.path.exists(self.sample_file_path):
            os.remove(self.sample_file_path)
        history_file = os.path.join(self.temp_dir, "code_complexity_history.json")
        if os.path.exists(history_file):
            os.remove(history_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_monitor_code_quality_initial_run(self):
        sample_content = "def test_function():\n    pass\n"
        with open(self.sample_file_path, "w", encoding="utf-8") as f:
            f.write(sample_content)

        expected = _complexity(sample_content)

        with self.assertLogs("root", level="INFO") as log:
            monitor_code_quality(self.temp_dir)
            joined = "\n".join(log.output)
            self.assertIn(f"Parsing file: {self.sample_file_path}", joined)
            self.assertIn(
                f"Code Complexity of sample.py: Lines={expected['lines']}, Functions={expected['functions']}, Classes={expected['classes']}",
                joined,
            )

    def test_monitor_code_quality_with_regression(self):
        history_file = os.path.join(self.temp_dir, "code_complexity_history.json")
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump({"sample.py": {"lines": 4, "functions": 1, "classes": 0}}, f)

        modified_content = (
            "def test_function():\n"
            "    pass\n"
            "\ndef another_test_function():\n"
            "    pass\n"
            "\nclass SampleClass:\n"
            "    pass\n"
        )
        with open(self.sample_file_path, "w", encoding="utf-8") as f:
            f.write(modified_content)

        expected = _complexity(modified_content)

        with self.assertLogs("root", level="INFO") as log:
            monitor_code_quality(self.temp_dir)
            joined = "\n".join(log.output)
            self.assertIn(f"Parsing file: {self.sample_file_path}", joined)
            self.assertIn("Regression detected in sample.py:", joined)
            self.assertIn(str(expected["lines"]), joined)
            self.assertIn(str(expected["functions"]), joined)
            self.assertIn(str(expected["classes"]), joined)

    def test_monitor_code_quality_no_regression(self):
        history_file = os.path.join(self.temp_dir, "code_complexity_history.json")
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump({"sample.py": {"lines": 4, "functions": 1, "classes": 0}}, f)

        sample_content = "def test_function():\n    pass\n"
        with open(self.sample_file_path, "w", encoding="utf-8") as f:
            f.write(sample_content)

        with self.assertLogs("root", level="INFO") as log:
            monitor_code_quality(self.temp_dir)
            joined = "\n".join(log.output)
            self.assertIn(f"Parsing file: {self.sample_file_path}", joined)
            self.assertIn("No regression detected in sample.py. Complexity remains the same.", joined)

    def test_monitor_code_quality_with_no_change(self):
        history_file = os.path.join(self.temp_dir, "code_complexity_history.json")
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump({"sample.py": {"lines": 4, "functions": 1, "classes": 0}}, f)

        sample_content = "def test_function():\n    pass\n"
        with open(self.sample_file_path, "w", encoding="utf-8") as f:
            f.write(sample_content)

        with self.assertLogs("root", level="INFO") as log:
            monitor_code_quality(self.temp_dir)
            joined = "\n".join(log.output)
            self.assertIn(f"Parsing file: {self.sample_file_path}", joined)
            self.assertIn("No regression detected in sample.py. Complexity remains the same.", joined)

    def test_monitor_code_quality_with_significant_regression(self):
        history_file = os.path.join(self.temp_dir, "code_complexity_history.json")
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump({"sample.py": {"lines": 4, "functions": 1, "classes": 0}}, f)

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
        with open(self.sample_file_path, "w", encoding="utf-8") as f:
            f.write(modified_content)

        expected = _complexity(modified_content)

        with self.assertLogs("root", level="INFO") as log:
            monitor_code_quality(self.temp_dir)
            joined = "\n".join(log.output)
            self.assertIn(f"Parsing file: {self.sample_file_path}", joined)
            self.assertIn("Regression detected in sample.py:", joined)
            self.assertIn(str(expected["lines"]), joined)
            self.assertIn(str(expected["functions"]), joined)
            self.assertIn(str(expected["classes"]), joined)


if __name__ == "__main__":
    unittest.main()
