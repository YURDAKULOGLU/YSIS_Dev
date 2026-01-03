import asyncio


def test_run_orchestrator_smoke(monkeypatch, tmp_path):
    import scripts.run_orchestrator as run_orchestrator

    updates = []

    def fake_update(task_id: str, status: str, final_status: str) -> None:
        updates.append((task_id, status, final_status))

    class FakeOrchestrator:
        def __init__(self, *args, **kwargs):
            pass

        async def run_task(self, state):
            return {"phase": "done"}

    monkeypatch.setattr(run_orchestrator, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(run_orchestrator, "USE_SPEC_FIRST", False)
    monkeypatch.setattr(run_orchestrator, "USE_REVIEW_GATE", False)
    monkeypatch.setattr(run_orchestrator, "USE_WORKTREES", False)
    monkeypatch.setattr(run_orchestrator, "USE_FRAMEWORK_DEBATE", False)
    monkeypatch.setattr(run_orchestrator, "USE_RAG", False)
    monkeypatch.setattr(run_orchestrator, "_run_closed_loop_verification", lambda *a, **k: True)
    monkeypatch.setattr(run_orchestrator, "_select_planner", lambda: object())
    monkeypatch.setattr(run_orchestrator, "OrchestratorGraph", FakeOrchestrator)
    monkeypatch.setattr(run_orchestrator, "AiderExecutorEnhanced", lambda *a, **k: object())
    monkeypatch.setattr(run_orchestrator, "SentinelVerifierEnhanced", lambda *a, **k: object())
    monkeypatch.setattr(run_orchestrator, "ArtifactGenerator", lambda *a, **k: object())
    monkeypatch.setattr(run_orchestrator.mcp_server, "update_task_status", fake_update)

    task = {"id": "TEST-002", "goal": "Smoke test", "details": "Integration"}
    status = asyncio.run(run_orchestrator._run_task(task, "codex"))

    workspace = tmp_path / "workspaces" / "active" / "TEST-002"
    assert status == "COMPLETED"
    assert (workspace / "docs" / "PLAN.md").exists()
    assert (workspace / "artifacts" / "RESULT.md").exists()
    assert updates == [("TEST-002", "COMPLETED", "SUCCESS")]
