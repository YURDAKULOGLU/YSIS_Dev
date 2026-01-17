import unittest
from src.agentic.core.plugin_system.registry import ToolRegistry

class TestToolRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = ToolRegistry()

    def test_register_tool(self):
        from src.agentic.core.plugin_system.protocol import ToolProtocol

        class MockTool(ToolProtocol):
            def execute(self, *args, **kwargs):
                return "Executed"

        tool_instance = MockTool()
        self.registry.register("mock_tool", tool_instance)
        self.assertIn("mock_tool", self.registry.tools)

    def test_get_tool(self):
        from src.agentic.core.plugin_system.protocol import ToolProtocol

        class MockTool(ToolProtocol):
            def execute(self, *args, **kwargs):
                return "Executed"

        tool_instance = MockTool()
        self.registry.register("mock_tool", tool_instance)
        retrieved_tool = self.registry.get("mock_tool")
        self.assertEqual(retrieved_tool.execute(), "Executed")

    def test_invoke_tool(self):
        from src.agentic.core.plugin_system.protocol import ToolProtocol

        class MockTool(ToolProtocol):
            def execute(self, *args, **kwargs):
                return f"Executed with {args} and {kwargs}"

        tool_instance = MockTool()
        self.registry.register("mock_tool", tool_instance)
        result = self.registry.invoke("mock_tool", 1, 2, key="value")
        self.assertEqual(result, "Executed with (1, 2) and {'key': 'value'}")

if __name__ == "__main__":
    unittest.main()
