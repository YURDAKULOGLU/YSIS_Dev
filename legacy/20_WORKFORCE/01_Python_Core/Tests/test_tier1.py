"""
Test script for YBIS_Dev Tier 1 MCP Server

Run this to verify server functionality before connecting to Cursor.
"""

import sys
from pathlib import Path

# Add Agentic to path
sys.path.insert(0, str(Path(__file__).parent))

from Agentic.utils import ProjectScanner, Logger
from rich.console import Console
from rich.tree import Tree
from rich.syntax import Syntax

console = Console()


def test_scanner():
    """Test ProjectScanner"""
    console.print("\n[bold blue]Testing ProjectScanner...[/bold blue]")

    scanner = ProjectScanner(str(Path(__file__).parent.parent))

    # Test 1: Get tree
    console.print("\n[yellow]Test 1: Get project tree (max_depth=2)[/yellow]")
    tree = scanner.get_tree(max_depth=2)
    console.print(tree)

    # Test 2: Get specific folder
    console.print("\n[yellow]Test 2: Get .YBIS_Dev tree[/yellow]")
    tree = scanner.get_tree(start_path=".YBIS_Dev", max_depth=2)
    console.print(tree)

    # Test 3: Read files
    console.print("\n[yellow]Test 3: Read files[/yellow]")
    results = scanner.read_files([".YBIS_Dev/README.md", "package.json"])

    for path, content in results.items():
        console.print(f"\n[green]✓ {path}[/green]")
        # Show first 10 lines
        lines = content.split('\n')[:10]
        console.print('\n'.join(lines))
        console.print(f"... ({len(content.split(chr(10)))} total lines)")

    console.print("\n[bold green]✓ ProjectScanner tests passed[/bold green]")


def test_logger():
    """Test Logger"""
    console.print("\n[bold blue]Testing Logger...[/bold blue]")

    logger = Logger(str(Path(__file__).parent / "logs"))

    # Test logging
    console.print("\n[yellow]Test: Logging messages[/yellow]")
    result = logger.log("Test message from test script", "INFO")
    console.print(f"[green]✓ {result}[/green]")

    result = logger.log("Warning test", "WARNING")
    console.print(f"[green]✓ {result}[/green]")

    # Read back
    console.print(f"\n[yellow]Log file contents:[/yellow]")
    with open(logger.session_file, 'r') as f:
        console.print(f.read())

    console.print("\n[bold green]✓ Logger tests passed[/bold green]")


def main():
    """Run all tests"""
    console.print("\n[bold cyan]YBIS_Dev Tier 1 - Component Tests[/bold cyan]")
    console.print("="*60)

    try:
        test_scanner()
        test_logger()

        console.print("\n[bold green]"+"="*60+"[/bold green]")
        console.print("[bold green]✓ All tests passed![/bold green]")
        console.print("\n[cyan]Next step: Start MCP server[/cyan]")
        console.print("[dim]Run: python .YBIS_Dev/Agentic/server.py[/dim]")

    except Exception as e:
        console.print(f"\n[bold red]✗ Test failed: {e}[/bold red]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
