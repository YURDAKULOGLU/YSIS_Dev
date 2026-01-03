import unittest
from src.agentic.core.plugin_system.protocol import ToolProtocol

class TestToolProtocol(unittest.TestCase):
    def test_tool_protocol(self):
        with self.assertRaises(TypeError):
            class InvalidTool(ToolProtocol):
                pass

            tool = InvalidTool()

        class ValidTool(ToolProtocol):
            def execute(self, *args, **kwargs):
                return "Executed"

        tool = ValidTool()
        result = tool.execute()
        self.assertEqual(result, "Executed")

    def test_valid_tool_instantiation(self):
        class AnotherValidTool(ToolProtocol):
            def execute(self, *args, **kwargs):
                return "Another Executed"

        tool = AnotherValidTool()
        result = tool.execute()
        self.assertEqual(result, "Another Executed")

if __name__ == "__main__":
    unittest.main()
