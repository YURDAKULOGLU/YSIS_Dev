"""
Simple test to verify repair loop routing logic.

Checks code directly without imports.
"""

from pathlib import Path

project_root = Path(__file__).parent.parent

print("=" * 60)
print("Repair Loop Routing Test")
print("=" * 60)

# Test 1: Check verify_node sets state flags
print("\n1. Checking verify_node sets state flags...")
verify_node_file = project_root / "src" / "ybis" / "orchestrator" / "nodes" / "execution.py"
verify_node_code = verify_node_file.read_text(encoding="utf-8")

checks = {
    'state["test_passed"]': "test_passed flag",
    'state["lint_passed"]': "lint_passed flag",
    'state["tests_passed"]': "tests_passed flag",
}

all_ok = True
for check_str, check_name in checks.items():
    if check_str in verify_node_code:
        print(f"   [OK] {check_name} is set")
    else:
        print(f"   [FAIL] {check_name} is NOT set")
        all_ok = False

if all_ok:
    print("   [PASS] verify_node sets all required state flags")
else:
    print("   [FAIL] verify_node missing some state flags")
    exit(1)

# Test 2: Check conditional routing functions exist
print("\n2. Checking conditional routing functions...")
routing_file = project_root / "src" / "ybis" / "workflows" / "conditional_routing.py"
routing_code = routing_file.read_text(encoding="utf-8")

routing_checks = {
    'def test_failed(': "test_failed function",
    'def test_passed(': "test_passed function",
    'return "repair"': "routes to repair",
    'return "integrate"': "routes to integrate",
}

all_ok = True
for check_str, check_name in routing_checks.items():
    if check_str in routing_code:
        print(f"   [OK] {check_name} exists")
    else:
        print(f"   [FAIL] {check_name} NOT found")
        all_ok = False

if all_ok:
    print("   [PASS] Conditional routing functions exist")
else:
    print("   [FAIL] Some routing functions missing")
    exit(1)

# Test 3: Check test_failed logic
print("\n3. Checking test_failed routing logic...")
logic_checks = {
    'state.get("test_passed"': "checks test_passed flag",
    'state.get("lint_passed"': "checks lint_passed flag",
    'state.get("tests_passed"': "checks tests_passed flag",
    'repair_retries': "checks repair retry count",
    'max_repair_retries': "checks max retry limit",
}

all_ok = True
for check_str, check_name in logic_checks.items():
    if check_str in routing_code:
        print(f"   [OK] {check_name}")
    else:
        print(f"   [FAIL] {check_name} NOT found")
        all_ok = False

if all_ok:
    print("   [PASS] test_failed routing logic is complete")
else:
    print("   [FAIL] Some routing logic missing")
    exit(1)

print("\n" + "=" * 60)
print("ALL CHECKS PASSED")
print("=" * 60)
print("\nSummary:")
print("  [OK] verify_node sets state flags (test_passed, lint_passed, tests_passed)")
print("  [OK] Conditional routing functions exist (test_failed, test_passed)")
print("  [OK] Routing logic checks all required flags and retry limits")
print("\nRepair loop should work correctly!")
print("\nTo test in real workflow:")
print("  1. Run a task that will fail tests")
print("  2. Check that verify_node sets state flags")
print("  3. Check that test_failed() routes to repair node")
print("  4. Check that repair node increments retry count")
print("  5. Check that after max retries, routes to integrate")


