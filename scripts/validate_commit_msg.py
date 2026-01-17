#!/usr/bin/env python3
"""
Commit Message Validator for YBIS
Constitution V3.0 compliant - X.1 Git Discipline

Validates commit messages follow the format:
<type>(<scope>): <subject>
"""

import re
import sys

# Pattern from COMMIT_STANDARDS.md
PATTERN = re.compile(
    r"^(feat|fix|perf|refactor|style|docs|test|chore|ci|revert)"
    r"(\([a-z_]+\))?"
    r":\s+.+"
)

# Max subject length
MAX_SUBJECT_LENGTH = 50


def validate_commit_message(msg: str) -> bool:
    """Validate commit message format."""
    if not msg:
        print("ERROR: Empty commit message")
        return False

    lines = msg.strip().split("\n")
    first_line = lines[0]

    # Check format
    if not PATTERN.match(first_line):
        print(f"ERROR: Invalid commit message format: {first_line}")
        print("\nExpected format: <type>(<scope>): <subject>")
        print("\nTypes: feat, fix, perf, refactor, style, docs, test, chore, ci, revert")
        print("Scope: Optional, lowercase with underscores (e.g., planner, executor)")
        print("Subject: Lowercase, imperative mood, max 50 chars, no period")
        print("\nExamples:")
        print("  feat(planner): add RAG context support")
        print("  fix(executor): handle empty LLM response")
        print("  refactor(graph): extract routing logic")
        return False

    # Check subject length
    subject = first_line.split(":", 1)[1].strip()
    if len(subject) > MAX_SUBJECT_LENGTH:
        print(f"ERROR: Subject too long ({len(subject)} > {MAX_SUBJECT_LENGTH}): {subject}")
        return False

    # Check for period at end
    if subject.endswith("."):
        print(f"ERROR: Subject should not end with period: {subject}")
        return False

    return True


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: validate_commit_msg.py <commit_msg_file>")
        sys.exit(1)

    commit_msg_file = sys.argv[1]

    try:
        with open(commit_msg_file, "r", encoding="utf-8") as f:
            msg = f.read()
    except Exception as e:
        print(f"ERROR: Failed to read commit message file: {e}")
        sys.exit(1)

    if validate_commit_message(msg):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

