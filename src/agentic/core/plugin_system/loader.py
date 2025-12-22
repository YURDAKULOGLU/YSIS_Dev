import importlib.util
import inspect
import re
from src.agentic.core.plugin_system.registry import ToolRegistry
from src.agentic.core.plugin_system.protocol import ToolProtocol

def camel_to_snake(name):
    """Convert CamelCase to snake_case"""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

class PluginLoader:
    def __init__(self, registry):
        self.registry = registry

    def load_plugins(self, directory):
        import os
        for filename in os.listdir(directory):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                try:
                    spec = importlib.util.spec_from_file_location(module_name, f"{directory}/{filename}")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for attr in dir(module):
                        if not attr.startswith("_"):
                            tool_class = getattr(module, attr)
                            # Only load concrete classes that implement ToolProtocol
                            if (inspect.isclass(tool_class) and
                                issubclass(tool_class, ToolProtocol) and
                                tool_class is not ToolProtocol):
                                tool_name = camel_to_snake(attr)
                                self.registry.register(tool_name, tool_class())
                except (ImportError, ModuleNotFoundError) as e:
                    # Skip plugins with missing dependencies
                    print(f"[PluginLoader] Skipping {filename}: {e}")
                    continue
