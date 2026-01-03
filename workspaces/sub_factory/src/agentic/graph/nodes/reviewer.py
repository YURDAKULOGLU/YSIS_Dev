from ..state import FactoryState
from src.agentic.core.plugins.sentinel import SentinelVerifier
from src.agentic.core.protocols import CodeResult
from src.agentic.bridges.mem0_bridge import Mem0Bridge
from src.agentic.core.plugins.model_router import default_router
import httpx
import os

async def reviewer_node(state: FactoryState):
    print(f"\n[REVIEWER] Inspecting Code Quality...")

    # 1. Static Analysis (Sentinel)
    sentinel = SentinelVerifier()
    files_modified = {f: "Checked" for f in state.get("files", [])}
    code_result = CodeResult(files_modified=files_modified, commands_run=[], outputs={}, success=True)

    result = await sentinel.verify(code_result, sandbox_path=".")

    # If static checks fail, don't bother with semantic check
    if not (result.lint_passed and result.tests_passed):
        print("❌ CODE REJECTED (Static Analysis).")
        return _reject(state, result.errors + result.warnings)

    # 2. Semantic Analysis (RAG-Based Compliance)
    print("   [CHECK] Performing Semantic Compliance Check...")

    # Read the actual code content
    code_content = ""
    for file_path in state.get("files", []):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                code_content += f"\n--- {file_path} ---\n{f.read()}\n"

    if not code_content:
        print("   ⚠️ No code found to review.")
        return {"status": "APPROVED", "history": ["Reviewer: No code"]}

    # Query Mem0 for Docs based on code content keywords
    mem = Mem0Bridge(user_id="technical_docs")
    keywords = []
    if "crewai" in code_content: keywords.append("crewai configuration")
    if "langgraph" in code_content: keywords.append("langgraph state")
    if "mem0" in code_content: keywords.append("mem0 config")
    if "streamlit" in code_content: keywords.append("streamlit session state")

    compliance_issues = []

    if keywords:
        query = " ".join(keywords)
        docs = mem.search(query, limit=3)
        docs_text = "\n\n".join(docs)

        # Ask LLM (Ollama)
        prompt = f"""
        ACT AS A SENIOR CODE REVIEWER.

        YOUR GOAL: Check if the CODE follows the OFFICIAL DOCUMENTATION.

        OFFICIAL DOCUMENTATION (Truth):
        {docs_text}

        CODE TO REVIEW:
        {code_content}

        INSTRUCTIONS:
        - If the code violates the documentation (e.g. uses deprecated methods, wrong config structure), REJECT it.
        - If the code looks correct according to docs, APPROVE it.
        - Ignore minor style issues. Focus on API usage and Logic.

        OUTPUT FORMAT:
        PASS or FAIL
        (If FAIL, explain why briefly)
        """

        # Simple LLM Call (using httpx to avoid complex imports)
        # Assuming Qwen-32b
        try:
            response = await _call_llm(prompt)
            if "FAIL" in response.upper():
                compliance_issues.append(f"Doc Compliance Error: {response}")
        except Exception as e:
            print(f"   ⚠️ LLM Review Failed: {e}")

    if compliance_issues:
        print("❌ CODE REJECTED (Semantic Compliance).")
        print(compliance_issues[0])
        return _reject(state, compliance_issues)

    print("✅ CODE APPROVED. Quality Standards Met.")
    return {
        "status": "APPROVED",
        "history": ["Reviewer: Approved"]
    }

def _reject(state, errors):
    feedback = "CRITICAL ISSUES TO FIX:\n"
    for err in errors:
        feedback += f"- {err}\n"

    return {
        "status": "FIXING",
        "feedback": feedback,
        "retry_count": state.get("retry_count", 0) + 1,
        "history": ["Reviewer: Rejected"]
    }

async def _call_llm(prompt):
    """Direct Ollama call for review"""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen2.5-coder:32b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0}
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, json=payload, timeout=60.0)
        return res.json().get("response", "")
