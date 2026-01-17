"""
Cleanup Outdated Reports - Move outdated reports from docs/reports/ to docs/legacy/reports/

Criteria for OUTDATED:
- Contains "Tier 4.5"
- Contains "Core Trinity"
- Contains dates from 2024 or earlier
- References files that don't exist
"""

import re
import shutil
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).parent.parent
REPORTS_DIR = PROJECT_ROOT / "docs" / "reports"
LEGACY_DIR = PROJECT_ROOT / "docs" / "legacy" / "reports"
RESULT_FILE = PROJECT_ROOT / "docs" / "legacy" / "reports" / "CLEANUP_RESULT.md"


def check_outdated(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Check if a report file is outdated.
    
    Returns:
        Tuple of (is_outdated, reasons)
    """
    reasons = []
    
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        reasons.append(f"Could not read file: {e}")
        return True, reasons
    
    # Check for "Tier 4.5"
    if "Tier 4.5" in content or "tier 4.5" in content.lower():
        reasons.append("Contains 'Tier 4.5'")
    
    # Check for "Core Trinity"
    if "Core Trinity" in content or "core trinity" in content.lower():
        reasons.append("Contains 'Core Trinity'")
    
    # Check for 2024 or earlier dates
    date_pattern = r"\b(202[0-4]|201[0-9]|200[0-9])\b"
    if re.search(date_pattern, content):
        reasons.append("Contains date from 2024 or earlier")
    
    # Check for references to non-existent files
    # Look for markdown links and file references
    link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    file_ref_pattern = r"`([^`]+\.(md|yaml|py|json))`"
    
    for match in re.finditer(link_pattern, content):
        ref_path = match.group(2)
        # Skip external URLs
        if ref_path.startswith("http"):
            continue
        # Check if file exists relative to reports dir or project root
        if not (PROJECT_ROOT / ref_path).exists() and not (REPORTS_DIR / ref_path).exists():
            reasons.append(f"References non-existent file: {ref_path}")
    
    for match in re.finditer(file_ref_pattern, content):
        ref_file = match.group(1)
        if not (PROJECT_ROOT / ref_file).exists() and not (REPORTS_DIR / ref_file).exists():
            reasons.append(f"References non-existent file: {ref_file}")
    
    is_outdated = len(reasons) > 0
    return is_outdated, reasons


def main():
    """Main cleanup function."""
    # Ensure legacy directory exists
    LEGACY_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get all markdown files in reports directory
    report_files = list(REPORTS_DIR.glob("*.md"))
    
    outdated_files = []
    current_files = []
    
    print(f"Scanning {len(report_files)} report files...")
    
    for file_path in report_files:
        # Skip special files
        if file_path.name in ["CLEANUP_RESULT.md", "__init__.py"]:
            continue
        
        is_outdated, reasons = check_outdated(file_path)
        
        if is_outdated:
            outdated_files.append((file_path, reasons))
            print(f"  OUTDATED: {file_path.name}")
            print(f"    Reasons: {', '.join(reasons)}")
        else:
            current_files.append(file_path.name)
            print(f"  CURRENT: {file_path.name}")
    
    # Move outdated files
    moved_files = []
    for file_path, reasons in outdated_files:
        try:
            dest_path = LEGACY_DIR / file_path.name
            shutil.move(str(file_path), str(dest_path))
            moved_files.append((file_path.name, reasons))
            print(f"  MOVED: {file_path.name} -> {dest_path}")
        except Exception as e:
            print(f"  ERROR moving {file_path.name}: {e}")
    
    # Write result file
    result_content = f"""# Outdated Reports Cleanup Result

**Date:** {Path(__file__).stat().st_mtime}
**Total Files Scanned:** {len(report_files)}
**Outdated Files Moved:** {len(moved_files)}
**Current Files Remaining:** {len(current_files)}

## Moved Files

"""
    
    for file_name, reasons in moved_files:
        result_content += f"### {file_name}\n\n"
        result_content += f"**Reasons:**\n"
        for reason in reasons:
            result_content += f"- {reason}\n"
        result_content += "\n"
    
    result_content += f"""## Current Files

The following files remain in `docs/reports/` as they are current:

"""
    
    for file_name in sorted(current_files):
        result_content += f"- {file_name}\n"
    
    RESULT_FILE.write_text(result_content, encoding="utf-8")
    print(f"\nResult written to: {RESULT_FILE}")
    print(f"\nSummary:")
    print(f"  - Outdated files moved: {len(moved_files)}")
    print(f"  - Current files remaining: {len(current_files)}")


if __name__ == "__main__":
    main()

