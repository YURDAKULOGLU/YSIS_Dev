"""
Cognee Memory Provider
Integrates Cognee for Graph+Vector hybrid memory.
Handles cognify() and search operations.
"""

import os
import asyncio
import cognee
from typing import List, Any, Dict, Optional

class CogneeProvider:
    def __init__(self):
        # Configure Cognee for our Neo4j instance
        os.environ['GRAPH_DATABASE_PROVIDER'] = 'neo4j'
        os.environ['GRAPH_DATABASE_URL'] = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        os.environ['GRAPH_DATABASE_USERNAME'] = os.getenv("NEO4J_USER", "neo4j")
        os.environ['GRAPH_DATABASE_PASSWORD'] = os.getenv("NEO4J_PASSWORD", "ybis-graph-2025")
        
        # Disable access control for local dev
        os.environ['ENABLE_BACKEND_ACCESS_CONTROL'] = 'false'

    async def add_memory(self, data: str):
        """Ingest and cognify data"""
        try:
            await cognee.add(data)
            await cognee.cognify()
            return True
        except Exception as e:
            print(f"[Cognee] Add failed: {e}")
            return False

    async def search(self, query: str, limit: int = 5) -> List[Any]:
        """Hybrid search across graph and vector"""
        try:
            results = await cognee.search(query, limit=limit)
            return results
        except Exception as e:
            print(f"[Cognee] Search failed: {e}")
            return []
