import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Agentic.Tools.code_exec import code_exec

def test_infinite_loop_timeout():
    """Verify that infinite loops are killed after timeout."""
    print("\n🧪 TEST: Infinite Loop Timeout")

    # Python infinite loop
    bad_code = """
import time
import sys
# Flush stdout to ensure we capture "Starting loop..." before hanging
print("Starting loop...", flush=True)
while True:
    time.sleep(0.1)
"""
    result = code_exec.run_python(bad_code)

    print(f"Result: {result}")

    # Check for timeout message (defined in code_exec.py: "Error: Execution timed out")
    assert "timed out" in result
    assert "Starting loop..." in result

if __name__ == "__main__":
    test_infinite_loop_timeout()
    print("[SUCCESS] Infinite loop test passed!")
