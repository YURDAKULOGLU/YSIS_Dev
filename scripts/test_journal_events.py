#!/usr/bin/env python3
"""Test journal events implementation."""

import json
import tempfile
from pathlib import Path

from src.ybis.constants import PROJECT_ROOT
from src.ybis.syscalls.journal import append_event

def test_append_event():
    """Test append_event function."""
    print("=== Testing append_event ===")
    
    # Create temporary directory
    test_path = Path(tempfile.mkdtemp())
    trace_id = "test-123"
    
    # Test 1: Basic event
    append_event(test_path, "TEST_EVENT", {"test": "value"}, trace_id=trace_id)
    print("✅ Event 1 appended")
    
    # Test 2: Event with more data
    append_event(test_path, "TEST_EVENT_2", {"key1": "value1", "key2": 42}, trace_id=trace_id)
    print("✅ Event 2 appended")
    
    # Check journal file
    journal_file = test_path / "journal" / "events.jsonl"
    if not journal_file.exists():
        print("❌ Journal file not created")
        return False
    
    # Read events
    events = []
    with journal_file.open() as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    
    print(f"✅ Journal file created: {len(events)} events")
    
    # Verify events
    if len(events) != 2:
        print(f"❌ Expected 2 events, got {len(events)}")
        return False
    
    if events[0]["event_type"] != "TEST_EVENT":
        print(f"❌ Expected TEST_EVENT, got {events[0]['event_type']}")
        return False
    
    if events[1]["event_type"] != "TEST_EVENT_2":
        print(f"❌ Expected TEST_EVENT_2, got {events[1]['event_type']}")
        return False
    
    print("✅ All events verified")
    return True

def test_imports():
    """Test that all modules can be imported."""
    print("\n=== Testing Imports ===")
    
    try:
        from src.ybis.adapters.local_coder import LocalCoderExecutor
        print("✅ LocalCoderExecutor imported")
    except Exception as e:
        print(f"❌ Failed to import LocalCoderExecutor: {e}")
        return False
    
    try:
        from src.ybis.adapters.aider import AiderExecutor
        print("✅ AiderExecutor imported")
    except Exception as e:
        print(f"❌ Failed to import AiderExecutor: {e}")
        return False
    
    try:
        from src.ybis.orchestrator.planner import LLMPlanner
        print("✅ LLMPlanner imported")
    except Exception as e:
        print(f"❌ Failed to import LLMPlanner: {e}")
        return False
    
    try:
        from src.ybis.orchestrator.verifier import run_verifier
        print("✅ run_verifier imported")
    except Exception as e:
        print(f"❌ Failed to import run_verifier: {e}")
        return False
    
    return True

def test_journal_integration():
    """Test that journal events are integrated in code."""
    print("\n=== Testing Journal Integration ===")
    
    # Check if append_event is imported in local_coder.py
    local_coder_path = PROJECT_ROOT / "src" / "ybis" / "adapters" / "local_coder.py"
    if local_coder_path.exists():
        content = local_coder_path.read_text()
        if "from ..syscalls.journal import append_event" in content:
            print("✅ local_coder.py has journal import")
        else:
            print("❌ local_coder.py missing journal import")
            return False
        
        if "append_event" in content:
            count = content.count("append_event")
            print(f"✅ local_coder.py has {count} append_event calls")
        else:
            print("❌ local_coder.py missing append_event calls")
            return False
    
    # Check aider.py
    aider_path = PROJECT_ROOT / "src" / "ybis" / "adapters" / "aider.py"
    if aider_path.exists():
        content = aider_path.read_text()
        if "from ..syscalls.journal import append_event" in content:
            print("✅ aider.py has journal import")
        else:
            print("❌ aider.py missing journal import")
            return False
    
    # Check planner.py
    planner_path = PROJECT_ROOT / "src" / "ybis" / "orchestrator" / "planner.py"
    if planner_path.exists():
        content = planner_path.read_text()
        if "from ..syscalls.journal import append_event" in content:
            print("✅ planner.py has journal import")
        else:
            print("❌ planner.py missing journal import")
            return False
    
    # Check verifier.py
    verifier_path = PROJECT_ROOT / "src" / "ybis" / "orchestrator" / "verifier.py"
    if verifier_path.exists():
        content = verifier_path.read_text()
        if "from ..syscalls.journal import append_event" in content:
            print("✅ verifier.py has journal import")
        else:
            print("❌ verifier.py missing journal import")
            return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("JOURNAL EVENTS TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Test 1: append_event function
    results.append(("append_event", test_append_event()))
    
    # Test 2: Imports
    results.append(("imports", test_imports()))
    
    # Test 3: Integration
    results.append(("integration", test_journal_integration()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60)

