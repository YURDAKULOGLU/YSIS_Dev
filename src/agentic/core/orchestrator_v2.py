import sys
import os
import asyncio

# Setup Environment
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434/v1"

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.agentic.core.state import AgentState
from Agentic.Tools.local_rag import local_rag
from Agentic.Tools.file_ops import file_ops
from Agentic.Tools.repo_mapper import repo_mapper
from Agentic.Tools.sandbox_manager import sandbox
from Agentic.Tools.git_ops import git_ops

# Agents
from Agentic.inference.router import IntelligentRouter, config as router_config
from Agentic.Agents.architect import ArchitectAgent
from Agentic.Agents.developer import DeveloperAgent
from Agentic.Agents.qa import QAAgent

router = IntelligentRouter(router_config)
architect_agent = ArchitectAgent(router=router)
developer_agent = DeveloperAgent(router=router)
qa_agent = QAAgent(router=router)

# --- Nodes ---

async def init_node(state: AgentState) -> AgentState:
    print("\n[SYSTEM] [System] Initializing Sandbox...")
    msg = sandbox.setup()
    print(f"   {msg}")
    
    # Load Baseline Context from AI_AGENT_PROTOCOLS.md
    print("   [SYSTEM] Loading Tier 1 Baseline Context...")
    protocol_path = os.path.join(parent_dir, "Veriler", "AI_AGENT_PROTOCOLS.md")
    if os.path.exists(protocol_path):
        with open(protocol_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Extract paths from Phase 1 table
            import re
            matches = re.findall(r"\|\s*\*\*.*?\*\*\s*\|\s*`(.*?)`", content)
            
            # Resolve relative paths
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(parent_dir))) # .YBIS_Dev/../..
            # Correction: parent_dir is .YBIS_Dev
            project_root = os.path.dirname(parent_dir)
            
            for rel_path in matches:
                full_path = os.path.join(project_root, rel_path)
                if os.path.exists(full_path):
                    state["files_context"].append(full_path)
                    print(f"   + Loaded: {rel_path}")
                else:
                    print(f"   ! Missing: {rel_path}")
    
    state["current_phase"] = "analyze"
    return state

async def analyze_node(state: AgentState) -> AgentState:
    print(f"\n[ARCHITECT] [Architect] Analyzing: {state['task']}")
    
    # Read context files
    full_context = ""
    for file_path in state["files_context"]:
        try:
            content = file_ops.read_file(file_path)
            full_context += f"\n--- FILE: {os.path.basename(file_path)} ---\n{content}\n"
        except Exception as e:
            print(f"   ! Failed to read {file_path}: {e}")

    # Add RAG context
    rag_context = local_rag.search(state['task'])
    full_context += f"\n--- RAG CONTEXT ---\n{rag_context}"
    
    repo_tree = repo_mapper.get_tree(max_depth=2)
    
    analysis = await architect_agent.analyze(
        f"Task: {state['task']}\nRepo: {repo_tree}\nContext: {full_context}"
    )
    # analysis is already unwrapped by base_agent.py

    print(f"   Plan: {analysis.technical_requirements[:2]}")
    state["decisions"].append(analysis.explanation)
    state["current_phase"] = "execute"
    return state

async def execute_node(state: AgentState) -> AgentState:
    print(f"\n[DEVELOPER] [Developer] Coding in Sandbox (Attempt {state['retry_count'] + 1})...")
    
    input_text = state["decisions"][0]
    if state["error"]:
        input_text += f"\n\nFIX ERROR: {state['error']}"
    
    try:
        result = await developer_agent.implement(input_text)
        
        # Write to SANDBOX, not real repo
        sandbox_file = sandbox.get_path(result.file_path)
        file_ops.write_file(sandbox_file, result.code)
        
        print(f"   Wrote to: {sandbox_file}")
        state["artifacts"]["code"] = result.code
        state["artifacts"]["path"] = result.file_path # Real path
        state["artifacts"]["sandbox_path"] = sandbox_file
        state["current_phase"] = "lint"
        state["error"] = None
        
    except Exception as e:
        print(f"   Error: {e}")
        state["error"] = str(e)
        state["status"] = "failed" # Fatal error
        
    return state

async def lint_node(state: AgentState) -> AgentState:
    print(f"\n[LINT] [System] Linting & Type Checking...")
    # Simulation: In real life we run 'eslint' or 'tsc' on sandbox_path
    # For now, we trust Developer's self-verification logic
    print("   Linting passed (simulated).")
    state["current_phase"] = "qa"
    return state

async def qa_node(state: AgentState) -> AgentState:
    print(f"\n[QA] [QA] Reviewing Code...")
    code = state["artifacts"].get("code", "")
    reqs = state["decisions"][0]

    try:
        validation = await qa_agent.validate(code, reqs)

        if validation.passed:
            print("   [SUCCESS] QA Passed! Auto-deploying...")
            state["current_phase"] = "commit"  # Skip approval, go straight to commit
        else:
            print(f"   [ERROR] QA Failed: {validation.issues}")
            state["error"] = f"QA Issues: {validation.issues}"
            state["retry_count"] += 1
            if state["retry_count"] < 3:
                print(f"   [RETRY] Retry {state['retry_count']}/3 - Sending back to Developer")
                state["current_phase"] = "execute"
            else:
                print("   [MAX_RETRIES] Max retries reached. Failing task.")
                state["status"] = "failed"

    except Exception as e:
        print(f"[ERROR] [QA] Validation failed: {e}")
        state["error"] = f"QA validation failed: {str(e)}"
        state["retry_count"] += 1

        if state["retry_count"] < 3:
            print(f"   [RETRY] Retry {state['retry_count']}/3 - Sending back to Developer with QA feedback")
            state["current_phase"] = "execute"
        else:
            print("   [MAX_RETRIES] Max retries reached. Failing task.")
            state["status"] = "failed"
            state["current_phase"] = "end"

    return state

async def commit_node(state: AgentState) -> AgentState:
    print(f"\n[COMMIT] [System] Committing to Real Repo...")
    
    real_path = state["artifacts"]["path"]
    code = state["artifacts"]["code"]
    
    # 1. Write to real path
    file_ops.write_file(real_path, code)
    
    # 2. Git Commit
    # branch = git_ops.create_branch(f"feature/{state['task_id'][:8]}")
    # commit = git_ops.commit_changes(f"feat: {state['task'][:50]}")
    # print(f"   Git: {commit}")
    print(f"   Saved to: {real_path}")
    
    state["status"] = "completed"
    return state

# --- Routing ---

def route_logic(state: AgentState) -> str:
    if state["status"] in ["failed", "cancelled", "completed"]:
        return END
    return state["current_phase"]

# --- Graph ---

def build_v2_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("init", init_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("execute", execute_node)
    workflow.add_node("lint", lint_node)
    workflow.add_node("qa", qa_node)
    workflow.add_node("commit", commit_node)

    workflow.set_entry_point("init")

    workflow.add_conditional_edges("init", route_logic)
    workflow.add_conditional_edges("analyze", route_logic)
    workflow.add_conditional_edges("execute", route_logic)
    workflow.add_conditional_edges("lint", route_logic)
    workflow.add_conditional_edges("qa", route_logic)
    workflow.add_conditional_edges("commit", route_logic)

    return workflow.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    import uuid
    print("[YBIS] YBIS-OS v2.0 (Production Grade) Starting...")
    
    # E2E RECURSIVE BOOTSTRAP TEST
    task = """
    Create a new agent file 'Agentic/Agents/planner.py'.
    It should contain a class 'PlannerAgent' inheriting from 'BaseAgent'.
    The 'plan' method should take a 'goal' string and return a JSON list of steps.
    Use 'Agentic/Agents/base_agent.py' as the reference for inheritance.
    Ensure it includes proper imports and error handling.
    """
    
    initial_state = AgentState(
        task=task,
        task_id=str(uuid.uuid4()),
        user_id="admin",
        current_phase="init",
        status="running",
        messages=[],
        files_context=[],
        decisions=[],
        artifacts={},
        error=None,
        retry_count=0
    )
    
    async def run():
        graph = build_v2_graph()
        async for event in graph.astream(initial_state, {"configurable": {"thread_id": "v2-1"}}):
            pass
            
    asyncio.run(run())
