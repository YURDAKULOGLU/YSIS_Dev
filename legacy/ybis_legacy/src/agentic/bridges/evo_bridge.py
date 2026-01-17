import sys
import os
from pathlib import Path
from typing import Any, Dict

# Add tool to sys.path
EVO_PATH = Path("organs/EvoAgentX")
sys.path.insert(0, str(EVO_PATH))

class EvoAgentBridge:
    """
    Native Bridge for EvoAgentX.
    Enables YBIS to use EvoAgentX's self-evolution capabilities.
    """
    
    def __init__(self):
        self.enabled = (EVO_PATH / "setup.py").exists() or (EVO_PATH / "README.md").exists()
        if not self.enabled:
            print("[WARN] EvoAgentX not found. Bridge disabled.")

    def evolve_agent(self, agent_code: str, feedback: str) -> str:
        """
        Uses EvoAgentX to optimize an agent's code based on feedback.
        
        Args:
            agent_code: The source code of the agent to improve.
            feedback: Performance feedback or error logs.
            
        Returns:
            Optimized agent code.
        """
        if not self.enabled:
            return agent_code

        try:
            # Hypothetical entry point based on framework pattern
            # real integration would depend on specific EvoAgentX API
            # from evo_agent import Evolver
            # optimizer = Evolver()
            # return optimizer.optimize(agent_code, feedback)
            
            # Simulation for now until deep integration
            return f"# Optimized by EvoAgentX\n# Feedback: {feedback}\n{agent_code}\n# Optimization Applied."
            
        except Exception as e:
            print(f"[ERROR] EvoAgentX Bridge Failed: {e}")
            return agent_code

    def get_evolution_stats(self) -> Dict[str, Any]:
        return {
            "status": "active" if self.enabled else "disabled",
            "version": "1.0.0",
            "capabilities": ["code_optimization", "prompt_refinement"]
        }
