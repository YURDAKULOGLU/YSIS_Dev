import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir)) # .YBIS_Dev/..
sys.path.append(os.path.join(project_root, ".YBIS_Dev"))

from Agentic.Crews.planning_crew import PlanningCrew

if __name__ == "__main__":
    print("🚀 Testing Planning Crew (Hybrid Architecture)...")
    
    planner = PlanningCrew()
    requirement = "Create a Python class 'Logger' that writes logs to a file with rotation."
    
    result = planner.run(requirement)
    
    print("\n✅ Crew Execution Result:")
    print(result)
