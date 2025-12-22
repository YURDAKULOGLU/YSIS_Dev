import asyncio
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.protocols import PlannerProtocol, ExecutorProtocol, VerifierProtocol, TaskState, Plan, CodeResult, VerificationResult

class MockPlanner(PlannerProtocol):
    async def plan(self, task: str, context: dict) -> Plan:
        return Plan(
            objective="Test Objective",
            steps=["Step 1", "Step 2"],
            files_to_modify=["file1.py"],
            dependencies=[],
            risks=[],
            success_criteria=["Criteria 1"],
            metadata={}
        )

    def name(self) -> str:
        return "MockPlanner"

class MockExecutor(ExecutorProtocol):
    async def execute(self, plan: Plan, sandbox_path: str) -> CodeResult:
        return CodeResult(
            files_modified={"file1.py": "content"},
            commands_run=[],
            outputs={},
            success=True,
            error=None
        )

    def name(self) -> str:
        return "MockExecutor"

class MockVerifier(VerifierProtocol):
    async def verify(self, code_result: CodeResult, sandbox_path: str) -> VerificationResult:
        if self.fail_verification:
            return VerificationResult(
                lint_passed=False,
                tests_passed=False,
                coverage=0.5,
                errors=["Test error"],
                warnings=[],
                logs={}
            )
        else:
            return VerificationResult(
                lint_passed=True,
                tests_passed=True,
                coverage=0.8,
                errors=[],
                warnings=[],
                logs={}
            )

    def name(self) -> str:
        return "MockVerifier"

    def __init__(self, fail_verification: bool = False):
        self.fail_verification = fail_verification

@pytest.mark.asyncio
async def test_retry_logic():
    planner = MockPlanner()
    executor = MockExecutor()
    verifier = MockVerifier(fail_verification=True)

    orchestrator_graph = OrchestratorGraph(planner=planner, executor=executor, verifier=verifier)
    
    initial_state: TaskState = {
        "task_id": "1",
        "task_description": "Test task",
        "phase": "init",
        "plan": None,
        "code_result": None,
        "verification": None,
        "retry_count": 0,
        "max_retries": 2,
        "error": None,
        "started_at": datetime.now(),
        "completed_at": None,
        "artifacts_path": "/tmp",
        "error_history": [],
        "failed_at": None
    }

    final_state = await orchestrator_graph.ainvoke(initial_state)

    assert final_state['phase'] == 'failed'
    assert len(final_state['error_history']) == 2  # 2 failures before hitting max_retries
    assert final_state['retry_count'] == 2  # Reached max_retries

@pytest.mark.asyncio
async def test_successful_verification():
    planner = MockPlanner()
    executor = MockExecutor()
    verifier = MockVerifier(fail_verification=False)

    orchestrator_graph = OrchestratorGraph(planner=planner, executor=executor, verifier=verifier)
    
    initial_state: TaskState = {
        "task_id": "1",
        "task_description": "Test task",
        "phase": "init",
        "plan": None,
        "code_result": None,
        "verification": None,
        "retry_count": 0,
        "max_retries": 2,
        "error": None,
        "started_at": datetime.now(),
        "completed_at": None,
        "artifacts_path": "/tmp",
        "error_history": [],
        "failed_at": None
    }

    final_state = await orchestrator_graph.ainvoke(initial_state)
    
    assert final_state['phase'] == 'verify'
    assert len(final_state['error_history']) == 0
    assert final_state['retry_count'] == 0

# Run tests
if __name__ == "__main__":
    asyncio.run(test_retry_logic())
    asyncio.run(test_successful_verification())
