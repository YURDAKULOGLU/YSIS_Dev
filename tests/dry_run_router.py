import sys
import os
import asyncio

# Add project root to path
sys.path.insert(0, os.getcwd())

from src.agentic.core.plugins.model_router import default_router
from src.agentic.core.plugins.simple_planner import SimplePlanner

async def test_router_integration():
    print("\n[ROUTER TEST] [INFO] Testing Brain Transplant...")

    # 1. Test Router Config
    planning_config = default_router.get_model("PLANNING")
    print(f"[ROUTER TEST] Router Profile: {default_router.profile}")
    print(f"[ROUTER TEST] Recommended Plan Model: {planning_config.model_name}")
    print(f"[ROUTER TEST] Context Window: {planning_config.context_window}")

    if "qwen2.5-coder:32b" not in planning_config.model_name:
        print("[ROUTER TEST] [ERROR] Unexpected model! Expected 32b beast.")
        return

    # 2. Test Planner Integration
    planner = SimplePlanner()
    print(f"[ROUTER TEST] Planner Name: {planner.name()}")

    if "qwen2.5-coder:32b" in planner.name():
        print("[ROUTER TEST] [OK] Planner is correctly using the Router!")
    else:
        print(f"[ROUTER TEST] [ERROR] Planner failed to pickup model. Name is: {planner.name()}")

if __name__ == "__main__":
    asyncio.run(test_router_integration())
