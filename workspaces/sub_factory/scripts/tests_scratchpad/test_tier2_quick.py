"""Quick test for Tier 2 components"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("🧪 Testing Tier 2 Components...")

# Test 1: Import checks
print("\n1️⃣ Testing imports...")
try:
    from Agentic.Core.state import AgentState
    print("   [SUCCESS] AgentState")
except Exception as e:
    print(f"   [ERROR] AgentState: {e}")

try:
    from Agentic.Tools.repo_mapper import repo_mapper
    print("   [SUCCESS] repo_mapper")
except Exception as e:
    print(f"   [ERROR] repo_mapper: {e}")

try:
    from Agentic.Tools.task_manager import task_manager
    print("   [SUCCESS] task_manager")
except Exception as e:
    print(f"   [ERROR] task_manager: {e}")

try:
    from Agentic.Tools.file_ops import file_ops
    print("   [SUCCESS] file_ops")
except Exception as e:
    print(f"   [ERROR] file_ops: {e}")

# Test 2: Tool functionality
print("\n2️⃣ Testing tools...")
try:
    tree = repo_mapper.get_tree(max_depth=1)
    print(f"   [SUCCESS] repo_mapper.get_tree() - Got {len(tree)} chars")
except Exception as e:
    print(f"   [ERROR] repo_mapper: {e}")

try:
    task_manager.add_task("Test task")
    print("   [SUCCESS] task_manager.add_task()")
except Exception as e:
    print(f"   [ERROR] task_manager: {e}")

# Test 3: State creation
print("\n3️⃣ Testing state...")
try:
    state = AgentState(
        task="Test",
        task_id="test-1",
        user_id="test",
        current_phase="test",
        status="running",
        messages=[],
        files_context=[],
        decisions=[],
        artifacts={},
        error=None,
        retry_count=0
    )
    print(f"   [SUCCESS] AgentState created")
except Exception as e:
    print(f"   [ERROR] AgentState: {e}")

print("\n[SUCCESS] Basic component tests completed!")
print("\nℹ️  For full LangGraph test, need to install dependencies:")
print("   pip install -r Agentic/requirements.txt")
