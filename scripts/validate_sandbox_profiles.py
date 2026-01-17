"""
Sandbox Profile Validation Script.

Validates that all policy profiles meet safety guarantees.
"""

import sys
import yaml
from pathlib import Path
from typing import Any, Dict, List

# Calculate project root (scripts/ is 2 levels down from root)
PROJECT_ROOT = Path(__file__).parent.parent


class ProfileValidationError(Exception):
    """Raised when a profile validation fails."""

    pass


def validate_profile(profile_path: Path) -> List[str]:
    """
    Validate a single profile against safety guarantees.

    Args:
        profile_path: Path to profile YAML file

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    try:
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = yaml.safe_load(f) or {}
    except Exception as e:
        errors.append(f"Failed to load profile: {e}")
        return errors

    profile_name = profile.get("profile", profile_path.stem)

    # Rule 1: Sandbox must be enabled
    sandbox = profile.get("sandbox", {})
    sandbox_enabled = sandbox.get("enabled", True)  # Defaults to True
    if not sandbox_enabled:
        errors.append(f"[{profile_name}] Rule 1 violation: sandbox.enabled must be true")

    # Rule 2: Network must be disabled by default
    sandbox_network = sandbox.get("network", False)  # Defaults to False
    if sandbox_network:
        errors.append(f"[{profile_name}] Rule 2 violation: sandbox.network must be false (default)")

    # Rule 3: Allowlist must be non-empty
    exec_config = profile.get("exec", {})
    allowlist = exec_config.get("allowlist", [])
    if not allowlist or len(allowlist) == 0:
        errors.append(f"[{profile_name}] Rule 3 violation: exec.allowlist must be non-empty")

    # Rule 4: Protected paths must be non-empty
    paths_config = profile.get("paths", {})
    protected_paths = paths_config.get("protected", [])
    if not protected_paths or len(protected_paths) == 0:
        errors.append(f"[{profile_name}] Rule 4 violation: paths.protected must be non-empty")

    # Rule 5: Verifier pass required
    gates = profile.get("gates", {})
    require_verifier_pass = gates.get("require_verifier_pass", True)  # Defaults to True
    if not require_verifier_pass:
        errors.append(f"[{profile_name}] Rule 5 violation: gates.require_verifier_pass must be true")

    # Rule 6: Sandbox type validation
    sandbox_type = sandbox.get("type", "local")
    valid_types = ["e2b", "local"]  # docker is planned but not implemented
    if sandbox_type not in valid_types:
        if sandbox_type == "docker":
            errors.append(
                f"[{profile_name}] Rule 6 violation: sandbox.type 'docker' is planned but not yet implemented. Use 'e2b' or 'local'."
            )
        else:
            errors.append(
                f"[{profile_name}] Rule 6 violation: sandbox.type must be one of {valid_types}, got '{sandbox_type}'"
            )

    # Rule 7: Adapter configuration consistency
    adapters = profile.get("adapters", {})
    e2b_enabled = adapters.get("e2b_sandbox", {}).get("enabled", False)

    if sandbox_type == "e2b" and not e2b_enabled:
        errors.append(
            f"[{profile_name}] Rule 7 violation: sandbox.type is 'e2b' but adapters.e2b_sandbox.enabled is false"
        )

    if sandbox_type == "local" and e2b_enabled:
        errors.append(
            f"[{profile_name}] Rule 7 warning: sandbox.type is 'local' but adapters.e2b_sandbox.enabled is true (inconsistent)"
        )

    return errors


def validate_all_profiles() -> Dict[str, List[str]]:
    """
    Validate all profiles in configs/profiles/.

    Returns:
        Dictionary mapping profile names to validation errors
    """
    profiles_dir = PROJECT_ROOT / "configs" / "profiles"
    if not profiles_dir.exists():
        return {"error": [f"Profiles directory not found: {profiles_dir}"]}

    results = {}
    profile_files = list(profiles_dir.glob("*.yaml"))

    if not profile_files:
        return {"error": ["No profile files found"]}

    for profile_path in profile_files:
        profile_name = profile_path.stem
        errors = validate_profile(profile_path)
        if errors:
            results[profile_name] = errors
        else:
            results[profile_name] = []  # Valid profile

    return results


def main() -> int:
    """Main entry point."""
    print("[INFO] Validating sandbox profiles...")
    results = validate_all_profiles()

    if "error" in results:
        print(f"[ERROR] {results['error'][0]}", file=sys.stderr)
        return 1

    total_profiles = len(results)
    valid_profiles = sum(1 for errors in results.values() if not errors)
    invalid_profiles = total_profiles - valid_profiles

    if invalid_profiles > 0:
        print(f"[ERROR] {invalid_profiles}/{total_profiles} profiles failed validation:\n", file=sys.stderr)

        for profile_name, errors in results.items():
            if errors:
                print(f"  {profile_name}:", file=sys.stderr)
                for error in errors:
                    print(f"    - {error}", file=sys.stderr)
                print("", file=sys.stderr)

        return 1

    print(f"[OK] All {valid_profiles} profiles passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

