#!/usr/bin/env python3
"""
Normalize non-ASCII decorations in code files.

This script replaces common emoji and unicode symbols with ASCII-safe tags.
It can also report remaining non-ASCII characters.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


# Emoji to ASCII replacements (using unicode escapes for reliability)
REPLACEMENTS = {
    # Status indicators
    "\u2705": "[OK]",      # [OK]
    "\u274C": "[FAIL]",    # [FAIL]
    "\u26A0": "[WARN]",    # [WARN]
    "\u2139": "[INFO]",    # [INFO]
    "\u2757": "[!]",       # [!]
    "\u2753": "[?]",       # [?]
    # Rockets and stars
    "\U0001F680": "[LAUNCH]",  # [LAUNCH]
    "\u2B50": "[*]",           # [*]
    "\U0001F31F": "[*]",       # [*]
    # Numbers in circles
    "\u0031\u20E3": "1.",  # 1️⃣
    "\u0032\u20E3": "2.",  # 2️⃣
    "\u0033\u20E3": "3.",  # 3️⃣
    # Arrows
    "\u2192": "->",        # ->
    "\u2190": "<-",        # <-
    "\u21D2": "=>",        # =>
    "\u2794": "->",        # ->
    "\u27A1": "->",        # ->
    # Tools and misc
    "\U0001F527": "[TOOL]",    # [TOOL]
    "\U0001F4DD": "[DOC]",     # [DOC]
    "\U0001F4A1": "[IDEA]",    # [IDEA]
    "\U0001F501": "[RETRY]",   # [RETRY]
    "\U0001F512": "[LOCK]",    # [LOCK]
    "\U0001F513": "[UNLOCK]",  # [UNLOCK]
    "\U0001F4CA": "[CHART]",   # [CHART]
    "\U0001F4C8": "[UP]",      # [UP]
    "\U0001F4C9": "[DOWN]",    # [DOWN]
    "\U0001F50D": "[SEARCH]",  # [SEARCH]
    "\U0001F3AF": "[TARGET]",  # [TARGET]
    "\U0001F6A8": "[ALERT]",   # [ALERT]
    "\U0001F6E0": "[TOOLS]",   # [TOOLS]
    "\U0001F9EA": "[TEST]",    # [TEST]
    "\U0001F4E6": "[PKG]",     # [PKG]
    "\U0001F389": "[OK]",      # [OK]
    "\U0001F3C6": "[WIN]",     # [WIN]
    # Simple replacements
    "\u2014": "-",         # -
    "\u2013": "-",         # -
    "\u201C": "\"",        # "
    "\u201D": "\"",        # "
    "\u2018": "'",         # '
    "\u2019": "'",         # '
}


def _iter_files(paths: Iterable[Path], extensions: set[str]) -> Iterable[Path]:
    for root in paths:
        if root.is_file():
            if root.suffix in extensions:
                yield root
            continue
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in extensions:
                yield path


def _apply_replacements(text: str) -> str:
    updated = text
    for src, dst in REPLACEMENTS.items():
        if src in updated:
            updated = updated.replace(src, dst)
    return updated


def _find_non_ascii(text: str) -> list[tuple[int, str]]:
    results = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if any(ord(ch) > 127 for ch in line):
            results.append((idx, line))
    return results


def _safe_print(msg: str) -> None:
    """Print with fallback for Windows console encoding issues."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="replace").decode("ascii"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize emoji/unicode in code files.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to disk (default is dry-run).",
    )
    parser.add_argument(
        "--paths",
        nargs="*",
        default=["src", "tests", "scripts"],
        help="Paths to scan.",
    )
    parser.add_argument(
        "--extensions",
        nargs="*",
        default=[".py", ".ts", ".js", ".tsx"],
        help="File extensions to process.",
    )
    parser.add_argument(
        "--report-non-ascii",
        action="store_true",
        help="Report remaining non-ASCII lines after replacements.",
    )
    args = parser.parse_args()

    paths = [Path(p) for p in args.paths]
    extensions = {ext if ext.startswith(".") else f".{ext}" for ext in args.extensions}

    updated_files = 0
    total_replacements = 0
    for path in _iter_files(paths, extensions):
        original = path.read_text(encoding="utf-8", errors="replace")
        updated = _apply_replacements(original)
        if updated != original:
            updated_files += 1
            for src in REPLACEMENTS:
                total_replacements += original.count(src)
            if args.apply:
                path.write_text(updated, encoding="utf-8")
            else:
                _safe_print(f"[DRY_RUN] Would update {path}")

        if args.report_non_ascii:
            remaining = _find_non_ascii(updated)
            for line_no, line in remaining:
                _safe_print(f"[NON_ASCII] {path}:{line_no} {line}")

    if args.apply:
        _safe_print(f"[OK] Updated files: {updated_files}")
        _safe_print(f"[OK] Total replacements: {total_replacements}")
    else:
        _safe_print(f"[OK] Dry-run complete. Files needing updates: {updated_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
