"""
ByteRover Adapter - Team knowledge sharing and cross-project memory.

Provides team-wide memory sharing and deep project context.
Complements YBIS VectorStore (task/run memory) and Mem0 (agent memory).
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Try to import ByteRover from vendors/ (local clone) first
try:
    import sys
    from pathlib import Path

    vendors_path = Path(__file__).parent.parent.parent.parent / "vendors" / "byterover"
    if vendors_path.exists():
        sys.path.insert(0, str(vendors_path))
        # ByteRover import (adjust based on actual package structure)
        try:
            from byterover import ByteRoverClient

            BYTEROVER_LOCAL_CLONE_AVAILABLE = True
            logger.info("Using ByteRover from vendors/ (local clone)")
        except ImportError:
            BYTEROVER_LOCAL_CLONE_AVAILABLE = False
    else:
        BYTEROVER_LOCAL_CLONE_AVAILABLE = False
except (ImportError, Exception) as e:
    BYTEROVER_LOCAL_CLONE_AVAILABLE = False
    logger.debug(f"ByteRover local clone not available: {e}")

# Try to import ByteRover from pip
if not BYTEROVER_LOCAL_CLONE_AVAILABLE:
    try:
        from byterover import ByteRoverClient

        BYTEROVER_PIP_AVAILABLE = True
        logger.info("Using ByteRover from pip")
    except ImportError:
        BYTEROVER_PIP_AVAILABLE = False
        logger.warning("ByteRover not installed. Install with: pip install byterover or clone to vendors/byterover")

# Combined availability
BYTEROVER_AVAILABLE = BYTEROVER_LOCAL_CLONE_AVAILABLE or BYTEROVER_PIP_AVAILABLE

# Fallback to VectorStore if ByteRover not available
try:
    from ..data_plane.vector_store import VectorStore

    VECTORSTORE_FALLBACK_AVAILABLE = True
except ImportError:
    VECTORSTORE_FALLBACK_AVAILABLE = False


class ByteRoverAdapter:
    """
    ByteRover Adapter - Team knowledge sharing.

    Provides:
    - Team-wide memory sharing (cross-agent, cross-project)
    - Deep project context (beyond single task/run)
    - Knowledge persistence across sessions

    Complements:
    - YBIS VectorStore: Task/run memory (per-instance)
    - Mem0: Agent session memory (per-agent)
    - ByteRover: Team knowledge (shared across all)
    """

    def __init__(
        self,
        api_key: str | None = None,
        team_id: str | None = None,
        project_id: str | None = None,
        vector_store: VectorStore | None = None,
    ):
        """
        Initialize ByteRover adapter.

        Args:
            api_key: ByteRover API key (optional, for cloud mode)
            team_id: Team identifier (optional)
            project_id: Project identifier (optional)
            vector_store: VectorStore instance (for fallback mode)
        """
        self.api_key = api_key
        self.team_id = team_id
        self.project_id = project_id
        self.client = None
        self.vector_store = vector_store
        self.collection = "team_knowledge"

        # Initialize ByteRover if available
        if BYTEROVER_AVAILABLE:
            try:
                if api_key:
                    # Cloud mode
                    self.client = ByteRoverClient(api_key=api_key)
                    logger.info("ByteRover adapter initialized (CLOUD mode)")
                else:
                    # Local mode (self-hosted)
                    self.client = ByteRoverClient()
                    logger.info("ByteRover adapter initialized (LOCAL mode)")
            except Exception as e:
                logger.warning(f"Failed to initialize ByteRover: {e}, using fallback")
                self.client = None
        else:
            logger.info("ByteRover not available, using VectorStore fallback")

    def share_knowledge(
        self,
        content: str,
        context: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Share knowledge with team.

        Args:
            content: Knowledge content to share
            context: Optional context metadata
            tags: Optional tags for categorization

        Returns:
            Share result
        """
        logger.info(f"Sharing knowledge: content_length={len(content)}, tags={tags}")
        try:
            if self.client:
                # Use ByteRover
                result = self.client.share(
                    content=content,
                    team_id=self.team_id,
                    project_id=self.project_id,
                    context=context or {},
                    tags=tags or [],
                )
                return result
            else:
                # Fallback to VectorStore
                document = {
                    "text": content,
                    "metadata": {
                        "team_id": self.team_id,
                        "project_id": self.project_id,
                        "tags": tags or [],
                        **(context or {}),
                    },
                }
                self.vector_store.add_documents(
                    collection=self.collection,
                    documents=[document],
                )
                result = {
                    "knowledge_id": f"team-{self.team_id}-{len(content)}",
                    "status": "shared",
                }
                logger.info(f"Knowledge shared successfully: {result['knowledge_id']}")
                return result
        except Exception as e:
            logger.error(f"Failed to share ByteRover knowledge: {e}")
            raise

    def search_team_knowledge(
        self,
        query: str,
        team_id: str | None = None,
        project_id: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Search team knowledge.

        Args:
            query: Search query
            team_id: Team identifier (optional, for filtering)
            project_id: Project identifier (optional, for filtering)
            limit: Maximum results to return

        Returns:
            List of knowledge results
        """
        logger.info(f"Searching team knowledge: query={query[:50]}, limit={limit}")
        try:
            if self.client:
                # Use ByteRover
                results = self.client.search(
                    query=query,
                    team_id=team_id or self.team_id,
                    project_id=project_id or self.project_id,
                    limit=limit,
                )
                return results if isinstance(results, list) else []
            else:
                # Fallback to VectorStore
                vector_results = self.vector_store.query(
                    collection=self.collection,
                    query=query,
                    top_k=limit,
                )

                # Filter by team_id/project_id if provided
                filtered_results = []
                for result in vector_results:
                    metadata = result.get("metadata", {})
                    if team_id and metadata.get("team_id") != team_id:
                        continue
                    if project_id and metadata.get("project_id") != project_id:
                        continue

                    filtered_results.append({
                        "content": result.get("document", ""),
                        "metadata": metadata,
                        "score": result.get("score", 0.0),
                    })

                results = filtered_results[:limit]
                logger.info(f"Found {len(results)} knowledge results")
                return results
        except Exception as e:
            logger.error(f"Failed to search ByteRover knowledge: {e}")
            return []

    def get_project_context(
        self,
        project_id: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Get deep project context.

        Args:
            project_id: Project identifier
            limit: Maximum results to return

        Returns:
            List of project context items
        """
        try:
            if self.client:
                # Use ByteRover
                context = self.client.get_project_context(
                    project_id=project_id or self.project_id,
                    limit=limit,
                )
                return context if isinstance(context, list) else []
            else:
                # Fallback to VectorStore
                results = self.vector_store.query(
                    collection=self.collection,
                    query="",  # Empty query to get all
                    top_k=limit,
                )

                # Filter by project_id if provided
                filtered = []
                for result in results:
                    metadata = result.get("metadata", {})
                    if project_id and metadata.get("project_id") != project_id:
                        continue

                    filtered.append({
                        "content": result.get("document", ""),
                        "metadata": metadata,
                    })

                return filtered[:limit]
        except Exception as e:
            logger.error(f"Failed to get ByteRover project context: {e}")
            return []

    def is_available(self) -> bool:
        """Check if ByteRover adapter is available."""
        available = self.client is not None or self.vector_store is not None
        logger.debug(f"ByteRover adapter available: {available}")
        return available


# Global instance
_byterover_adapter: ByteRoverAdapter | None = None


def get_byterover_adapter(
    api_key: str | None = None,
    team_id: str | None = None,
    project_id: str | None = None,
    vector_store: VectorStore | None = None,
) -> ByteRoverAdapter:
    """
    Get global ByteRover adapter instance.

    Args:
        api_key: ByteRover API key (optional, for cloud mode)
        team_id: Team identifier (optional)
        project_id: Project identifier (optional)
        vector_store: VectorStore instance (for fallback mode)

    Returns:
        ByteRoverAdapter instance
    """
    global _byterover_adapter

    if _byterover_adapter is None:
        # Get configuration from policy if not provided
        if api_key is None or team_id is None:
            from ..services.policy import get_policy_provider

            policy_provider = get_policy_provider()
            if policy_provider._policy is None:
                policy_provider.load_profile()

            policy = policy_provider.get_policy()
            byterover_config = policy.get("adapters", {}).get("byterover", {})

            if api_key is None:
                import os

                api_key = os.getenv("BYTEROVER_API_KEY") or byterover_config.get("api_key")
            if team_id is None:
                team_id = byterover_config.get("team_id")
            if project_id is None:
                project_id = byterover_config.get("project_id")

        try:
            _byterover_adapter = ByteRoverAdapter(
                api_key=api_key,
                team_id=team_id,
                project_id=project_id,
                vector_store=vector_store,
            )
        except Exception as e:
            logger.warning(f"Failed to initialize ByteRover adapter: {e}")
            # Try fallback mode
            try:
                _byterover_adapter = ByteRoverAdapter(
                    api_key=None,
                    team_id=team_id,
                    project_id=project_id,
                    vector_store=vector_store,
                )
            except Exception:
                raise

    return _byterover_adapter

