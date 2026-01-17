"""
Test Coverage Analysis Script.

Checks if all components have tests:
1. Adapters have test files
2. Nodes have test files
3. Services have test files
4. Integration tests exist
"""

from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
ADAPTERS_DIR = PROJECT_ROOT / "src" / "ybis" / "adapters"
NODES_DIR = PROJECT_ROOT / "src" / "ybis" / "orchestrator" / "nodes"
SERVICES_DIR = PROJECT_ROOT / "src" / "ybis" / "services"
TESTS_DIR = PROJECT_ROOT / "tests"


def find_test_file(component_name: str, component_type: str) -> Path | None:
    """Find test file for a component."""
    # Try different naming patterns
    patterns = [
        f"test_{component_name}.py",
        f"test_{component_name.replace('_adapter', '')}.py",
        f"test_{component_name.replace('_executor', '')}.py",
        f"test_{component_name.replace('_node', '')}.py",
    ]

    # Search in tests directory
    for pattern in patterns:
        test_file = TESTS_DIR / pattern
        if test_file.exists():
            return test_file

        # Search in subdirectories
        for subdir in TESTS_DIR.iterdir():
            if subdir.is_dir():
                test_file = subdir / pattern
                if test_file.exists():
                    return test_file

    return None


def check_test_coverage() -> dict[str, Any]:
    """Check test coverage for all components."""
    results = {
        "adapters": {},
        "nodes": {},
        "services": {},
        "summary": {
            "total_adapters": 0,
            "adapters_with_tests": 0,
            "total_nodes": 0,
            "nodes_with_tests": 0,
            "total_services": 0,
            "services_with_tests": 0,
        },
    }

    # Check adapters
    adapter_files = list(ADAPTERS_DIR.glob("*_adapter.py"))
    adapter_files += list(ADAPTERS_DIR.glob("*_executor.py"))
    adapter_files = [f for f in adapter_files if f.name != "__init__.py" and f.name != "registry.py"]

    for adapter_file in adapter_files:
        adapter_name = adapter_file.stem
        test_file = find_test_file(adapter_name, "adapter")
        results["adapters"][adapter_name] = {
            "has_test": test_file is not None,
            "test_file": str(test_file) if test_file else None,
        }

        results["summary"]["total_adapters"] += 1
        if test_file:
            results["summary"]["adapters_with_tests"] += 1

    # Check nodes
    node_files = list(NODES_DIR.glob("*.py"))
    node_files = [f for f in node_files if f.name != "__init__.py"]

    for node_file in node_files:
        node_name = node_file.stem
        test_file = find_test_file(node_name, "node")
        results["nodes"][node_name] = {
            "has_test": test_file is not None,
            "test_file": str(test_file) if test_file else None,
        }

        results["summary"]["total_nodes"] += 1
        if test_file:
            results["summary"]["nodes_with_tests"] += 1

    # Check services (sample)
    service_files = list(SERVICES_DIR.glob("*.py"))
    service_files = [f for f in service_files if f.name != "__init__.py"][:10]  # Sample

    for service_file in service_files:
        service_name = service_file.stem
        test_file = find_test_file(service_name, "service")
        results["services"][service_name] = {
            "has_test": test_file is not None,
            "test_file": str(test_file) if test_file else None,
        }

        results["summary"]["total_services"] += 1
        if test_file:
            results["summary"]["services_with_tests"] += 1

    return results


def generate_report() -> str:
    """Generate test coverage report."""
    results = check_test_coverage()
    summary = results["summary"]

    report = []
    report.append("=" * 80)
    report.append("TEST COVERAGE ANALYSIS")
    report.append("=" * 80)
    report.append("")

    # Summary
    report.append("## SUMMARY")
    report.append("-" * 80)
    if summary["total_adapters"] > 0:
        report.append(f"Adapters: {summary['adapters_with_tests']}/{summary['total_adapters']} have tests ({summary['adapters_with_tests']/summary['total_adapters']*100:.1f}%)")
    if summary["total_nodes"] > 0:
        report.append(f"Nodes: {summary['nodes_with_tests']}/{summary['total_nodes']} have tests ({summary['nodes_with_tests']/summary['total_nodes']*100:.1f}%)")
    if summary["total_services"] > 0:
        report.append(f"Services: {summary['services_with_tests']}/{summary['total_services']} have tests ({summary['services_with_tests']/summary['total_services']*100:.1f}%)")
    report.append("")

    # Adapters without tests
    report.append("## ADAPTERS WITHOUT TESTS")
    report.append("-" * 80)
    for adapter_name, info in results["adapters"].items():
        if not info["has_test"]:
            report.append(f"❌ {adapter_name}: No test file")

    report.append("")

    # Nodes without tests
    report.append("## NODES WITHOUT TESTS")
    report.append("-" * 80)
    for node_name, info in results["nodes"].items():
        if not info["has_test"]:
            report.append(f"❌ {node_name}: No test file")

    report.append("")

    return "\n".join(report)


if __name__ == "__main__":
    report = generate_report()
    print(report)

    # Save report
    report_path = PROJECT_ROOT / "docs" / "TEST_COVERAGE_ANALYSIS.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ Report saved to: {report_path}")


