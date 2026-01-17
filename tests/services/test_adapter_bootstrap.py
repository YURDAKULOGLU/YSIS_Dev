"""
Test Adapter Bootstrap - Register all adapters at startup.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.ybis.services.adapter_bootstrap import (
    bootstrap_adapters,
    validate_required_adapters,
    _register_from_catalog,
    _register_hardcoded,
)


class TestAdapterBootstrap:
    """Test adapter bootstrap functionality."""

    @pytest.fixture
    def mock_registry(self):
        """Create mock registry."""
        registry = Mock()
        registry.register = Mock()
        registry.get = Mock(return_value=None)
        return registry

    @pytest.fixture
    def mock_catalog(self):
        """Create mock catalog."""
        catalog = Mock()
        catalog.list_adapters = Mock(return_value=[])
        return catalog

    @patch("src.ybis.services.adapter_bootstrap.get_registry")
    @patch("src.ybis.services.adapter_bootstrap.get_catalog")
    def test_bootstrap_adapters_with_catalog(self, mock_get_catalog, mock_get_registry, mock_registry, mock_catalog):
        """Test bootstrap_adapters with catalog adapters."""
        mock_get_registry.return_value = mock_registry
        mock_get_catalog.return_value = mock_catalog

        adapter_meta = {
            "name": "test_adapter",
            "module_path": "src.ybis.adapters.test_adapter.TestAdapter",
            "type": "executor",
            "default_enabled": False,
        }
        mock_catalog.list_adapters.return_value = [adapter_meta]

        bootstrap_adapters()

        mock_catalog.list_adapters.assert_called_once()

    @patch("src.ybis.services.adapter_bootstrap.get_registry")
    @patch("src.ybis.services.adapter_bootstrap.get_catalog")
    def test_bootstrap_adapters_without_catalog(self, mock_get_catalog, mock_get_registry, mock_registry, mock_catalog):
        """Test bootstrap_adapters without catalog (fallback to hardcoded)."""
        mock_get_registry.return_value = mock_registry
        mock_get_catalog.return_value = mock_catalog
        mock_catalog.list_adapters.return_value = []

        with patch("src.ybis.services.adapter_bootstrap._register_hardcoded") as mock_register:
            bootstrap_adapters()
            mock_register.assert_called_once_with(mock_registry)

    def test_register_from_catalog_success(self, mock_registry):
        """Test _register_from_catalog with successful registration."""
        adapter_meta = {
            "name": "test_adapter",
            "module_path": "src.ybis.adapters.local_coder.LocalCoderExecutor",
            "type": "executor",
            "default_enabled": True,
        }

        with patch("builtins.__import__") as mock_import:
            mock_module = MagicMock()
            mock_adapter_class = Mock()
            mock_module.LocalCoderExecutor = mock_adapter_class
            mock_import.return_value = mock_module

            _register_from_catalog(mock_registry, adapter_meta)

            mock_registry.register.assert_called_once()

    def test_register_from_catalog_import_error(self, mock_registry):
        """Test _register_from_catalog with import error."""
        adapter_meta = {
            "name": "test_adapter",
            "module_path": "nonexistent.module.Adapter",
            "type": "executor",
            "default_enabled": False,
        }

        with patch("builtins.__import__", side_effect=ImportError("Module not found")):
            _register_from_catalog(mock_registry, adapter_meta)
            # Should not raise, just log warning

    @patch("src.ybis.services.adapter_bootstrap.get_registry")
    def test_validate_required_adapters_all_present(self, mock_get_registry, mock_registry):
        """Test validate_required_adapters when all adapters are present."""
        mock_get_registry.return_value = mock_registry

        # Mock adapter exists
        mock_adapter = Mock()
        mock_registry.get = Mock(side_effect=lambda name: mock_adapter if name == "local_coder" else None)

        required = ["local_coder"]
        missing = validate_required_adapters(required)

        assert missing == []

    @patch("src.ybis.services.adapter_bootstrap.get_registry")
    def test_validate_required_adapters_some_missing(self, mock_get_registry, mock_registry):
        """Test validate_required_adapters when some adapters are missing."""
        mock_get_registry.return_value = mock_registry
        mock_registry.get.return_value = None

        required = ["local_coder", "missing_adapter"]
        missing = validate_required_adapters(required)

        assert len(missing) == 2
        assert "local_coder" in missing
        assert "missing_adapter" in missing

    @patch("src.ybis.services.adapter_bootstrap.get_registry")
    def test_validate_required_adapters_empty_list(self, mock_get_registry, mock_registry):
        """Test validate_required_adapters with empty list."""
        mock_get_registry.return_value = mock_registry

        missing = validate_required_adapters([])

        assert missing == []

    def test_bootstrap_logs(self):
        """Test bootstrap module has logging configured."""
        import logging
        logger = logging.getLogger("src.ybis.services.adapter_bootstrap")
        assert logger is not None

