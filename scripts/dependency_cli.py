#!/usr/bin/env python3
"""
Dependency Analysis CLI - Command-line interface for dependency analysis.

Usage:
    python scripts/dependency_cli.py scan              # Scan project
    python scripts/dependency_cli.py impact <file>    # Analyze impact
    python scripts/dependency_cli.py stale [since]    # Find stale files
    python scripts/dependency_cli.py list <file>      # List dependencies
"""

import sys
import argparse
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.dependencies import DependencyGraph
from src.ybis.constants import PROJECT_ROOT


def cmd_scan():
    """Scan project and build dependency graph."""
    print("Scanning project for dependencies...")
    graph = DependencyGraph(PROJECT_ROOT)
    file_count = graph.scan_project()
    graph.save()
    
    type_counts = {}
    for node in graph.nodes.values():
        t = node.file_type.value
        type_counts[t] = type_counts.get(t, 0) + 1
    
    print(f"Scanned {file_count} files")
    print("Files by type:")
    for file_type, count in sorted(type_counts.items()):
        print(f"  {file_type}: {count}")
    print(f"\nGraph saved to: {graph.graph_file}")


def cmd_impact(file_path: str):
    """Analyze impact of changing a file."""
    graph = DependencyGraph(PROJECT_ROOT)
    if not graph.load():
        print("Graph not found. Running scan first...")
        graph.scan_project()
        graph.save()
    
    impact = graph.analyze_change(file_path)
    
    print(f"Impact analysis for: {impact.changed_file}")
    print(f"\nDirectly affected ({len(impact.directly_affected)} files):")
    for file in impact.directly_affected[:20]:
        print(f"  - {file}")
    if len(impact.directly_affected) > 20:
        print(f"  ... and {len(impact.directly_affected) - 20} more")
    
    if impact.indirectly_affected:
        print(f"\nIndirectly affected ({len(impact.indirectly_affected)} files):")
        for file in impact.indirectly_affected[:10]:
            print(f"  - {file}")
        if len(impact.indirectly_affected) > 10:
            print(f"  ... and {len(impact.indirectly_affected) - 10} more")
    
    if impact.critical_updates_needed:
        print(f"\nCritical updates needed ({len(impact.critical_updates_needed)} files):")
        for file in impact.critical_updates_needed:
            print(f"  - {file}")
    
    if impact.suggested_actions:
        print("\nSuggested actions:")
        for action in impact.suggested_actions:
            print(f"  - {action}")


def cmd_stale(since: str = "HEAD~10"):
    """Find stale files."""
    graph = DependencyGraph(PROJECT_ROOT)
    if not graph.load():
        print("Graph not found. Running scan first...")
        graph.scan_project()
        graph.save()
    
    stale = graph.detect_stale_files(since)
    
    if not stale:
        print("No stale files found.")
        return
    
    print(f"Found {len(stale)} potentially stale files (changed since {since}):")
    for file, changed_by, reason in stale:
        print(f"  - {file}")
        print(f"    Changed by: {changed_by}")
        print(f"    Reason: {reason}")
        print()


def cmd_list(file_path: str):
    """List dependencies for a file."""
    graph = DependencyGraph(PROJECT_ROOT)
    if not graph.load():
        print("Graph not found. Running scan first...")
        graph.scan_project()
        graph.save()
    
    normalized = file_path.lstrip("./")
    
    if normalized not in graph.nodes:
        print(f"ERROR: File not in graph: {file_path}")
        print("Tip: Run 'python scripts/dependency_cli.py scan' first")
        return
    
    node = graph.nodes[normalized]
    print(f"File: {normalized}")
    print(f"Type: {node.file_type.value}")
    
    if node.dependencies:
        print(f"\nDepends on ({len(node.dependencies)}):")
        for dep in node.dependencies:
            critical = " [CRITICAL]" if dep.critical else ""
            print(f"  - {dep.target} ({dep.dep_type.value}){critical}")
    else:
        print("\nDepends on: (none)")
    
    if node.dependents:
        print(f"\nDepended by ({len(node.dependents)}):")
        for dependent in node.dependents:
            print(f"  - {dependent}")
    else:
        print("\nDepended by: (none)")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="YBIS Dependency Analysis CLI")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # scan command
    subparsers.add_parser('scan', help='Scan project and build dependency graph')
    
    # impact command
    impact_parser = subparsers.add_parser('impact', help='Analyze impact of changing a file')
    impact_parser.add_argument('file', help='File path to analyze')
    
    # stale command
    stale_parser = subparsers.add_parser('stale', help='Find stale files')
    stale_parser.add_argument('since', nargs='?', default='HEAD~10', help='Git ref to compare (default: HEAD~10)')
    
    # list command
    list_parser = subparsers.add_parser('list', help='List dependencies for a file')
    list_parser.add_argument('file', help='File path to analyze')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'scan':
            cmd_scan()
        elif args.command == 'impact':
            cmd_impact(args.file)
        elif args.command == 'stale':
            cmd_stale(args.since)
        elif args.command == 'list':
            cmd_list(args.file)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

