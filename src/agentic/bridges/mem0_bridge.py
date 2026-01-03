"""
Mem0 Bridge for YBIS
Wraps the Mem0 library to provide a standardized memory interface.
"""

from typing import List, Dict, Any, Optional
from mem0 import Memory
import os

class Mem0Bridge:
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id

        # Configure Mem0
        # FULL LOCAL MODE (No OpenAI)
        config = {
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "collection_name": "ybis_mem0",
                    "path": "Knowledge/LocalDB/chroma_db"
                }
            },
            "llm": {
                "provider": "ollama",
                "config": {
                    "model": "qwen2.5-coder:32b",
                    "temperature": 0.1,
                    "max_tokens": 2000,
                    "ollama_base_url": "http://localhost:11434"
                }
            },
            "embedder": {
                "provider": "huggingface",
                "config": {
                    "model": "all-MiniLM-L6-v2"
                }
            }
        }

        self.client = Memory.from_config(config)
        print(f"[Mem0Bridge] Initialized for user: {self.user_id}")

    def add(self, text: str, metadata: Dict[str, Any] = None):
        """Add a memory."""
        self.client.add(text, user_id=self.user_id, metadata=metadata)

    def search(self, query: str, limit: int = 5) -> List[str]:
        """Search memories."""
        response = self.client.search(query, user_id=self.user_id, limit=limit)
        print(f"[DEBUG] Search Response Raw: {response}")

        # Handle dict response (Mem0 v1.0.1 style)
        if isinstance(response, dict):
            results = response.get("results", [])
        else:
            results = response

        if not results:
            return []

        normalized = []
        for r in results:
            # Handle Dict
            if isinstance(r, dict):
                normalized.append(r.get("memory", str(r)))
            # Handle Pydantic Model (if any)
            elif hasattr(r, "memory"):
                normalized.append(r.memory)
            # Handle String
            elif isinstance(r, str):
                normalized.append(r)
            else:
                normalized.append(str(r))

        return normalized

    def get_all(self) -> List[str]:
        """Get all memories for user."""
        results = self.client.get_all(user_id=self.user_id)
        return [r["memory"] for r in results] if results else []
