import os
import unittest
from src.core.Infrastructure import PluginManager
from src.plugins.PluginInterface import PluginInterface

class MockPlugin(PluginInterface):
    name = 'MockPlugin'
    version = '1.0.0'
    description = 'Bir test eklenti'
    permissions = ['execute']

    def init(self) -> None:
        print(f"{self.name} başlatıldı.")

    async def execute(self, params: any) -> any:
        if hasattr(self, 'sanitizeInputs'):
            self.sanitizeInputs(params)
        return { "success": True, "data": params }

    def destroy(self) -> None:
        print(f"{self.name} sonlandırıldı.")

    def sanitizeInputs(self, params: any) -> None:
        # Girdi verilerini temizleme mantığınızı buraya yazın
        if not isinstance(params, dict):
            raise ValueError('Geçersiz girdi parametreleri.')
        for key in params:
            value = params[key]
            if isinstance(value, str) and ("'" in value or ";" in value):
                raise ValueError('Potansiyel güvenlik ihlali tespit edildi.')

class FaultyPlugin(PluginInterface):
    name = 'FaultyPlugin'
    version = '1.0.0'
    description = 'Hata veren bir eklenti'
    permissions = ['execute']

    def init(self) -> None:
        pass

    async def execute(self, params: any) -> any:
        raise Exception("Execution failed")

    def destroy(self) -> None:
        pass

class TestPluginManager(unittest.TestCase):
    def setUp(self) -> None:
        self.plugin_manager = PluginManager()

    def test_register_plugin(self) -> None:
        mock_plugin = MockPlugin()
        self.plugin_manager.register(mock_plugin)
        self.assertIn(mock_plugin, self.plugin_manager.plugins)

    def test_execute_plugin_success(self) -> None:
        mock_plugin = MockPlugin()
        self.plugin_manager.register(mock_plugin)
        result = self.plugin_manager.executeAll({"key": "value"})
        self.assertTrue(result[0]["success"])
        self.assertEqual(result[0]["data"], {"key": "value"})

    def test_execute_plugin_failure(self) -> None:
        faulty_plugin = FaultyPlugin()
        self.plugin_manager.register(faulty_plugin)
        result = self.plugin_manager.executeAll({"key": "value"})
        self.assertFalse(result[0]["success"])
        self.assertIsNotNone(result[0]["error"])

    def test_sandbox_environment(self) -> None:
        mock_plugin = MockPlugin()
        self.plugin_manager.register(mock_plugin)
        try:
            with unittest.mock.patch.dict(os.environ, {"SANDBOX_ENABLED": "false"}):
                result = self.plugin_manager.executeAll({"key": "value"})
                self.assertFalse(result[0]["success"])
                self.assertIsNotNone(result[0]["error"])
        except Exception as e:
            self.fail(f"Test başarısız oldu: {e}")

    def test_plugin_permissions(self) -> None:
        mock_plugin = MockPlugin()
        faulty_plugin = FaultyPlugin()

        # Test with insufficient permissions
        try:
            result = self.plugin_manager.executeAll({"key": "value"}, ['read'])
            self.assertFalse(result[0]["success"])
            self.assertIsNotNone(result[0]["error"])
        except Exception as e:
            self.fail(f"Test başarısız oldu: {e}")

        # Test with sufficient permissions
        try:
            result = self.plugin_manager.executeAll({"key": "value"}, ['execute'])
            self.assertTrue(result[0]["success"])
            self.assertEqual(result[0]["data"], {"key": "value"})
        except Exception as e:
            self.fail(f"Test başarısız oldu: {e}")

    def test_plugin_sanitize_inputs(self) -> None:
        mock_plugin = MockPlugin()
        self.plugin_manager.register(mock_plugin)
        try:
            with unittest.mock.patch.object(mock_plugin, 'sanitizeInputs') as mock_method:
                result = self.plugin_manager.executeAll({"key": "value"})
                mock_method.assert_called_once_with({"key": "value"})
                self.assertTrue(result[0]["success"])
                self.assertEqual(result[0]["data"], {"key": "value"})
        except Exception as e:
            self.fail(f"Test başarısız oldu: {e}")

    def test_plugin_sanitize_inputs_invalid(self) -> None:
        mock_plugin = MockPlugin()
        self.plugin_manager.register(mock_plugin)
        try:
            with self.assertRaises(Exception):
                result = self.plugin_manager.executeAll({"key": "value'; DROP TABLE users;"})
        except Exception as e:
            self.fail(f"Test başarısız oldu: {e}")

    def test_plugin_enforce_sandbox(self) -> None:
        mock_plugin = MockPlugin()
        self.plugin_manager.register(mock_plugin)
        try:
            with unittest.mock.patch.dict(os.environ, {"SANDBOX_ENABLED": "true"}):
                result = self.plugin_manager.executeAll({"key": "value"})
                self.assertTrue(result[0]["success"])
                self.assertEqual(result[0]["data"], {"key": "value"})
        except Exception as e:
            self.fail(f"Test başarısız oldu: {e}")

    def test_plugin_sanitize_inputs_invalid_command(self) -> None:
        mock_plugin = MockPlugin()
        self.plugin_manager.register(mock_plugin)
        try:
            with self.assertRaises(Exception):
                result = self.plugin_manager.executeAll({"key": "rm -rf /"})
        except Exception as e:
            self.fail(f"Test başarısız oldu: {e}")

    def test_plugin_sanitize_inputs_invalid_sql(self) -> None:
        mock_plugin = MockPlugin()
        self.plugin_manager.register(mock_plugin)
        try:
            with self.assertRaises(Exception):
                result = self.plugin_manager.executeAll({"key": "SELECT * FROM users;"})
        except Exception as e:
            self.fail(f"Test başarısız oldu: {e}")

    def test_plugin_sanitize_inputs_invalid_script(self) -> None:
        mock_plugin = MockPlugin()
        self.plugin_manager.register(mock_plugin)
        try:
            with self.assertRaises(Exception):
                result = self.plugin_manager.executeAll({"key": "<script>alert('XSS');</script>"})
        except Exception as e:
            self.fail(f"Test başarısız oldu: {e}")

if __name__ == '__main__':
    unittest.main()
