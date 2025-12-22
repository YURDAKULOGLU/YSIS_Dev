import os
from ..state import FactoryState
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.model_router import default_router

async def planner_node(state: FactoryState):
    print(f"\n[PLANNER] Thinking about: {state['goal']}")
    
    # 1. Get List of available Documentation
    docs_dir = "Knowledge/API_References"
    available_docs = []
    if os.path.exists(docs_dir):
        available_docs = [f for f in os.listdir(docs_dir) if f.endswith(".md")]
    
    doc_context = "\n".join([f"- {d}" for d in available_docs])
    
    # 3. Context Injection (Memory)
    mem_prompt = ""
    if state.get("memory_context"):
        mem_prompt = "RELEVANT MEMORY (Use this to guide your plan):\n" + "\n".join(state["memory_context"])

    # 2. Enhanced Prompt with Doc Awareness & Memory
    task_with_docs = f"""
    GOAL: {state['goal']}
    
    {mem_prompt}
    
    AVAILABLE DOCUMENTATION (Read before planning):
    {doc_context}
    
    If you need to use any of these frameworks, refer to the corresponding .md file in {docs_dir}.
    """
    
    # Use Real Planner
    planner = SimplePlanner(router=default_router)
    
    try:
        plan_obj = await planner.plan(task=state['goal'], context={})
        
        print(f"Plan Generated: {len(plan_obj.steps)} steps.")
        
        return {
            "plan": plan_obj.objective, # Store goal update if needed, or pass steps differently
            # SimplePlanner returns steps list, we need to format it for Aider
            # But here we just pass metadata to state
            "files": plan_obj.files_to_modify,
            "history": [f"Plan: {plan_obj.objective}"],
            "status": "EXECUTING"
        }
    except Exception as e:
        print(f"Planning Failed: {e}")
        return {
            "status": "FAILED",
            "history": [f"Planning Error: {e}"]
        }

