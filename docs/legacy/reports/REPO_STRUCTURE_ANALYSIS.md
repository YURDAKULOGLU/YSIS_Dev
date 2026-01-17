# YBIS_Dev Repository Structure Analysis
## Comprehensive Documentation for AI Agents

> **Purpose:** This document provides a complete overview of the repository structure, explaining what each directory and key file contains, their purposes, and how they relate to the overall system architecture.

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Root Directory Structure](#root-directory-structure)
3. [Core Source Code (`src/`)](#core-source-code-src)
4. [Scripts & Tools (`scripts/`)](#scripts--tools-scripts)
5. [Documentation (`docs/`)](#documentation-docs)
6. [Knowledge Base (`Knowledge/`)](#knowledge-base-knowledge)
7. [Workspaces (`workspaces/`)](#workspaces-workspaces)
8. [Organ Systems (`organs/`)](#organ-systems-organs)
9. [Tests (`tests/`)](#tests-tests)
10. [Configuration (`config/`)](#configuration-config)
11. [Legacy Code (`legacy/`)](#legacy-code-legacy)
12. [Infrastructure Files](#infrastructure-files)

---

## System Overview

**YBIS_Dev** is a **Tier 4.5 Autonomous Software Factory** that uses:
- **LangGraph** for orchestration (state machine management)
- **Pydantic** for data validation and type safety
- **SQLite** (aiosqlite) for task persistence
- **Aider** for code generation
- **Git** for version control and cleanup

**Current Status:** ACTIVE - STABLE  
**Version:** 4.5.0  
**Main Entry Point:** `scripts/run_orchestrator.py` or `src/orchestrator/runner.py`

---

## Root Directory Structure

### Key Files at Root

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation and quick start guide |
| `AI_START_HERE.md` | **MANDATORY** onboarding document for AI agents |
| `SYSTEM_STATE.md` | Current system state, architecture, and health status |
| `ARCHITECTURE.md` | High-level architecture overview |
| `ARCHITECTURE_V2.md` | Detailed architecture v4.5 (LangGraph + Pydantic + SQLite) |
| `DOC_INDEX.md` | Navigation map for all documentation |
| `pyproject.toml` | Python project configuration (Ruff, MyPy, Pytest) |
| `requirements.txt` | Python dependencies (LangGraph, LangChain, Pydantic, etc.) |
| `docker-compose.yml` | Docker orchestration for services |
| `workflow-registry.yaml` | Workflow definitions registry |

### Important Markdown Files

- `404_CAUSES_EXPLAINED.md` - Analysis of 404 errors
- `404_FIX_REPORT.md` - Fix report for 404 issues
- `DUPLICATE_CHECK_REPORT.md` - Duplicate file analysis
- `PERFORMANCE_SUMMARY.md` - Performance metrics
- `SCRAPER_PERFORMANCE_OPTIMIZATION.md` - Scraper optimization notes

---

## Core Source Code (`src/`)

The main application code lives here. This is the **active codebase** that agents should modify.

### `src/agentic/` - Core Agentic System

**Main Components:**

#### `src/agentic/core/` - Core Infrastructure
- **`config.py`** - **CRITICAL**: Single source of truth for all paths and configuration
  - `PROJECT_ROOT` - Base project path
  - `TASKS_DB_PATH` - SQLite database location
  - All environment variable handling
- **`protocols.py`** - **CRITICAL**: Pydantic models for all data structures
  - `TaskState` - Main state model for LangGraph
  - `Plan`, `CodeResult`, `VerificationResult` - Task artifacts
  - All data contracts between components
- **`graphs/orchestrator_graph.py`** - **THE BRAIN**: Main LangGraph workflow
  - State machine that orchestrates PLAN → EXECUTE → VERIFY → COMMIT
- **`executors/aider_executor.py`** - Code generation executor using Aider
- **`executors/openhands_executor.py`** - Alternative executor using OpenHands
- **`logger.py`** - Centralized logging (loguru wrapper)
- **`constants.py`** - Default configuration values

#### `src/agentic/core/execution/` - Execution Safety
- **`sandbox.py`** - Sandboxed code execution
- **`guardrails.py`** - Security guardrails
- **`command_allowlist.py`** - Allowed command whitelist
- **`aci.py`** - Application Container Isolation

#### `src/agentic/core/llm/` - LLM Providers
- **`base.py`** - Base LLM interface
- **`litellm_provider.py`** - LiteLLM integration (unified provider)
- **`provider_factory.py`** - Factory for creating LLM instances
- **`providers/`** - Specific provider implementations

#### `src/agentic/core/memory/` - Memory & RAG
- **`manager.py`** - Memory management interface
- **`cognee_provider.py`** - Cognee RAG provider

#### `src/agentic/core/plugin_system/` - Plugin Architecture
- Plugin loading and management system
- Protocol-based plugin interface

#### `src/agentic/core/plugins/` - Built-in Plugins
- 33 plugin files implementing various capabilities
- Each plugin follows the protocol interface

#### `src/agentic/bridges/` - External Framework Bridges
- **`council_bridge.py`** - Council AI integration
- **`crewai_bridge.py`** - CrewAI integration
- **`mem0_bridge.py`** - Mem0 memory integration
- **`interpreter_bridge.py`** - Open Interpreter integration
- **`swarm_bridge.py`** - Swarm framework integration
- **`investigator_bridge.py`** - Investigation tools
- **`evo_bridge.py`** - EvoAgentX integration

#### `src/agentic/infrastructure/` - Infrastructure Layer
- **`db.py`** - **CRITICAL**: SQLite task database interface (aiosqlite)
- **`task_manager.py`** - Task lifecycle management
- **`messaging.py`** - Agent messaging system
- **`unified_message_manager.py`** - Unified messaging interface
- **`redis_queue.py`** - Redis message queue
- **`graph_db.py`** - Neo4j graph database interface

#### `src/agentic/intelligence/` - Intelligence Layer
- **`debate_manager.py`** - Multi-agent debate system
- **`poetiq_bridge.py`** - Poetiq ARC solver integration

#### `src/agentic/skills/` - Specialized Skills
- **`spec_writer.py`** - Specification writing
- **`code_graph.py`** - Code dependency graph analysis
- **`ccpm_manager.py`** - Critical Chain Project Management

#### `src/agentic/mcp_server.py` - MCP Server
- Model Context Protocol server
- Exposes tools for task management, messaging, memory

#### `src/agentic/crews/` - CrewAI Crews
- **`planning_crew.py`** - Planning crew implementation

#### `src/agentic/graph/` - Graph Workflow
- **`workflow.py`** - Workflow definitions
- **`state.py`** - State management
- **`nodes/`** - Individual graph nodes

### `src/dashboard/` - Web Dashboard
- **`app.py`** - Streamlit dashboard application
- **`chainlit_app.py`** - Chainlit chat interface
- **`components/`** - Dashboard components
  - `health_monitor.py` - System health monitoring
  - `hive_visualizer.py` - Hive architecture visualization
  - `lessons_viewer.py` - Lessons learned viewer
- **`viz/`** - Visualization frontend (TypeScript/React)

### `src/orchestrator/` - Orchestration Runner
- **`runner.py`** - Main orchestrator runner (alternative entry point)
- **`config.py`** - Orchestrator configuration

### `src/sentinel/` - Verification System
- **`main.py`** - Sentinel verifier (AST analysis, linting, testing)

### `src/monitoring/` - Code Quality Monitoring
- **`code_quality_monitor.py`** - Code quality tracking
- **`regression_detection.py`** - Regression detection
- **`code_complexity.py`** - Complexity analysis

### Other `src/` Subdirectories
- **`bridges/`** - Base bridge interfaces
- **`capabilities/`** - Capability implementations (git_ops, sandbox)
- **`components/`** - React/TypeScript components
- **`discovery/`** - Plugin discovery
- **`infrastructure/`** - Infrastructure utilities
- **`intelligence/`** - Intelligence utilities
- **`memory/`** - Memory wrappers
- **`modules/`** - Module definitions
- **`planner/`** - Planning utilities
- **`plugins/`** - TypeScript plugin interfaces
- **`quality_monitoring/`** - Quality metrics
- **`security/`** - Security layers
- **`services/`** - Service implementations
- **`utils/`** - Utility functions

---

## Scripts & Tools (`scripts/`)

All executable scripts and tools. **Primary entry point for running tasks.**

### Main Entry Points

| Script | Purpose | Usage |
|--------|---------|-------|
| **`ybis_run.py`** | **CANONICAL ENTRY POINT** - Run single task | `python scripts/ybis_run.py TASK-123` |
| **`ybis_worker.py`** | **BACKGROUND WORKER** - Continuous task processing | `python scripts/ybis_worker.py` |
| **`ybis.py`** | **MCP CLI** - Unified messaging and task operations | `python scripts/ybis.py message send/read/ack` |
| **`smart_exec.py`** | **CRITICAL**: Quiet command execution (saves tokens) | `python scripts/smart_exec.py <command>` |
| **`run_orchestrator.py`** | ~~Legacy~~ → Use `ybis_run.py` instead | ~~Deprecated~~ |

### Task Management

- **`add_task.py`** - Add new task to database
- **`diagnose_tasks.py`** - Diagnose task issues
- **`test_unified_task.py`** - Test task system

### Health & Diagnostics

- **`system_health_check.py`** - System health check
- **`check_quality.py`** - Code quality check
- **`check_rag_quality.py`** - RAG quality check
- **`check_graph.py`** - Graph validation
- **`final_pulse.py`** - Final system pulse check

### Knowledge & Ingestion

- **`auto_scrape_package_docs.py`** - Auto-scrape package documentation
- **`ingest_knowledge.py`** - Ingest knowledge into RAG
- **`ingest_framework_docs_to_rag.py`** - Ingest framework docs
- **`ingest_code_graph.py`** - Ingest code dependency graph
- **`ingest_graph.py`** - Ingest graph data
- **`fetch_docs.py`** - Fetch documentation
- **`check_scraped_status.py`** - Check scraping status

### Framework Management

- **`install_framework.py`** - Install framework packages
- **`verify_framework_installation.py`** - Verify framework installs
- **`ensure_dependencies.py`** - Ensure dependencies are installed

### Testing & Verification

- **`verify_code.py`** - Verify code changes
- **`verify_propagation.py`** - Verify change propagation
- **`test_services.py`** - Test services
- **`test_mcp_server.py`** - Test MCP server
- **`test_event_bus.py`** - Test event bus

### Missions (`scripts/missions/`)

Pre-defined mission scripts:
- **`run_bootstrap_phase2.py`** - Bootstrap phase 2
- **`run_build_dashboard.py`** - Build dashboard
- **`run_build_rag.py`** - Build RAG system
- **`run_fix_core_tests.py`** - Fix core tests
- **`run_fix_governance.py`** - Fix governance
- **`run_fix_memory.py`** - Fix memory system
- **`run_fix_sentinel.py`** - Fix sentinel
- **`run_stress_test_suite.py`** - Stress testing
- **`run_tier3_step1.py`** - Tier 3 step 1
- **`run_weather_mission.py`** - Weather mission example
- And many more...

### Utilities (`scripts/utils/`)

- **`debug_ollama_models.py`** - Debug Ollama models
- **`debug_orchestrator_boot.py`** - Debug orchestrator startup
- **`debug_rag.py`** - Debug RAG system
- **`error_parser.py`** - Parse errors

### Other Important Scripts

- **`listen.py`** - Redis listener (event bus)
- **`worker.py`** - Worker process
- **`rebuild_sentinel.py`** - Rebuild sentinel
- **`enforce_architecture.py`** - Enforce architecture rules
- **`normalize_ascii.py`** - Normalize ASCII characters
- **`worktree_cleanup.py`** - Clean up Git worktrees
- **`worktree_list.py`** - List Git worktrees

---

## Documentation (`docs/`)

Comprehensive documentation for agents and developers.

### `docs/governance/` - Governance & Constitution

**CRITICAL READING FOR ALL AGENTS**

- **`00_GENESIS/YBIS_CONSTITUTION.md`** - **SUPREME LAW**: All agents must follow
- **`00_GENESIS/AGENT_CONTRACT.md`** - Agent contract
- **`00_GENESIS/CODE_STANDARDS.md`** - Code standards
- **`00_GENESIS/ARCHITECTURE_PRINCIPLES.md`** - Architecture principles
- **`YBIS_CONSTITUTION.md`** - Main constitution (may be duplicate)

#### `docs/governance/10_META/` - Meta Governance

- **`Agent_Profiles/`** - Agent role profiles (Architect, Developer, QA, UX, ProductManager)
- **`Agent_Registry/Agent_Registry.yaml`** - Agent registry
- **`Governance/`** - Governance documents
  - `1_PRINCIPLES.md` - Core principles
  - `2_ROLES.md` - Role definitions
  - `3_PROTOCOLS.md` - Protocols
  - `4_SECURITY.md` - Security guidelines
  - `agents.yaml` - Agent definitions
  - `INFORMATION_HIERARCHY.md` - Information hierarchy
- **`Strategy/`** - Strategic documents
  - `DEVELOPMENT_ROADMAP.md` - Development roadmap
  - `EVOLUTION_PLAN.md` - Evolution plan
  - `PRODUCT_ROADMAP.md` - Product roadmap
  - `SYSTEM_ROADMAP.md` - System roadmap

### `docs/specs/` - Specifications

- **`GOVERNANCE_ACTION_PLAN.md`** - Governance action plan
- **`STABLE_VNEXT_ROADMAP.md`** - Next stable version roadmap
- **`UAP_MIGRATION_GUIDE.md`** - Unified Agent Protocol migration
- **`MCP_MESSAGING_CUTOVER_PLAN.md`** - MCP messaging cutover
- **`FRAMEWORK_DOC_QUALITY_GATE.md`** - Framework doc quality gates
- **`ENTERPRISE_STABILIZATION.md`** - Enterprise stabilization
- **`mission_tasks/`** - Mission task specifications

### Other Documentation

- **`AGENTS_ONBOARDING.md`** - Agent onboarding guide
- **`EXTERNAL_AGENTS_PIPELINE.md`** - External agents pipeline
- **`GOLDEN_TASKS.md`** - Golden task examples
- **`META_PLANES.md`** - Meta planes documentation
- **`MULTI_AGENT.md`** - Multi-agent system docs
- **`PROMPTS_WORKFLOWS.md`** - Prompts and workflows
- **`protocols.md`** - Protocol definitions
- **`SETUP.md`** - Setup instructions
- **`system_overview.md`** - System overview
- **`SYSTEM_LESSONS.md`** - Lessons learned
- **`UAP_MIGRATION_GUIDE.md`** - UAP migration guide

---

## Knowledge Base (`Knowledge/`)

Central knowledge repository for the system.

### `Knowledge/LocalDB/` - Local Database

- **`tasks.db`** - **CRITICAL**: SQLite database for all tasks
  - Source of truth for task status, metadata, history
  - Accessed via `src/agentic/infrastructure/db.py`
- **`chroma_db/`** - ChromaDB vector database for embeddings
- **`TASK_BOARD.md`** - Task board documentation

### `Knowledge/Frameworks/` - Framework Documentation

**Extensive collection of framework documentation** (scraped and indexed):
- Agent frameworks: CrewAI, AutoGen, LangGraph, MemGPT, etc.
- LLM providers: LiteLLM, OpenAI, Anthropic, Google, etc.
- Infrastructure: FastAPI, Streamlit, Redis, Neo4j, etc.
- Tools: Ruff, Pytest, Selenium, etc.
- Each framework has `metadata.json` and documentation files

### `Knowledge/API_References/` - API References

- `langgraph_docs.md`, `langgraph_api.md`, `langgraph_concepts.md`
- `crewai_docs.md`, `crewai_advanced.md`
- `fastapi_docs.md`
- `mcp_docs.md`
- `mem0_full_config.md`
- `streamlit_docs.md`
- `transformers_docs.md`
- And more...

### `Knowledge/Messages/` - Agent Messaging

- **`inbox/`** - Incoming messages (JSON format)
- **`outbox/`** - Outgoing messages (JSON format)
- **`debates/`** - Debate threads (JSON format)
- **`README.md`** - Messaging documentation

### `Knowledge/Context/` - Project Context

- `PROJECT_CONTEXT.md` - Project context
- `lessons_learned.md` - Lessons learned
- `FEEDBACK_LOOP_IMPLEMENTATION.md` - Feedback loop docs
- `ARTIFACT_PREVENTION_SYSTEM.md` - Artifact prevention

### `Knowledge/Bootstrap/` - Bootstrap

- `BOOTSTRAP_PROTOCOL.md` - Bootstrap protocol
- `SYSTEM_INVENTORY.md` - System inventory

### `Knowledge/Errors/` - Error Logs

- **`Linting/`** - Linting error logs (JSON format)
  - Timestamped error files

### `Knowledge/Logs/` - System Logs

- Various log files for different components
- `lessons.jsonl` - Lessons learned (JSONL format)
- `staleness.jsonl` - Staleness detection logs

### `Knowledge/Reports/` - Reports

- `GOVERNANCE_DOC_CONFLICTS_PATCH_PLAN.md`
- `META_TECH_AUDIT_2025.txt`

### `Knowledge/Tasks/` - Task Definitions

- **`backlog/`** - Backlog tasks (Markdown)
- **`done/`** - Completed tasks (Markdown)
- **`README.md`** - Task documentation

### `Knowledge/VectorDB/` - Vector Database

- ChromaDB vector store files
- Used for RAG and semantic search

---

## Workspaces (`workspaces/`)

Task workspaces where agents work on individual tasks.

### `workspaces/active/` - Active Task Workspaces

Each task gets its own workspace directory:
- **Structure:**
  - `docs/PLAN.md` - Task plan (with YAML frontmatter)
  - `docs/RUNBOOK.md` - Execution runbook
  - `artifacts/RESULT.md` - Task result
  - `CHANGES/` - Change logs
  - `META.json` - Task metadata

**Example:** `workspaces/active/TASK-New-1005/`

### `workspaces/archive/` - Archived Workspaces

Completed tasks are archived here:
- Organized by year/month: `workspaces/archive/2025/12/TASK-ID/`

### `workspaces/sub_factory/` - Sub-Factory

Independent sub-factory implementation:
- Has its own `src/`, `scripts/`, `config/`
- Separate `pyproject.toml` and `requirements.txt`

### `workspaces/templates/` - Templates

- `PLAN_TEMPLATE.md` - Plan template

### `workspaces/worktrees/` - Git Worktrees

Git worktrees for isolated task work (one per active task)

---

## Organ Systems (`organs/`)

**"Self-Healing Frankenstein"** approach: Integrate best components from various AI frameworks.

### Major Organ Systems

Each subdirectory is a complete framework/organ:

1. **`agent-zero/`** - Agent Zero framework
2. **`agentforge/`** - AgentForge framework
3. **`autogen/`** - AutoGen (Microsoft)
4. **`autogpt/`** - AutoGPT
5. **`babyagi/`** - BabyAGI
6. **`chatdev/`** - ChatDev
7. **`crewai/`** - CrewAI (integrated via bridge)
8. **`dspy/`** - DSPy (Declarative Self-improving Python)
9. **`embedchain/`** - Embedchain
10. **`evoagentx/`** - EvoAgentX
11. **`flowise/`** - Flowise
12. **`gpt-pilot/`** - GPT Pilot
13. **`gpt-researcher/`** - GPT Researcher
14. **`langfuse/`** - LangFuse (observability)
15. **`langroid/`** - Langroid
16. **`llamaindex/`** - LlamaIndex
17. **`memgpt/`** - MemGPT
18. **`metagpt/`** - MetaGPT
19. **`microsoft-agent-framework/`** - Microsoft Agent Framework
20. **`mlflow/`** - MLflow
21. **`open-interpreter/`** - Open Interpreter
22. **`opendevin/`** - OpenDevin
23. **`OpenHands/`** - OpenHands
24. **`semantic-kernel/`** - Semantic Kernel
25. **`superagi/`** - SuperAGI
26. And many more...

**Purpose:** These are reference implementations and potential integration targets. The system uses bridges to connect to these frameworks rather than directly importing them.

---

## Tests (`tests/`)

Test suite for the system.

### Test Structure

- **`conftest.py`** - Pytest configuration
- **`unit/`** - Unit tests
  - `test_math_helper.py`, `test_string_reverser.py`, etc.
- **`integration/`** - Integration tests
  - `test_run_orchestrator_smoke.py` - Orchestrator smoke test
  - `test_testcontainers_smoke.py` - Testcontainers test
- **`e2e/`** - End-to-end tests
  - `test_playwright_smoke.py` - Playwright E2E test
- **`regression_tests/`** - Regression tests
  - `test_code_quality.py` - Code quality regression
- **`core/`** - Core tests
- **`test_orchestrator_graph.py`** - Orchestrator graph test
- **`test_sentinel.py`** - Sentinel test
- **`test_aider_executor.py`** - Aider executor test
- **`test_mcp_server.py`** - MCP server test
- **`stress_test_system.py`** - Stress tests

---

## Configuration (`config/`)

Configuration files for the system.

- **`settings.json`** - Main settings
- **`aider_model_settings.yml`** - Aider model configuration
- **`code_quality_thresholds.json`** - Code quality thresholds
- **`integration_settings.json`** - Integration settings

---

## Legacy Code (`legacy/`)

**READ-ONLY**: Historical code and archives. **DO NOT MODIFY.**

### Structure

- **`_Archive/`** - Historical archives
  - `125325kas2025/` - Archive from specific date
  - `Agentic_v1/` - Version 1 agentic system
  - `consolidated_2025_12_22/` - Consolidated archive
- **`20_WORKFORCE/`** - Workforce-related legacy code
  - `01_Python_Core/` - Python core implementations
  - `05_AutoGen_Team/` - AutoGen team code
- **`30_INFRASTRUCTURE/`** - Infrastructure legacy
- **`99_ARCHIVE/`** - General archive
  - `Legacy_Structure/` - Legacy structure
  - `v4_orchestrator/` - Version 4 orchestrator
- **`cleanup_20251224/`** - Cleanup scripts
- **`old_tests/`** - Old test files
- **`Workflows/`** - Legacy workflow definitions
  - `commands/` - Command definitions
  - `definitions/` - Workflow YAML files

**Rule:** Agents should NOT modify anything in `legacy/`. It is for reference only.

---

## Infrastructure Files

### Docker

- **`docker-compose.yml`** (root) - Main Docker Compose
- **`docker/`** - Docker configuration
  - `docker-compose.yml` - Docker services
  - `Dockerfile.sandbox` - Sandbox container
  - `Dockerfile.worker` - Worker container
  - `README.md` - Docker documentation

### Other Infrastructure

- **`worker/worker_process.ts`** - TypeScript worker process
- **`rag/local_rag.py`** - Local RAG implementation
- **`state_management/state_object.py`** - State management

---

## Key Paths & Constants

### Critical Paths (from `src/agentic/core/config.py`)

```python
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
TASKS_DB_PATH = PROJECT_ROOT / "Knowledge" / "LocalDB" / "tasks.db"
CHROMA_DB_PATH = PROJECT_ROOT / "Knowledge" / "LocalDB" / "chroma_db"
CONSTITUTION_PATH = PROJECT_ROOT / "docs" / "governance" / "00_GENESIS" / "YBIS_CONSTITUTION.md"
```

### Workspace Paths

- Active: `workspaces/active/<TASK_ID>/`
- Archive: `workspaces/archive/YYYY/MM/<TASK_ID>/`
- Worktrees: `workspaces/worktrees/<TASK_ID>/`

---

## System Flow

### Task Execution Flow

1. **Task Creation**: Task added to `Knowledge/LocalDB/tasks.db`
2. **Task Claiming**: Agent claims task via `scripts/run_orchestrator.py` or MCP
3. **Workspace Creation**: Workspace created in `workspaces/active/<TASK_ID>/`
4. **Planning**: Planner generates `docs/PLAN.md`
5. **Execution**: Executor (Aider) modifies code in `src/` and `tests/`
6. **Verification**: Sentinel verifies changes (AST, lint, test)
7. **Commit**: GitManager commits changes atomically
8. **Archive**: Workspace moved to `workspaces/archive/`

### Data Flow

- **Tasks**: SQLite (`Knowledge/LocalDB/tasks.db`)
- **Memory/RAG**: ChromaDB (`Knowledge/LocalDB/chroma_db/`)
- **Messages**: SQLite + JSON files (`Knowledge/Messages/`)
- **Code**: Git repository
- **Knowledge**: Vector DB + Markdown files (`Knowledge/Frameworks/`)

---

## Important Rules for AI Agents

1. **PATH INTEGRITY**: Always use `src.agentic.core.config` for paths, never hardcode
2. **TEST-FIRST**: New logic must have unit tests in `tests/unit/`
3. **CLEAN WORKSPACE**: Only modify `src/` and `tests/`, never `legacy/`
4. **STATE VALIDATION**: Use Pydantic models from `protocols.py`
5. **TOOL-BASED**: Use MCP tools or `scripts/ybis.py` for operations, don't edit DB directly
6. **ARTIFACTS**: Every task must produce PLAN, RUNBOOK, RESULT, META
7. **SMART EXEC**: Use `scripts/smart_exec.py` for commands to save tokens
8. **CONSTITUTION**: Read and follow `docs/governance/YBIS_CONSTITUTION.md`

---

## Quick Reference

### Where to Find Things

| What | Where |
|------|-------|
| **Main entry point** | `scripts/run_orchestrator.py` |
| **Task database** | `Knowledge/LocalDB/tasks.db` |
| **Core code** | `src/agentic/core/` |
| **Orchestrator graph** | `src/agentic/core/graphs/orchestrator_graph.py` |
| **Protocols/models** | `src/agentic/core/protocols.py` |
| **Configuration** | `src/agentic/core/config.py` |
| **Constitution** | `docs/governance/00_GENESIS/YBIS_CONSTITUTION.md` |
| **Agent onboarding** | `AI_START_HERE.md` |
| **System state** | `SYSTEM_STATE.md` |
| **Active workspaces** | `workspaces/active/` |
| **Framework docs** | `Knowledge/Frameworks/` |
| **Tests** | `tests/` |

---

## Summary

**YBIS_Dev** is a sophisticated autonomous software factory with:
- **Modular architecture** using LangGraph for orchestration
- **Type-safe data flow** using Pydantic
- **Persistent task management** using SQLite
- **Code generation** using Aider
- **Comprehensive knowledge base** with RAG capabilities
- **Multi-agent coordination** via messaging and debates
- **Extensive framework integration** via bridges
- **Strict governance** via Constitution

The system follows a "Self-Healing Frankenstein" philosophy, integrating the best components from various AI frameworks while maintaining a clean, protocol-based architecture.

---

**Last Updated:** 2025-01-04  
**Document Version:** 1.0  
**For AI Agents:** Read `AI_START_HERE.md` first, then `SYSTEM_STATE.md`, then this document.


