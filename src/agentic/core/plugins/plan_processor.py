"""
Plan Post-Processor: Resolves glob patterns and validates file paths.

Fixes LIMIT-TEST Problem 1: CrewAI produces glob patterns, Aider needs concrete paths.
"""
import glob
import os
from pathlib import Path
from src.agentic.core.utils.logging_utils import log_event

from src.agentic.core.config import PROJECT_ROOT
from src.agentic.core.protocols import Plan


def _looks_like_path(value: str) -> bool:
    if not value:
        return False
    lowered = value.lower()
    if "all files" in lowered or "all other" in lowered or "files under" in lowered:
        return False
    if " " in value:
        return False
    if "/" in value or "\\" in value:
        return True
    # Allow plain filenames with extensions for new files
    return "." in value

# Constants
MAX_FILES_FROM_GLOB = 10  # Limit expansion to prevent token overflow
GLOB_WARNING_THRESHOLD = 5


def _code_root() -> Path:
    code_root = os.getenv("YBIS_CODE_ROOT")
    if code_root:
        return Path(code_root).resolve()
    return Path(PROJECT_ROOT).resolve()


def resolve_glob_pattern(pattern: str, base_path: Path | None = None) -> list[str]:
    """
    Resolve a glob pattern to concrete file paths.

    Args:
        pattern: Glob pattern like 'src/agentic/core/*.py'
        base_path: Base directory for resolution

    Returns:
        List of resolved absolute file paths
    """
    # If not a glob pattern, return as-is
    resolved_base = base_path or _code_root()
    if '*' not in pattern and '?' not in pattern:
        full_path = resolved_base / pattern
        if full_path.exists():
            return [str(full_path)]
        return [pattern]  # Keep original if not found

    # Resolve glob
    search_path = resolved_base / pattern
    matches = list(glob.glob(str(search_path), recursive=True))

    # Filter to only existing files (not directories)
    files = [f for f in matches if Path(f).is_file()]

    # Limit results to prevent token overflow
    if len(files) > MAX_FILES_FROM_GLOB:
        log_event(f"WARNING: Glob '{pattern}' matched {len(files)} files, limiting to {MAX_FILES_FROM_GLOB}", component="plan_processor", level="warning")
        files = files[:MAX_FILES_FROM_GLOB]

    return files


def process_plan(plan: Plan) -> Plan:
    """
    Post-process a plan to resolve glob patterns and validate paths.

    Args:
        plan: Original Plan object from planner

    Returns:
        Processed Plan with resolved file paths
    """
    if not plan or not plan.files_to_modify:
        return plan

    resolved_files = []
    glob_count = 0

    for file_pattern in plan.files_to_modify:
        # Check if it's a glob pattern
        if '*' in file_pattern or '?' in file_pattern:
            glob_count += 1
            expanded = resolve_glob_pattern(file_pattern)
            if expanded:
                log_event(f"Resolved '{file_pattern}' -> {len(expanded)} files", component="plan_processor")
                resolved_files.extend(expanded)
            else:
                log_event(f"WARNING: Glob '{file_pattern}' matched 0 files", component="plan_processor", level="warning")
        else:
            # Concrete path - validate existence
            full_path = _code_root() / file_pattern
            if full_path.exists():
                resolved_files.append(str(full_path))
            else:
                # New file - keep only if it looks like a path
                if _looks_like_path(file_pattern):
                    resolved_files.append(file_pattern)
                else:
                    log_event(f"WARNING: Skipping invalid file entry: {file_pattern}", component="plan_processor", level="warning")

    # Remove duplicates while preserving order
    seen = set()
    unique_files = []
    for f in resolved_files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    if glob_count > 0:
        log_event(f"Processed {glob_count} glob patterns -> {len(unique_files)} concrete files", component="plan_processor")

    max_files = MAX_FILES_FROM_GLOB * 2
    if len(unique_files) > max_files:
        log_event(f"WARNING: {len(unique_files)} files requested, limiting to {max_files}", component="plan_processor", level="warning")
        unique_files = unique_files[:max_files]

    # Create new plan with resolved files
    plan.files_to_modify = unique_files
    return plan


def validate_plan_files(plan: Plan) -> tuple[bool, list[str]]:
    """
    Validate that plan files are actionable (no globs remaining).

    Returns:
        (is_valid, list of issues)
    """
    issues = []

    for f in plan.files_to_modify:
        if '*' in f or '?' in f:
            issues.append(f"Unresolved glob pattern: {f}")

    if len(plan.files_to_modify) > MAX_FILES_FROM_GLOB * 2:
        issues.append(f"Too many files: {len(plan.files_to_modify)} (max recommended: {MAX_FILES_FROM_GLOB * 2})")

    return len(issues) == 0, issues
