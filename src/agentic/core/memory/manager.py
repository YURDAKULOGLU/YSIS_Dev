"""
Unified Memory Manager
Coordinates between Core (Short-term), Episodic (Vector), and Semantic (Graph) memory.
"""

from typing import List, Any, Dict, Optional
from .cognee_provider import CogneeProvider

class MemoryManager:
    def __init__(self):
        self.semantic = CogneeProvider()
        self.short_term = {} # Simple dict for current session context

    async def remember(self, data: str, memory_type: str = "semantic"):
        """Store information in memory"""
        if memory_type == "semantic":
            return await self.semantic.add_memory(data)
        elif memory_type == "short_term":
            # Just append to internal state for this run
            key = f"memo_{len(self.short_term)}"
            self.short_term[key] = data
            return True
        return False

    async def retrieve(self, query: str, limit: int = 5) -> List[Any]:
        """Search memory for relevant context"""
        # Search semantic memory (GraphRAG)
        results = await self.semantic.search(query, limit=limit)
        return results

    def get_short_term_context(self) -> str:
        """Return all short term context as a string"""
        return "\n".join(self.short_term.values())

# Singleton instance
memory_manager = MemoryManager()
