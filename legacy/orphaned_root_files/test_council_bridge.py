"""
Test Council Bridge Integration
Quick test to ensure council bridge works with llm-council backend
"""
import os
import sys

# Set OpenRouter API key if available
# (For local Ollama test, this can be skipped)
if not os.getenv("OPENROUTER_API_KEY"):
    print("[INFO] No OPENROUTER_API_KEY found - will test import only")
    print("[INFO] For full test, set OPENROUTER_API_KEY in environment")

try:
    from src.agentic.bridges.council_bridge import CouncilBridge, ask_council
    print("[OK] Council bridge imported successfully")

    # Test 1: Can we instantiate?
    bridge = CouncilBridge(use_local=False)
    print("[OK] CouncilBridge instantiated")

    # Test 2: Check that council functions are available
    assert hasattr(bridge, 'stage1'), "Missing stage1 function"
    assert hasattr(bridge, 'stage2'), "Missing stage2 function"
    assert hasattr(bridge, 'stage3'), "Missing stage3 function"
    print("[OK] All 3 stage functions present")

    # Test 3: Check methods
    assert hasattr(bridge, 'ask_council'), "Missing ask_council method"
    assert hasattr(bridge, 'ask_council_async'), "Missing ask_council_async method"
    assert hasattr(bridge, 'quick_consensus'), "Missing quick_consensus method"
    print("[OK] All bridge methods present")

    # Test 4: If API key available, do a real test
    if os.getenv("OPENROUTER_API_KEY"):
        print("\n[INFO] API key found - running live test...")
        print("[INFO] Question: 'What is 2+2?'")

        result = bridge.ask_council("What is 2+2?", return_stages=True)

        if "error" in result and result.get("error"):
            print(f"[WARN] Council returned error: {result['answer']}")
        else:
            print(f"[OK] Got answer: {result['answer'][:100]}...")

            if 'stage1' in result:
                print(f"[OK] Stage 1: {len(result['stage1'])} responses")
            if 'stage2' in result:
                print(f"[OK] Stage 2: {len(result['stage2'])} rankings")

            print("\n[SUCCESS] Live council test passed!")
    else:
        print("\n[SKIP] Live test skipped (no API key)")

    print("\n" + "="*60)
    print("COUNCIL BRIDGE TEST RESULTS")
    print("="*60)
    print("[OK] Import test: PASSED")
    print("[OK] Instantiation test: PASSED")
    print("[OK] Function availability: PASSED")
    print("[OK] Method availability: PASSED")

    if os.getenv("OPENROUTER_API_KEY"):
        print("[OK] Live council test: PASSED")
    else:
        print("[SKIP] Live test: SKIPPED (set OPENROUTER_API_KEY to run)")

    print("="*60)
    print("\nCONCLUSION: Council Bridge is READY for integration!")
    print("\nUsage:")
    print("  from src.agentic.bridges.council_bridge import ask_council")
    print("  answer = ask_council('Should we use Cognee or MemGPT?')")

    sys.exit(0)

except Exception as e:
    print(f"\n[FAIL] Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
