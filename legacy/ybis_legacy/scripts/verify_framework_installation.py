#!/usr/bin/env python3
"""
Framework Installation Verification Script

Verifies that all installed frameworks have:
1. Package installed
2. Documentation downloaded
3. Documentation ingested into RAG
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Known frameworks
FRAMEWORKS = [
    "temporalio",
    "ray",
    "prefect",
    "spade",
    "celery",
    "crewai",
    "pyautogen",
    "langgraph",
    "litellm",
    "instructor",
    "ollama",
]

def check_package_installed(framework_name: str) -> bool:
    """Check if framework package is installed."""
    try:
        # Handle package name variations
        import_name = framework_name
        if framework_name == "pyautogen":
            import_name = "autogen"
        elif framework_name == "temporalio":
            import_name = "temporalio"
        
        __import__(import_name)
        return True
    except ImportError:
        return False

def check_documentation(framework_name: str) -> tuple[bool, int]:
    """Check if documentation exists."""
    docs_dir = Path(f"Knowledge/Frameworks/{framework_name}/docs")
    if not docs_dir.exists():
        return False, 0
    
    md_files = list(docs_dir.rglob("*.md"))
    return len(md_files) > 0, len(md_files)

def check_rag_ingestion(framework_name: str) -> bool:
    """Check if documentation is in RAG."""
    try:
        from src.agentic.tools.local_rag import get_local_rag
        
        rag = get_local_rag()
        if not rag or not rag.is_available():
            return False
        
        # Search for framework docs
        results = rag.search(f"framework:{framework_name}", limit=1)
        return "No relevant context" not in results
    except Exception:
        return False

def verify_framework(framework_name: str) -> Dict:
    """Verify framework installation."""
    results = {
        "framework": framework_name,
        "package_installed": False,
        "docs_downloaded": False,
        "docs_count": 0,
        "rag_ingested": False,
        "status": "UNKNOWN",
        "errors": []
    }
    
    # Check package
    results["package_installed"] = check_package_installed(framework_name)
    if not results["package_installed"]:
        results["errors"].append(f"Package {framework_name} not installed")
        results["status"] = "MISSING_PACKAGE"
        return results
    
    # Check documentation
    docs_exists, docs_count = check_documentation(framework_name)
    results["docs_downloaded"] = docs_exists
    results["docs_count"] = docs_count
    if not docs_exists:
        results["errors"].append(f"No documentation found (expected in Knowledge/Frameworks/{framework_name}/docs)")
        results["status"] = "MISSING_DOCS"
        return results
    
    # Check RAG ingestion
    results["rag_ingested"] = check_rag_ingestion(framework_name)
    if not results["rag_ingested"]:
        results["errors"].append(f"Documentation not ingested into RAG")
        results["status"] = "MISSING_RAG"
        return results
    
    results["status"] = "OK"
    return results

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Verify framework installations")
    parser.add_argument("--framework", help="Verify specific framework")
    parser.add_argument("--all", action="store_true", help="Verify all frameworks")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix missing docs")
    
    args = parser.parse_args()
    
    frameworks_to_check = []
    if args.framework:
        frameworks_to_check = [args.framework]
    elif args.all:
        frameworks_to_check = FRAMEWORKS
    else:
        print("Error: Specify --framework <name> or --all")
        sys.exit(1)
    
    print("=" * 80)
    print("FRAMEWORK INSTALLATION VERIFICATION")
    print("=" * 80)
    print()
    
    all_results = []
    for framework in frameworks_to_check:
        result = verify_framework(framework)
        all_results.append(result)
        
        status_icon = "[OK]" if result["status"] == "OK" else "[FAIL]"
        print(f"{status_icon} {framework}")
        print(f"  Package: {'[OK]' if result['package_installed'] else '[FAIL]'}")
        print(f"  Docs: {result['docs_count']} files {'[OK]' if result['docs_downloaded'] else '[FAIL]'}")
        print(f"  RAG: {'[OK]' if result['rag_ingested'] else '[FAIL]'}")
        if result["errors"]:
            for error in result["errors"]:
                print(f"    ERROR: {error}")
        print()
        
        # Auto-fix if requested
        if args.fix and result["status"] != "OK":
            if not result["package_installed"]:
                print(f"  [FIX] Installing {framework}...")
                subprocess.run([sys.executable, "-m", "pip", "install", framework], check=False)
            if not result["docs_downloaded"]:
                print(f"  [FIX] Downloading docs for {framework}...")
                subprocess.run([sys.executable, "scripts/install_framework.py", framework], check=False)
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    ok_count = sum(1 for r in all_results if r["status"] == "OK")
    total_count = len(all_results)
    
    print(f"Total: {total_count}")
    print(f"OK: {ok_count}")
    print(f"Failed: {total_count - ok_count}")
    
    if ok_count < total_count:
        print("\nFailed frameworks:")
        for result in all_results:
            if result["status"] != "OK":
                print(f"  - {result['framework']}: {result['status']}")
        sys.exit(1)
    
    print("\n[SUCCESS] All frameworks verified!")

if __name__ == "__main__":
    main()

