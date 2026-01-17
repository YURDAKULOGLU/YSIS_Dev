"""
Mem0 Adapter - Agent memory infrastructure.

Supports both LOCAL (self-hosted) and CLOUD (API) modes.
Mode is selected based on policy configuration and LLM provider.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Try to import Mem0 from vendors/ (local clone) first
try:
    import sys
    from pathlib import Path

    vendors_path = Path(__file__).parent.parent.parent.parent / "vendors" / "mem0"
    if vendors_path.exists():
        # Mem0 structure: vendors/mem0/mem0/ (package is in mem0 subdirectory)
        mem0_package_path = vendors_path / "mem0"
        if mem0_package_path.exists() and (mem0_package_path / "__init__.py").exists():
            # Add parent directory to path so we can import mem0
            sys.path.insert(0, str(vendors_path))
            from mem0 import Memory

            MEM0_LOCAL_CLONE_AVAILABLE = True
            logger.info("Using Mem0 from vendors/ (local clone)")
        else:
            MEM0_LOCAL_CLONE_AVAILABLE = False
    else:
        MEM0_LOCAL_CLONE_AVAILABLE = False
except (ImportError, Exception) as e:
    MEM0_LOCAL_CLONE_AVAILABLE = False
    logger.debug(f"Mem0 local clone not available: {e}")

# Try to import Mem0 from pip (cloud API or self-hosted)
if not MEM0_LOCAL_CLONE_AVAILABLE:
    try:
        from mem0 import Memory

        MEM0_PIP_AVAILABLE = True
        logger.info("Using Mem0 from pip")
    except ImportError:
        MEM0_PIP_AVAILABLE = False
        logger.warning("Mem0 not installed. Install with: pip install mem0ai or clone to vendors/mem0")

# Combined availability
MEM0_AVAILABLE = MEM0_LOCAL_CLONE_AVAILABLE or MEM0_PIP_AVAILABLE

# Fallback to VectorStore if Mem0 not available
try:
    from ..data_plane.vector_store import VectorStore

    VECTORSTORE_FALLBACK_AVAILABLE = True
except ImportError:
    VECTORSTORE_FALLBACK_AVAILABLE = False


class Mem0Adapter:
    """
    Mem0 Adapter - Agent memory infrastructure.

    Supports multiple modes:
    - CLOUD: Mem0 hosted platform (requires API key)
    - LOCAL: Mem0 self-hosted (uses local LLM)
    - FALLBACK: YBIS VectorStore (if Mem0 not available)

    Mode is selected based on:
    1. Policy configuration (mem0.mode: "cloud" | "local" | "auto")
    2. LLM provider availability (Ollama = local, OpenAI = cloud)
    3. API key availability (cloud requires key)
    """

    def __init__(
        self,
        mode: str = "auto",
        api_key: str | None = None,
        llm_provider: str | None = None,
        vector_store: VectorStore | None = None,
    ):
        """
        Initialize Mem0 adapter.

        Args:
            mode: "cloud" | "local" | "auto" | "fallback"
            api_key: Mem0 API key (for cloud mode)
            llm_provider: LLM provider name (e.g., "ollama", "openai")
            vector_store: VectorStore instance (for fallback mode)
        """
        self.mode = mode
        self.api_key = api_key
        self.llm_provider = llm_provider
        self.client = None
        self.vector_store = vector_store
        self.collection = "agent_memory"

        # Determine actual mode
        actual_mode = self._determine_mode()
        self._initialize_mode(actual_mode)

    def _determine_mode(self) -> str:
        """Determine which mode to use based on configuration."""
        # If explicitly set, use that
        if self.mode in ("cloud", "local", "fallback"):
            return self.mode

            # Auto mode: decide based on availability
            if self.mode == "auto":
                # Check LLM provider preference
                if self.llm_provider == "ollama":
                    # Ollama = local, prefer self-hosted Mem0
                    if MEM0_AVAILABLE:
                        return "local"
                    elif VECTORSTORE_FALLBACK_AVAILABLE:
                        return "fallback"

                # Check for API key (cloud mode)
                if self.api_key and MEM0_AVAILABLE:
                    return "cloud"

                # Check for local Mem0 (from clone or pip)
                if MEM0_AVAILABLE:
                    return "local"

                # Fallback to VectorStore
                if VECTORSTORE_FALLBACK_AVAILABLE:
                    return "fallback"

        # Default to fallback
        return "fallback"

    def _initialize_mode(self, mode: str) -> None:
        """Initialize the selected mode."""
        if mode == "cloud":
            if not MEM0_AVAILABLE:
                raise ImportError(
                    "Mem0 not available. Install with: pip install mem0ai or clone to vendors/mem0"
                )
            if not self.api_key:
                raise ValueError("Mem0 API key required for cloud mode")
            try:
                self.client = Memory(api_key=self.api_key)
                logger.info("Mem0 adapter initialized (CLOUD mode)")
            except Exception as e:
                logger.error(f"Failed to initialize Mem0 cloud: {e}")
                raise

        elif mode == "local":
            if not MEM0_AVAILABLE:
                raise ImportError(
                    "Mem0 not available. Install with: pip install mem0ai or clone to vendors/mem0"
                )
            try:
                # Mem0 local mode - uses local LLM (Ollama)
                # Works with both local clone and pip install
                self.client = Memory()  # No API key = self-hosted mode
                logger.info("Mem0 adapter initialized (LOCAL mode - self-hosted)")
            except Exception as e:
                logger.error(f"Failed to initialize Mem0 local: {e}")
                raise

        elif mode == "fallback":
            if not VECTORSTORE_FALLBACK_AVAILABLE:
                raise ImportError("VectorStore not available for fallback mode")
            try:
                self.vector_store = self.vector_store or VectorStore()
                logger.info("Mem0 adapter initialized (FALLBACK mode - using VectorStore)")
            except Exception as e:
                logger.error(f"Failed to initialize VectorStore fallback: {e}")
                raise

        else:
            raise ValueError(f"Unknown Mem0 mode: {mode}")

    def add_memory(
        self,
        messages: list[dict[str, str]],
        user_id: str | None = None,
        agent_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Add memory from agent interaction.

        Args:
            messages: List of message dicts with "role" and "content"
            user_id: User identifier (optional)
            agent_id: Agent identifier (optional)
            metadata: Optional metadata dict

        Returns:
            Memory addition result
        """
        logger.info(f"Adding Mem0 memory: agent_id={agent_id}, messages={len(messages)}")
        try:
            if self.client:
                # Use Mem0 (cloud or local)
                result = self.client.add(
                    messages=messages,
                    user_id=user_id,
                    agent_id=agent_id,
                    metadata=metadata or {},
                )
                logger.info(f"Mem0 memory added successfully: {result.get('memory_id', 'unknown')}")
                return result
            else:
                # Fallback to VectorStore
                memory_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
                document = {
                    "text": memory_text,
                    "metadata": {
                        "user_id": user_id,
                        "agent_id": agent_id,
                        **(metadata or {}),
                    },
                }
                self.vector_store.add_documents(
                    collection=self.collection,
                    documents=[document],
                )
                return {
                    "memory_id": f"{agent_id or 'unknown'}-{len(messages)}",
                    "status": "added",
                }
        except Exception as e:
            logger.error(f"Failed to add Mem0 memory: {e}")
            raise

    def search_memory(
        self,
        query: str,
        user_id: str | None = None,
        agent_id: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Search agent memory.

        Args:
            query: Search query
            user_id: User identifier (optional, for filtering)
            agent_id: Agent identifier (optional, for filtering)
            limit: Maximum results to return

        Returns:
            List of memory results
        """
        logger.info(f"Searching Mem0 memory: query={query[:50]}, agent_id={agent_id}, limit={limit}")
        try:
            if self.client:
                # Use Mem0 (cloud or local)
                results = self.client.search(
                    query=query,
                    user_id=user_id,
                    agent_id=agent_id,
                    limit=limit,
                )
                # Mem0 returns dict with "results" key
                if isinstance(results, dict) and "results" in results:
                    return results["results"]
                return results if isinstance(results, list) else []
            else:
                # Fallback to VectorStore
                vector_results = self.vector_store.query(
                    collection=self.collection,
                    query=query,
                    top_k=limit,
                )

                # Filter by user_id/agent_id if provided
                filtered_results = []
                for result in vector_results:
                    metadata = result.get("metadata", {})
                    if user_id and metadata.get("user_id") != user_id:
                        continue
                    if agent_id and metadata.get("agent_id") != agent_id:
                        continue

                    filtered_results.append({
                        "memory": result.get("document", ""),
                        "metadata": metadata,
                        "score": result.get("score", 0.0),
                    })

                return filtered_results[:limit]
        except Exception as e:
            logger.error(f"Failed to search Mem0 memory: {e}")
            return []

    def get_all_memories(
        self,
        user_id: str | None = None,
        agent_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get all memories for a user/agent.

        Args:
            user_id: User identifier (optional, for filtering)
            agent_id: Agent identifier (optional, for filtering)

        Returns:
            List of all memories
        """
        try:
            if self.client:
                # Use Mem0 (cloud or local)
                memories = self.client.get_all(
                    user_id=user_id,
                    agent_id=agent_id,
                )
                return memories if isinstance(memories, list) else []
            else:
                # Fallback to VectorStore
                results = self.vector_store.query(
                    collection=self.collection,
                    query="",  # Empty query to get all
                    top_k=1000,
                )

                # Filter by user_id/agent_id if provided
                filtered = []
                for result in results:
                    metadata = result.get("metadata", {})
                    if user_id and metadata.get("user_id") != user_id:
                        continue
                    if agent_id and metadata.get("agent_id") != agent_id:
                        continue

                    filtered.append({
                        "memory": result.get("document", ""),
                        "metadata": metadata,
                    })

                return filtered
        except Exception as e:
            logger.error(f"Failed to get Mem0 memories: {e}")
            return []

    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a specific memory.

        Args:
            memory_id: Memory identifier

        Returns:
            True if deleted, False otherwise
        """
        try:
            if self.client:
                # Use Mem0 (cloud or local)
                self.client.delete(memory_id=memory_id)
                return True
            else:
                # VectorStore deletion not implemented yet
                logger.warning("VectorStore deletion by ID not implemented")
                return False
        except Exception as e:
            logger.error(f"Failed to delete Mem0 memory: {e}")
            return False

    def update_memory(
        self,
        memory_id: str,
        messages: list[dict[str, str]] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Update an existing memory.

        Args:
            memory_id: Memory identifier
            messages: Updated messages (optional)
            metadata: Updated metadata (optional)

        Returns:
            Update result
        """
        try:
            if self.client:
                # Use Mem0 (cloud or local)
                result = self.client.update(
                    memory_id=memory_id,
                    messages=messages,
                    metadata=metadata,
                )
                return result
            else:
                # Fallback: add new memory instead
                if messages:
                    return self.add_memory(messages=messages, metadata=metadata)
                return {"status": "no_update"}
        except Exception as e:
            logger.error(f"Failed to update Mem0 memory: {e}")
            raise

    def is_available(self) -> bool:
        """Check if Mem0 adapter is available."""
        available = self.client is not None or self.vector_store is not None
        logger.debug(f"Mem0 adapter available: {available}, mode={self.get_mode()}")
        return available

    def get_mode(self) -> str:
        """Get current mode."""
        if self.client:
            return "cloud" if self.api_key else "local"
        return "fallback"


# Global instance
_mem0_adapter: Mem0Adapter | None = None


def get_mem0_adapter(
    mode: str | None = None,
    api_key: str | None = None,
    llm_provider: str | None = None,
    vector_store: VectorStore | None = None,
) -> Mem0Adapter:
    """
    Get global Mem0 adapter instance.

    Args:
        mode: "cloud" | "local" | "auto" | "fallback" (default from policy)
        api_key: Mem0 API key (for cloud mode, default from env)
        llm_provider: LLM provider name (default from policy)
        vector_store: VectorStore instance (for fallback mode)

    Returns:
        Mem0Adapter instance
    """
    global _mem0_adapter

    if _mem0_adapter is None:
        # Get configuration from policy if not provided
        if mode is None or llm_provider is None:
            from ..services.policy import get_policy_provider

            policy_provider = get_policy_provider()
            if policy_provider._policy is None:
                policy_provider.load_profile()

            policy = policy_provider.get_policy()
            mem0_config = policy.get("adapters", {}).get("mem0", {})

            if mode is None:
                mode = mem0_config.get("mode", "auto")
            if api_key is None:
                import os

                api_key = os.getenv("MEM0_API_KEY") or mem0_config.get("api_key")
            if llm_provider is None:
                llm_config = policy_provider.get_llm_config()
                # Determine provider from model name
                model = llm_config.get("planner_model", "")
                if "ollama" in model.lower():
                    llm_provider = "ollama"
                elif "openai" in model.lower() or "gpt" in model.lower():
                    llm_provider = "openai"
                else:
                    llm_provider = "ollama"  # Default

        try:
            _mem0_adapter = Mem0Adapter(
                mode=mode or "auto",
                api_key=api_key,
                llm_provider=llm_provider,
                vector_store=vector_store,
            )
        except Exception as e:
            logger.warning(f"Failed to initialize Mem0 adapter: {e}")
            # Try fallback mode
            try:
                _mem0_adapter = Mem0Adapter(mode="fallback", vector_store=vector_store)
            except Exception:
                raise

    return _mem0_adapter

