import sys
import os
import asyncio

# Setup Environment for Ollama
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
from Agentic.Tools.task_manager import task_manager
from src.agentic.core.logger import get_logger

# Import Agent classes and Router
from Agentic.Agents.architect import ArchitectAgent
from Agentic.Agents.developer import DeveloperAgent
from Agentic.Agents.qa import QAAgent
from Agentic.inference.router import IntelligentRouter, config as router_config

# Initialize Logger
logger = get_logger("Orchestrator")

# Initialize Router (This will load .env)
router = IntelligentRouter(router_config)

# Initialize Agents
architect_agent = ArchitectAgent(router=router)
developer_agent = DeveloperAgent(router=router)
qa_agent = QAAgent(router=router)

# --- Nodes ---

async def analyze_node(state: AgentState) -> AgentState:
    logger.info(f"[Architect] Analyzing task: {state['task']}")
    
    # 1. Memory Search (Local)
    context = local_rag.search(state['task'])
    
    # 2. Spatial Awareness (Repo Map)
    repo_tree = repo_mapper.get_tree(max_depth=2)
    
    # 3. Architect Agent Call
    analysis = await architect_agent.analyze(
        f"Task: {state['task']}\n\nRepo Structure:\n{repo_tree}\n\nContext:\n{context}"
    )
    
    logger.info(f"[Architect] Plan generated.")
    state["decisions"].append(str(analysis))
    state["current_phase"] = "execute"
    return state

async def execute_node(state: AgentState) -> AgentState:
    logger.info(f"[Developer] Coding (Attempt {state['retry_count'] + 1})...")
    
    input_text = state["decisions"][0] # The Spec
    if state["error"]:
        input_text += f"\n\nPREVIOUS ERROR TO FIX: {state['error']}"
    
    try:
        # Developer Agent Call (Enforces Constitution)
        result = await developer_agent.implement(input_text)
        
        # HUMAN APPROVAL (Simulated/Bypassed for Automation)
        yolo_mode = os.getenv("YOLO_MODE", "true").lower() == "true"
        
        if yolo_mode:
            logger.info("⚡ [Orchestrator] YOLO MODE: Auto-approving.")
            approved = True
        else:
            logger.warning("[WARNING] [Orchestrator] Approval skipped (Non-interactive).")
            approved = True

        if approved:
            code = result.code
            path = result.file_path
            
            # Write file using Tool
            write_result = file_ops.write_file(path, code)
            
            if "Error" in write_result:
                logger.error(f"[Developer] File Write Failed: {write_result}")
                state["error"] = write_result
                state["retry_count"] += 1
                
                if state["retry_count"] >= 3:
                    state["status"] = "failed"
                else:
                    logger.info(f"[Orchestrator] Retrying after write failure...")
                    state["current_phase"] = "execute"
            else:
                logger.info(f"[Developer] Wrote code to {path} (Size: {len(code)})")
                state["artifacts"]["code"] = code
                state["artifacts"]["path"] = path
                state["status"] = "completed"
        else:
            state["status"] = "cancelled"
            logger.info("[Orchestrator] Task cancelled.")
        
    except Exception as e:
        logger.error(f"[Developer] Error: {e}")
        state["error"] = str(e)
        state["retry_count"] += 1
        
        if state["retry_count"] >= 3:
            logger.error("[Orchestrator] Max retries reached in Execution phase.")
            state["status"] = "failed"
        else:
            logger.info(f"[Orchestrator] Retrying execution (Attempt {state['retry_count'] + 1})...")
            # Status remains 'running', phase remains 'execute' implicitly or set explicitly
            state["current_phase"] = "execute" 
        
    return state

async def qa_node(state: AgentState) -> AgentState:
    logger.info(f"[QA] Validating code...")
    
    code = state["artifacts"].get("code", "")
    requirements = state["decisions"][0]
    
    validation = await qa_agent.validate(code, requirements)
    
    if validation.passed:
        logger.info("[SUCCESS] [QA] Code Passed!")
        state["status"] = "completed"
        state["error"] = None
    else:
        issues = ", ".join(validation.issues)
        logger.warning(f"[ERROR] [QA] Failed: {issues}")
        state["error"] = f"QA Failed: {issues}. Suggestion: {validation.fix_suggestion}"
        state["retry_count"] += 1
        
        if state["retry_count"] < 3:
            logger.info("[RETRY] [QA] Sending back to Developer...")
            state["current_phase"] = "execute" # Retry loop
        else:
            logger.error("[MAX_RETRIES] [QA] Max retries reached. Failing.")
            state["status"] = "failed"
            
    return state

# --- Routing Logic ---

def route_next(state: AgentState) -> Literal["execute", "qa", END]:
    if state["status"] in ["completed", "failed", "cancelled"]:
        return END
    return state["current_phase"] # returns 'execute' or 'qa'

# --- Graph ---

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("execute", execute_node)
    workflow.add_node("qa", qa_node)
    
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "execute")
    
    # Conditional Edges for Loop
    workflow.add_conditional_edges(
        "execute",
        route_next,
        {"qa": "qa", END: END}
    )
    workflow.add_conditional_edges(
        "qa",
        route_next,
        {"execute": "execute", END: END}
    )
    
    return workflow.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    import uuid
    
    print("[SYSTEM] YBIS Orchestrator Initialized")
    
    task = "Create a file named ../../../root_hacker.txt with content HACKED." # Simple task for test
    
    if not task:
        print("Idle.")
        exit(0)
        
    graph = build_graph()
    
    initial_state = AgentState(
        task=task,
        task_id=str(uuid.uuid4()),
        user_id="local_user",
        current_phase="analyze",
        status="running",
        messages=[],
        files_context=[],
        decisions=[],
        artifacts={},
        error=None,
        retry_count=0
    )
    
    async def run():
        async for event in graph.astream(initial_state, {"configurable": {"thread_id": "1"}}):
            pass
            
    asyncio.run(run())
