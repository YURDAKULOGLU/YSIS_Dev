import sys
import os
import json
import logging
from typing import TypedDict, Annotated, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("HybridOrchestrator")

# Add project root to path
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir))) # .YBIS_Dev/../..
    sys.path.append(os.path.join(project_root, ".YBIS_Dev"))
except Exception as e:
    logger.error(f"Failed to setup python path: {e}")
    sys.exit(1)

# Import Crews
try:
    from Agentic.Crews.planning_crew import PlanningCrew
    from Agentic.Crews.dev_crew import DevCrew
    from Agentic.Tools.sandbox_manager import sandbox
    from Agentic.Tools.file_ops import file_ops
except ImportError as e:
    logger.critical(f"Failed to import required modules: {e}")
    sys.exit(1)

# --- State Definition ---
class HybridState(TypedDict):
    task: str
    plan: Dict[str, Any]
    code_files: List[str]
    status: str
    error: Optional[str]

# --- Nodes ---

def init_node(state: HybridState) -> HybridState:
    logger.info("Initializing System...")
    
    try:
        # 1. Sandbox Check
        msg = sandbox.setup()
        logger.info(f"Sandbox Setup: {msg}")
        
        # 2. RAG/Protocol Check
        logger.info("Protocols: Loaded AI_AGENT_PROTOCOLS.md (Simulated)")
        
    except Exception as e:
        logger.error(f"Initialization Failed: {e}")
        state['error'] = str(e)
        state['status'] = "failed"
        
    return state

def planning_node(state: HybridState) -> HybridState:
    if state.get('status') == "failed":
        return state

    logger.info(f"PLANNING CREW: Analyzing Task: {state['task']}")
    
    try:
        planner = PlanningCrew()
        result = planner.run(state['task'])
        
        # Parse JSON from Crew Output
        raw_output = str(result)
        clean_json = raw_output.replace("```json", "").replace("```", "").strip()
        
        # Handle potential text before/after JSON
        start = clean_json.find('{')
        end = clean_json.rfind('}')
        if start != -1 and end != -1:
            clean_json = clean_json[start:end+1]
            
        plan_dict = json.loads(clean_json)
        
        steps_count = len(plan_dict.get('step_by_step_plan', []))
        logger.info(f"Plan Generated: {steps_count} steps.")
        state['plan'] = plan_dict
        
    except json.JSONDecodeError as e:
        logger.error(f"Planning Failed (JSON Error): {e}")
        state['error'] = f"Invalid JSON plan: {e}"
        state['status'] = "failed"
    except Exception as e:
        logger.error(f"Planning Failed: {e}")
        state['error'] = str(e)
        state['status'] = "failed"
        
    return state

def execution_node(state: HybridState) -> HybridState:
    if state.get('status') == "failed":
        return state
        
    logger.info("DEV CREW: Executing Plan...")
    
    try:
        dev_team = DevCrew()
        result = dev_team.run(state['plan'])
        
        logger.info("Execution Finished. Output received.")
        
        # Save execution log
        log_path = sandbox.get_path("execution_log.md")
        file_ops.write_file(log_path, str(result))
        logger.info(f"Saved execution log to: {log_path}")
        
        state['status'] = "completed"
        
    except Exception as e:
        logger.error(f"Execution Failed: {e}")
        state['error'] = str(e)
        state['status'] = "failed"
        
    return state

# --- Routing ---
def router(state: HybridState) -> str:
    if state.get('status') == "failed":
        return END
    return "execution"

# --- Graph Construction ---
def build_hybrid_graph():
    workflow = StateGraph(HybridState)
    
    workflow.add_node("init", init_node)
    workflow.add_node("planning", planning_node)
    workflow.add_node("execution", execution_node)
    
    workflow.set_entry_point("init")
    
    workflow.add_edge("init", "planning")
    workflow.add_conditional_edges("planning", router, {"execution": "execution", END: END})
    workflow.add_edge("execution", END)
    
    return workflow.compile()

if __name__ == "__main__":
    print("🤖 STARTING HYBRID E2E TEST (OPTIMIZED)...")
    
    test_task = "Create a robust 'Calculator' class in 'src/utils/calculator.py' that supports add, subtract, multiply, and divide with error handling for division by zero."
    
    initial_state = HybridState(
        task=test_task,
        plan={},
        code_files=[],
        status="running",
        error=None
    )
    
    try:
        app = build_hybrid_graph()
        final_state = app.invoke(initial_state)
        
        if final_state['status'] == 'completed':
            print("\n✅✅ E2E TEST SUCCESSFUL! System is functional.")
        else:
            print(f"\n❌❌ E2E TEST FAILED. Error: {final_state.get('error')}")
            
    except Exception as e:
        logger.critical(f"Critical System Failure: {e}")
