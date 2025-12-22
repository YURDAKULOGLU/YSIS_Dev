"""
RAG Aware Planner - Enhances planning with historical context.

Wraps a base planner (like SimplePlanner) and injects RAG context
into the planning process.
"""

from typing import Dict, Any, Optional
from src.agentic.core.protocols import Plan, PlannerProtocol
from src.agentic.core.plugins.rag_memory import RAGMemory
from src.agentic.core.plugins.simple_planner import SimplePlanner

class RAGAwarePlanner:
    """
    Decorator/Wrapper for planners that adds RAG capabilities.
    """

    def __init__(self, base_planner: Optional[PlannerProtocol] = None, rag_memory: Optional[RAGMemory] = None):
        self.planner = base_planner or SimplePlanner()
        self.rag = rag_memory or RAGMemory()

    async def plan(self, task: str, context: Dict[str, Any]) -> Plan:
        """
        1. Query RAG for similar past tasks/code.
        2. Inject retrieved context into the 'context' dictionary.
        3. Delegate to the base planner.
        """
        # 1. Query RAG Memory
        print(f"[{self.name()}] Querying RAG for: {task[:50]}...")
        try:
            rag_results = self.rag.query(task, n_results=3)
            # Format RAG results into a string
            rag_context_str = "\n---\n".join(rag_results) if rag_results else "No relevant history found."
        except Exception as e:
            print(f"[{self.name()}] RAG Query failed: {e}")
            rag_context_str = "RAG Error: Could not retrieve context."

        # 2. Inject into context
        # We assume the base planner looks for 'rag_context' or simply dump everything into context
        context = context.copy()
        context["relevant_history"] = rag_context_str
        
        # 3. Delegate to Base Planner
        # The base planner (SimplePlanner) dumps the whole context JSON into the prompt,
        # so the LLM will see 'relevant_history'.
        return await self.planner.plan(task, context)

    def name(self) -> str:
        return f"RAGAware({self.planner.name()})"
