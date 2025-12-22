import importlib.util
from src.agentic.core.plugin_system.registry import ToolRegistry

class PluginLoader:
    def __init__(self, registry):
        self.registry = registry

    def load_plugins(self, directory):
        import os
        for filename in os.listdir(directory):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                spec = importlib.util.spec_from_file_location(module_name, f"{directory}/{filename}")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attr in dir(module):
                    if not attr.startswith("_"):
                        tool_class = getattr(module, attr)
                        if hasattr(tool_class, "execute") and callable(getattr(tool_class, "execute")):
                            self.registry.register(attr.lower(), tool_class())
