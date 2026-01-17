"""
Logging Coverage Analysis Script.

Checks if all components log their operations:
1. Adapters log initialization, operations, errors
2. Nodes log execution, state changes
3. Services log important operations
"""

import ast
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
ADAPTERS_DIR = PROJECT_ROOT / "src" / "ybis" / "adapters"
NODES_DIR = PROJECT_ROOT / "src" / "ybis" / "orchestrator" / "nodes"
SERVICES_DIR = PROJECT_ROOT / "src" / "ybis" / "services"


def analyze_logging(file_path: Path) -> dict[str, Any]:
    """Analyze logging in a file."""
    result = {
        "has_logger": False,
        "has_journal": False,
        "log_calls": [],
        "journal_calls": [],
        "methods_without_logging": [],
    }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            tree = ast.parse(content)

        # Check for logger
        if "logger" in content or "logging.getLogger" in content:
            result["has_logger"] = True

        # Check for journal
        if "append_event" in content or "journal" in content:
            result["has_journal"] = True

        # Find all methods
        methods = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                methods.append(node.name)

        # Check each method for logging
        for method in methods:
            method_has_log = False
            method_has_journal = False

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == method:
                    # Check method body
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call):
                            if isinstance(child.func, ast.Attribute):
                                if child.func.attr in ["info", "warning", "error", "debug"]:
                                    method_has_log = True
                            if isinstance(child.func, ast.Name):
                                if child.func.id == "append_event":
                                    method_has_journal = True

                    if not method_has_log and not method_has_journal and not method.startswith("_"):
                        result["methods_without_logging"].append(method)

        # Count log calls
        result["log_calls"] = content.count("logger.")
        result["journal_calls"] = content.count("append_event")

    except Exception as e:
        result["error"] = str(e)

    return result


def check_all_components() -> dict[str, Any]:
    """Check logging coverage for all components."""
    results = {
        "adapters": {},
        "nodes": {},
        "services": {},
        "summary": {
            "total_adapters": 0,
            "adapters_with_logger": 0,
            "adapters_with_journal": 0,
            "total_nodes": 0,
            "nodes_with_logger": 0,
            "nodes_with_journal": 0,
        },
    }

    # Check adapters
    adapter_files = list(ADAPTERS_DIR.glob("*_adapter.py"))
    adapter_files += list(ADAPTERS_DIR.glob("*_executor.py"))
    adapter_files = [f for f in adapter_files if f.name != "__init__.py" and f.name != "registry.py"]

    for adapter_file in adapter_files:
        adapter_name = adapter_file.stem
        analysis = analyze_logging(adapter_file)
        results["adapters"][adapter_name] = analysis

        results["summary"]["total_adapters"] += 1
        if analysis.get("has_logger"):
            results["summary"]["adapters_with_logger"] += 1
        if analysis.get("has_journal"):
            results["summary"]["adapters_with_journal"] += 1

    # Check nodes
    node_files = list(NODES_DIR.glob("*.py"))
    node_files = [f for f in node_files if f.name != "__init__.py"]

    for node_file in node_files:
        node_name = node_file.stem
        analysis = analyze_logging(node_file)
        results["nodes"][node_name] = analysis

        results["summary"]["total_nodes"] += 1
        if analysis.get("has_logger"):
            results["summary"]["nodes_with_logger"] += 1
        if analysis.get("has_journal"):
            results["summary"]["nodes_with_journal"] += 1

    return results


def generate_report() -> str:
    """Generate logging coverage report."""
    results = check_all_components()
    summary = results["summary"]

    report = []
    report.append("=" * 80)
    report.append("LOGGING COVERAGE ANALYSIS")
    report.append("=" * 80)
    report.append("")

    # Summary
    report.append("## SUMMARY")
    report.append("-" * 80)
    report.append(f"Adapters: {summary['adapters_with_logger']}/{summary['total_adapters']} have logger ({summary['adapters_with_logger']/summary['total_adapters']*100:.1f}%)")
    report.append(f"Adapters: {summary['adapters_with_journal']}/{summary['total_adapters']} use journal ({summary['adapters_with_journal']/summary['total_adapters']*100:.1f}%)")
    report.append(f"Nodes: {summary['nodes_with_logger']}/{summary['total_nodes']} have logger ({summary['nodes_with_logger']/summary['total_nodes']*100:.1f}%)")
    report.append(f"Nodes: {summary['nodes_with_journal']}/{summary['total_nodes']} use journal ({summary['nodes_with_journal']/summary['total_nodes']*100:.1f}%)")
    report.append("")

    # Adapters without logging
    report.append("## ADAPTERS WITHOUT LOGGING")
    report.append("-" * 80)
    for adapter_name, analysis in results["adapters"].items():
        if not analysis.get("has_logger") and not analysis.get("has_journal"):
            report.append(f"❌ {adapter_name}: No logging")
        elif analysis.get("methods_without_logging"):
            report.append(f"⚠️  {adapter_name}: Methods without logging: {', '.join(analysis['methods_without_logging'][:5])}")

    report.append("")

    # Nodes without logging
    report.append("## NODES WITHOUT LOGGING")
    report.append("-" * 80)
    for node_name, analysis in results["nodes"].items():
        if not analysis.get("has_logger") and not analysis.get("has_journal"):
            report.append(f"❌ {node_name}: No logging")
        elif analysis.get("methods_without_logging"):
            report.append(f"⚠️  {node_name}: Methods without logging: {', '.join(analysis['methods_without_logging'][:5])}")

    report.append("")

    return "\n".join(report)


if __name__ == "__main__":
    report = generate_report()
    print(report)

    # Save report
    report_path = PROJECT_ROOT / "docs" / "LOGGING_COVERAGE_ANALYSIS.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ Report saved to: {report_path}")


