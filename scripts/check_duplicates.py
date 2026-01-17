#!/usr/bin/env python3
"""
Check for duplicate scraped packages (case sensitivity issues).
"""

import sys
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
FRAMEWORKS_DIR = PROJECT_ROOT / "platform_data" / "knowledge" / "Frameworks"

def find_duplicates():
    """Find potential duplicate packages."""
    if not FRAMEWORKS_DIR.exists():
        print("No frameworks directory found!")
        return
    
    packages = {}
    duplicates = defaultdict(list)
    
    for package_dir in FRAMEWORKS_DIR.iterdir():
        if not package_dir.is_dir():
            continue
        
        package_name = package_dir.name
        package_lower = package_name.lower()
        
        # Count files
        md_files = list(package_dir.rglob("*.md"))
        json_files = list(package_dir.glob("metadata.json"))
        
        packages[package_name] = {
            "md_files": len(md_files),
            "has_metadata": len(json_files) > 0,
            "size_mb": sum(f.stat().st_size for f in md_files) / (1024 * 1024) if md_files else 0
        }
        
        # Check for case-insensitive duplicates
        if package_lower in duplicates:
            duplicates[package_lower].append(package_name)
        else:
            duplicates[package_lower] = [package_name]
    
    # Find actual duplicates (case-insensitive)
    actual_duplicates = {k: v for k, v in duplicates.items() if len(v) > 1}
    
    print("\n" + "="*70)
    print("DUPLICATE PACKAGE CHECK")
    print("="*70)
    
    if actual_duplicates:
        print(f"\n[WARNING] Found {len(actual_duplicates)} duplicate packages (case-insensitive):\n")
        for lower_name, variants in actual_duplicates.items():
            print(f"  '{lower_name}' has {len(variants)} variants:")
            for variant in variants:
                info = packages[variant]
                print(f"    - {variant}: {info['md_files']} files ({info['size_mb']:.2f} MB)")
            
            # Recommend which one to keep
            # Keep the one with more files, or lowercase if equal
            best = max(variants, key=lambda v: (packages[v]['md_files'], -len(v)))
            others = [v for v in variants if v != best]
            print(f"    [RECOMMEND] Keep: {best}")
            print(f"    [RECOMMEND] Remove: {', '.join(others)}")
            print()
    else:
        print("\n[OK] No duplicate packages found!")
    
    # Check for packages with many files (might be over-scraped)
    large_packages = [(name, info) for name, info in packages.items() if info['md_files'] > 100]
    if large_packages:
        print(f"\n[INFO] Packages with >100 files (might be over-scraped):")
        for name, info in sorted(large_packages, key=lambda x: x[1]['md_files'], reverse=True):
            print(f"  - {name}: {info['md_files']} files ({info['size_mb']:.2f} MB)")
    
    print("\n" + "="*70)
    
    return actual_duplicates, packages

if __name__ == "__main__":
    duplicates, packages = find_duplicates()
    
    if duplicates:
        print("\n[ACTION] To remove duplicates, run:")
        for lower_name, variants in duplicates.items():
            best = max(variants, key=lambda v: (packages[v]['md_files'], -len(v)))
            others = [v for v in variants if v != best]
            for other in others:
                print(f"  Remove-Item -Recurse -Force 'platform_data/knowledge/Frameworks/{other}'")


