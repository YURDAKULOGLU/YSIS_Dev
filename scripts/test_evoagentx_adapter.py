#!/usr/bin/env python3
"""Test EvoAgentX adapter."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.adapters.evoagentx import EvoAgentXAdapter
from src.ybis.workflows.registry import WorkflowRegistry

def test_evoagentx_adapter():
    """Test EvoAgentX adapter."""
    print("Testing EvoAgentX Adapter...")
    print("=" * 50)
    
    # Create adapter
    adapter = EvoAgentXAdapter()
    print(f"EvoAgentX available: {adapter.is_available()}")
    
    if not adapter.is_available():
        print("EvoAgentX not available - check vendors/EvoAgentX exists")
        return
    
    # Load a workflow
    try:
        workflow_spec = WorkflowRegistry.load_workflow("ybis_native")
        workflow_dict = workflow_spec._raw_data
        
        print(f"\nLoaded workflow: {workflow_spec.name}")
        print(f"Nodes: {len(workflow_spec.nodes)}")
        print(f"Connections: {len(workflow_spec.connections)}")
        
        # Test evolution
        metrics = {
            "execution_time": 10.5,
            "success_rate": 0.85,
            "lint_passed": True,
            "tests_passed": True,
        }
        
        print("\nTesting evolution...")
        evolved = adapter.evolve(workflow_dict, metrics)
        
        if evolved.get("_evolution_metadata", {}).get("evolved"):
            print("[OK] Evolution successful!")
            print(f"Changes: {evolved.get('_evolution_metadata', {}).get('changes', [])}")
        else:
            print("[WARN] Evolution not applied (expected for now)")
            print(f"Reason: {evolved.get('_evolution_metadata', {}).get('reason', 'Unknown')}")
        
        # Test scoring
        print("\nTesting scoring...")
        artifacts = {
            "verifier_report": {
                "lint_passed": True,
                "tests_passed": True,
            },
            "gate_report": {
                "decision": "PASS",
            },
        }
        
        score = adapter.score(workflow_dict, artifacts)
        print(f"Workflow score: {score:.2f}/1.0")
        
        print("\n" + "=" * 50)
        print("[OK] EvoAgentX adapter test complete!")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_evoagentx_adapter()

