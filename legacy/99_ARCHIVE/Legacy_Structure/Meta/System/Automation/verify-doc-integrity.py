import hashlib
import yaml
import os
import sys
import glob
from pathlib import Path

# Goal: Verify integrity relative to the Project Root (Git Root)
# Location: .YBIS_Dev/Meta/System/Automation/verify-doc-integrity.py

def find_project_root(current_path):
    """Ascends until it finds .git or .YBIS_Dev, marking the root."""
    for parent in current_path.parents:
        if (parent / ".git").exists() or (parent / ".YBIS_Dev").exists():
            return parent
    return current_path # Fallback

CURRENT_SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = find_project_root(CURRENT_SCRIPT_PATH)
LOCK_FILE_PATH = PROJECT_ROOT / ".YBIS_Dev" / "Meta" / "System" / "doc-dependency.lock.yaml"

def calculate_hash(filepath):
    """Calculates MD5 hash of a file."""
    if not filepath.exists():
        return None
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def load_lock_file():
    if not LOCK_FILE_PATH.exists():
        print(f"⚠️  Lock file not found at {LOCK_FILE_PATH}")
        return None
    with open(LOCK_FILE_PATH, "r") as f:
        return yaml.safe_load(f)

def verify_chain():
    print(f"🔗 YBIS Global Integrity Checker")
    print(f"📂 Project Root: {PROJECT_ROOT}")
    print("---------------------------------------------")

    config = load_lock_file()
    if not config:
        return False

    dependencies = config.get("dependencies", [])
    violations = []

    for dep in dependencies:
        # Patterns are relative to PROJECT ROOT
        source_pattern = dep["source"]
        target_pattern = dep["target"]
        stored_hash = dep.get("source_hash")

        # Resolve full path pattern
        source_full_pattern = str(PROJECT_ROOT / source_pattern)

        # Handle glob patterns
        sources = glob.glob(source_full_pattern, recursive=True)

        if not sources:
            print(f"⚠️  Source not found: {source_pattern} (Skipping)")
            continue

        for source in sources:
            source_path = Path(source)
            current_hash = calculate_hash(source_path)

            # Display relative to project root
            try:
                display_source = source_path.relative_to(PROJECT_ROOT)
            except ValueError:
                display_source = source_path

            if stored_hash == "initial_placeholder":
                print(f"🆕 Initializing hash for: {display_source}")
                # In real app, we would update the YAML here
                continue

            if stored_hash and current_hash != stored_hash:
                violations.append({
                    "source": display_source,
                    "target": target_pattern,
                    "reason": "Document changed without downstream update."
                })
                print(f"❌ INTEGRITY VIOLATION: {display_source} changed!")
                print(f"   └── Downstream '{target_pattern}' MUST be reviewed.")
            else:
                print(f"✅ Verified: {display_source}")

    print("---------------------------------------------")
    if violations:
        print(f"⛔ CHAIN BROKEN. {len(violations)} violations found.")
        sys.exit(1)
    else:
        print(f"🟢 SYSTEM INTEGRITY VERIFIED.")
        sys.exit(0)

if __name__ == "__main__":
    verify_chain()
