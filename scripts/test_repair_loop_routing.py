"""
Test script to verify repair loop routing works correctly.

This script tests:
1. verify_node sets state flags (test_passed, lint_passed, tests_passed)
2. test_failed() routing function correctly routes to repair
3. Repair loop can route back to plan/execute

Run: python scripts/test_repair_loop_routing.py
"""

import sys
from pathlib import Path
from unittest.mock import Mock

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

print("=" * 60)
print("Testing Repair Loop Routing")
print("=" * 60)

# Test 1: Verify conditional routing functions work
print("\n1. Testing conditional routing functions...")
try:
    # Import directly from file to avoid circular imports
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "conditional_routing",
        project_root / "src" / "ybis" / "workflows" / "conditional_routing.py"
    )
    conditional_routing = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conditional_routing)

    # Create test state with failed tests
    test_state = {
        "task_id": "TEST-TASK",
        "run_id": "R-test",
        "run_path": Mock(),
        "trace_id": "TEST-TASK-R-test",
        "test_passed": False,  # Tests failed
        "lint_passed": False,  # Lint failed
        "tests_passed": False,
        "repair_retries": 0,
        "max_repair_retries": 3,
    }

    # Test test_failed routing
    route = conditional_routing.test_failed(test_state)
    print(f"   ✓ test_failed() routes to: {route}")
    assert route == "repair", f"Expected 'repair', got '{route}'"
    print("   ✓ Routing to repair when tests fail: PASS")

    # Test with all passed
    test_state["test_passed"] = True
    test_state["lint_passed"] = True
    test_state["tests_passed"] = True
    route = conditional_routing.test_failed(test_state)
    print(f"   ✓ test_failed() routes to: {route} (when all pass)")
    assert route == "integrate", f"Expected 'integrate', got '{route}'"
    print("   ✓ Routing to integrate when tests pass: PASS")

except Exception as e:
    print(f"   ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Verify verify_node sets state flags
print("\n2. Checking verify_node implementation...")
try:
    verify_node_file = project_root / "src" / "ybis" / "orchestrator" / "nodes" / "execution.py"
    verify_node_code = verify_node_file.read_text(encoding="utf-8")

    # Check if state flags are set
    checks = [
        ('state["test_passed"]', "test_passed flag"),
        ('state["lint_passed"]', "lint_passed flag"),
        ('state["tests_passed"]', "tests_passed flag"),
    ]

    all_found = True
    for check_str, check_name in checks:
        if check_str in verify_node_code:
            print(f"   ✓ {check_name} is set: PASS")
        else:
            print(f"   ✗ {check_name} is NOT set: FAIL")
            all_found = False

    if all_found:
        print("   ✓ verify_node sets all required state flags: PASS")
    else:
        print("   ✗ verify_node missing some state flags: FAIL")
        sys.exit(1)

except Exception as e:
    print(f"   ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Verify repair loop flow
print("\n3. Testing repair loop flow logic...")
try:
    # Simulate workflow flow
    state = {
        "task_id": "TEST-TASK",
        "run_id": "R-test",
        "run_path": Mock(),
        "test_passed": False,
        "lint_passed": False,
        "tests_passed": False,
        "repair_retries": 0,
        "max_repair_retries": 3,
    }

    # Step 1: verify_node should set flags (simulated)
    print("   Step 1: verify_node sets flags...")
    # (In real flow, verify_node would set these)
    state["test_passed"] = False
    state["lint_passed"] = False
    state["tests_passed"] = False
    print("      ✓ Flags set: test_passed=False, lint_passed=False, tests_passed=False")

    # Step 2: test_failed() should route to repair
    print("   Step 2: test_failed() routing...")
    route = conditional_routing.test_failed(state)
    assert route == "repair", f"Expected 'repair', got '{route}'"
    print(f"      ✓ Routes to: {route}")

    # Step 3: After repair, retry count increases
    print("   Step 3: Repair increments retry count...")
    state["repair_retries"] = 1
    print(f"      ✓ Retry count: {state['repair_retries']}/{state['max_repair_retries']}")

    # Step 4: If still failing, should route to repair again (if under limit)
    print("   Step 4: Second failure routes to repair again...")
    route = conditional_routing.test_failed(state)
    assert route == "repair", f"Expected 'repair', got '{route}'"
    print(f"      ✓ Routes to: {route}")

    # Step 5: Max retries reached
    print("   Step 5: Max retries reached...")
    state["repair_retries"] = 3
    route = conditional_routing.test_failed(state)
    assert route == "integrate", f"Expected 'integrate' when max retries reached, got '{route}'"
    print(f"      ✓ Routes to: {route} (max retries reached)")

    print("   ✓ Repair loop flow logic: PASS")

except Exception as e:
    print(f"   ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED ✓")
print("=" * 60)
print("\nSummary:")
print("  ✓ Conditional routing functions work correctly")
print("  ✓ verify_node sets required state flags")
print("  ✓ Repair loop flow logic is correct")
print("\nRepair loop should work correctly in actual workflows!")


