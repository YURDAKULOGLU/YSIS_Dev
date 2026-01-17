import unittest
from src.agentic.core.plugins.builtin.file_ops import FileOps
from src.agentic.core.config import PROJECT_ROOT

class TestFileOps(unittest.TestCase):
    def setUp(self):
        self.file_ops = FileOps()

    def test_read_file(self):
        file_path = PROJECT_ROOT / "src" / "agentic" / "core" / "plugin_system" / "tests" / "test_protocol.py"
        result = self.file_ops.execute("read", str(file_path))
        self.assertIn("TestToolProtocol", result)

if __name__ == "__main__":
    unittest.main()
