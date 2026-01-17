"""
Framework Docs Auto-Sync - Download framework documentation to local cache.

Downloads framework documentation from official sources and caches locally.
Policy-gated for network access.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
import yaml

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent
FRAMEWORKS_DIR = PROJECT_ROOT / "docs" / "frameworks"
FRAMEWORKS_CONFIG = PROJECT_ROOT / "configs" / "framework_docs.yaml"


def load_framework_config() -> Dict[str, Any]:
    """Load framework configuration."""
    if not FRAMEWORKS_CONFIG.exists():
        return {}

    with open(FRAMEWORKS_CONFIG, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def check_network_allowed() -> bool:
    """Check if network access is allowed by policy."""
    from src.ybis.services.policy import get_policy_provider

    policy = get_policy_provider()
    policy_config = policy.get_policy()

    # Check sandbox.network or exec.network
    sandbox_config = policy_config.get("sandbox", {})
    exec_config = policy_config.get("exec", {})

    # Network is allowed if sandbox.network is True or exec.network is True
    return sandbox_config.get("network", False) or exec_config.get("network", False)


def download_framework_docs(framework_name: str, config: Dict[str, Any]) -> bool:
    """
    Download framework documentation.

    Args:
        framework_name: Framework name
        config: Framework configuration

    Returns:
        True if successful
    """
    if not check_network_allowed():
        print(f"[SKIP] Network access disabled by policy. Skipping {framework_name}.")
        return False

    framework_dir = FRAMEWORKS_DIR / framework_name
    framework_dir.mkdir(parents=True, exist_ok=True)

    source_type = config.get("source", "github")
    url = config.get("url")
    version = config.get("version", "latest")

    if not url:
        print(f"[ERROR] No URL configured for {framework_name}")
        return False

    try:
        # Download based on source type
        if source_type == "github":
            success = _download_from_github(framework_name, url, version, framework_dir)
        elif source_type == "direct":
            success = _download_direct(framework_name, url, framework_dir)
        else:
            print(f"[ERROR] Unknown source type: {source_type}")
            return False

        if success:
            # Write metadata
            metadata = {
                "framework": framework_name,
                "version": version,
                "source": source_type,
                "url": url,
                "downloaded_at": None,  # Will be set when full implementation
            }
            metadata_path = framework_dir / "metadata.json"
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

        return success

    except Exception as e:
        print(f"[ERROR] Failed to download {framework_name}: {e}")
        return False


def _download_from_github(framework_name: str, url: str, version: str, target_dir: Path) -> bool:
    """Download from GitHub repository."""
    try:
        # Parse GitHub URL
        # Format: https://github.com/owner/repo or https://github.com/owner/repo/tree/branch
        if "/tree/" in url:
            base_url, branch = url.split("/tree/", 1)
            repo_path = base_url.replace("https://github.com/", "")
        else:
            repo_path = url.replace("https://github.com/", "")
            branch = version if version != "latest" else "main"

        # For now, just create a placeholder
        # Full implementation would use GitHub API to download docs
        readme_path = target_dir / "README.md"
        readme_path.write_text(
            f"# {framework_name} Documentation\n\n"
            f"Source: {url}\n"
            f"Branch: {branch}\n\n"
            f"Full documentation sync will be implemented in future version.\n",
            encoding="utf-8",
        )

        print(f"[OK] Created placeholder for {framework_name} (GitHub sync not fully implemented)")
        return True

    except Exception as e:
        print(f"[ERROR] GitHub download failed: {e}")
        return False


def _download_direct(framework_name: str, url: str, target_dir: Path) -> bool:
    """Download directly from URL."""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url)
            response.raise_for_status()

            # Save to target directory
            # For now, save as index.html or based on content type
            content_type = response.headers.get("content-type", "")
            if "text/html" in content_type:
                output_path = target_dir / "index.html"
            else:
                output_path = target_dir / "content.txt"

            output_path.write_bytes(response.content)

        print(f"[OK] Downloaded {framework_name} from {url}")
        return True

    except Exception as e:
        print(f"[ERROR] Direct download failed: {e}")
        return False


def sync_all_frameworks() -> None:
    """Sync all configured frameworks."""
    config = load_framework_config()
    frameworks = config.get("frameworks", {})

    if not frameworks:
        print("[INFO] No frameworks configured. Create configs/framework_docs.yaml")
        return

    print(f"[INFO] Syncing {len(frameworks)} frameworks...")

    for framework_name, framework_config in frameworks.items():
        print(f"\n[SYNC] {framework_name}...")
        download_framework_docs(framework_name, framework_config)

    print("\n[OK] Framework sync complete!")


if __name__ == "__main__":
    sync_all_frameworks()


