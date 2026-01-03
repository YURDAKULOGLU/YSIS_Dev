import unittest
from src.sandbox_executor import DockerSandboxExecutor

class TestDockerSandboxExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = DockerSandboxExecutor()

    def test_run_code_success(self):
        code = "print('Hello, World!')"
        result = self.executor.run_code(code)
        self.assertEqual(result.strip(), "Hello, World!")

    def test_run_code_with_error(self):
        code = "print(1 / 0)"
        result = self.executor.run_code(code)
        self.assertIn("ZeroDivisionError", result)

if __name__ == "__main__":
    unittest.main()
