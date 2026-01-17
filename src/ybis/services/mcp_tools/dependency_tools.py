"""
Dependency Analysis MCP Tools.

Tools for code dependency analysis.
Supports both local graph (no external deps) and Neo4j (if available).
"""

import json
import logging
from pathlib import Path

from ...constants import PROJECT_ROOT
from ...syscalls.journal import append_event

logger = logging.getLogger(__name__)

# ============================================================================
# LOCAL GRAPH TOOLS (No external dependencies)
# ============================================================================

def _get_local_graph():
    """Get local dependency graph"""
    from ...dependencies import DependencyGraph
    graph = DependencyGraph(PROJECT_ROOT)
    if not graph.load():
        graph.scan_project()
        graph.save()
    return graph


async def dependency_scan(run_path: Path | None = None, trace_id: str | None = None) -> str:
    """
    Scan project and build local dependency graph.
    No external dependencies required.

    Args:
        run_path: Optional run path for journal logging
        trace_id: Optional trace ID for journal logging

    Returns:
        JSON with scan results
    """
    from ...dependencies import DependencyGraph
    graph = DependencyGraph(PROJECT_ROOT)
    file_count = graph.scan_project()
    graph.save()

    # Journal: MCP dep check
    if run_path:
        append_event(
            run_path,
            "MCP_DEP_CHECK",
            {
                "files_scanned": file_count,
            },
            trace_id=trace_id,
        )

    type_counts = {}
    for node in graph.nodes.values():
        t = node.file_type.value
        type_counts[t] = type_counts.get(t, 0) + 1

    return json.dumps({
        "status": "success",
        "files_scanned": file_count,
        "by_type": type_counts,
        "graph_saved": str(graph.graph_file),
    }, indent=2)


async def dependency_impact(file_path: str, run_path: Path | None = None, trace_id: str | None = None) -> str:
    """
    Analyze what files are affected if this file changes.
    Uses local graph - no Neo4j needed.

    Args:
        file_path: Path to analyze
        run_path: Optional run path for journal logging
        trace_id: Optional trace ID for journal logging

    Returns:
        JSON with impact analysis
    """
    graph = _get_local_graph()
    impact = graph.analyze_change(file_path)

    # Journal: MCP dep impact
    if run_path:
        append_event(
            run_path,
            "MCP_DEP_IMPACT",
            {
                "file_path": file_path,
                "affected_count": len(impact.directly_affected) + len(impact.indirectly_affected),
            },
            trace_id=trace_id,
        )

    return json.dumps({
        "changed_file": impact.changed_file,
        "directly_affected": impact.directly_affected,
        "directly_affected_count": len(impact.directly_affected),
        "indirectly_affected": impact.indirectly_affected[:20],
        "indirectly_affected_count": len(impact.indirectly_affected),
        "critical_updates_needed": impact.critical_updates_needed,
        "suggested_actions": impact.suggested_actions,
    }, indent=2)


async def dependency_stale(since: str = "HEAD~10") -> str:
    """
    Find files that may be outdated due to recent changes.

    Args:
        since: Git ref to compare (default: HEAD~10)

    Returns:
        JSON with stale files
    """
    graph = _get_local_graph()
    stale = graph.detect_stale_files(since)

    return json.dumps({
        "stale_files": [
            {"file": s[0], "changed_by": s[1], "reason": s[2]}
            for s in stale
        ],
        "count": len(stale),
    }, indent=2)


async def dependency_list(file_path: str) -> str:
    """
    List what a file depends on and what depends on it.

    Args:
        file_path: Path to analyze

    Returns:
        JSON with dependency info
    """
    graph = _get_local_graph()
    normalized = file_path.lstrip("./")

    if normalized not in graph.nodes:
        return json.dumps({"error": f"File not in graph: {file_path}", "tip": "Run dependency_scan first"})

    node = graph.nodes[normalized]
    return json.dumps({
        "file": normalized,
        "type": node.file_type.value,
        "depends_on": [{"target": d.target, "type": d.dep_type.value, "critical": d.critical} for d in node.dependencies],
        "depended_by": node.dependents,
    }, indent=2)


# ============================================================================
# NEO4J TOOLS (Requires Neo4j running)
# ============================================================================

async def check_dependency_impact(file_path: str, max_depth: int = 3) -> str:
    """
    Check what breaks if you modify this file.

    Args:
        file_path: Path to file to analyze (e.g., 'src/config.py')
        max_depth: Maximum dependency depth to analyze (default: 3)

    Returns:
        Impact analysis report with affected files
    """
    try:
        # Try to get graph adapter from registry
        from ...adapters.registry import get_registry

        registry = get_registry()
        db = registry.get("neo4j_graph", adapter_type="graph_store")

        if db is None:
            return "[ERROR] Neo4j graph adapter not enabled. Enable it in policy: adapters.neo4j_graph.enabled: true"

        with db:
            # Get impact
            affected = db.impact_analysis(file_path, max_depth)

            if not affected:
                return f"[SAFE] No dependencies found on {file_path}\n\nThis file can be modified with minimal risk."

            # Build report
            report = f"[WARNING] {len(affected)} files will be affected if you modify {file_path}:\n\n"

            # Group by distance
            by_distance = {}
            for item in affected:
                dist = item["distance"]
                if dist not in by_distance:
                    by_distance[dist] = []
                by_distance[dist].append(item)

            for dist in sorted(by_distance.keys()):
                report += f"\nDistance {dist} (direct dependents):\n"
                for item in by_distance[dist][:10]:  # Limit to 10 per distance
                    report += f"  - {item['path']} ({item['type']})\n"

                if len(by_distance[dist]) > 10:
                    report += f"  ... and {len(by_distance[dist]) - 10} more\n"

            # Risk assessment
            if len(affected) > 20:
                report += "\n[HIGH RISK] This is a critical file with many dependents!"
            elif len(affected) > 10:
                report += "\n[MEDIUM RISK] Careful - multiple files depend on this."
            else:
                report += "\n[LOW RISK] Limited impact - proceed with caution."

            return report

    except ImportError:
        return "[ERROR] Graph database adapter not yet implemented. This feature requires Task E (Memory + Graph Adapters).\n\nInstall Neo4j:\n  docker-compose up neo4j -d\n\nThen populate the graph:\n  python scripts/ingest_graph.py"
    except Exception as e:
        error_msg = str(e)
        if "ServiceUnavailable" in str(type(e)) or "Failed to establish connection" in error_msg:
            return "[ERROR] Neo4j is not running or unreachable.\n\nStart Neo4j:\n  docker-compose up neo4j -d\n\nThen populate the graph:\n  python scripts/ingest_graph.py"
        return f"[ERROR] Failed to analyze dependencies: {error_msg}\n\nMake sure Neo4j is running and graph has been populated:\n  python scripts/ingest_graph.py"


async def find_circular_dependencies() -> str:
    """
    Find circular dependency chains in the codebase.

    Returns:
        List of circular dependency cycles
    """
    try:
        from ...adapters.registry import get_registry

        registry = get_registry()
        db = registry.get("neo4j_graph", adapter_type="graph_store")

        if db is None:
            return "[ERROR] Neo4j graph adapter not enabled. Enable it in policy: adapters.neo4j_graph.enabled: true"

        with db:
            cycles = db.find_circular_dependencies()

            if not cycles:
                return "[OK] No circular dependencies found!"

            report = f"[WARNING] Found {len(cycles)} circular dependency chains:\n\n"

            for i, cycle in enumerate(cycles[:10], 1):  # Limit to 10
                report += f"{i}. Cycle length {len(cycle)}:\n"
                for file in cycle:
                    report += f"   -> {file}\n"
                report += "\n"

            if len(cycles) > 10:
                report += f"... and {len(cycles) - 10} more cycles\n"

            report += "\n[ACTION] Break these cycles to improve code maintainability."

            return report

    except ImportError:
        return "[ERROR] Graph database adapter not yet implemented. This feature requires Task E (Memory + Graph Adapters)."
    except Exception as e:
        error_msg = str(e)
        if "ServiceUnavailable" in str(type(e)) or "Failed to establish connection" in error_msg:
            return "[ERROR] Neo4j is not running or unreachable.\n\nStart Neo4j:\n  docker-compose up neo4j -d\n\nThen populate the graph:\n  python scripts/ingest_graph.py"
        return f"[ERROR] {error_msg}"


async def get_critical_files(limit: int = 10) -> str:
    """
    Get files with the most dependents (high-risk files).

    Args:
        limit: Maximum number of files to return (default: 10)

    Returns:
        List of critical files ranked by number of dependents
    """
    try:
        from ...adapters.registry import get_registry

        registry = get_registry()
        db = registry.get("neo4j_graph", adapter_type="graph_store")

        if db is None:
            return "[ERROR] Neo4j graph adapter not enabled. Enable it in policy: adapters.neo4j_graph.enabled: true"

        with db:
            critical = db.get_critical_nodes(min_dependents=3, limit=limit)

            if not critical:
                return "[INFO] No critical nodes found (all files have < 3 dependents)"

            report = f"[CRITICAL FILES] Top {len(critical)} files with most dependents:\n\n"

            for i, node in enumerate(critical, 1):
                report += f"{i}. {node['path']}\n"
                report += f"   Type: {node['type']}\n"
                report += f"   Dependents: {node['dependents']}\n"
                report += f"   [RISK] Changing this affects {node['dependents']} other files!\n\n"

            report += "[WARNING] These files are infrastructure - changes here have wide impact."

            return report

    except ImportError:
        return "[ERROR] Graph database adapter not yet implemented. This feature requires Task E (Memory + Graph Adapters)."
    except Exception as e:
        error_msg = str(e)
        if "ServiceUnavailable" in str(type(e)) or "Failed to establish connection" in error_msg:
            return "[ERROR] Neo4j is not running or unreachable.\n\nStart Neo4j:\n  docker-compose up neo4j -d\n\nThen populate the graph:\n  python scripts/ingest_graph.py"
        return f"[ERROR] {error_msg}"

