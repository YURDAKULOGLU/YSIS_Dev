#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check scraped documentation status and find duplicates/missing packages.
"""

import sys
import io
# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
import json
import re

PROJECT_ROOT = Path(__file__).parent.parent

def get_requirements_packages():
    """Get all packages from requirements.txt."""
    requirements_file = PROJECT_ROOT / "requirements.txt"
    packages = []
    
    with open(requirements_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            match = re.match(r'^([a-zA-Z0-9_-]+(?:\[[^\]]+\])?)', line)
            if match:
                package_name = match.group(1)
                package_name = re.sub(r'\[.*\]', '', package_name)
                packages.append(package_name)
    
    return packages

def get_scraped_packages():
    """Get all scraped packages."""
    frameworks_dir = PROJECT_ROOT / "platform_data" / "knowledge" / "Frameworks"
    scraped = {}
    
    if not frameworks_dir.exists():
        return scraped
    
    for package_dir in frameworks_dir.iterdir():
        if not package_dir.is_dir():
            continue
        
        package_name = package_dir.name
        
        # Count files
        md_files = list(package_dir.rglob("*.md"))
        json_files = list(package_dir.glob("metadata.json"))
        
        scraped[package_name] = {
            "md_files": len(md_files),
            "has_metadata": len(json_files) > 0,
            "size_mb": sum(f.stat().st_size for f in md_files) / (1024 * 1024) if md_files else 0
        }
    
    return scraped

def find_duplicates(scraped):
    """Find potential duplicates (packages with many files)."""
    duplicates = []
    for name, info in scraped.items():
        if info["md_files"] > 100:  # More than 100 files might be duplicate
            duplicates.append((name, info))
    return sorted(duplicates, key=lambda x: x[1]["md_files"], reverse=True)

def main():
    """Check scraped status."""
    print("\n" + "="*70)
    print("SCRAPED DOCUMENTATION STATUS CHECK")
    print("="*70)
    
    # Get packages
    requirements_packages = get_requirements_packages()
    scraped_packages = get_scraped_packages()
    
    print(f"\n[INFO] Requirements.txt packages: {len(requirements_packages)}")
    print(f"[INFO] Scraped packages: {len(scraped_packages)}")
    
    # Find missing
    scraped_names = set(scraped_packages.keys())
    required_names = set(requirements_packages)
    missing = required_names - scraped_names
    
    print(f"\n[MISSING] Missing packages: {len(missing)}")
    if missing:
        print("   Missing packages:")
        for pkg in sorted(missing)[:20]:
            print(f"     - {pkg}")
        if len(missing) > 20:
            print(f"     ... and {len(missing) - 20} more")
    
    # Find extra (scraped but not in requirements)
    extra = scraped_names - required_names
    print(f"\n[EXTRA] Extra packages (scraped but not in requirements): {len(extra)}")
    if extra:
        print("   Extra packages:")
        for pkg in sorted(extra)[:10]:
            print(f"     - {pkg}")
        if len(extra) > 10:
            print(f"     ... and {len(extra) - 10} more")
    
    # Find duplicates
    duplicates = find_duplicates(scraped_packages)
    print(f"\n[DUPLICATES] Potential duplicates (packages with >100 files): {len(duplicates)}")
    if duplicates:
        print("   Large packages:")
        for name, info in duplicates[:10]:
            print(f"     - {name}: {info['md_files']} files ({info['size_mb']:.2f} MB)")
    
    # Statistics
    total_files = sum(info["md_files"] for info in scraped_packages.values())
    total_size = sum(info["size_mb"] for info in scraped_packages.values())
    
    print(f"\n[STATS] Statistics:")
    print(f"   Total markdown files: {total_files}")
    print(f"   Total size: {total_size:.2f} MB")
    print(f"   Average files per package: {total_files / len(scraped_packages) if scraped_packages else 0:.1f}")
    
    # Recommendations
    print(f"\n[RECOMMENDATIONS]")
    if missing:
        print(f"   - Scrape {len(missing)} missing packages")
    if duplicates:
        print(f"   - Review {len(duplicates)} large packages for duplicates")
    if not missing and not duplicates:
        print(f"   - [OK] All packages scraped! No duplicates found.")
    
    print("\n" + "="*70)
    
    # Save report
    report = {
        "requirements_count": len(requirements_packages),
        "scraped_count": len(scraped_packages),
        "missing": sorted(missing),
        "extra": sorted(extra),
        "duplicates": [{"name": name, "files": info["md_files"], "size_mb": info["size_mb"]} 
                      for name, info in duplicates],
        "statistics": {
            "total_files": total_files,
            "total_size_mb": total_size,
            "average_files_per_package": total_files / len(scraped_packages) if scraped_packages else 0
        }
    }
    
    report_path = PROJECT_ROOT / "platform_data" / "knowledge" / "Frameworks" / "scraping_status.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"[REPORT] Report saved to: {report_path}")

if __name__ == "__main__":
    main()

