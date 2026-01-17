#!/usr/bin/env python3
"""
Dependency System Usage Examples

Shows how to use the dependency graph programmatically.
"""

from pathlib import Path
from src.ybis.dependencies import DependencyGraph
from src.ybis.constants import PROJECT_ROOT


def example_scan():
    """Example: Scan project and build graph."""
    print("Example 1: Scanning project...")
    graph = DependencyGraph(PROJECT_ROOT)
    file_count = graph.scan_project()
    graph.save()
    print(f"Scanned {file_count} files")
    print(f"Graph saved to: {graph.graph_file}\n")


def example_impact():
    """Example: Analyze impact of changing a file."""
    print("Example 2: Analyzing impact...")
    graph = DependencyGraph(PROJECT_ROOT)
    if not graph.load():
        print("Graph not found. Running scan first...")
        graph.scan_project()
        graph.save()
    
    # Analyze impact of changing constants.py
    impact = graph.analyze_change("src/ybis/constants.py")
    
    print(f"Changing {impact.changed_file} affects:")
    print(f"  - {len(impact.directly_affected)} files directly")
    print(f"  - {len(impact.indirectly_affected)} files indirectly")
    
    if impact.directly_affected:
        print("\nDirectly affected files:")
        for file in impact.directly_affected[:5]:
            print(f"  - {file}")
        if len(impact.directly_affected) > 5:
            print(f"  ... and {len(impact.directly_affected) - 5} more")
    print()


def example_list():
    """Example: List dependencies for a file."""
    print("Example 3: Listing dependencies...")
    graph = DependencyGraph(PROJECT_ROOT)
    if not graph.load():
        print("Graph not found. Running scan first...")
        graph.scan_project()
        graph.save()
    
    # List dependencies for graph.py
    file_path = "src/ybis/orchestrator/graph.py"
    normalized = file_path.lstrip("./")
    
    if normalized in graph.nodes:
        node = graph.nodes[normalized]
        print(f"File: {normalized}")
        print(f"Type: {node.file_type.value}")
        print(f"Depends on: {len(node.dependencies)} files")
        print(f"Depended by: {len(node.dependents)} files")
        
        if node.dependencies:
            print("\nDependencies:")
            for dep in node.dependencies[:5]:
                print(f"  - {dep.target} ({dep.dep_type.value})")
    print()


def example_stale():
    """Example: Find stale files."""
    print("Example 4: Finding stale files...")
    graph = DependencyGraph(PROJECT_ROOT)
    if not graph.load():
        print("Graph not found. Running scan first...")
        graph.scan_project()
        graph.save()
    
    stale = graph.detect_stale_files("HEAD~10")
    
    if stale:
        print(f"Found {len(stale)} potentially stale files:")
        for file, changed_by, reason in stale[:5]:
            print(f"  - {file} (changed by {changed_by})")
    else:
        print("No stale files found.")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("YBIS Dependency System Examples")
    print("=" * 60)
    print()
    
    # Run examples
    example_scan()
    example_impact()
    example_list()
    example_stale()
    
    print("=" * 60)
    print("Examples complete!")
    print("=" * 60)

