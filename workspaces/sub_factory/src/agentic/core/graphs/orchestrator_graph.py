import os
from pathlib import Path
from typing import Any

from langgraph.graph import END, START, StateGraph

from src.agentic.core.plugins.git_manager import GitManager
from src.agentic.core.utils.logging_utils import log_event
from src.agentic.core.plugins.plan_processor import process_plan
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
        log_event(f"Analyzing task: {s.task_id}", component="orchestrator_graph")

        # Handle both sync and async planners (CrewAI is sync, SimplePlanner is async)
        import inspect
        plan_result = self.planner.plan(s.task_description, s.context or {})
        if inspect.iscoroutine(plan_result):
            plan_obj = await plan_result
        else:
            plan_obj = plan_result

        # FIX-1: Backfill missing files and resolve glob patterns
        if plan_obj:
            if "task_id" not in plan_obj.metadata:
                plan_obj.metadata["task_id"] = s.task_id
            if not plan_obj.files_to_modify:
                related_files = (s.context or {}).get("related_files", [])
                if related_files:
                    plan_obj.files_to_modify = list(related_files)
                    log_event(f"Backfilled files_to_modify from context: {len(plan_obj.files_to_modify)}", component="orchestrator_graph")

            # If task targets src/agentic/core, prefix bare filenames into that folder
            if plan_obj.files_to_modify and "src/agentic/core" in s.task_description:
                normalized = []
                for path in plan_obj.files_to_modify:
                    if "/" not in path and "\\" not in path:
                        normalized.append(f"src/agentic/core/{path}")
                    else:
                        normalized.append(path)
                plan_obj.files_to_modify = normalized

            if plan_obj.files_to_modify:
                plan_obj = process_plan(plan_obj)
                log_event(f"Files to modify: {len(plan_obj.files_to_modify)}", component="orchestrator_graph")

        return {"plan": plan_obj, "phase": "plan"}

    async def _executor_node(self, s: TaskState) -> dict[str, Any]:
        log_event(f"Execute attempt {s.retry_count + 1}/{s.max_retries + 1}", component="orchestrator_graph")

        if not s.plan:
            log_event("[!] No plan found in state.", component="orchestrator_graph", level="warning")
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
        log_event("Verifying changes...", component="orchestrator_graph")

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
                log_event("[!] Linting issues detected. Sending feedback to Aider for auto-correction.", component="orchestrator_graph", level="warning")
            else:
                new_history.append(f"Verification failed: {verification_obj.errors}")

            updates['retry_count'] = s.retry_count + 1
            updates['error_history'] = new_history
            log_event(f"[X] Issues found. Retry count: {updates['retry_count']}", component="orchestrator_graph", level="warning")
        else:
            log_event("[OK] All checks passed.", component="orchestrator_graph")

        return updates

    async def _commit_node(self, s: TaskState) -> dict[str, Any]:
        log_event(f"Committing changes for {s.task_id}...", component="orchestrator_graph")

        commit_msg = s.plan.objective if s.plan else "Task completed by YBIS"
        success = await self.git_manager.commit_task(
            s.task_id,
            commit_msg,
            allowed_files=s.files_modified
        )

        if success:
            # POST-COMMIT MEMORY TRIGGER (Constitution Section 4.2)
            # Delta-ingest modified files into RAG to keep Knowledge Base fresh
            try:
                from src.agentic.tools.local_rag import get_local_rag
                rag = get_local_rag()
                if rag.is_available() and s.files_modified:
                    ingested = 0
                    for file_path in s.files_modified:
                        if rag.add_code_file(file_path):
                            ingested += 1
                    if ingested > 0:
                        log_event(f"Delta-ingested {ingested} files into Knowledge Base", component="orchestrator_graph")
            except Exception as e:
                log_event(f"Delta-ingestion warning: {e}", component="orchestrator_graph", level="warning")

            # Optionally push (can be toggled via config)
            # await self.git_manager.push_changes()
            return {"phase": "done", "final_status": "SUCCESS"}
        else:
            return {"phase": "failed", "final_status": "FAILED", "warnings": ["Git commit failed; task blocked by commit gate"]}

    async def _artifact_node(self, s: TaskState) -> dict[str, Any]:
        if not self.artifact_gen:
            return {}

        log_event("Generating documentation...", component="orchestrator_graph")

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
            log_event(f"[OK] Artifacts written under {workspace_root}", component="orchestrator_graph")
        except Exception as e:
            log_event(f"[WARN] Failed to generate artifacts: {e}", component="orchestrator_graph", level="warning")

        return {}

    async def _failed_node(self, s: TaskState) -> dict[str, Any]:
        log_event("Task failed after max retries.", component="orchestrator_graph", level="warning")
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

        log_event(f"Processing {len(s.proposed_tasks)} proposed tasks...", component="orchestrator_graph")

        # We need a board manager to add tasks
        board = TaskBoardManager()
        for task in s.proposed_tasks:
            try:
                new_id = await board.create_task(task.title, task.description, task.priority)
                log_event(f"[OK] Added follow-up task: {new_id}", component="orchestrator_graph")
            except Exception as e:
                log_event(f"[!] Failed to add task: {e}", component="orchestrator_graph", level="warning")

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
        log_event(f"Graph Orchestrator Starting for {task_id}", component="orchestrator_graph")

        # LangGraph will now automatically validate against TaskState
        final_output = await self.workflow.ainvoke(state)

        # Ensure we return a TaskState object even if ainvoke returns a dict
        if isinstance(final_output, dict):
            final_state = TaskState.model_validate(final_output)
        else:
            final_state = final_output

        return final_state
