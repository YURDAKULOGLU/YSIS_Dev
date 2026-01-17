================================================================================
LOGGING COVERAGE ANALYSIS
================================================================================

## SUMMARY
--------------------------------------------------------------------------------
Adapters: 5/6 have logger (83.3%)
Adapters: 1/6 use journal (16.7%)
Nodes: 0/7 have logger (0.0%)
Nodes: 4/7 use journal (57.1%)

## ADAPTERS WITHOUT LOGGING
--------------------------------------------------------------------------------
⚠️  dspy_adapter: Methods without logging: is_available
⚠️  llamaindex_adapter: Methods without logging: is_available
⚠️  mem0_adapter: Methods without logging: get_mode

## NODES WITHOUT LOGGING
--------------------------------------------------------------------------------
⚠️  execution: Methods without logging: verify_node
❌ experimental: No logging
⚠️  gate: Methods without logging: gate_node, should_retry
❌ plan: No logging
❌ validation: No logging
