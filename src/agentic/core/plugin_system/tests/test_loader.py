import unittest
from src.agentic.core.plugin_system.loader import PluginLoader
from src.agentic.core.plugin_system.registry import ToolRegistry
from src.agentic.core.config import PROJECT_ROOT

class TestPluginLoader(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()
        self.loader = PluginLoader(self.registry)

    def test_load_plugins(self):
        plugin_path = PROJECT_ROOT / "src" / "agentic" / "core" / "plugins" / "builtin"
        self.loader.load_plugins(str(plugin_path))
        self.assertIn("calculator", self.registry.tools)
        self.assertIn("file_ops", self.registry.tools)
        self.assertIn("git_ops", self.registry.tools)

if __name__ == "__main__":
    unittest.main()
