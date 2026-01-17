================================================================================
COMPREHENSIVE PROJECT COVERAGE ANALYSIS
================================================================================

## OVERALL SUMMARY
--------------------------------------------------------------------------------
Total Files Analyzed: 82
Files with Tests: 36/82 (43.9%)
Files with Logger: 57/82 (69.5%)
Files with Journal: 39/82 (47.6%)

## ADAPTERS
--------------------------------------------------------------------------------
Total: 19
Without Tests: 6
  ❌ aiwaves_agents
  ❌ observability_langfuse
  ❌ observability_opentelemetry
  ❌ self_improve_swarms
  ❌ vector_store_chroma
  ❌ vector_store_qdrant
Without Logger: 10
  ⚠️  aiwaves_agents
  ⚠️  e2b_sandbox
  ⚠️  evoagentx
  ⚠️  graph_store_neo4j
  ⚠️  llamaindex_adapter
  ⚠️  llm_council
  ⚠️  reactive_agents
  ⚠️  self_improve_swarms
  ⚠️  vector_store_chroma
  ⚠️  vector_store_qdrant

## NODES
--------------------------------------------------------------------------------
Total: 7
Without Tests: 7
  ❌ execution
  ❌ experimental
  ❌ factory
  ❌ gate
  ❌ plan
  ❌ spec
  ❌ validation
Without Logger: 1
  ⚠️  factory

## SERVICES
--------------------------------------------------------------------------------
Total: 42
Without Tests: 31
  ❌ adapter_bootstrap
  ❌ adapter_catalog
  ❌ circuit_breaker_simple
  ❌ code_graph
  ❌ dashboard
  ❌ error_knowledge_base
  ❌ file_cache
  ❌ ingestor
  ❌ knowledge
  ❌ lesson_engine
  ❌ llm_cache
  ❌ llm_cache_gptcache
  ❌ model_router
  ❌ programmatic_tools
  ❌ rag_cache
Without Logger: 13
  ⚠️  code_graph
  ⚠️  dashboard
  ⚠️  debate
  ⚠️  error_knowledge_base
  ⚠️  ingestor
  ⚠️  knowledge
  ⚠️  lesson_engine
  ⚠️  model_router
  ⚠️  staleness
  ⚠️  staleness_hook
  ⚠️  story_sharder
  ⚠️  task_board
  ⚠️  artifact_tools

## DATA PLANE
--------------------------------------------------------------------------------
Total: 4
Without Tests: 0
Without Logger: 0

## DETAILED ISSUES
--------------------------------------------------------------------------------
### Methods Without Logging
adapters/aiwaves_agents: is_available, learn, update_pipeline
adapters/dspy_adapter: is_available
adapters/e2b_sandbox: is_available, execute, create
adapters/evoagentx: is_available, evolve, score
adapters/graph_store_neo4j: is_available, impact_analysis, find_circular_dependencies
adapters/llamaindex_adapter: is_available
adapters/llm_council: is_available
adapters/mem0_adapter: get_mode
adapters/observability_langfuse: is_available, trace_generation, trace_span
adapters/observability_opentelemetry: is_available, start_span
adapters/reactive_agents: is_available, run, supports_tools
adapters/self_improve_swarms: is_available, reflect, plan
adapters/vector_store_chroma: is_available, add_documents, query
adapters/vector_store_qdrant: is_available, add_documents, query
nodes/execution: verify_node
nodes/gate: gate_node, should_retry
services/adapter_bootstrap: bootstrap_adapters, validate_required_adapters
services/adapter_catalog: get_catalog, get_adapter, list_adapters
services/backup: list_backups
services/circuit_breaker: get_breaker, get_breaker_status, get_all_breaker_status
services/circuit_breaker_simple: get_state, is_open, reset
services/code_graph: get_dependencies, get_impact_analysis, format_impact_warning
services/dashboard: get_db_data, main
services/debate: to_dict, conduct_debate
services/error_knowledge_base: record_from_verifier_report, get_similar_errors, get_insights_for_task
services/event_bus: get_event_bus, is_available, publish
services/file_cache: get_file_cache, get, set
services/ingestor: ingest_codebase
services/knowledge: scan_codebase
services/lesson_engine: generate_auto_policy, apply_lessons_to_policy
services/llm_cache: get_llm_cache, get_stats, clear_expired
services/llm_cache_gptcache: get_stats
services/model_router: get_model_router, get_model_for_task, get_api_base
services/observability: get_observability_service, trace_generation, start_span
services/policy: get_policy_provider, load_profile, get_policy
services/programmatic_tools: orchestrate
services/rag_cache: get_rag_cache, get, set
services/rate_limiter: get_limiter_status
services/resilience: retry_with_backoff, decorator, decorator
services/shutdown_manager: is_shutting_down, unregister_shutdown_handler, shutdown_aware
services/staleness: detect_staleness, get_changed_since_last_check, update_last_check
services/staleness_hook: run_staleness_check_sync
services/story_sharder: get_story_sharder, shard_task
services/task_board: get_task_board
services/tool_registry: register_tool, search_tools, get_tool
services/test_tools: run_test_sync
data_plane/journal: append_event
data_plane/vector_store: get_collection
data_plane/workspace: init_run_structure
