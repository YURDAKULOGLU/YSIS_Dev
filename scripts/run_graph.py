import asyncio
import sys
import os

# Add project root
sys.path.insert(0, os.getcwd())

from src.agentic.graph.workflow import app

async def main():
    print("🚀 Starting LangGraph Factory...")
    
    # Initial State
    initial_state = {
        "task_id": "TEST-001",
        "goal": "Create a python script at 'src/utils/hello_factory.py' that prints 'Hello from LangGraph'.",
        "plan": "",
        "files": [],
        "history": [],
        "status": "STARTING",
        "retry_count": 0
    }
    
    # Run Graph
    # app.ainvoke executes the graph until END
    result = await app.ainvoke(initial_state)
    
    print("\n✅ Graph Execution Complete!")
    print(f"Final Status: {result['status']}")
    print(f"History: {result['history']}")

if __name__ == "__main__":
    asyncio.run(main())

