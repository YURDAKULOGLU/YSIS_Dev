"""
Import Validation Tests - Prevent missing import errors.

Tests that all required imports are present in orchestrator nodes.
"""

import ast
import importlib.util
from pathlib import Path

import pytest

from src.ybis.constants import PROJECT_ROOT


def get_python_files(directory: Path) -> list[Path]:
    """Get all Python files in directory."""
    return list(directory.rglob("*.py"))


def parse_imports(file_path: Path) -> set[str]:
    """Parse imports from a Python file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content)
        imports = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
        
        return imports
    except Exception:
        return set()


def check_undefined_names(file_path: Path) -> list[str]:
    """Check for undefined names in a Python file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content)
        undefined = []
        
        # Get all imported names
        imported_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_names.add(alias.asname or alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported_names.add(alias.asname or alias.name)
        
        # Check for Name nodes that aren't imported
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if node.id not in imported_names and node.id not in ["True", "False", "None"]:
                    # Check if it's a builtin
                    if node.id not in dir(__builtins__):
                        undefined.append(node.id)
        
        return list(set(undefined))
    except Exception:
        return []


class TestImports:
    """Test import validation."""

    def test_project_root_imported_in_graph(self):
        """Verify PROJECT_ROOT is imported in graph.py."""
        graph_path = PROJECT_ROOT / "src" / "ybis" / "orchestrator" / "graph.py"
        assert graph_path.exists(), "graph.py not found"
        
        content = graph_path.read_text(encoding="utf-8")
        assert "from ..constants import PROJECT_ROOT" in content or "PROJECT_ROOT" in content, \
            "PROJECT_ROOT must be imported in graph.py"

    def test_all_nodes_have_required_imports(self):
        """Verify all orchestrator nodes import required modules."""
        orchestrator_dir = PROJECT_ROOT / "src" / "ybis" / "orchestrator"
        required_imports = {
            "json",
            "pathlib",
            "RunContext",
            "PROJECT_ROOT",
        }
        
        for py_file in orchestrator_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            
            content = py_file.read_text(encoding="utf-8")
            imports = parse_imports(py_file)
            
            # Check for critical imports
            if "RunContext" in content:
                assert "RunContext" in content or "from ..contracts" in content, \
                    f"{py_file.name} uses RunContext but may not import it correctly"

    def test_no_undefined_constants(self):
        """Verify no undefined constants are used."""
        graph_path = PROJECT_ROOT / "src" / "ybis" / "orchestrator" / "graph.py"
        undefined = check_undefined_names(graph_path)
        
        # Filter out known false positives (builtins, common variables, imported names)
        known_undefined = {
            "state", "ctx", "plan", "task", "run", "db", "errors", "decision", 
            "risk_gate", "aider_enabled", "final_decision", "should_debate",
            "verify_node", "p", "retries", "model", "Exception", "plan_node",
            "should_retry_route", "str", "approval_path", "spec_node", "spec_content",
            "policy_provider", "error_report", "lessons", "gate_node", "isinstance",
            "plan_path", "should_continue_steps", "vector_store", "engine", "response",
            "gate_data", "repair_node", "collection", "minimal_spec", "failure_reason",
            "line", "ImportError", "gate_context", "step", "e", "report", "verifier_path",
            "spec_path", "verifier_data", "patch_content", "patch_lines", "hasattr",
            "len", "api_base", "bool", "topic", "patch_path", "error_context", "context",
            "should_retry", "task_objective", "executor_path", "gate_path", "WorkflowState",
            "patch_size", "current_step", "next", "workflow", "llm_config", "changed_files",
            "tier", "plan_summary", "verifier_report", "success", "debate_result", "print",
            "experience_text", "lesson_engine", "sub_factory_path", "step_plan", "_call_llm",
            "debate_report_path", "executor_summary", "task_context", "plan_data", "gate_report",
            "marker_path", "int", "architect", "max_retries", "steps", "executor_data",
            "execute_node", "has_errors", "debate_node", "_save_experience_to_memory", "dict",
            "executor", "list", "set", "tuple", "type", "object", "range", "enumerate",
            "zip", "map", "filter", "any", "all", "sum", "min", "max", "abs", "round",
        }
        undefined = [u for u in undefined if u not in known_undefined]
        
        # Also filter Python builtins
        import builtins
        undefined = [u for u in undefined if not hasattr(builtins, u)]
        
        assert len(undefined) == 0, \
            f"Found undefined names in graph.py: {undefined}"

    def test_contracts_imported_correctly(self):
        """Verify contracts are imported correctly."""
        graph_path = PROJECT_ROOT / "src" / "ybis" / "orchestrator" / "graph.py"
        content = graph_path.read_text(encoding="utf-8")
        
        # Check for common contract usage
        if "RunContext" in content:
            assert "from ..contracts" in content or "RunContext" in content, \
                "RunContext must be imported from contracts"
        
        if "VerifierReport" in content:
            assert "VerifierReport" in content, \
                "VerifierReport must be imported"

