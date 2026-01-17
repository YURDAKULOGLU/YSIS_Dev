#!/usr/bin/env python3
"""
Emoji and Unicode Checker for YBIS
Constitution V3.0 compliant - VI.2 Naming Consistency

Checks for emoji and problematic unicode characters in code files.
Windows terminals (CP1254) crash on emojis, so they're forbidden.
"""

import re
import sys
from pathlib import Path

# Emoji pattern (common emojis)
EMOJI_PATTERN = re.compile(
    r"["
    r"\U0001F300-\U0001F9FF"  # Emoticons & Symbols
    r"\U00002600-\U000027BF"  # Miscellaneous Symbols
    r"\U0001F600-\U0001F64F"  # Emoticons
    r"\U0001F680-\U0001F6FF"  # Transport & Map
    r"\U0001F1E0-\U0001F1FF"  # Flags
    r"\U00002702-\U000027B0"  # Dingbats
    r"\U000024C2-\U0001F251"  # Enclosed characters
    r"]"
)

# Problematic unicode ranges (Windows terminal issues)
PROBLEMATIC_UNICODE = re.compile(
    r"["
    r"\U0001FA00-\U0001FAFF"  # Chess symbols, etc.
    r"]"
)

# Allowed unicode (basic Latin, common symbols)
ALLOWED_PATTERN = re.compile(r"[\x00-\x7F\u00A0-\u00FF\u0100-\u017F]")


def check_file(file_path: Path) -> list[str]:
    """Check a single file for emoji/unicode issues."""
    errors = []

    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [f"Error reading {file_path}: {e}"]

    lines = content.split("\n")

    for line_num, line in enumerate(lines, 1):
        # Check for emojis
        emoji_matches = EMOJI_PATTERN.findall(line)
        if emoji_matches:
            errors.append(
                f"{file_path}:{line_num}: Contains emoji: {', '.join(set(emoji_matches))}"
            )

        # Check for problematic unicode
        problematic = PROBLEMATIC_UNICODE.findall(line)
        if problematic:
            errors.append(
                f"{file_path}:{line_num}: Contains problematic unicode: {', '.join(set(problematic))}"
            )

    return errors


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: check_emoji.py <file1> [file2] ...")
        sys.exit(1)

    all_errors = []

    for file_arg in sys.argv[1:]:
        file_path = Path(file_arg)
        if not file_path.exists():
            continue

        errors = check_file(file_path)
        all_errors.extend(errors)

    if all_errors:
        print("ERROR: Emoji/Unicode violations found (Constitution VI.2):")
        for error in all_errors:
            print(f"  {error}")
        print("\nUse plain text instead of emojis:")
        print("  [OK] instead of ✅")
        print("  [ERROR] instead of ❌")
        print("  [WARNING] instead of ⚠️")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()

