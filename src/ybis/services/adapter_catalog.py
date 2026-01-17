"""
Adapter Catalog - Load and validate adapter catalog from YAML.

Provides catalog-based adapter discovery and validation.
"""

import logging

logger = logging.getLogger(__name__)

from pathlib import Path
from typing import Any

import yaml

from ..constants import PROJECT_ROOT


class AdapterCatalog:
    """
    Adapter Catalog - Loads and validates adapter catalog from YAML.

    The catalog is the source of truth for adapter metadata, dependencies,
    and lifecycle information.
    """

    def __init__(self, catalog_path: Path | None = None):
        """
        Initialize adapter catalog.

        Args:
            catalog_path: Path to adapters.yaml (default: configs/adapters.yaml)
        """
        if catalog_path is None:
            catalog_path = PROJECT_ROOT / "configs" / "adapters.yaml"

        self.catalog_path = catalog_path
        self._catalog: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load catalog from YAML file."""
        if not self.catalog_path.exists():
            # Empty catalog if file doesn't exist
            self._catalog = {"adapters": {}}
            return

        try:
            with open(self.catalog_path, encoding="utf-8") as f:
                self._catalog = yaml.safe_load(f) or {"adapters": {}}
        except Exception as e:
            raise ValueError(f"Failed to load adapter catalog: {e}")

    def get_adapter(self, name: str) -> dict[str, Any] | None:
        """
        Get adapter metadata by name.

        Args:
            name: Adapter name

        Returns:
            Adapter metadata dictionary or None if not found
        """
        adapters = self._catalog.get("adapters", {})
        return adapters.get(name)

    def list_adapters(
        self, adapter_type: str | None = None, maturity: str | None = None
    ) -> list[dict[str, Any]]:
        """
        List adapters with optional filtering.

        Args:
            adapter_type: Filter by adapter type (executor, sandbox, etc.)
            maturity: Filter by maturity (stable, beta, experimental)

        Returns:
            List of adapter metadata dictionaries
        """
        adapters = self._catalog.get("adapters", {})
        result = []

        for name, metadata in adapters.items():
            if adapter_type and metadata.get("type") != adapter_type:
                continue
            if maturity and metadata.get("maturity") != maturity:
                continue

            result.append({"name": name, **metadata})

        return result

    def get_dependencies(self, adapter_name: str) -> list[str]:
        """
        Get adapter dependencies.

        Args:
            adapter_name: Adapter name

        Returns:
            List of dependency strings (e.g., ["chromadb>=0.4.0"])
        """
        adapter = self.get_adapter(adapter_name)
        if not adapter:
            return []

        return adapter.get("dependencies", [])

    def validate_catalog(self) -> list[str]:
        """
        Validate catalog structure and completeness.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        adapters = self._catalog.get("adapters", {})

        required_fields = ["name", "type", "module_path", "maturity", "default_enabled"]

        for name, metadata in adapters.items():
            # Check required fields
            for field in required_fields:
                if field not in metadata:
                    errors.append(f"Adapter '{name}' missing required field: {field}")

            # Validate maturity
            maturity = metadata.get("maturity")
            valid_maturities = ["stable", "beta", "experimental", "deprecated"]
            if maturity not in valid_maturities:
                errors.append(
                    f"Adapter '{name}' has invalid maturity: {maturity}. Must be one of {valid_maturities}"
                )

            # Validate deprecated adapters
            if maturity == "deprecated":
                if "deprecated_since" not in metadata:
                    errors.append(f"Deprecated adapter '{name}' missing 'deprecated_since' field")
                if "removal_date" not in metadata:
                    errors.append(f"Deprecated adapter '{name}' missing 'removal_date' field")

            # Validate type
            adapter_type = metadata.get("type")
            valid_types = [
                "executor",
                "sandbox",
                "vector_store",
                "graph_store",
                "llm_adapter",
                "event_bus",
            ]
            if adapter_type not in valid_types:
                errors.append(
                    f"Adapter '{name}' has invalid type: {adapter_type}. Must be one of {valid_types}"
                )

            # Check name consistency
            if metadata.get("name") != name:
                errors.append(f"Adapter '{name}' name field mismatch: {metadata.get('name')}")

            # Validate CVE status if present
            if "cve_status" in metadata:
                cve_status = metadata["cve_status"]
                if "active_cves" in cve_status:
                    for cve in cve_status["active_cves"]:
                        if "cve_id" not in cve:
                            errors.append(f"Adapter '{name}' CVE entry missing 'cve_id'")
                        if "severity" not in cve:
                            errors.append(f"Adapter '{name}' CVE entry missing 'severity'")

        return errors


# Global catalog instance
_catalog: AdapterCatalog | None = None


def get_catalog() -> AdapterCatalog:
    """Get global adapter catalog instance."""
    global _catalog
    if _catalog is None:
        _catalog = AdapterCatalog()
    return _catalog

