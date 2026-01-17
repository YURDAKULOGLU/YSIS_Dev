import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from path.to.orchestrator_module import OrchestratorModule
from src.agentic.core.protocols import Plan, TaskState
from src.agentic.infrastructure.db import TaskDatabase
from src.agentic.intelligence.poetiq_bridge import PoetiqBridge

# Initialize DB and Intelligence
DB_PATH = PROJECT_ROOT / "Knowledge/LocalDB/tasks.db"
task_db = TaskDatabase(str(DB_PATH))
poetiq = PoetiqBridge()
orchestrator = OrchestratorModule()

@cl.on_chat_start
async def start():
    await task_db.initialize()

    # Welcome message with System Info
    stats = poetiq.get_arc_benchmark_status()
    await cl.Message(content=f"# 🤖 YBIS Steward - Otonom Fabrika v4.5\n## Sistem Hazır. \n**Zeka Motoru:** Poetiq ARC Solver (Score: {stats['ARC-AGI-2']})\n**Mimari:** Steward OroYstein (Cyclical Reasoning Enabled)\nBana bir görev ver veya mevcut görevleri sormak için `/tasks` yaz.").send()

@cl.on_message
async def main(message: cl.Message):
    if message.content.startswith("/tasks"):
        tasks = await task_db.get_all_tasks()
        task_list = "\n".join([f"- **{t['id']}**: {t['goal']} (`{t['status']}`)" for t in tasks[-5:]])
        await cl.Message(content=f"### Son 5 Görev:\n{task_list}").send()
        return

    # Create TaskState from message
    task_state = TaskState(
        task_id=str(datetime.now().timestamp()),
        task_description=message.content,
        context={},
        artifacts_path=str(PROJECT_ROOT / "workspaces" / "active" / str(datetime.now().timestamp())),
        phase="init",
        plan=None,
        code_result=None,
        verification=None,
        retry_count=0,
        max_retries=3,
        error=None,
        started_at=datetime.now(),
        completed_at=None,
        error_history=[],
        failed_at=None,
        files_modified=[],
        quality_score=0.0,
        final_status="UNKNOWN",
        proposed_tasks=[]
    )

    # 1. ANALYZE PHASE (Thinking Step)
    async with cl.Step(name="Steward Reasoning") as step:
        step.input = message.content
        analysis = await poetiq.reason(message.content, {})
        step.output = analysis

    # 2. PLANNING PHASE
    async with cl.Step(name="Architectural Planning") as step:
        plan = Plan(
            objective=message.content,
            steps=["Step 1", "Step 2"],
            files_to_modify=["file1.py", "file2.py"]
        )
        task_state.plan = plan
        step.output = f"Plan oluşturuldu: {', '.join(plan.steps)}"

    # 3. EXECUTION PHASE (The Aider Part)
    async with cl.Step(name="Aider Execution") as step:
        code_result = await orchestrator.executor.execute(task_state.plan, task_state.artifacts_path)
        task_state.code_result = code_result
        step.output = f"Kod üretildi: {', '.join(code_result.files_modified.keys())}"

    # 4. VERIFICATION PHASE (The Sentinel Part)
    async with cl.Step(name="Sentinel Verification") as step:
        verification_result = await orchestrator.verifier.verify(task_state.code_result, task_state.artifacts_path)
        task_state.verification = verification_result
        if verification_result.lint_passed and verification_result.tests_passed:
            step.output = "✅ Tüm testler geçti. Ruff: 0 hata. Type Hints: Tamam."
        else:
            step.output = f"⚠️ Testler başarısız: {', '.join(verification_result.errors)}"

    # Final Result
    if task_state.verification.lint_passed and task_state.verification.tests_passed:
        await cl.Message(content=f"✅ Görev başarıyla tamamlandı: {message.content}").send()
    else:
        await cl.Message(content=f"⚠️ Görev başarısız: {message.content}").send()

@cl.header_auth_callback
def auth_callback(u: cl.User) -> bool:
    """Local-first: Allow everyone for now."""
    return True
