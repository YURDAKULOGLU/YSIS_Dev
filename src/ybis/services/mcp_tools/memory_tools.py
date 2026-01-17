"""
Memory MCP Tools (Adapter Stubs).

Tools for memory system integration using vector/graph adapters.
"""

import logging
from pathlib import Path

from ...syscalls.journal import append_event

logger = logging.getLogger(__name__)



async def add_to_memory(
    data: str,
    agent_id: str = "mcp-client",
    metadata: str | None = None,
    run_path: Path | None = None,
    trace_id: str | None = None,
) -> str:
    """
    Add information to the system's persistent memory.

    This stores data in a graph+vector hybrid database for later retrieval.
    Use this to remember important information, decisions, or learnings.

    Args:
        data: The information to store (text)
        agent_id: ID of agent adding the memory
        metadata: Optional JSON string with metadata

    Returns:
        Success message or error

    Example:
        add_to_memory("We decided to use Cognee for memory because it integrates with Neo4j")
    """
    try:
        # Try to import memory adapter (adapter-based)
        from ...adapters.memory_store import MemoryStoreAdapter

        adapter = MemoryStoreAdapter()
        adapter.add(data, agent_id=agent_id, metadata=metadata)

        # Journal: MCP memory store
        if run_path:
            append_event(
                run_path,
                "MCP_MEMORY_STORE",
                {
                    "agent_id": agent_id,
                    "data_length": len(data),
                },
                trace_id=trace_id,
            )

        # Log memory addition
        from .messaging_tools import send_message

        await send_message(
            to="all",
            subject=f"Memory Added by {agent_id}",
            content=f"Added to system memory:\n\n{data[:200]}...",
            from_agent=agent_id,
            message_type="direct",
            priority="LOW",
            tags="memory,learning",
        )

        return f"SUCCESS: Memory added and indexed. {len(data)} characters stored."

    except ImportError:
        return "MEMORY ERROR: Memory store adapter not yet implemented. This feature requires Task E (Memory + Graph Adapters).\n\n(Ensure memory adapter is configured and vector store is accessible)"
    except Exception as e:
        return f"MEMORY ERROR: Failed to add memory: {e!s}\n(Ensure memory adapter is configured and vector store is accessible)"


async def search_memory(
    query: str,
    agent_id: str = "mcp-client",
    limit: int = 5,
    run_path: Path | None = None,
    trace_id: str | None = None,
) -> str:
    """
    Search the system's persistent memory for relevant information.

    Uses hybrid graph+vector search to find related memories.

    Args:
        query: Search query (question or keywords)
        agent_id: ID of agent searching
        limit: Maximum number of results

    Returns:
        Search results or error

    Example:
        search_memory("What did we decide about memory systems?")
    """
    try:
        from ...adapters.memory_store import MemoryStoreAdapter

        adapter = MemoryStoreAdapter()
        results = adapter.search(query, limit=limit)

        # Journal: MCP memory query
        if run_path:
            append_event(
                run_path,
                "MCP_MEMORY_QUERY",
                {
                    "query_length": len(query),
                    "results_count": len(results) if results else 0,
                },
                trace_id=trace_id,
            )

        if not results or len(results) == 0:
            return f"MEMORY: No results found for: {query}"

        # Format results
        response = f"MEMORY SEARCH RESULTS ({len(results)} found):\n\n"
        for i, result in enumerate(results, 1):
            # Handle different result formats
            if isinstance(result, dict):
                content = result.get("content", result.get("text", str(result)))
            elif isinstance(result, str):
                content = result
            else:
                content = str(result)

            response += f"{i}. {content[:300]}\n\n"

        return response

    except ImportError:
        return "MEMORY ERROR: Memory store adapter not yet implemented. This feature requires Task E (Memory + Graph Adapters).\n\n(Ensure memory adapter is configured and has data)"
    except Exception as e:
        return f"MEMORY ERROR: Failed to search memory: {e!s}\n(Ensure memory adapter is configured and has data)"


