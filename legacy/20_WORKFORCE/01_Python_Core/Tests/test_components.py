"""
Component tests for YBIS_Dev Tier 2
Tests basic functionality without requiring LangGraph
"""
import sys
from pathlib import Path

# Add parent directories to path
test_dir = Path(__file__).parent
agentic_dir = test_dir.parent
ybis_dev_dir = agentic_dir.parent

sys.path.insert(0, str(ybis_dev_dir))
sys.path.insert(0, str(agentic_dir))

def test_imports():
    """Test that all modules can be imported"""
    print("\n[1] Testing imports...")

    try:
        from Agentic.Tools.repo_mapper import repo_mapper
        print("  OK: repo_mapper")
        return True
    except Exception as e:
        print(f"  FAIL: repo_mapper - {e}")
        return False

def test_repo_mapper():
    """Test repo mapper functionality"""
    print("\n[2] Testing repo_mapper...")

    try:
        from Agentic.Tools.repo_mapper import repo_mapper
        tree = repo_mapper.get_tree(max_depth=1)
        print(f"  OK: Got tree ({len(tree)} chars)")
        # Skip printing tree sample due to Windows emoji encoding
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False

def test_task_manager():
    """Test task manager"""
    print("\n[3] Testing task_manager...")

    try:
        from Agentic.Tools.task_manager import task_manager

        # Add a test task
        task_id = task_manager.add_task("Test task from component test")
        print(f"  OK: Added task {task_id}")

        # Try to pick it
        next_task = task_manager.pick_next_task()
        print(f"  OK: Picked task: {next_task}")

        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False

def test_file_ops():
    """Test file operations"""
    print("\n[4] Testing file_ops...")

    try:
        from Agentic.Tools.file_ops import file_ops

        # Test read (this file)
        content = file_ops.read_file(__file__)
        print(f"  OK: Read this file ({len(content)} chars)")

        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False

def test_state():
    """Test AgentState (requires langgraph)"""
    print("\n[5] Testing AgentState...")

    try:
        from Agentic.Core.state import AgentState

        state = AgentState(
            task="Test task",
            task_id="test-123",
            user_id="test-user",
            current_phase="test",
            status="running",
            messages=[],
            files_context=[],
            decisions=[],
            artifacts={},
            error=None,
            retry_count=0
        )

        print(f"  OK: Created state for task: {state['task']}")
        return True
    except ImportError as e:
        print(f"  SKIP: langgraph not installed ({e})")
        return None  # None = skipped
    except Exception as e:
        print(f"  FAIL: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("YBIS_Dev Tier 2 - Component Tests")
    print("=" * 60)

    results = {
        "imports": test_imports(),
        "repo_mapper": test_repo_mapper(),
        "task_manager": test_task_manager(),
        "file_ops": test_file_ops(),
        "state": test_state(),
    }

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)

    for name, result in results.items():
        status = "PASS" if result is True else ("SKIP" if result is None else "FAIL")
        print(f"  {name:20s} [{status}]")

    print(f"\nPassed: {passed}/{len(results)}")
    if skipped > 0:
        print(f"Skipped: {skipped} (install dependencies with: pip install -r ../requirements.txt)")

    print("\n" + "=" * 60)

    if failed == 0:
        print("All tests passed!")
        return 0
    else:
        print(f"{failed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
