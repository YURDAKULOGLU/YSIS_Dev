import unittest
from src.agentic.core.plugins.builtin.git_ops import GitOps

class TestGitOps(unittest.TestCase):
    def setUp(self):
        self.git_ops = GitOps()

    def test_status(self):
        result = self.git_ops.execute("status")
        self.assertIn("On branch", result)

if __name__ == "__main__":
    unittest.main()
