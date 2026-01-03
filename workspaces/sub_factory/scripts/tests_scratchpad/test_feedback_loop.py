"""
Test script to verify error feedback loop works correctly
"""

import asyncio
from src.agentic.core.protocols import Plan, TaskState
from src.agentic.core.plugins.aider_executor_enhanced import AiderExecutorEnhanced
from datetime import datetime

async def test_error_feedback():
    """Test that error_history is properly injected into prompt"""

    executor = AiderExecutorEnhanced()

    # Create a sample plan
    plan = Plan(
        objective="Fix test failures",
        steps=["Fix import paths", "Run tests"],
        files_to_modify=["src/agentic/core/plugin_system/tests/test_calculator.py"],
        dependencies=[],
        risks=[],
        success_criteria=["All tests pass"],
        metadata={}
    )

    # Simulate error history
    error_history = [
        "Verification failed: ['Incorrect import path in test_calculator.py']",
        "Verification failed: ['Missing import: ToolProtocol not imported']"
    ]

    # Test 1: Build prompt with no errors (first attempt)
    print("[TEST 1] First attempt (no error history)")
    print("="*80)
    prompt_first = executor._build_enhanced_prompt(plan, error_history=None, retry_count=0)

    # Should NOT contain error feedback
    if "PREVIOUS ATTEMPT FAILED" in prompt_first:
        print("[FAIL] First attempt should not show error feedback")
        return False
    else:
        print("[PASS] First attempt correctly has no error feedback")

    print()

    # Test 2: Build prompt with errors (retry)
    print("[TEST 2] Retry attempt (with error history)")
    print("="*80)
    prompt_retry = executor._build_enhanced_prompt(plan, error_history=error_history, retry_count=1)

    # Should contain error feedback
    if "PREVIOUS ATTEMPT FAILED" not in prompt_retry:
        print("[FAIL] Retry should show error feedback")
        print("DEBUG: Prompt content:")
        print(prompt_retry[:500])
        return False

    if "Retry Attempt:" not in prompt_retry:
        print("[FAIL] Retry count not shown")
        print("DEBUG: Prompt content (first 1000 chars):")
        print(prompt_retry[:1000])
        return False

    if "Incorrect import path" not in prompt_retry:
        print("[FAIL] Error details not shown")
        return False

    print("[PASS] Retry attempt correctly shows error feedback")
    print()
    print("Error feedback section:")
    print("-"*80)
    # Extract error feedback section
    lines = prompt_retry.split('\n')
    in_error_section = False
    for line in lines:
        if "PREVIOUS ATTEMPT FAILED" in line:
            in_error_section = True
        if in_error_section:
            print(line)
            if "CRITICAL CONSTRAINTS" in line:
                break

    print()
    print("="*80)
    print("[SUCCESS] Feedback loop test passed!")
    print()
    print("Summary:")
    print("- First attempt: No error feedback (correct)")
    print("- Retry attempt: Error feedback injected (correct)")
    print("- Error details preserved in prompt (correct)")
    print()
    print("System is ready to auto-correct errors on retry!")

    return True

if __name__ == "__main__":
    asyncio.run(test_error_feedback())
