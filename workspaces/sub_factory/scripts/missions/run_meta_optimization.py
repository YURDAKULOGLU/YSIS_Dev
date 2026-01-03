import sys
import os
import json
import ast

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) # .YBIS_Dev/.. -> YBIS root
sys.path.append(os.path.join(project_root, ".YBIS_Dev"))

from Agentic.Crews.planning_crew import PlanningCrew
from Agentic.Crews.dev_crew import DevCrew
from Agentic.Tools.file_ops import file_ops

def main():
    print("[SYSTEM] META-OPTIMIZATION PROTOCOL V2 (PRODUCTION GRADE) INITIATED...")

    # 1. READ TARGET CODE (FAIL FAST)
    target_file = "Agentic/Core/orchestrator_hybrid.py"
    target_path = os.path.join(project_root, ".YBIS_Dev", target_file)
    print(f"   [INFO] Reading: {target_path}")

    if not os.path.exists(target_path):
        print(f"[CRITICAL] Target file not found at {target_path}")
        sys.exit(1)

    try:
        source_code = file_ops.read_file(target_path)
        if not source_code or len(source_code) < 100:
            print(f"[CRITICAL] Source code seems empty or too short.")
            sys.exit(1)
    except Exception as e:
        print(f"[CRITICAL] Failed to read target file: {e}")
        sys.exit(1)

    # 2. PLAN OPTIMIZATION (PlanningCrew)
    print("\n[PLANNING] Analyzing Code for Optimization...")
    planner = PlanningCrew()

    requirement = f"""
    Refactor and optimize the provided Python code (`orchestrator_hybrid.py`).

    CRITICAL CONSTRAINT:
    1. You MUST NOT create mock classes for libraries. Use actual `langgraph` imports.
    2. NO EMOJIS in output. Use standard logging tags [INFO], [ERROR].

    Code Content:
    ```python
    {source_code}
    ```

    Optimization Goals:
    1. Robust Error Handling: Add try-except blocks.
    2. Structured Logging: Replace print with logging module.
    3. Type Safety: Ensure correct type hints.
    4. Robust Architecture: Keep init -> planning -> execution flow.

    Output a JSON plan.
    """

    plan_result = planner.run(requirement)

    # Clean and parse JSON plan
    raw_plan = str(plan_result)
    # Basic cleanup
    if "```json" in raw_plan:
        raw_plan = raw_plan.split("```json")[1].split("```")[0].strip()
    elif "```" in raw_plan:
        raw_plan = raw_plan.split("```")[1].split("```")[0].strip()

    print(f"   [INFO] Plan Generated.")

    # 3. EXECUTE OPTIMIZATION (DevCrew)
    print("\n[EXECUTION] Writing Optimized Code...")
    dev_team = DevCrew()

    execution_context = {
        "plan": raw_plan,
        "original_code": source_code,
        "strict_instructions": """
        1. DO NOT create mock classes. Use actual `langgraph` imports.
        2. Use `logging` module.
        3. NO EMOJIS in comments or logs.
        4. Return ONLY the FULL, compilable Python code inside a single markdown code block.
        5. Do not wrap the code in JSON. Just providing the code block is enough.
        """
    }

    dev_result = dev_team.run(execution_context)

    # 4. VALIDATE & SAVE
    output_file = "Agentic/Core/orchestrator_hybrid_optimized.py"
    output_path = os.path.join(project_root, ".YBIS_Dev", output_file)
    log_path = os.path.join(project_root, ".YBIS_Dev", "meta_optimization_log.md")

    code_content = str(dev_result)

    # Save full log first
    file_ops.write_file(log_path, code_content)
    print(f"   [INFO] Full execution log saved to: {log_path}")

    # Extract code block using regex - Find ALL blocks and pick the longest one
    import re
    code_matches = re.findall(r'```python\n(.*?)```', code_content, re.DOTALL)

    if not code_matches:
        # Fallback: try finding just backticks
        code_matches = re.findall(r'```\n(.*?)```', code_content, re.DOTALL)

    if code_matches:
        # Pick the longest block (heuristic: the full code is likely longer than snippets)
        code_content = max(code_matches, key=len).strip()
    else:
        print("\n[WARNING] No code blocks found in output. Saving raw output (likely to fail syntax check).")
        # If no blocks, maybe the whole output is code? (Unlikely with CrewAI)

    # Validation: Check for mocks
    if "class LangGraph" in code_content and "import" not in code_content:
         print("\n[VALIDATION FAILED] Detected mock class generation. Aborting save.")
         sys.exit(1)

    # Validation: Check for syntax
    try:
        ast.parse(code_content)
        print("\n   [INFO] Syntax Check Passed.")
    except SyntaxError as e:
        print(f"\n[VALIDATION FAILED] Syntax Error in generated code: {e}")
        sys.exit(1)

    print(f"   [INFO] Saving optimized code to: {output_file}")
    file_ops.write_file(output_path, code_content)

    print("\n[SUCCESS] META-OPTIMIZATION COMPLETE & VERIFIED.")

if __name__ == "__main__":
    main()
