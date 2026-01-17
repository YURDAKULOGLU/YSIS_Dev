"""
Comprehensive Coverage Analysis - Entire Project.

Checks:
1. Every adapter has tests
2. Every node has tests
3. Every service has tests
4. Every component logs operations
5. Journal logging coverage
"""

import ast
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src" / "ybis"
TESTS_DIR = PROJECT_ROOT / "tests"


def find_all_python_files(directory: Path, exclude_patterns: list[str] | None = None) -> list[Path]:
    """Find all Python files in directory."""
    if exclude_patterns is None:
        exclude_patterns = ["__pycache__", ".pyc", "__init__.py"]

    files = []
    for file_path in directory.rglob("*.py"):
        if any(pattern in str(file_path) for pattern in exclude_patterns):
            continue
        files.append(file_path)
    return files


def find_test_file(component_path: Path) -> Path | None:
    """Find test file for a component."""
    # Get relative path from src/ybis
    rel_path = component_path.relative_to(SRC_DIR)

    # Try different naming patterns
    patterns = [
        f"test_{component_path.stem}.py",
        f"test_{rel_path.stem}.py",
    ]

    # Search in tests directory
    for pattern in patterns:
        # Try direct match
        test_file = TESTS_DIR / pattern
        if test_file.exists():
            return test_file

        # Try matching directory structure
        test_file = TESTS_DIR / rel_path.parent / pattern
        if test_file.exists():
            return test_file

        # Try in adapters/nodes/services subdirectories
        for subdir in ["adapters", "orchestrator", "services"]:
            test_file = TESTS_DIR / subdir / pattern
            if test_file.exists():
                return test_file

    return None


def check_logging(file_path: Path) -> dict[str, Any]:
    """Check if file has logging."""
    result = {
        "has_logger": False,
        "has_journal": False,
        "log_calls": 0,
        "journal_calls": 0,
        "methods": [],
        "methods_without_logging": [],
    }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for logger
        if "logger" in content or "logging.getLogger" in content:
            result["has_logger"] = True

        # Check for journal
        if "append_event" in content or "journal" in content.lower():
            result["has_journal"] = True

        # Count log calls
        result["log_calls"] = content.count("logger.")
        result["journal_calls"] = content.count("append_event")

        # Parse AST to find methods
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    method_name = node.name
                    if not method_name.startswith("_"):
                        result["methods"].append(method_name)

                        # Check if method has logging
                        method_has_log = False
                        for child in ast.walk(node):
                            if isinstance(child, ast.Call):
                                if isinstance(child.func, ast.Attribute):
                                    if child.func.attr in ["info", "warning", "error", "debug", "exception"]:
                                        method_has_log = True
                                elif isinstance(child.func, ast.Name):
                                    if child.func.id == "append_event":
                                        method_has_log = True

                        if not method_has_log and len(node.body) > 1:  # Skip trivial methods
                            result["methods_without_logging"].append(method_name)
        except SyntaxError:
            pass  # Skip files with syntax errors

    except Exception as e:
        result["error"] = str(e)

    return result


def analyze_comprehensive_coverage() -> dict[str, Any]:
    """Analyze comprehensive coverage for entire project."""
    results = {
        "adapters": {},
        "nodes": {},
        "services": {},
        "data_plane": {},
        "orchestrator": {},
        "summary": {
            "total_files": 0,
            "files_with_tests": 0,
            "files_with_logger": 0,
            "files_with_journal": 0,
        },
    }

    # Analyze adapters
    adapters_dir = SRC_DIR / "adapters"
    if adapters_dir.exists():
        adapter_files = find_all_python_files(adapters_dir, exclude_patterns=["__pycache__", "__init__.py", "registry.py"])
        for adapter_file in adapter_files:
            adapter_name = adapter_file.stem
            test_file = find_test_file(adapter_file)
            logging_info = check_logging(adapter_file)

            results["adapters"][adapter_name] = {
                "file": str(adapter_file.relative_to(PROJECT_ROOT)),
                "has_test": test_file is not None,
                "test_file": str(test_file.relative_to(PROJECT_ROOT)) if test_file else None,
                "has_logger": logging_info["has_logger"],
                "has_journal": logging_info["has_journal"],
                "log_calls": logging_info["log_calls"],
                "journal_calls": logging_info["journal_calls"],
                "methods_without_logging": logging_info["methods_without_logging"][:5],  # Limit to 5
            }

            results["summary"]["total_files"] += 1
            if test_file:
                results["summary"]["files_with_tests"] += 1
            if logging_info["has_logger"]:
                results["summary"]["files_with_logger"] += 1
            if logging_info["has_journal"]:
                results["summary"]["files_with_journal"] += 1

    # Analyze nodes
    nodes_dir = SRC_DIR / "orchestrator" / "nodes"
    if nodes_dir.exists():
        node_files = find_all_python_files(nodes_dir, exclude_patterns=["__pycache__", "__init__.py"])
        for node_file in node_files:
            node_name = node_file.stem
            test_file = find_test_file(node_file)
            logging_info = check_logging(node_file)

            results["nodes"][node_name] = {
                "file": str(node_file.relative_to(PROJECT_ROOT)),
                "has_test": test_file is not None,
                "test_file": str(test_file.relative_to(PROJECT_ROOT)) if test_file else None,
                "has_logger": logging_info["has_logger"],
                "has_journal": logging_info["has_journal"],
                "log_calls": logging_info["log_calls"],
                "journal_calls": logging_info["journal_calls"],
                "methods_without_logging": logging_info["methods_without_logging"][:5],
            }

            results["summary"]["total_files"] += 1
            if test_file:
                results["summary"]["files_with_tests"] += 1
            if logging_info["has_logger"]:
                results["summary"]["files_with_logger"] += 1
            if logging_info["has_journal"]:
                results["summary"]["files_with_journal"] += 1

    # Analyze services
    services_dir = SRC_DIR / "services"
    if services_dir.exists():
        service_files = find_all_python_files(services_dir, exclude_patterns=["__pycache__", "__init__.py"])
        for service_file in service_files:
            service_name = service_file.stem
            test_file = find_test_file(service_file)
            logging_info = check_logging(service_file)

            results["services"][service_name] = {
                "file": str(service_file.relative_to(PROJECT_ROOT)),
                "has_test": test_file is not None,
                "test_file": str(test_file.relative_to(PROJECT_ROOT)) if test_file else None,
                "has_logger": logging_info["has_logger"],
                "has_journal": logging_info["has_journal"],
                "log_calls": logging_info["log_calls"],
                "journal_calls": logging_info["journal_calls"],
                "methods_without_logging": logging_info["methods_without_logging"][:5],
            }

            results["summary"]["total_files"] += 1
            if test_file:
                results["summary"]["files_with_tests"] += 1
            if logging_info["has_logger"]:
                results["summary"]["files_with_logger"] += 1
            if logging_info["has_journal"]:
                results["summary"]["files_with_journal"] += 1

    # Analyze data_plane
    data_plane_dir = SRC_DIR / "data_plane"
    if data_plane_dir.exists():
        data_plane_files = find_all_python_files(data_plane_dir, exclude_patterns=["__pycache__", "__init__.py"])
        for data_file in data_plane_files:
            data_name = data_file.stem
            test_file = find_test_file(data_file)
            logging_info = check_logging(data_file)

            results["data_plane"][data_name] = {
                "file": str(data_file.relative_to(PROJECT_ROOT)),
                "has_test": test_file is not None,
                "test_file": str(test_file.relative_to(PROJECT_ROOT)) if test_file else None,
                "has_logger": logging_info["has_logger"],
                "has_journal": logging_info["has_journal"],
                "log_calls": logging_info["log_calls"],
                "journal_calls": logging_info["journal_calls"],
                "methods_without_logging": logging_info["methods_without_logging"][:5],
            }

            results["summary"]["total_files"] += 1
            if test_file:
                results["summary"]["files_with_tests"] += 1
            if logging_info["has_logger"]:
                results["summary"]["files_with_logger"] += 1
            if logging_info["has_journal"]:
                results["summary"]["files_with_journal"] += 1

    # Analyze orchestrator (non-node files)
    orchestrator_dir = SRC_DIR / "orchestrator"
    if orchestrator_dir.exists():
        orchestrator_files = [
            f for f in find_all_python_files(orchestrator_dir, exclude_patterns=["__pycache__", "__init__.py"])
            if "nodes" not in str(f)
        ]
        for orch_file in orchestrator_files:
            orch_name = orch_file.stem
            test_file = find_test_file(orch_file)
            logging_info = check_logging(orch_file)

            results["orchestrator"][orch_name] = {
                "file": str(orch_file.relative_to(PROJECT_ROOT)),
                "has_test": test_file is not None,
                "test_file": str(test_file.relative_to(PROJECT_ROOT)) if test_file else None,
                "has_logger": logging_info["has_logger"],
                "has_journal": logging_info["has_journal"],
                "log_calls": logging_info["log_calls"],
                "journal_calls": logging_info["journal_calls"],
                "methods_without_logging": logging_info["methods_without_logging"][:5],
            }

            results["summary"]["total_files"] += 1
            if test_file:
                results["summary"]["files_with_tests"] += 1
            if logging_info["has_logger"]:
                results["summary"]["files_with_logger"] += 1
            if logging_info["has_journal"]:
                results["summary"]["files_with_journal"] += 1

    return results


def generate_comprehensive_report() -> str:
    """Generate comprehensive coverage report."""
    results = analyze_comprehensive_coverage()
    summary = results["summary"]

    report = []
    report.append("=" * 80)
    report.append("COMPREHENSIVE PROJECT COVERAGE ANALYSIS")
    report.append("=" * 80)
    report.append("")

    # Overall Summary
    report.append("## OVERALL SUMMARY")
    report.append("-" * 80)
    if summary["total_files"] > 0:
        test_pct = (summary["files_with_tests"] / summary["total_files"]) * 100
        logger_pct = (summary["files_with_logger"] / summary["total_files"]) * 100
        journal_pct = (summary["files_with_journal"] / summary["total_files"]) * 100

        report.append(f"Total Files Analyzed: {summary['total_files']}")
        report.append(f"Files with Tests: {summary['files_with_tests']}/{summary['total_files']} ({test_pct:.1f}%)")
        report.append(f"Files with Logger: {summary['files_with_logger']}/{summary['total_files']} ({logger_pct:.1f}%)")
        report.append(f"Files with Journal: {summary['files_with_journal']}/{summary['total_files']} ({journal_pct:.1f}%)")
    report.append("")

    # Adapters
    report.append("## ADAPTERS")
    report.append("-" * 80)
    adapters_without_tests = [name for name, info in results["adapters"].items() if not info["has_test"]]
    adapters_without_logger = [name for name, info in results["adapters"].items() if not info["has_logger"]]

    report.append(f"Total: {len(results['adapters'])}")
    report.append(f"Without Tests: {len(adapters_without_tests)}")
    if adapters_without_tests:
        for name in adapters_without_tests[:10]:  # Limit to 10
            report.append(f"  ❌ {name}")
    report.append(f"Without Logger: {len(adapters_without_logger)}")
    if adapters_without_logger:
        for name in adapters_without_logger[:10]:
            report.append(f"  ⚠️  {name}")
    report.append("")

    # Nodes
    report.append("## NODES")
    report.append("-" * 80)
    nodes_without_tests = [name for name, info in results["nodes"].items() if not info["has_test"]]
    nodes_without_logger = [name for name, info in results["nodes"].items() if not info["has_logger"]]

    report.append(f"Total: {len(results['nodes'])}")
    report.append(f"Without Tests: {len(nodes_without_tests)}")
    if nodes_without_tests:
        for name in nodes_without_tests[:10]:
            report.append(f"  ❌ {name}")
    report.append(f"Without Logger: {len(nodes_without_logger)}")
    if nodes_without_logger:
        for name in nodes_without_logger[:10]:
            report.append(f"  ⚠️  {name}")
    report.append("")

    # Services
    report.append("## SERVICES")
    report.append("-" * 80)
    services_without_tests = [name for name, info in results["services"].items() if not info["has_test"]]
    services_without_logger = [name for name, info in results["services"].items() if not info["has_logger"]]

    report.append(f"Total: {len(results['services'])}")
    report.append(f"Without Tests: {len(services_without_tests)}")
    if services_without_tests:
        for name in services_without_tests[:15]:  # Services can be more
            report.append(f"  ❌ {name}")
    report.append(f"Without Logger: {len(services_without_logger)}")
    if services_without_logger:
        for name in services_without_logger[:15]:
            report.append(f"  ⚠️  {name}")
    report.append("")

    # Data Plane
    report.append("## DATA PLANE")
    report.append("-" * 80)
    data_without_tests = [name for name, info in results["data_plane"].items() if not info["has_test"]]
    data_without_logger = [name for name, info in results["data_plane"].items() if not info["has_logger"]]

    report.append(f"Total: {len(results['data_plane'])}")
    report.append(f"Without Tests: {len(data_without_tests)}")
    if data_without_tests:
        for name in data_without_tests[:10]:
            report.append(f"  ❌ {name}")
    report.append(f"Without Logger: {len(data_without_logger)}")
    if data_without_logger:
        for name in data_without_logger[:10]:
            report.append(f"  ⚠️  {name}")
    report.append("")

    # Detailed Issues
    report.append("## DETAILED ISSUES")
    report.append("-" * 80)

    # Files with methods without logging
    report.append("### Methods Without Logging")
    for category in ["adapters", "nodes", "services", "data_plane"]:
        for name, info in results[category].items():
            if info.get("methods_without_logging"):
                report.append(f"{category}/{name}: {', '.join(info['methods_without_logging'][:3])}")

    report.append("")

    return "\n".join(report)


if __name__ == "__main__":
    report = generate_comprehensive_report()
    print(report)

    # Save report
    report_path = PROJECT_ROOT / "docs" / "COMPREHENSIVE_COVERAGE_ANALYSIS.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ Report saved to: {report_path}")


