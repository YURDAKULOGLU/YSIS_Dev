"""
System Homogeneity Analysis Script.

Analyzes whether all adapters and components follow central standards:
1. Policy-driven configuration
2. Registry registration
3. Standard interfaces
4. Fallback mechanisms
5. Self-improvement capability
"""

import ast
import importlib.util
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).parent.parent
ADAPTERS_DIR = PROJECT_ROOT / "src" / "ybis" / "adapters"
ORCHESTRATOR_DIR = PROJECT_ROOT / "src" / "ybis" / "orchestrator"


def analyze_adapter_files() -> dict[str, Any]:
    """Analyze all adapter files for homogeneity."""
    results = {
        "adapters": {},
        "issues": [],
        "stats": {
            "total_adapters": 0,
            "registry_registered": 0,
            "policy_integrated": 0,
            "has_fallback": 0,
            "direct_imports": 0,
        },
    }

    # Find all adapter files
    adapter_files = list(ADAPTERS_DIR.glob("*_adapter.py"))
    adapter_files += list(ADAPTERS_DIR.glob("*_executor.py"))

    for adapter_file in adapter_files:
        adapter_name = adapter_file.stem
        results["adapters"][adapter_name] = {
            "file": str(adapter_file),
            "registry_registered": False,
            "policy_integrated": False,
            "has_fallback": False,
            "direct_imports": [],
            "uses_getter": False,
            "issues": [],
        }

        # Parse file
        try:
            with open(adapter_file, "r", encoding="utf-8") as f:
                content = f.read()
                tree = ast.parse(content)

            # Check for registry registration
            if "registry.register" in content or "AdapterRegistry" in content:
                results["adapters"][adapter_name]["registry_registered"] = True
                results["stats"]["registry_registered"] += 1

            # Check for policy integration
            if "get_policy_provider" in content or "policy.get" in content:
                results["adapters"][adapter_name]["policy_integrated"] = True
                results["stats"]["policy_integrated"] += 1

            # Check for fallback
            if "fallback" in content.lower() or "except" in content:
                results["adapters"][adapter_name]["has_fallback"] = True
                results["stats"]["has_fallback"] += 1

            # Check for getter function
            if f"get_{adapter_name}" in content or f"def get_" in content:
                results["adapters"][adapter_name]["uses_getter"] = True

            # Check for direct imports (anti-pattern)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module and "adapters" in node.module:
                        if any("get_" in alias.name for alias in node.names):
                            results["adapters"][adapter_name]["direct_imports"].append(
                                f"from {node.module} import {', '.join(a.name for a in node.names)}"
                            )
                            results["stats"]["direct_imports"] += 1

        except Exception as e:
            results["adapters"][adapter_name]["issues"].append(f"Parse error: {e}")

    results["stats"]["total_adapters"] = len(results["adapters"])
    return results


def analyze_orchestrator_usage() -> dict[str, Any]:
    """Analyze how orchestrator uses adapters."""
    results = {
        "nodes": {},
        "issues": [],
        "stats": {
            "uses_registry": 0,
            "direct_imports": 0,
            "policy_aware": 0,
        },
    }

    # Find all node files
    node_files = list((ORCHESTRATOR_DIR / "nodes").glob("*.py"))
    node_files = [f for f in node_files if f.name != "__init__.py"]

    for node_file in node_files:
        node_name = node_file.stem
        results["nodes"][node_name] = {
            "file": str(node_file),
            "uses_registry": False,
            "direct_imports": [],
            "policy_aware": False,
            "issues": [],
        }

        try:
            with open(node_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for registry usage
            if "registry.get" in content or "get_registry" in content:
                results["nodes"][node_name]["uses_registry"] = True
                results["stats"]["uses_registry"] += 1

            # Check for direct adapter imports
            if "from ...adapters" in content or "from ..adapters" in content:
                # Extract import statements
                import re
                imports = re.findall(r"from\s+[\.\w]+\s+import\s+[\w, ]+", content)
                adapter_imports = [imp for imp in imports if "adapters" in imp]
                results["nodes"][node_name]["direct_imports"] = adapter_imports
                if adapter_imports:
                    results["stats"]["direct_imports"] += len(adapter_imports)

            # Check for policy awareness
            if "get_policy_provider" in content or "policy.get" in content:
                results["nodes"][node_name]["policy_aware"] = True
                results["stats"]["policy_aware"] += 1

        except Exception as e:
            results["nodes"][node_name]["issues"].append(f"Parse error: {e}")

    return results


def check_bootstrap_registration() -> dict[str, Any]:
    """Check if adapters are registered in bootstrap."""
    bootstrap_file = PROJECT_ROOT / "src" / "ybis" / "services" / "adapter_bootstrap.py"

    results = {
        "registered_adapters": [],
        "missing_adapters": [],
    }

    if not bootstrap_file.exists():
        return results

    with open(bootstrap_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all adapter files
    adapter_files = list(ADAPTERS_DIR.glob("*_adapter.py"))
    adapter_files += list(ADAPTERS_DIR.glob("*_executor.py"))

    for adapter_file in adapter_files:
        adapter_name = adapter_file.stem
        # Check if registered in bootstrap
        if f'"{adapter_name}"' in content or f"'{adapter_name}'" in content:
            results["registered_adapters"].append(adapter_name)
        else:
            results["missing_adapters"].append(adapter_name)

    return results


def generate_report() -> str:
    """Generate comprehensive homogeneity report."""
    adapter_analysis = analyze_adapter_files()
    orchestrator_analysis = analyze_orchestrator_usage()
    bootstrap_check = check_bootstrap_registration()

    report = []
    report.append("=" * 80)
    report.append("SYSTEM HOMOGENEITY ANALYSIS")
    report.append("=" * 80)
    report.append("")

    # Adapter Statistics
    report.append("## ADAPTER STATISTICS")
    report.append("-" * 80)
    stats = adapter_analysis["stats"]
    total = stats["total_adapters"]
    report.append(f"Total Adapters: {total}")
    report.append(f"Registry Registered: {stats['registry_registered']}/{total} ({stats['registry_registered']/total*100:.1f}%)")
    report.append(f"Policy Integrated: {stats['policy_integrated']}/{total} ({stats['policy_integrated']/total*100:.1f}%)")
    report.append(f"Has Fallback: {stats['has_fallback']}/{total} ({stats['has_fallback']/total*100:.1f}%)")
    report.append(f"Direct Imports Found: {stats['direct_imports']}")
    report.append("")

    # Bootstrap Registration
    report.append("## BOOTSTRAP REGISTRATION")
    report.append("-" * 80)
    report.append(f"Registered: {len(bootstrap_check['registered_adapters'])}")
    report.append(f"Missing: {len(bootstrap_check['missing_adapters'])}")
    if bootstrap_check["missing_adapters"]:
        report.append("Missing Adapters:")
        for adapter in bootstrap_check["missing_adapters"]:
            report.append(f"  - {adapter}")
    report.append("")

    # Orchestrator Usage
    report.append("## ORCHESTRATOR USAGE")
    report.append("-" * 80)
    orch_stats = orchestrator_analysis["stats"]
    total_nodes = len(orchestrator_analysis["nodes"])
    report.append(f"Total Nodes: {total_nodes}")
    report.append(f"Uses Registry: {orch_stats['uses_registry']}/{total_nodes}")
    report.append(f"Direct Imports: {orch_stats['direct_imports']}")
    report.append(f"Policy Aware: {orch_stats['policy_aware']}/{total_nodes}")
    report.append("")

    # Issues
    report.append("## ISSUES FOUND")
    report.append("-" * 80)

    # Adapters not in registry
    for adapter_name, adapter_info in adapter_analysis["adapters"].items():
        if not adapter_info["registry_registered"]:
            report.append(f"❌ {adapter_name}: Not registered in registry")
        if not adapter_info["policy_integrated"]:
            report.append(f"⚠️  {adapter_name}: Not policy-integrated")
        if not adapter_info["has_fallback"]:
            report.append(f"⚠️  {adapter_name}: No fallback mechanism")
        if adapter_info["direct_imports"]:
            report.append(f"⚠️  {adapter_name}: Has direct imports: {adapter_info['direct_imports']}")

    # Nodes with direct imports
    for node_name, node_info in orchestrator_analysis["nodes"].items():
        if node_info["direct_imports"]:
            report.append(f"❌ {node_name}: Direct adapter imports (should use registry)")
        if not node_info["uses_registry"] and node_info["direct_imports"]:
            report.append(f"⚠️  {node_name}: Not using registry")

    report.append("")

    # Recommendations
    report.append("## RECOMMENDATIONS")
    report.append("-" * 80)
    report.append("1. All adapters should be registered in adapter_bootstrap.py")
    report.append("2. All adapters should read configuration from policy")
    report.append("3. All adapters should have fallback mechanisms")
    report.append("4. Nodes should use registry.get() instead of direct imports")
    report.append("5. Adapters should implement AdapterProtocol (is_available())")
    report.append("")

    return "\n".join(report)


if __name__ == "__main__":
    report = generate_report()
    print(report)

    # Save report
    report_path = PROJECT_ROOT / "docs" / "SYSTEM_HOMOGENEITY_ANALYSIS.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ Report saved to: {report_path}")


