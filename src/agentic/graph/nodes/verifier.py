from ..state import FactoryState
from src.agentic.core.plugins.sentinel import SentinelVerifier
from src.agentic.core.protocols import CodeResult
import asyncio

async def verifier_node(state: FactoryState):
    print(f"\n[VERIFIER] Checking work with Sentinel...")
    
    # Initialize Sentinel
    sentinel = SentinelVerifier()
    
    # Adapter for CodeResult (Sentinel expects this)
    # We assume Aider modified the files in the plan
    files_modified = {f: "Modified" for f in state["files"]}
    
    code_result = CodeResult(
        files_modified=files_modified,
        commands_run=[],
        outputs={},
        success=True
    )
    
    # Run Verification
    # We pass "." as sandbox path since Aider works on real repo
    result = await sentinel.verify(code_result, sandbox_path=".")
    
    new_history = []
    if result.lint_passed and result.tests_passed:
        print("✅ Sentinel Approved.")
        return {"status": "DONE", "history": ["Sentinel: Approved"]}
    else:
        print("❌ Sentinel Rejected.")
        errors = result.errors + result.warnings
        for e in errors:
            new_history.append(f"Verification Error: {e}")
            
        return {
            "status": "FAILED", 
            "retry_count": state.get("retry_count", 0) + 1,
            "history": new_history
        }

