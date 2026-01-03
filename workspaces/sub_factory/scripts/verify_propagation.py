import os
import shutil
import subprocess
import sys
from pathlib import Path

def run_propagation():
    print("🧬 Starting Self-Propagation Test...")
    
    root = Path(os.getcwd())
    sub_factory = root / "workspaces" / "sub_factory"
    
    # 1. Cleanup old attempt
    if sub_factory.exists():
        shutil.rmtree(sub_factory)
    
    sub_factory.mkdir(parents=True)
    
    # 2. Copy core organs
    dirs_to_copy = ["src", "scripts", "config"]
    files_to_copy = ["requirements.txt", "pyproject.toml"]
    
    print(f"📦 Cloning core organs into {sub_factory}...")
    for d in dirs_to_copy:
        src_path = root / d
        if src_path.exists():
            shutil.copytree(src_path, sub_factory / d)
            
    for f in files_to_copy:
        src_path = root / f
        if src_path.exists():
            shutil.copy2(src_path, sub_factory / f)

    # 3. Verify Health in Sub-Factory
    print("🔬 Verifying health of the new organism...")
    try:
        # Use the same python interpreter
        result = subprocess.run(
            [sys.executable, "scripts/system_health_check.py"],
            cwd=sub_factory,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("\n--- SUB-FACTORY HEALTH LOG ---")
        print(result.stdout)
        
        if "[SUCCESS] SYSTEM INTEGRITY: 100%" in result.stdout:
            print("\n✨ SUCCESS: The organism has successfully propagated!")
            return True
        else:
            print("\n❌ FAILURE: Sub-factory integrity compromised.")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Propagation Error: {e}")
        return False

if __name__ == "__main__":
    success = run_propagation()
    sys.exit(0 if success else 1)
