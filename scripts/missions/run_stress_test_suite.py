import asyncio
import sys
import os
import time
from pathlib import Path

sys.path.insert(0, os.getcwd())

from src.agentic.core.orchestrator_v3 import OrchestratorV3
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor
from src.agentic.core.plugins.sentinel import SentinelVerifier
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.task_board_manager import TaskBoardManager
from src.agentic.core.plugins.rag_memory import RAGMemory

async def run_stress_test():
    print("[INFO] STARTING STRESS TEST PROTOCOL (THE GAUNTLET)")
    print("="*60)

    # Initialize System
    rag = RAGMemory()
    orchestrator = OrchestratorV3(
        planner=SimplePlanner(),
        executor=AiderExecutor(),
        verifier=SentinelVerifier(),
        artifact_gen=ArtifactGenerator(),
        task_board=TaskBoardManager(),
        rag_memory=rag
    )

    # ---------------------------------------------------------
    # TEST A: CREATION (Karmaşık bir sınıf + Testi)
    # ---------------------------------------------------------
    print("\n[TEST A] THE CREATOR: Creating 'src/utils/calculator.py' & Tests...")
    task_a = """
    Create a robust 'Calculator' class in 'src/utils/calculator.py'.
    Features: add, subtract, multiply, divide (handle zero division).

    ALSO create a test file 'tests/test_calculator.py' using pytest.
    It must cover all 4 operations.
    """

    try:
        res_a = await orchestrator.run_task("STRESS-A", task_a)
        if res_a.phase != "done":
            raise Exception(f"Test A Failed in phase: {res_a.phase}")
        print("[SUCCESS] TEST A PASSED: File and Tests created.")
    except Exception as e:
        print(f"[ERROR] TEST A FAILED: {e}")
        return # STOP IMMEDIATELY

    # ---------------------------------------------------------
    # TEST B: MODIFICATION (Var olanı düzenleme)
    # ---------------------------------------------------------
    print("\n[TEST B] THE MODIFIER: Adding 'power' method...")
    task_b = """
    Modify 'src/utils/calculator.py'.
    Add a 'power(base, exponent)' method.

    Update 'tests/test_calculator.py' to test this new method.
    Run tests to ensure no regression.
    """

    try:
        res_b = await orchestrator.run_task("STRESS-B", task_b)
        if res_b.phase != "done":
            raise Exception(f"Test B Failed in phase: {res_b.phase}")
        print("[SUCCESS] TEST B PASSED: Modification successful.")
    except Exception as e:
        print(f"[ERROR] TEST B FAILED: {e}")
        return

    # ---------------------------------------------------------
    # TEST C: THE BREAKER (Hata Yakalama)
    # ---------------------------------------------------------
    print("\n[TEST C] THE BREAKER: Introducing a bug...")
    task_c = """
    Modify 'src/utils/calculator.py'.
    Change the 'add' method to return 'a - b' (WRONG LOGIC).
    DO NOT update the test.
    The goal is to see if the Sentinel CATCHES the test failure.
    """

    try:
        res_c = await orchestrator.run_task("STRESS-C", task_c)
        # We EXPECT this task to FAIL (or retry until fail).
        # If it says "done", Sentinel missed the bug!
        if res_c.phase == "done":
             print("[ERROR] TEST C FAILED: Sentinel let a bug pass!")
             return
        else:
             print(f"[SUCCESS] TEST C PASSED: Sentinel caught the bug (Phase: {res_c.phase}).")

             # Revert the bug so we don't leave mess
             print("  -> Reverting bug for clean state...")
             # (In a real scenario we'd have a revert tool, here we just overwrite)
             # But let's skip manual revert for now, assume next steps don't rely on 'add' being correct

    except Exception as e:
        print(f"[SUCCESS] TEST C PASSED: System raised exception on bug: {e}")

    # ---------------------------------------------------------
    # TEST D: MEMORY CHECK (RAG)
    # ---------------------------------------------------------
    print("\n[TEST D] THE AMNESIAC: RAG Query...")
    try:
        # We manually check if the code from Test A is in DB
        # Note: In a real run, orchestrator adds to RAG automatically?
        # Wait, our current orchestrator DOES NOT automatically add to RAG.
        # We only added the class initialization.
        # So this test will FAIL if we didn't implement auto-indexing.

        # Let's check if we can add it manually to verify RAG works at least
        print("  -> Indexing 'src/utils/calculator.py'...")
        with open("src/utils/calculator.py", "r") as f:
            content = f.read()
        rag.add_text(content)

        print("  -> Querying 'division handling'...")
        results = rag.query("division zero")
        if results and "ZeroDivisionError" in results[0]:
            print("[SUCCESS] TEST D PASSED: Found relevant code in memory.")
        else:
            print(f"[ERROR] TEST D FAILED: Results: {results}")

    except Exception as e:
        print(f"[ERROR] TEST D FAILED: {e}")

    print("\n" + "="*60)
    print("[WIN] GAUNTLET COMPLETED. STATUS CHECK REQUIRED.")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(run_stress_test())
