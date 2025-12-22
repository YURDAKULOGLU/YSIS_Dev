import hashlib
import yaml
import os
import sys
import glob
from pathlib import Path
from typing import Dict, List, Optional

# Goal: Verify integrity with detailed file tracking
# Location: .YBIS_Dev/10_META/Governance/Auditors/verify_doc_integrity.py

def find_project_root(current_path: Path) -> Path:
    for parent in current_path.parents:
        if (parent / ".git").exists() or (parent / ".YBIS_Dev").exists():
            return parent
    return current_path

CURRENT_SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = find_project_root(CURRENT_SCRIPT_PATH)
LOCK_FILE_PATH = PROJECT_ROOT / ".YBIS_Dev" / "10_META" / "Governance" / "Locks" / "doc-dependency.lock.yaml"

def calculate_hash(filepath: Path) -> Optional[str]:
    if not filepath.exists():
        return None
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        print(f"⚠️ Error reading {filepath}: {e}")
        return None

def load_lock_file() -> Optional[Dict]:
    if not LOCK_FILE_PATH.exists():
        print(f"⚠️  Lock file not found at {LOCK_FILE_PATH}")
        return None
    try:
        with open(LOCK_FILE_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {{}}
    except Exception as e:
        print(f"❌ Error loading lock file: {e}")
        return None

def save_lock_file(data: Dict):
    try:
        with open(LOCK_FILE_PATH, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print("💾 Lock file updated.")
    except Exception as e:
        print(f"❌ Error saving lock file: {e}")

def verify_chain():
    force_update = "--force-update" in sys.argv
    print(f"🔗 YBIS Global Integrity Checker (v2.0 - File Tracking)")
    print(f"📂 Project Root: {PROJECT_ROOT}")
    if force_update:
        print("🚨 Running in --force-update mode.")
    print("---------------------------------------------")
    
    config = load_lock_file()
    if not config:
        sys.exit(1)

    dependencies = config.get("dependencies", [])
    if not dependencies:
        print("⚠️ No dependencies found in lock file.")
        sys.exit(0)

    violations = []
    modifications = False

    # Process each dependency rule
    for dep in dependencies:
        source_pattern = dep.get("source_pattern") or dep.get("source") # Handle legacy key
        target = dep.get("target")
        
        # Ensure tracked_files is a dict (filename -> hash)
        # If it's old format (list) or missing, initialize as empty dict
        tracked_files = dep.get("tracked_files", {})
        if not isinstance(tracked_files, dict):
            tracked_files = {} 
            dep["tracked_files"] = tracked_files # Update the config object in place

        # 1. Find all current files matching the pattern
        source_full_pattern = str(PROJECT_ROOT / source_pattern)
        # Exclude .pyc and __pycache__
        current_files_paths = [
            Path(p) for p in glob.glob(source_full_pattern, recursive=True) 
            if not p.endswith(".pyc") and "__pycache__" not in p and Path(p).is_file()
        ]
        
        current_files_map = {} # path_str -> current_hash

        # 2. Calculate current hashes
        for file_path in current_files_paths:
            try:
                rel_path = str(file_path.relative_to(PROJECT_ROOT)).replace("\\", "/")
            except ValueError:
                continue # Should not happen if glob is correct
            
            file_hash = calculate_hash(file_path)
            if file_hash:
                current_files_map[rel_path] = file_hash

        # 3. Compare with Tracked Files
        
        # Check for MODIFIED or NEW files
        for rel_path, current_hash in current_files_map.items():
            stored_hash = tracked_files.get(rel_path)

            if stored_hash is None:
                # NEW FILE
                if force_update:
                    tracked_files[rel_path] = current_hash
                    modifications = True
                    print(f"🆕 Added: {rel_path}")
                else:
                    violations.append(f"Untracked file found: {rel_path}")
                    print(f"❌ UNTRACKED: {rel_path} (Run with --force-update to add)")
            
            elif stored_hash != current_hash:
                # MODIFIED FILE
                if force_update:
                    tracked_files[rel_path] = current_hash
                    modifications = True
                    print(f"🔄 Updated: {rel_path}")
                else:
                    violations.append(f"Hash mismatch: {rel_path}")
                    print(f"❌ CHANGED: {rel_path}")
                    print(f"   └── Target '{target}' may be stale.")

        # Check for DELETED files
        # Convert keys to list to avoid runtime error during iteration if we modify dict
        for rel_path in list(tracked_files.keys()):
            if rel_path not in current_files_map:
                if force_update:
                    del tracked_files[rel_path]
                    modifications = True
                    print(f"🗑️ Removed: {rel_path}")
                else:
                    violations.append(f"Missing file: {rel_path}")
                    print(f"❌ MISSING: {rel_path} (Run with --force-update to remove)")

    # Save changes if any
    if modifications and force_update:
        # Clean up legacy fields if they exist
        for dep in dependencies:
            if "source_hash" in dep:
                del dep["source_hash"]
            if "source" in dep: # Migrate 'source' to 'source_pattern'
                dep["source_pattern"] = dep["source"]
                del dep["source"]
                
        save_lock_file(config)

    print("---------------------------------------------")
    if violations:
        print(f"⛔ CHAIN BROKEN. {len(violations)} violations found.")
        sys.exit(1)
    else:
        print(f"🟢 SYSTEM INTEGRITY VERIFIED.")
        sys.exit(0)

if __name__ == "__main__":
    verify_chain()
