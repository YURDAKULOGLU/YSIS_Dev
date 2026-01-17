"""
Parallel Node Execution - Support for parallel node execution in workflows.

LangGraph supports parallel execution by adding multiple edges from the same source.
This module provides utilities to handle parallel node groups and synchronization.
"""

import logging
from collections.abc import Callable

logger = logging.getLogger(__name__)

from ..orchestrator.graph import WorkflowState


def create_parallel_node_wrapper(
    node_funcs: dict[str, Callable[[WorkflowState], WorkflowState]]
) -> Callable[[WorkflowState], WorkflowState]:
    """
    Create a wrapper function that executes multiple nodes in parallel.

    Args:
        node_funcs: Dictionary mapping node IDs to their functions

    Returns:
        Wrapper function that executes all nodes in parallel and merges results
    """
    from concurrent.futures import ThreadPoolExecutor

    def parallel_wrapper(state: WorkflowState) -> WorkflowState:
        """
        Execute multiple nodes in parallel and merge their state updates.

        Note: LangGraph handles parallel execution automatically when multiple
        edges are added from the same source. This wrapper is for explicit
        parallel groups defined in YAML.
        """
        # Execute all nodes in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=len(node_funcs)) as executor:
            futures = {
                node_id: executor.submit(node_func, state.copy())
                for node_id, node_func in node_funcs.items()
            }

            # Wait for all to complete and collect results
            results = {}
            for node_id, future in futures.items():
                try:
                    result_state = future.result()
                    results[node_id] = result_state
                except Exception as e:
                    # If a node fails, log but continue with others
                    state[f"error_{node_id}"] = str(e)
                    results[node_id] = state.copy()

        # Merge all state updates
        merged_state = state.copy()
        for node_id, result_state in results.items():
            # Merge state updates (later nodes override earlier ones)
            merged_state.update(result_state)

        return merged_state

    return parallel_wrapper


def detect_parallel_groups(connections: list[dict]) -> dict[str, list[str]]:
    """
    Detect parallel execution groups from connections.

    If multiple connections have the same source, those targets run in parallel.

    Args:
        connections: List of connection dictionaries

    Returns:
        Dictionary mapping source nodes to lists of parallel target nodes
    """
    parallel_groups = {}

    for conn in connections:
        source = conn.get("from")
        target = conn.get("to")

        # Skip conditional connections (they're handled separately)
        if "condition" in conn:
            continue

        # Skip START/END
        if source == "START" or target == "END":
            continue

        if source not in parallel_groups:
            parallel_groups[source] = []

        if target not in parallel_groups[source]:
            parallel_groups[source].append(target)

    # Filter to only groups with multiple targets (true parallel execution)
    return {
        source: targets
        for source, targets in parallel_groups.items()
        if len(targets) > 1
    }

