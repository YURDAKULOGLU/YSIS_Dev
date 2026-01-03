import importlib.util
from typing import Dict, Any

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, Any] = {}

    def register_plugin(self, plugin_path: str) -> None:
        spec = importlib.util.spec_from_file_location("plugin", plugin_path)
        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            plugin_instance = module.Plugin()

            # Güvenlik izinlerini kontrol et
            if not hasattr(plugin_instance, 'permissions') or not isinstance(plugin_instance.permissions, list):
                raise ValueError(f"Plugin {plugin_instance.name} does not have valid permissions.")

            # İletişim yöntemini kontrol et
            if not callable(getattr(plugin_instance, 'communicate', None)):
                raise ValueError(f"Plugin {plugin_instance.name} does not have a communicate method.")

            self.plugins[plugin_instance.name] = plugin_instance
            print(f"Plugin registered: {plugin_instance.name}")

    def execute_plugin(self, plugin_name: str, params: Any) -> None:
        if plugin_name in self.plugins:
            # Güvenlik kontrolleri
            if not self.plugins[plugin_name].permissions:
                raise PermissionError(f"Plugin {plugin_name} does not have the required permissions.")

            self.plugins[plugin_name].execute(params)
        else:
            print(f"Plugin not found: {plugin_name}")

    def destroy_plugin(self, plugin_name: str) -> None:
        if plugin_name in self.plugins:
            self.plugins[plugin_name].destroy()
            del self.plugins[plugin_name]
            print(f"Plugin destroyed: {plugin_name}")
        else:
            print(f"Plugin not found: {plugin_name}")
