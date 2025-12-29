import sys
import os
import importlib
from pathlib import Path

# Add project root to path
project_root = Path(os.getcwd())
sys.path.insert(0, str(project_root))

def check_import(module_name, class_name=None):
    try:
        module = importlib.import_module(module_name)
        if class_name:
            getattr(module, class_name)
        print(f"[OK] Import Successful: {module_name}" + (f".{class_name}" if class_name else ""))
        return True
    except ImportError as e:
        print(f"[FAIL] Import Failed: {module_name} - {e}")
        return False
    except AttributeError as e:
        print(f"[FAIL] Class not found: {module_name}.{class_name} - {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Error importing {module_name}: {e}")
        return False

def main():
    print("[INFO] YBIS System Health Check")
    print("--------------------------------")
    
    # Core Config
    if not check_import("src.agentic.core.config"):
        print("CRITICAL: Config module missing.")
        return

    # Core Components
    components = [
        ("src.agentic.core.graphs.orchestrator_graph", "OrchestratorGraph"),
        ("src.agentic.core.plugins.simple_planner", "SimplePlanner"),
        ("src.agentic.core.plugins.aider_executor", "AiderExecutor"),
        ("src.agentic.core.plugins.aider_executor", "AiderExecutor"),
        ("src.agentic.core.plugins.sentinel", "SentinelVerifier"),
        ("src.agentic.core.plugins.rag_memory", "RAGMemory"),
        ("src.agentic.core.plugins.task_board_manager", "TaskBoardManager"),
    ]

    # Bridges
    bridges = [
        ("src.agentic.bridges.crewai_bridge", "CrewAIBridge"),
        ("src.agentic.bridges.mem0_bridge", "Mem0Bridge"),
    ]

    all_passed = True
    
    print("\n[INFO] Checking Core Components...")
    for mod, cls in components:
        if not check_import(mod, cls):
            all_passed = False

    print("\n[INFO] Checking Bridges...")
    for mod, cls in bridges:
        if not check_import(mod, cls):
            all_passed = False
            
    print("\n--------------------------------")
    if all_passed:
        print("[SUCCESS] SYSTEM INTEGRITY: 100% - Ready to Start")
    else:
        print("[WARNING] SYSTEM INTEGRITY: COMPROMISED - Check errors above")

if __name__ == "__main__":
    main()