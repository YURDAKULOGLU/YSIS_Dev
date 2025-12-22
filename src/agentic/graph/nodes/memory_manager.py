from ..state import FactoryState
from src.agentic.bridges.mem0_bridge import Mem0Bridge

def memory_read_node(state: FactoryState):
    print(f"\n[MEMORY] Accessing Neural Bank for: '{state['goal']}'")
    
    try:
        mem = Mem0Bridge(user_id="ybis_factory")
        # Search for similar tasks or guidelines
        context = mem.search(state['goal'], limit=3)
        # Search for past failures related to this
        failures = mem.search(f"failure {state['goal']}", limit=2)
        
        full_context = context + failures
        
        if full_context:
            print(f"   Found {len(full_context)} relevant memories.")
            return {"memory_context": full_context}
        else:
            print("   No prior knowledge found. Exploring new territory.")
            return {"memory_context": []}
            
    except Exception as e:
        print(f"   Memory Access Error: {e}")
        return {"memory_context": []}

def memory_write_node(state: FactoryState):
    print(f"\n[MEMORY] Storing experience...")
    
    try:
        mem = Mem0Bridge(user_id="ybis_factory")
        
        if state["status"] == "APPROVED":
            content = f"SUCCESS: Task '{state['goal']}' completed. Plan used: {state['plan']}"
            meta = {"type": "success", "task_id": state["task_id"]}
        else:
            content = f"FAILURE: Task '{state['goal']}' failed after retries. Feedback: {state.get('feedback', 'Unknown')}"
            meta = {"type": "failure", "task_id": state["task_id"]}
            
        mem.add(content, metadata=meta)
        print("   Experience saved.")
        
    except Exception as e:
        print(f"   Memory Write Error: {e}")
    
    return {"status": "DONE"} # Finalize graph
