"""
Context Limiter: Reduces token usage by smart file content extraction.

Fixes LIMIT-TEST Problem 3: Token context overflow (34k > 32k).
"""
import re
from pathlib import Path
from src.agentic.core.utils.logging_utils import log_event

# Constants
MAX_TOKENS_ESTIMATE = 28000  # Leave buffer for prompt
CHARS_PER_TOKEN = 4  # Rough estimate
MAX_FILE_CHARS = 8000  # Per-file limit
MAX_TOTAL_CHARS = MAX_TOKENS_ESTIMATE * CHARS_PER_TOKEN


def estimate_tokens(text: str) -> int:
    """Rough token count estimation."""
    return len(text) // CHARS_PER_TOKEN


def extract_skeleton(content: str, file_ext: str = ".py") -> str:
    """
    Extract file skeleton: imports, class/function signatures only.

    Args:
        content: Full file content
        file_ext: File extension for language detection

    Returns:
        Skeleton with signatures only
    """
    if file_ext != ".py":
        # For non-Python, just truncate
        return content[:MAX_FILE_CHARS] + "\n# ... [truncated]" if len(content) > MAX_FILE_CHARS else content

    lines = content.split('\n')
    skeleton_lines = []
    in_docstring = False
    docstring_char = None

    for line in lines:
        stripped = line.strip()

        # Track docstrings
        if '"""' in stripped or "'''" in stripped:
            if not in_docstring:
                in_docstring = True
                docstring_char = '"""' if '"""' in stripped else "'''"
                # Check if single-line docstring
                if stripped.count(docstring_char) >= 2:
                    in_docstring = False
            elif docstring_char in stripped:
                in_docstring = False
            continue

        if in_docstring:
            continue

        # Keep imports
        if stripped.startswith(('import ', 'from ')):
            skeleton_lines.append(line)
            continue

        # Keep class/function definitions
        if stripped.startswith(('class ', 'def ', 'async def ')):
            skeleton_lines.append(line)
            # Add ... placeholder for body
            indent = len(line) - len(line.lstrip())
            skeleton_lines.append(' ' * (indent + 4) + '...')
            continue

        # Keep decorators
        if stripped.startswith('@'):
            skeleton_lines.append(line)
            continue

        # Keep module-level constants (UPPER_CASE = ...)
        if re.match(r'^[A-Z][A-Z0-9_]* *=', stripped):
            skeleton_lines.append(line)
            continue

    return '\n'.join(skeleton_lines)


def limit_file_content(file_path: Path, max_chars: int = MAX_FILE_CHARS) -> str:
    """
    Read file with smart truncation.

    Args:
        file_path: Path to file
        max_chars: Maximum characters to return

    Returns:
        File content (possibly truncated with skeleton)
    """
    if not file_path.exists():
        return ""

    try:
        content = file_path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return ""

    if len(content) <= max_chars:
        return content

    # File too large - extract skeleton
    ext = file_path.suffix
    skeleton = extract_skeleton(content, ext)

    if len(skeleton) <= max_chars:
        return skeleton + f"\n# [Skeleton only - full file: {len(content)} chars]"

    # Even skeleton too large - hard truncate
    return skeleton[:max_chars] + f"\n# ... [truncated from {len(skeleton)} chars]"


def smart_context_selection(
    files: list[str],
    task_description: str,
    base_path: Path
) -> list[tuple[str, str]]:
    """
    Select and limit context files based on task.

    Args:
        files: List of file paths
        task_description: Task description for relevance scoring
        base_path: Base path for file resolution

    Returns:
        List of (file_path, limited_content) tuples
    """
    results = []
    total_chars = 0

    # Keywords from task for relevance
    task_keywords = set(re.findall(r'\b\w+\b', task_description.lower()))

    # Score files by relevance
    scored_files = []
    for f in files:
        path = Path(f) if Path(f).is_absolute() else base_path / f
        if not path.exists():
            scored_files.append((f, 0, True))  # New file, high priority
            continue

        try:
            content = path.read_text(encoding='utf-8', errors='replace')
            # Simple relevance: count keyword matches
            file_words = set(re.findall(r'\b\w+\b', content.lower()))
            score = len(task_keywords & file_words)
            scored_files.append((f, score, False))
        except Exception:
            scored_files.append((f, 0, False))

    # Sort by relevance (new files first, then by score)
    scored_files.sort(key=lambda x: (not x[2], -x[1]))

    for file_path, score, is_new in scored_files:
        if total_chars >= MAX_TOTAL_CHARS:
            log_event(f"Skipping {file_path} - context limit reached", component="context_limiter", level="warning")
            break

        path = Path(file_path) if Path(file_path).is_absolute() else base_path / file_path

        if is_new:
            # New file - include empty placeholder
            results.append((file_path, "# New file - to be created"))
            total_chars += 30
        else:
            content = limit_file_content(path)
            results.append((file_path, content))
            total_chars += len(content)

    log_event(f"Selected {len(results)} files, ~{total_chars // CHARS_PER_TOKEN} tokens", component="context_limiter")
    return results
