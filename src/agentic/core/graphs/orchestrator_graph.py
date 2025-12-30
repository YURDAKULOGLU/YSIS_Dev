import os
from pathlib import Path
from typing import Any

from langgraph.graph import END, START, StateGraph

from src.agentic.core.plugins.git_manager import GitManager
from src.agentic.core.plugins.task_board_manager import TaskBoardManager
from src.agentic.core.protocols import (
    ArtifactGeneratorProtocol,
    ExecutorProtocol,
    PlannerProtocol,
    TaskState,
    VerifierProtocol,
)


class OrchestratorGraph:
    """
    Modern LangGraph implementation of the YBIS Orchestrator.
    Powered by Pydantic for robust state management and Git for cleanup.
    """

    def __init__(
        self,
        planner: PlannerProtocol,
        executor: ExecutorProtocol,
        verifier: VerifierProtocol,
        artifact_gen: ArtifactGeneratorProtocol = None,
        git_manager: GitManager = None
    ):
        self.planner = planner
        self.executor = executor
        self.verifier = verifier
        self.artifact_gen = artifact_gen
        self.git_manager = git_manager or GitManager()
        self.workflow = self._build_graph()

    # --- NODES ---

    async def _planner_node(self, s: TaskState) -> dict[str, Any]:
        print(f"\n[Graph:PLAN] Analyzing task: {s.task_id}")

        plan_obj = await self.planner.plan(s.task_description, {})
        return {"plan": plan_obj, "phase": "plan"}

    async def _executor_node(self, s: TaskState) -> dict[str, Any]:
        print(f"\n[Graph:EXECUTE] Attempt {s.retry_count + 1}/{s.max_retries + 1}")

        if not s.plan:
            print("[Graph:EXECUTE] [!] No plan found in state.")
            return {"error": "No plan available", "phase": "failed"}

        Path(s.artifacts_path).mkdir(parents=True, exist_ok=True)

        result_obj = await self.executor.execute(
            s.plan,
            s.artifacts_path,
            error_history=s.error_history,
            retry_count=s.retry_count
        )

        return {
            "code_result": result_obj,
            "phase": "execute",
            "files_modified": list(result_obj.files_modified.keys())
        }

    async def _verifier_node(self, s: TaskState) -> dict[str, Any]:
        print("\n[Graph:VERIFY] Verifying changes...")

        if not s.code_result:
            return {"error": "No code result to verify", "phase": "failed"}

        verification_obj = await self.verifier.verify(s.code_result, s.artifacts_path)

        updates: dict[str, Any] = {
            "verification": verification_obj,
            "phase": "verify"
        }

        if not verification_obj.lint_passed or not verification_obj.tests_passed:
            new_history = list(s.error_history)

            # Check if we have linting feedback for Aider
            if verification_obj.logs.get("ruff_needs_feedback"):
                feedback = f"LINTING FEEDBACK:\n{verification_obj.logs.get('ruff_feedback', '')}"
                new_history.append(feedback)
                print("[Graph:VERIFY] [!] Linting issues detected. Sending feedback to Aider for auto-correction.")
            else:
                new_history.append(f"Verification failed: {verification_obj.errors}")

            updates['retry_count'] = s.retry_count + 1
            updates['error_history'] = new_history
            print(f"[Graph:VERIFY] [X] Issues found. Retry count: {updates['retry_count']}")
        else:
            print("[Graph:VERIFY] [OK] All checks passed.")

        return updates

    async def _commit_node(self, s: TaskState) -> dict[str, Any]:
        print(f"\n[Graph:COMMIT] Committing changes for {s.task_id}...")

        commit_msg = s.plan.objective if s.plan else "Task completed by YBIS"
        success = await self.git_manager.commit_task(s.task_id, commit_msg)

        if success:
            # Optionally push (can be toggled via config)
            # await self.git_manager.push_changes()
            return {"phase": "done", "final_status": "SUCCESS"}
        else:
            return {"phase": "done", "final_status": "SUCCESS", "warnings": ["Git commit failed, but code is verified"]}

    async def _artifact_node(self, s: TaskState) -> dict[str, Any]:
        if not self.artifact_gen:
            return {}

        print("\n[Graph:ARTIFACTS] Generating documentation...")

        try:
            artifacts = await self.artifact_gen.generate(s)
            workspace_root = Path(s.artifacts_path).resolve().parent
            for file_name, content in artifacts.items():
                if os.path.isabs(file_name):
                    full_path = Path(file_name)
                else:
                    full_path = workspace_root / file_name
                full_path.parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content if isinstance(content, str) else "\n".join(content))
            print(f"[Graph:ARTIFACTS] [OK] Artifacts written under {workspace_root}")
        except Exception as e:
            print(f"[Graph:ARTIFACTS] [WARN] Failed to generate artifacts: {e}")

        return {}

    async def _failed_node(self, s: TaskState) -> dict[str, Any]:
        print("\n[Graph:FAILED] Task failed after max retries.")
        await self._artifact_node(s)
        return {"phase": "failed", "final_status": "FAILED"}

    # --- EDGES ---

    def _should_retry_or_commit(self, s: TaskState) -> str:
        if s.verification and s.verification.lint_passed and s.verification.tests_passed:
            return "commit"

        if s.retry_count >= s.max_retries:
            return "failed"

        return "retry"

    async def _chainer_node(self, s: TaskState) -> dict[str, Any]:
        if not s.proposed_tasks:
            return {}

        print(f"\n[Graph:CHAINER] Processing {len(s.proposed_tasks)} proposed tasks...")

        # We need a board manager to add tasks
        board = TaskBoardManager()
        for task in s.proposed_tasks:
            try:
                new_id = await board.create_task(task.title, task.description, task.priority)
                print(f"[Graph:CHAINER] [OK] Added follow-up task: {new_id}")
            except Exception as e:
                print(f"[Graph:CHAINER] [!] Failed to add task: {e}")

        return {"proposed_tasks": []} # Clear list after processing

    def _build_graph(self):
        # Use Pydantic TaskState directly as the state schema
        builder = StateGraph(TaskState)

        builder.add_node("planner", self._planner_node)
        builder.add_node("executor", self._executor_node)
        builder.add_node("verifier", self._verifier_node)
        builder.add_node("commit", self._commit_node)
        builder.add_node("artifacts", self._artifact_node)
        builder.add_node("chainer", self._chainer_node)
        builder.add_node("failed", self._failed_node)

        builder.add_edge(START, "planner")
        builder.add_edge("planner", "executor")
        builder.add_edge("executor", "verifier")

        builder.add_conditional_edges(
            "verifier",
            self._should_retry_or_commit,
            {
                "retry": "executor",
                "commit": "commit",
                "failed": "failed"
            }
        )

        builder.add_edge("commit", "artifacts")
        builder.add_edge("artifacts", "chainer")
        builder.add_edge("chainer", END)
        builder.add_edge("failed", END)

        return builder.compile()

    # --- PUBLIC API ---

    async def run_task(self, state: dict[str, Any]) -> TaskState:
        task_id = state.get('task_id', 'UNKNOWN')
        print(f"Graph Orchestrator Starting for {task_id}")

        # LangGraph will now automatically validate against TaskState
        final_output = await self.workflow.ainvoke(state)

        # Ensure we return a TaskState object even if ainvoke returns a dict
        if isinstance(final_output, dict):
            final_state = TaskState.model_validate(final_output)
        else:
            final_state = final_output

        if final_state.phase == 'done':
            commit_msg = final_state.plan.objective if final_state.plan else "Task completed by YBIS"
            await self.git_manager.commit_task(task_id, commit_msg)

        return final_state
