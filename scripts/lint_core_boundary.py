#!/usr/bin/env python3
"""
Core Boundary Lint - Enforce adapter/service import restrictions.

This script ensures that core modules (contracts, syscalls, control_plane,
orchestrator, data_plane) do not import from adapters or services.

Core modules are:
- src/ybis/contracts/
- src/ybis/syscalls/
- src/ybis/control_plane/
- src/ybis/orchestrator/
- src/ybis/data_plane/

Forbidden imports:
- src/ybis/adapters/
- src/ybis/services/ (except for policy.py which is core)

Exit code: 0 if all checks pass, 1 if violations found.
"""

import ast
import sys
from pathlib import Path
from typing import List, Tuple

# Core module paths (relative to src/ybis/)
CORE_MODULES = {
    "contracts",
    "syscalls",
    "control_plane",
    "orchestrator",
    "data_plane",
}

# Forbidden import prefixes
FORBIDDEN_PREFIXES = [
    "ybis.adapters",
    "ybis.services",
    "..adapters",
    "..services",
    ".adapters",
    ".services",
]

# Allowed service imports (these are considered core)
ALLOWED_SERVICE_IMPORTS = {
    "ybis.services.policy",
    "..services.policy",
    ".services.policy",
}


class ImportVisitor(ast.NodeVisitor):
    """AST visitor to collect all imports."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.imports: List[Tuple[int, str, int]] = []  # (line, module, level)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.append((node.lineno, alias.name, 0))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        level = node.level if node.level else 0
        module = node.module if node.module else ""
        self.imports.append((node.lineno, module, level))
        self.generic_visit(node)


def is_core_module(file_path: Path) -> bool:
    """Check if a file is in a core module."""
    parts = file_path.parts
    if "src" in parts and "ybis" in parts:
        ybis_idx = parts.index("ybis")
        if ybis_idx + 1 < len(parts):
            module_name = parts[ybis_idx + 1]
            return module_name in CORE_MODULES
    return False


def check_forbidden_import(import_name: str, level: int) -> bool:
    """
    Check if an import is forbidden.
    
    Args:
        import_name: Module name
        level: Relative import level (0 = absolute, 1 = ., 2 = ..)
    """
    # Check allowed exceptions first
    if any(import_name.startswith(allowed) for allowed in ALLOWED_SERVICE_IMPORTS):
        return False
    
    # Check relative imports (level > 0)
    if level > 0:
        # Relative import like ..adapters or ..services
        if import_name.startswith("adapters") or import_name.startswith("services"):
            # Check if it's the allowed policy import
            if import_name == "services.policy":
                return False
            return True
    
    # Check absolute imports
    if level == 0:
        # Check forbidden prefixes
        for prefix in FORBIDDEN_PREFIXES:
            if import_name.startswith(prefix):
                return True
    
    return False


def lint_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """
    Lint a single file for forbidden imports.

    Returns:
        List of (line_number, import_name, error_message) tuples
    """
    violations = []

    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
        visitor = ImportVisitor(file_path)
        visitor.visit(tree)

        for line_no, import_name, level in visitor.imports:
            if check_forbidden_import(import_name, level):
                violations.append(
                    (
                        line_no,
                        import_name,
                        f"Forbidden import: core modules cannot import from adapters or services",
                    )
                )

    except SyntaxError as e:
        violations.append(
            (
                e.lineno or 0,
                "",
                f"Syntax error: {e.msg}",
            )
        )
    except Exception as e:
        violations.append(
            (
                0,
                "",
                f"Error parsing file: {e}",
            )
        )

    return violations


def main() -> int:
    """Main lint function."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src" / "ybis"

    if not src_dir.exists():
        print(f"Error: {src_dir} does not exist", file=sys.stderr)
        return 1

    all_violations = []

    # Find all Python files in core modules
    for core_module in CORE_MODULES:
        core_path = src_dir / core_module
        if not core_path.exists():
            continue

        for py_file in core_path.rglob("*.py"):
            # Check __init__.py too (re-exports can bypass lint)
            violations = lint_file(py_file)
            if violations:
                all_violations.extend(
                    [(py_file, line_no, import_name, error) for line_no, import_name, error in violations]
                )

    # Report violations
    if all_violations:
        print("[ERROR] Core Boundary Violations Found:\n", file=sys.stderr)
        for file_path, line_no, import_name, error in all_violations:
            rel_path = file_path.relative_to(project_root)
            print(f"  {rel_path}:{line_no}", file=sys.stderr)
            if import_name:
                print(f"    Import: {import_name}", file=sys.stderr)
            print(f"    Error: {error}\n", file=sys.stderr)

        print(
            "\n[INFO] Core modules (contracts, syscalls, control_plane, orchestrator, data_plane)",
            file=sys.stderr,
        )
        print("   cannot import from adapters/ or services/ (except policy.py).", file=sys.stderr)
        print("   Use adapter registry pattern or dependency injection instead.", file=sys.stderr)
        return 1

    print("[OK] Core boundary check passed: no forbidden imports found")
    return 0


if __name__ == "__main__":
    sys.exit(main())

