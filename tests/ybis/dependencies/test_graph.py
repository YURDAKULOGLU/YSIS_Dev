"""
Tests for dependency graph system.
"""

import pytest
from pathlib import Path
from src.ybis.dependencies import DependencyGraph
from src.ybis.dependencies.schema import extract_python_imports, FileType
from src.ybis.constants import PROJECT_ROOT


def test_scan_project_finds_files():
    """Test that scan_project finds files."""
    graph = DependencyGraph(PROJECT_ROOT)
    file_count = graph.scan_project()
    
    assert file_count > 0
    assert len(graph.nodes) > 0
    
    # Check that some expected files are found
    found_python = False
    found_markdown = False
    for node in graph.nodes.values():
        if node.file_type == FileType.CODE_PYTHON:
            found_python = True
        if node.file_type == FileType.DOC_MARKDOWN:
            found_markdown = True
    
    assert found_python, "Should find Python files"
    assert found_markdown, "Should find Markdown files"


def test_analyze_change_finds_dependents():
    """Test that analyze_change finds dependents."""
    graph = DependencyGraph(PROJECT_ROOT)
    graph.scan_project()
    
    # Analyze a file that likely has dependents
    impact = graph.analyze_change("src/ybis/constants.py")
    
    assert impact.changed_file == "src/ybis/constants.py"
    assert isinstance(impact.directly_affected, list)
    assert isinstance(impact.indirectly_affected, list)
    assert isinstance(impact.critical_updates_needed, list)
    assert isinstance(impact.suggested_actions, list)


def test_path_normalization():
    """Test that path normalization works correctly."""
    # Test relative import resolution
    test_file = PROJECT_ROOT / "src" / "ybis" / "orchestrator" / "graph.py"
    
    # Test relative import: from ..contracts import X
    content = "from ..contracts import RunContext"
    deps = extract_python_imports(content, str(test_file))
    
    assert len(deps) > 0
    # Should resolve to src/ybis/contracts.py (not //contracts.py)
    dep = deps[0]
    assert not dep.target.startswith("//"), "Should not have double slashes"
    assert "contracts" in dep.target.lower(), "Should resolve to contracts module"
    
    # Test absolute import: from src.ybis.constants import X
    content2 = "from src.ybis.constants import PROJECT_ROOT"
    deps2 = extract_python_imports(content2, str(test_file))
    
    assert len(deps2) > 0
    dep2 = deps2[0]
    assert "constants" in dep2.target.lower(), "Should resolve to constants module"
    assert not dep2.target.startswith("//"), "Should not have double slashes"


def test_graph_save_load():
    """Test that graph can be saved and loaded."""
    graph = DependencyGraph(PROJECT_ROOT)
    graph.scan_project()
    
    # Save
    graph.save()
    assert graph.graph_file.exists()
    
    # Load into new graph
    graph2 = DependencyGraph(PROJECT_ROOT)
    loaded = graph2.load()
    
    assert loaded, "Should load successfully"
    assert len(graph2.nodes) > 0, "Should have nodes after load"
    assert len(graph2.nodes) == len(graph.nodes), "Should have same number of nodes"


def test_detect_stale_files():
    """Test that detect_stale_files works."""
    graph = DependencyGraph(PROJECT_ROOT)
    graph.scan_project()
    
    stale = graph.detect_stale_files("HEAD~10")
    
    assert isinstance(stale, list)
    # Each item should be a tuple of (file, changed_by, reason)
    if stale:
        assert len(stale[0]) == 3, "Stale items should be tuples of (file, changed_by, reason)"

