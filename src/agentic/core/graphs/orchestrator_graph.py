from typing import TypedDict, Annotated, Literal, Dict, Any
import asyncio
from datetime import datetime
from langgraph.graph import StateGraph, START, END
from src.agentic.core.protocols import TaskState, PlannerProtocol, ExecutorProtocol, VerifierProtocol

class OrchestratorGraph:
    def __init__(self, planner: PlannerProtocol, executor: ExecutorProtocol, verifier: VerifierProtocol): 
        self.planner = planner
        self.executor = executor
        self.verifier = verifier
        self.workflow = self._build_graph()

    async def _planner_node(self, state: TaskState) -> Dict[str, Any]:
        # Safe print for Windows console (avoid unicode errors)
        task_id = state.get('task_id', 'UNKNOWN')
        print(f"[Graph] Planner Node: Task {task_id}")
        # Call planner
        plan = await self.planner.plan(state['task_description'], {})
        # Return update to state (LangGraph merges this)
        return {"plan": plan, "phase": "plan"}

    async def _executor_node(self, state: TaskState) -> Dict[str, Any]:
        retry_count = state.get('retry_count', 0)
        if retry_count > 0:
            print(f"[Graph] Executor Node (RETRY {retry_count}/{state['max_retries']})")
        else:
            print(f"[Graph] Executor Node")

        # Call executor with error feedback for retries
        error_history = state.get('error_history', [])
        result = await self.executor.execute(
            state['plan'],
            state['artifacts_path'],
            error_history=error_history,
            retry_count=retry_count
        )
        return {"code_result": result, "phase": "execute"}

    async def _verifier_node(self, state: TaskState) -> Dict[str, Any]:
        print(f"[Graph] Verifier Node")
        # Call verifier
        verification = await self.verifier.verify(state['code_result'], state['artifacts_path'])

        # Prepare state updates
        updates = {
            "verification": verification,
            "phase": "verify"
        }

        # If verification failed, update retry count and error history
        if not verification.lint_passed or not verification.tests_passed:
            current_retry = state.get('retry_count', 0)
            error_message = f"Verification failed: {verification.errors}"
            error_history = list(state.get('error_history', []))
            error_history.append(error_message)

            updates['retry_count'] = current_retry + 1
            updates['error_history'] = error_history

            print(f"[Graph] Verification Failed. Retrying... ({updates['retry_count']} / {state['max_retries']})")

        return updates

    def _build_graph(self):
        builder = StateGraph(TaskState)

        # Add Nodes
        builder.add_node("planner", self._planner_node)
        builder.add_node("executor", self._executor_node)
        builder.add_node("verifier", self._verifier_node)
        builder.add_node("failed", self._failed_node)

        # Add Edges
        builder.add_edge(START, "planner")
        builder.add_edge("planner", "executor")
        builder.add_edge("executor", "verifier")

        # Conditional edge from verifier (retry loop implementation)
        builder.add_conditional_edges(
            "verifier",
            self._should_retry_or_end,
            {
                "retry": "executor",
                "done": END,
                "failed": "failed"
            }
        )

        builder.add_edge("failed", END)

        return builder.compile()

    def _should_retry_or_end(self, state: TaskState) -> str:
        """Routing function: determine next step after verification."""
        verification = state.get("verification")

        # Success case
        if verification and verification.tests_passed and verification.lint_passed:
            return "done"

        # Retry budget exhausted
        if state["retry_count"] >= state["max_retries"]:
            return "failed"

        # Retry available
        return "retry"

    async def _failed_node(self, state: TaskState) -> Dict[str, Any]:
        """Handle final failure state."""
        print(f"[Graph] Failed Node: Task {state['task_id']}")
        return {
            "phase": "failed",
            "failed_at": datetime.now()
        }

    async def ainvoke(self, input_state: TaskState):
        return await self.workflow.ainvoke(input_state)
