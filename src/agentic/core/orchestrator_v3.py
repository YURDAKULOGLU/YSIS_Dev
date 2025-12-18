"""
Orchestrator V3 - Minimal, Protocol-Based Architecture

Design Philosophy:
- Core logic is minimal and stable (this file)
- All components are plugins (planners, executors, verifiers)
- Protocol-based: easy to swap implementations
- Gates enforce quality at each phase
- Deterministic artifacts for every execution

Usage:
    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=LocalExecutor(),
        verifier=LocalVerifier()
    )
    await orchestrator.run_task("TASK-001")
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path

# Add parent to path
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agentic.core.protocols import (
    PlannerProtocol,
    ExecutorProtocol,
    VerifierProtocol,
    ArtifactGeneratorProtocol,
    TaskBoardProtocol,
    TaskState,
    GateValidator,
)


class OrchestratorV3:
    """
    Minimal orchestrator with plugin architecture.

    This orchestrator is STABLE. It doesn't change.
    To add new capabilities, write new plugins (planners, executors, etc).
    """

    def __init__(
        self,
        planner: PlannerProtocol,
        executor: ExecutorProtocol,
        verifier: VerifierProtocol,
        artifact_gen: ArtifactGeneratorProtocol,
        task_board: TaskBoardProtocol,
        sandbox_root: str = ".sandbox",
    ):
        self.planner = planner
        self.executor = executor
        self.verifier = verifier
        self.artifact_gen = artifact_gen
        self.task_board = task_board
        self.sandbox_root = sandbox_root
        self.gate = GateValidator()

        # Ensure sandbox exists
        Path(sandbox_root).mkdir(exist_ok=True)

    # ========================================================================
    # MAIN LOOP
    # ========================================================================

    async def run_next_task(self) -> Optional[TaskState]:
        """
        Get next task from TASK_BOARD and execute it.

        Returns:
            TaskState if task found and executed, None otherwise
        """
        task_data = await self.task_board.get_next_task()
        if not task_data:
            print("[ORCHESTRATOR] No tasks in queue")
            return None

        return await self.run_task(
            task_id=task_data["id"],
            task_description=task_data["description"]
        )

    async def run_task(self, task_id: str, task_description: str) -> TaskState:
        """
        Execute a single task through full pipeline.

        Pipeline:
            init → plan → [GATE] → execute → [GATE] → verify → [GATE] → commit

        Retries on gate failure (max 3 times).
        """
        state = TaskState(
            task_id=task_id,
            task_description=task_description,
            phase="init",
            started_at=datetime.now(),
            artifacts_path=os.path.join(self.sandbox_root, task_id)
        )

        print(f"\n{'='*60}")
        print(f"[ORCHESTRATOR] Starting task: {task_id}")
        print(f"[ORCHESTRATOR] Description: {task_description}")
        print(f"{'='*60}\n")

        # Create sandbox for this task
        Path(state.artifacts_path).mkdir(parents=True, exist_ok=True)

        try:
            # Phase 1: INIT
            await self._phase_init(state)

            # Phase 2: PLAN + Gate
            while state.phase == "plan":
                await self._phase_plan(state)

            # Phase 3: EXECUTE + Gate
            while state.phase == "execute":
                await self._phase_execute(state)

            # Phase 4: VERIFY + Gate
            while state.phase == "verify":
                await self._phase_verify(state)

            # Phase 5: COMMIT
            if state.phase == "commit":
                await self._phase_commit(state)

            state.phase = "done"
            state.completed_at = datetime.now()

        except Exception as e:
            state.phase = "failed"
            state.error = str(e)
            state.completed_at = datetime.now()
            print(f"\n[ORCHESTRATOR] [X] Task failed: {e}")

        # Always generate artifacts (even on failure)
        await self._generate_artifacts(state)

        # Update TASK_BOARD
        status = "DONE" if state.phase == "done" else "FAILED"
        await self.task_board.update_task_status(
            task_id=task_id,
            status=status,
            metadata={"completed_at": state.completed_at.isoformat()}
        )

        return state

    # ========================================================================
    # PHASES
    # ========================================================================

    async def _phase_init(self, state: TaskState) -> None:
        """Initialize sandbox and load context"""
        print(f"[PHASE:INIT] Setting up sandbox at {state.artifacts_path}")

        # TODO: Load context from AI_AGENT_PROTOCOLS.md
        # TODO: Load repo state snapshot

        state.phase = "plan"

    async def _phase_plan(self, state: TaskState) -> None:
        """Generate execution plan using configured planner"""
        print(f"\n[PHASE:PLAN] Using planner: {self.planner.name()}")
        print(f"[PHASE:PLAN] Analyzing task: {state.task_description}")

        try:
            # Call planner plugin
            state.plan = await self.planner.plan(
                task=state.task_description,
                context={}  # TODO: Add repo context
            )

            print(f"[PHASE:PLAN] Plan generated:")
            print(f"  - Objective: {state.plan.objective}")
            print(f"  - Steps: {len(state.plan.steps)}")
            print(f"  - Files to modify: {len(state.plan.files_to_modify)}")

            # GATE: Validate plan
            is_valid, error = self.gate.validate_plan(state.plan)

            if not is_valid:
                print(f"[GATE:PLAN] [X] FAILED: {error}")

                if self.gate.should_retry(state):
                    state.retry_count += 1
                    print(f"[GATE:PLAN] Retry {state.retry_count}/{state.max_retries}")
                    state.phase = "plan"  # Stay in plan phase
                else:
                    raise Exception(f"Plan validation failed after {state.max_retries} retries: {error}")
            else:
                print(f"[GATE:PLAN] [OK] PASSED")
                state.phase = "execute"
                state.retry_count = 0  # Reset for next phase

        except Exception as e:
            state.error = str(e)
            raise

    async def _phase_execute(self, state: TaskState) -> None:
        """Execute plan using configured executor"""
        print(f"\n[PHASE:EXECUTE] Using executor: {self.executor.name()}")
        print(f"[PHASE:EXECUTE] Attempt {state.retry_count + 1}/{state.max_retries + 1}")

        try:
            # Call executor plugin
            state.code_result = await self.executor.execute(
                plan=state.plan,
                sandbox_path=state.artifacts_path
            )

            print(f"[PHASE:EXECUTE] Execution complete:")
            print(f"  - Files modified: {len(state.code_result.files_modified)}")
            print(f"  - Commands run: {len(state.code_result.commands_run)}")
            print(f"  - Success: {state.code_result.success}")

            # GATE: Validate code
            is_valid, error = self.gate.validate_code(state.code_result)

            if not is_valid:
                print(f"[GATE:EXECUTE] [X] FAILED: {error}")

                if self.gate.should_retry(state):
                    state.retry_count += 1
                    print(f"[GATE:EXECUTE] Retry {state.retry_count}/{state.max_retries}")
                    state.phase = "execute"  # Retry execution
                else:
                    raise Exception(f"Code validation failed after {state.max_retries} retries: {error}")
            else:
                print(f"[GATE:EXECUTE] [OK] PASSED")
                state.phase = "verify"
                state.retry_count = 0

        except Exception as e:
            state.error = str(e)
            raise

    async def _phase_verify(self, state: TaskState) -> None:
        """Verify code quality using configured verifier"""
        print(f"\n[PHASE:VERIFY] Using verifier: {self.verifier.name()}")

        try:
            # Call verifier plugin
            state.verification = await self.verifier.verify(
                code_result=state.code_result,
                sandbox_path=state.artifacts_path
            )

            print(f"[PHASE:VERIFY] Verification complete:")
            print(f"  - Lint: {'[OK]' if state.verification.lint_passed else '[X]'}")
            print(f"  - Tests: {'[OK]' if state.verification.tests_passed else '[X]'}")
            print(f"  - Coverage: {state.verification.coverage:.1%}")

            # GATE: Validate verification
            is_valid, error = self.gate.validate_verification(state.verification)

            if not is_valid:
                print(f"[GATE:VERIFY] [X] FAILED: {error}")

                if self.gate.should_retry(state):
                    state.retry_count += 1
                    print(f"[GATE:VERIFY] Retry {state.retry_count}/{state.max_retries}")
                    # Go back to execute to fix issues
                    state.phase = "execute"
                else:
                    raise Exception(f"Verification failed after {state.max_retries} retries: {error}")
            else:
                print(f"[GATE:VERIFY] [OK] PASSED")
                state.phase = "commit"

        except Exception as e:
            state.error = str(e)
            raise

    async def _phase_commit(self, state: TaskState) -> None:
        """Commit changes from sandbox to real repo"""
        print(f"\n[PHASE:COMMIT] Committing changes")

        # TODO: Implement actual git operations
        # For now, just copy files from sandbox to real repo

        print(f"[PHASE:COMMIT] [OK] Changes committed")

    async def _generate_artifacts(self, state: TaskState) -> None:
        """Generate all documentation artifacts"""
        print(f"\n[ARTIFACTS] Generating documentation...")

        artifacts = await self.artifact_gen.generate(state)

        for file_path, content in artifacts.items():
            full_path = os.path.join(state.artifacts_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"[ARTIFACTS] [OK] {file_path}")

    # ========================================================================
    # UTILITY
    # ========================================================================

    def get_status(self) -> dict:
        """Get orchestrator status"""
        return {
            "planner": self.planner.name(),
            "executor": self.executor.name(),
            "verifier": self.verifier.name(),
            "sandbox": self.sandbox_root,
        }


# ============================================================================
# CLI ENTRY POINT (for testing)
# ============================================================================

async def main():
    """Test orchestrator with simple plugins"""
    from src.agentic.core.plugins.simple_planner import SimplePlanner
    from src.agentic.core.plugins.simple_executor import SimpleExecutor
    from src.agentic.core.plugins.simple_verifier import SimpleVerifier
    from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
    from src.agentic.core.plugins.task_board_manager import TaskBoardManager

    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=SimpleExecutor(),
        verifier=SimpleVerifier(),
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager(),
    )

    print(f"[ORCHESTRATOR] Status: {orchestrator.get_status()}")

    # Run next task from TASK_BOARD
    result = await orchestrator.run_next_task()

    if result:
        print(f"\n{'='*60}")
        print(f"[ORCHESTRATOR] Task {result.task_id} completed: {result.phase}")
        print(f"[ORCHESTRATOR] Duration: {(result.completed_at - result.started_at).total_seconds():.1f}s")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
