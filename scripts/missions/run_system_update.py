import sys
import os
import json

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir)) # .YBIS_Dev/..
sys.path.append(os.path.join(project_root, ".YBIS_Dev"))

from Agentic.Crews.planning_crew import PlanningCrew
from Agentic.Crews.dev_crew import DevCrew

def main():
    print(" MASTER ORCHESTRATOR: System Update Initiated...")

    # 1. PLAN PHASE
    print("\n[PHASE 1] Planning...")
    planner = PlanningCrew()

    requirement = """
    Update the project documentation (README.md) to reflect the new architectural reality.

    Current State issues to fix:
    1. README says we stop at Tier 2.5. We are now moving to Tier 3 (Hybrid Architecture).
    2. It mentions PydanticAI. We are now using CrewAI for execution and LangGraph for orchestration.
    3. It needs to emphasize 'Local LLM' capabilities (Llama 3.2, DeepSeek) which are now proven to work.
    4. Define Tier 3 as "The Hybrid Engine" and Tier 4 as "The Sentinel" (Autonomic Maintenance).
    5. Mention the 3 Constitutions (Project, Universal, Development).

    Goal: Create a plan to rewrite README.md to be the 'Single Source of Truth' for this new direction.
    """

    plan_result = planner.run(requirement)

    print("\n[SUCCESS] Plan Generated:")
    print(plan_result)

    # In a full autonomous loop, we would parse this plan and feed it to DevCrew.
    # For now, as the Architect, I (Gemini) will review this plan.

if __name__ == "__main__":
    main()
