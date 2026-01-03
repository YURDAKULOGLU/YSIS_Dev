from ..state import FactoryState
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.model_router import default_router
# Need dummy Plan object for compatibility with old AiderExecutor
from src.agentic.core.protocols import Plan
import asyncio

async def executor_node(state: FactoryState):
    print(f"\n[EXECUTOR] Coding... (Attempt {state.get('retry_count', 0)})")

    # Bridge to existing AiderExecutor
    executor = AiderExecutor(router=default_router)

    # Create Plan object adapter
    plan_obj = Plan(
        objective=state["goal"],
        steps=[state["plan"]],
        files_to_modify=state["files"],
        dependencies=[], risks=[], success_criteria=[], metadata={}
    )

    # Construct Error History + Explicit Feedback
    errors = [h for h in state["history"] if "Error" in h]

    if state.get("feedback"):
        errors.append(f"REVIEWER FEEDBACK: {state['feedback']}")

    # Inject Memory Context if available
    if state.get("memory_context"):
        mem_text = "\n".join(state["memory_context"])
        errors.append(f"RELEVANT MEMORY:\n{mem_text}")

    result = await executor.execute(
        plan=plan_obj,
        sandbox_path=".", # Working on real repo
        error_history=errors
    )

    status = "VERIFYING" # Handover to Reviewer
    new_history = [f"Executed: {result.success}"]
    if not result.success:
        new_history.append(f"Error: {result.error}")

    return {
        "history": new_history,
        "status": status
    }
