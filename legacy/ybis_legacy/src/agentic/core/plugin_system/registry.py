from src.agentic.core.plugin_system.protocol import ToolProtocol

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, tool_instance):
        if not isinstance(tool_instance, ToolProtocol):
            raise TypeError("Tool instance must implement ToolProtocol")
        self.tools[name] = tool_instance

    def get(self, name):
        return self.tools.get(name)

    def invoke(self, name, *args, **kwargs):
        tool = self.get(name)
        if tool:
            return tool.execute(*args, **kwargs)
        else:
            raise ValueError(f"Tool '{name}' not found")
