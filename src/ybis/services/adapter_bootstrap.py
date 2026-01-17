"""
Adapter Bootstrap - Register all adapters at startup.

This module populates the adapter registry with all available adapters.
It should be called during system initialization.

Uses adapter catalog (configs/adapters.yaml) as source of truth.
"""

import logging

logger = logging.getLogger(__name__)

from ..adapters.registry import get_registry
from .adapter_catalog import get_catalog


def bootstrap_adapters() -> None:
    """
    Register all available adapters in the registry.

    This function should be called during system initialization to populate
    the adapter registry. Adapters are registered but only enabled if policy
    allows (opt-in via policy configuration).

    Uses adapter catalog (configs/adapters.yaml) as source of truth.
    Falls back to hardcoded registration if catalog is unavailable.
    """
    logger.info("Starting adapter bootstrap")
    registry = get_registry()
    catalog = get_catalog()

    # Try to load from catalog first
    adapters = catalog.list_adapters()

    if adapters:
        logger.info(f"Registering {len(adapters)} adapters from catalog")
        # Register from catalog
        for adapter_meta in adapters:
            _register_from_catalog(registry, adapter_meta)
        logger.info("Adapter bootstrap from catalog completed")
    else:
        logger.info("Catalog empty, falling back to hardcoded registration")
        # Fallback to hardcoded registration
        _register_hardcoded(registry)
        logger.info("Adapter bootstrap from hardcoded registration completed")


def _register_from_catalog(registry, adapter_meta: dict) -> None:
    """Register adapter from catalog metadata."""
    name = adapter_meta["name"]
    module_path = adapter_meta["module_path"]
    adapter_type = adapter_meta["type"]
    default_enabled = adapter_meta.get("default_enabled", False)

    try:
        logger.debug(f"Registering adapter from catalog: {name} ({adapter_type})")
        # Import adapter class from module path
        module_parts = module_path.split(".")
        module_name = ".".join(module_parts[:-1])
        class_name = module_parts[-1]

        module = __import__(module_name, fromlist=[class_name])
        adapter_class = getattr(module, class_name)

        registry.register(
            name=name,
            adapter_class=adapter_class,
            adapter_type=adapter_type,
            default_enabled=default_enabled,
        )
        logger.info(f"Successfully registered adapter: {name}")
    except (ImportError, AttributeError) as e:
        logger.warning(f"Failed to register adapter {name} from catalog: {e}")
        pass  # Adapter not available


def _register_hardcoded(registry) -> None:
    """Fallback: Register adapters using hardcoded logic."""
    logger.debug("Starting hardcoded adapter registration")

    # Register executor adapters
    try:
        from ..adapters.local_coder import LocalCoderExecutor

        registry.register(
            name="local_coder",
            adapter_class=LocalCoderExecutor,
            adapter_type="executor",
            default_enabled=True,  # Default executor, always available
        )
        logger.debug("Registered local_coder adapter")
    except ImportError as e:
        logger.debug(f"local_coder adapter not available: {e}")
        pass  # Adapter not available

    try:
        from ..adapters.aider import AiderExecutor

        registry.register(
            name="aider",
            adapter_class=AiderExecutor,
            adapter_type="executor",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register sandbox adapters
    try:
        from ..adapters.e2b_sandbox import E2BSandboxAdapter

        registry.register(
            name="e2b_sandbox",
            adapter_class=E2BSandboxAdapter,
            adapter_type="sandbox",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register vector store adapters
    try:
        from ..adapters.vector_store_chroma import ChromaVectorStoreAdapter

        registry.register(
            name="chroma_vector_store",
            adapter_class=ChromaVectorStoreAdapter,
            adapter_type="vector_store",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    try:
        from ..adapters.vector_store_qdrant import QdrantVectorStoreAdapter

        registry.register(
            name="qdrant_vector_store",
            adapter_class=QdrantVectorStoreAdapter,
            adapter_type="vector_store",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register graph store adapters
    try:
        from ..adapters.graph_store_neo4j import Neo4jGraphStoreAdapter

        registry.register(
            name="neo4j_graph",
            adapter_class=Neo4jGraphStoreAdapter,
            adapter_type="graph_store",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register workflow evolution adapters
    try:
        from ..adapters.evoagentx import EvoAgentXAdapter

        registry.register(
            name="evoagentx",
            adapter_class=EvoAgentXAdapter,
            adapter_type="workflow_evolution",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register agent runtime adapters
    try:
        from ..adapters.reactive_agents import ReactiveAgentsAdapter

        registry.register(
            name="reactive_agents",
            adapter_class=ReactiveAgentsAdapter,
            adapter_type="agent_runtime",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register council review adapters
    try:
        from ..adapters.llm_council import LLMCouncilAdapter

        registry.register(
            name="llm_council",
            adapter_class=LLMCouncilAdapter,
            adapter_type="council_review",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register agent learning adapters
    try:
        from ..adapters.aiwaves_agents import AIWavesAgentsAdapter

        registry.register(
            name="aiwaves_agents",
            adapter_class=AIWavesAgentsAdapter,
            adapter_type="agent_learning",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register self-improve loop adapters
    try:
        from ..adapters.self_improve_swarms import SelfImproveSwarmsAdapter

        registry.register(
            name="self_improve_swarms",
            adapter_class=SelfImproveSwarmsAdapter,
            adapter_type="self_improve_loop",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register vector store adapters
    try:
        from ..adapters.vector_store_chroma import ChromaVectorStoreAdapter

        registry.register(
            name="chroma_vector_store",
            adapter_class=ChromaVectorStoreAdapter,
            adapter_type="vector_store",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    try:
        from ..adapters.vector_store_qdrant import QdrantVectorStoreAdapter

        registry.register(
            name="qdrant_vector_store",
            adapter_class=QdrantVectorStoreAdapter,
            adapter_type="vector_store",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register LLM adapters
    try:
        from ..adapters.llamaindex_adapter import LlamaIndexAdapter

        registry.register(
            name="llamaindex_adapter",
            adapter_class=LlamaIndexAdapter,
            adapter_type="llm_adapter",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register event bus adapters
    try:
        from ..services.event_bus import RedisEventBusAdapter

        registry.register(
            name="redis_event_bus",
            adapter_class=RedisEventBusAdapter,
            adapter_type="event_bus",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register observability adapters
    try:
        from ..adapters.observability_langfuse import LangfuseObservabilityAdapter

        registry.register(
            name="langfuse_observability",
            adapter_class=LangfuseObservabilityAdapter,
            adapter_type="observability",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    try:
        from ..adapters.observability_opentelemetry import OpenTelemetryObservabilityAdapter

        registry.register(
            name="opentelemetry_observability",
            adapter_class=OpenTelemetryObservabilityAdapter,
            adapter_type="observability",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register Week 4 adapters (Mem0, DSPy)
    try:
        from ..adapters.mem0_adapter import Mem0Adapter

        registry.register(
            name="mem0",
            adapter_class=Mem0Adapter,
            adapter_type="memory",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    try:
        from ..adapters.dspy_adapter import DSPyPlannerOptimizer

        registry.register(
            name="dspy",
            adapter_class=DSPyPlannerOptimizer,
            adapter_type="planner_optimizer",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    # Register Week 5 adapters (ByteRover, CrewAI, AutoGen)
    try:
        from ..adapters.byterover_adapter import ByteRoverAdapter

        registry.register(
            name="byterover",
            adapter_class=ByteRoverAdapter,
            adapter_type="memory",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    try:
        from ..adapters.crewai_adapter import CrewAIAdapter

        registry.register(
            name="crewai",
            adapter_class=CrewAIAdapter,
            adapter_type="agent_runtime",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available

    try:
        from ..adapters.autogen_adapter import AutoGenAdapter

        registry.register(
            name="autogen",
            adapter_class=AutoGenAdapter,
            adapter_type="council_review",
            default_enabled=False,
        )
    except ImportError:
        pass  # Adapter not available


def validate_required_adapters(required_adapters: list[str]) -> list[str]:
    """
    Validate that required adapters are registered and enabled.

    Args:
        required_adapters: List of adapter names that must be enabled

    Returns:
        List of missing or disabled adapter names
    """
    logger.info(f"Validating {len(required_adapters)} required adapters")
    registry = get_registry()
    missing = []

    for adapter_name in required_adapters:
        adapter = registry.get(adapter_name)
        if adapter is None:
            logger.warning(f"Required adapter not found: {adapter_name}")
            missing.append(adapter_name)
        else:
            logger.debug(f"Required adapter found: {adapter_name}")

    if missing:
        logger.warning(f"Missing {len(missing)} required adapters: {missing}")
    else:
        logger.info("All required adapters are available")

    return missing

