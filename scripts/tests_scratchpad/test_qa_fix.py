"""
RECURSIVE DOGFOODING: Orchestrator fixes its own QA agent
"""
import asyncio
import sys
import os
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Agentic'))

async def main():
    print("=== RECURSIVE FIX: orchestrator_v2 fixes QA agent ===")
    print("-" * 60)

    from Agentic.Core.orchestrator_v2 import build_v2_graph
    from Agentic.Core.state import AgentState

    task = """Fix QA agent Pydantic validation error in Agentic/Agents/qa.py

ERROR:
pydantic_core._pydantic_core.ValidationError: 1 validation error for QAValidationResult
Invalid JSON: trailing characters at line 3 column 1

PROBLEM:
QA agent's LLM output has trailing characters after JSON, causing validation to fail.

FIX:
In qa.py, update the validate() method to:
1. Extract only the JSON part from LLM response
2. Strip any trailing text/explanations
3. Use regex to find JSON block: r'```json\\s*({.*?})\\s*```' or just find first {...}

Add this helper before validate():

```python
import re
import json

def extract_json(text: str) -> dict:
    '''Extract JSON from LLM response with markdown or trailing text'''
    # Try markdown JSON block first
    match = re.search(r'```json\\s*({.*?})\\s*```', text, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    # Try raw JSON object
    match = re.search(r'{.*}', text, re.DOTALL)
    if match:
        return json.loads(match.group(0))

    # Fallback: try parsing whole text
    return json.loads(text)
```

Then in validate() method (line ~40), before creating QAValidationResult:
```python
# Extract JSON from potentially messy LLM output
validation_dict = extract_json(str(validation_result))
validation_result = QAValidationResult(**validation_dict)
```

Files: Agentic/Agents/qa.py
"""

    print(f"\n[TASK]\n{task}\n")

    initial_state = AgentState(
        task=task,
        task_id=str(uuid.uuid4()),
        user_id="claude-recursive",
        current_phase="init",
        status="running",
        messages=[],
        files_context=[],
        decisions=[],
        artifacts={},
        error=None,
        retry_count=0
    )

    print("[START] Orchestrator fixing itself...\n")

    graph = build_v2_graph()

    try:
        async for event in graph.astream(initial_state, {"configurable": {"thread_id": "qa-fix"}}):
            for node_name, node_state in event.items():
                phase = node_state.get('current_phase', '')
                if phase:
                    print(f">>> {phase.upper()}")

                # Show errors
                if node_state.get('error'):
                    print(f"    ERROR: {node_state['error'][:100]}")

                # Show retry
                retry = node_state.get('retry_count', 0)
                if retry > 0:
                    print(f"    RETRY #{retry}")

        print("\n[SUCCESS] QA agent fixed!")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
