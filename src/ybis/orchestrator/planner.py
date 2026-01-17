"""
Real Planner Node - LLM-based task planning.

Analyzes task objective and generates structured plan with files to modify.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any

# LlamaIndex adapter - use registry if available, direct import as fallback
try:
    from ..adapters.registry import get_registry
    _registry = get_registry()
    _llamaindex_adapter_class = _registry.get("llamaindex_adapter", adapter_type="llm_adapter")
    if _llamaindex_adapter_class:
        LlamaIndexAdapter = _llamaindex_adapter_class
    else:
        from ..adapters.llamaindex_adapter import LlamaIndexAdapter
except (ImportError, AttributeError):
    from ..adapters.llamaindex_adapter import LlamaIndexAdapter

logger = logging.getLogger(__name__)
from ..constants import PROJECT_ROOT
from ..contracts import Plan, RunContext, Task
from ..data_plane.vector_store import VectorStore
from ..services.code_graph import CodeGraph
from ..services.error_knowledge_base import ErrorKnowledgeBase
from ..services.policy import get_policy_provider
from ..services.rag_cache import get_rag_cache
from ..syscalls.journal import append_event


def _feature_mode(value: Any) -> str:
    if isinstance(value, bool):
        return "required" if value else "disabled"
    if value is None:
        return "auto"
    value_str = str(value).lower()
    if value_str in {"required", "strict"}:
        return "required"
    if value_str in {"disabled", "false", "off", "0"}:
        return "disabled"
    return "auto"


class LLMPlanner:
    """
    LLM-based Planner - Generates execution plans from task objectives.

    Uses LiteLLM or direct provider APIs to analyze tasks and create plans.
    """

    def __init__(self, model: str | None = None, api_base: str | None = None, vector_store: VectorStore | None = None):
        """
        Initialize planner.

        Args:
            model: Model name (default from policy config)
            api_base: API base URL (default from policy config)
            vector_store: Vector store for RAG (creates new if None)
        """
        policy_provider = get_policy_provider()
        # Ensure policy is loaded
        if policy_provider._policy is None:
            policy_provider.load_profile()
        llm_config = policy_provider.get_llm_config()

        self.model = model or llm_config.get("planner_model", "ollama/llama3.2:3b")
        self.api_base = api_base or llm_config.get("api_base", "http://localhost:11434")

        # Initialize DSPy optimizer (optional, for prompt optimization) - via registry
        self.dspy_optimizer = None
        try:
            from ..adapters.registry import get_registry
            registry = get_registry()
            dspy_adapter = registry.get("dspy", adapter_type="planner_optimizer", fallback_to_default=False)
            if dspy_adapter and dspy_adapter.is_available():
                self.dspy_optimizer = dspy_adapter
        except Exception:
            pass  # DSPy is optional

        features = policy_provider.get_policy().get("features", {})
        vector_mode = _feature_mode(features.get("vector_store", "auto"))
        code_graph_mode = _feature_mode(features.get("code_graph", "auto"))
        llamaindex_mode = _feature_mode(features.get("llamaindex", "auto"))

        # Initialize vector store (with error handling)
        self.vector_store = None
        if vector_mode != "disabled":
            try:
                self.vector_store = vector_store or VectorStore()
            except (ImportError, Exception):
                if vector_mode == "required":
                    raise

        # Initialize code graph for impact analysis
        self.code_graph = None
        if code_graph_mode != "disabled":
            try:
                self.code_graph = CodeGraph(PROJECT_ROOT)
            except Exception:
                if code_graph_mode == "required":
                    raise

        # Initialize LlamaIndex adapter for context management
        self.llamaindex = None
        if llamaindex_mode != "disabled":
            try:
                self.llamaindex = LlamaIndexAdapter(PROJECT_ROOT)
            except Exception:
                if llamaindex_mode == "required":
                    raise

    def plan(self, task: Task, ctx: RunContext | None = None) -> Plan:
        """
        Generate plan from task with RAG context.

        Args:
            task: Task to plan
            ctx: Optional run context for journal events

        Returns:
            Plan object with files and instructions
        """
        # Journal: Planner start
        journal_path = ctx.run_path if ctx else PROJECT_ROOT / "platform_data"
        trace_id = ctx.trace_id if ctx else None
        append_event(
            journal_path,
            "PLANNER_START",
            {
                "task_id": task.task_id,
                "objective_length": len(task.objective),
            },
            trace_id=trace_id,
        )

        policy_provider = get_policy_provider()
        planner_mode = policy_provider.get_policy().get("planner", {}).get("mode")
        if planner_mode == "heuristic":
            plan = self._heuristic_plan(task)
            append_event(
                journal_path,
                "PLANNER_FALLBACK",
                {"reason": "heuristic mode"},
                trace_id=trace_id,
            )
            return plan

        # Query vector store for relevant context
        relevant_context = []
        if self.vector_store:
            relevant_context = self._get_relevant_context(task.objective, ctx)

        # Perform impact analysis if code graph is available
        impact_warnings = []
        if self.code_graph:
            # Extract file paths from objective (simple heuristic)
            # In a real scenario, we'd parse the plan first, but for now we'll add warnings after
            pass  # Will be added to prompt after plan generation

        # Get error context from Error Knowledge Base
        error_context = self._get_error_context(task.objective, ctx)
        context_files = []
        for ctx_item in relevant_context:
            metadata = ctx_item.get("metadata", {})
            file_path = metadata.get("file") or metadata.get("file_path")
            if file_path:
                context_files.append(file_path)
        rules_pack_available = (
            PROJECT_ROOT
            / "platform_data"
            / "knowledge"
            / "Rules"
            / "YBIS_RULES.md"
        ).exists()
        append_event(
            journal_path,
            "PLANNER_CONTEXT",
            {
                "context_items": len(relevant_context),
                "context_files": list(dict.fromkeys(context_files))[:10],
                "error_context_count": len(error_context),
                "rules_pack_available": rules_pack_available,
            },
            trace_id=trace_id,
        )

        # Try to use LiteLLM if available
        try:
            import litellm

            from ..services.resilience import ollama_retry

            system_prompt = self._get_system_prompt(relevant_context, impact_warnings, error_context)

            # Try DSPy optimizer if available (Week 3: Prompt optimization)
            plan_data = None
            elapsed_ms = 0
            if self.dspy_optimizer and self.dspy_optimizer.is_available():
                try:
                    # Use DSPy-optimized plan generation
                    plan_json = self.dspy_optimizer.generate_plan(
                        task_objective=task.objective,
                        task_title=task.title,
                    )
                    plan_data = json.loads(plan_json)
                    append_event(
                        journal_path,
                        "LLM_PLAN_DSPY",
                        {
                            "model": self.model,
                            "optimized": True,
                        },
                        trace_id=trace_id,
                    )
                except Exception as e:
                    # DSPy failed, fallback to regular LLM
                    logger.warning(f"DSPy plan generation failed: {e}, using regular LLM")
                    plan_data = None

            # Fallback to regular LLM if DSPy not used or failed
            if plan_data is None:
                # Journal: LLM plan request
                start_time = time.time()
                append_event(
                    journal_path,
                    "LLM_PLAN_REQUEST",
                    {
                        "model": self.model,
                        "prompt_length": len(system_prompt),
                    },
                    trace_id=trace_id,
                )

                @ollama_retry
                def _call_llm():
                    return litellm.completion(
                        model=self.model,
                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt,
                            },
                            {
                                "role": "user",
                                "content": f"Task: {task.title}\nObjective: {task.objective}",
                            },
                        ],
                        api_base=self.api_base,
                        response_format={"type": "json_object"},
                        timeout=30,
                    )

                response = _call_llm()
                elapsed_ms = (time.time() - start_time) * 1000

                plan_data = json.loads(response.choices[0].message.content)
            plan = self._parse_plan(plan_data, task)

            # Journal: LLM plan response
            append_event(
                journal_path,
                "LLM_PLAN_RESPONSE",
                {
                    "files_count": len(plan.files),
                    "steps_count": len(plan.steps) if hasattr(plan, "steps") else 0,
                    "response_time_ms": round(elapsed_ms, 2),
                },
                trace_id=trace_id,
            )

            # Perform impact analysis on planned files
            if self.code_graph and plan.files:
                impact_map = self.code_graph.get_impact_analysis(
                    [PROJECT_ROOT / f for f in plan.files if Path(f).suffix == ".py"]
                )
                # Add impact warnings to plan instructions
                for file_path, dependents in impact_map.items():
                    if dependents:
                        warning = self.code_graph.format_impact_warning(file_path, dependents)
                        if warning:
                            plan.instructions = f"{warning}\n\n{plan.instructions}"

            # Add referenced context to plan
            plan.referenced_context = relevant_context

            # Journal: Plan validation (if validation happens)
            # Note: Validation happens in self_improve.py, not here
            append_event(
                journal_path,
                "PLANNER_COMPLETE",
                {
                    "files_count": len(plan.files),
                    "steps_count": len(plan.steps) if hasattr(plan, "steps") else 0,
                },
                trace_id=trace_id,
            )

            return plan

        except ImportError:
            # Fallback: Simple heuristic-based planning
            append_event(
                journal_path,
                "PLANNER_FALLBACK",
                {"reason": "ImportError - litellm not available"},
                trace_id=trace_id,
            )
            return self._heuristic_plan(task)
        except Exception as e:
            # Fallback on any error
            append_event(
                journal_path,
                "PLANNER_FALLBACK",
                {"reason": f"LLM planning failed: {e}"},
                trace_id=trace_id,
            )
            print(f"LLM planning failed: {e}, using heuristic fallback")
            return self._heuristic_plan(task)

    def _get_relevant_context(self, objective: str, ctx: RunContext | None = None) -> list[dict]:
        """
        Get relevant context from vector store and LlamaIndex.

        Args:
            objective: Task objective
            ctx: Optional run context for journal events

        Returns:
            List of relevant context documents
        """
        journal_path = ctx.run_path if ctx else PROJECT_ROOT / "platform_data"
        trace_id = ctx.trace_id if ctx else None

        context_results = []

        # Try vector store first (ChromaDB/Qdrant) with caching
        if self.vector_store:
            try:
                rag_cache = get_rag_cache()
                top_k = 3

                # Check cache first
                cached_results = rag_cache.get("codebase", objective, top_k=top_k)
                if cached_results:
                    context_results.extend(cached_results)
                    append_event(
                        journal_path,
                        "RAG_CACHE_HIT",
                        {
                            "collection": "codebase",
                            "query_length": len(objective),
                            "results_count": len(cached_results),
                        },
                        trace_id=trace_id,
                    )
                else:
                    # Query vector store
                    start_time = time.time()
                    vector_results = self.vector_store.query("codebase", objective, top_k=top_k)
                    elapsed_ms = (time.time() - start_time) * 1000
                    context_results.extend(vector_results)

                    # Cache results
                    rag_cache.set("codebase", objective, vector_results, top_k=top_k)

                    # Journal: RAG query
                    append_event(
                        journal_path,
                        "RAG_QUERY",
                        {
                            "collection": "codebase",
                            "query_length": len(objective),
                            "results_count": len(vector_results),
                        "duration_ms": round(elapsed_ms, 2),
                    },
                    trace_id=trace_id,
                )
            except Exception:
                pass

        # Try LlamaIndex for deeper context (legacy + new code)
        if self.llamaindex and self.llamaindex.is_available():
            try:
                start_time = time.time()
                llamaindex_results = self.llamaindex.query_codebase(objective, top_k=3)
                elapsed_ms = (time.time() - start_time) * 1000
                # Convert LlamaIndex format to vector store format
                for result in llamaindex_results:
                    context_results.append(
                        {
                            "document": result.get("document", ""),
                            "metadata": {"file_path": result.get("file_path", "")},
                        }
                    )
                # Journal: LlamaIndex query
                append_event(
                    journal_path,
                    "LLAMAINDEX_QUERY",
                    {
                        "query": objective[:100],
                        "results_count": len(llamaindex_results),
                        "duration_ms": round(elapsed_ms, 2),
                    },
                    trace_id=trace_id,
                )
            except Exception:
                pass

        return context_results

    def _get_error_context(self, objective: str, ctx: RunContext | None = None) -> list[dict]:
        """
        Get relevant error patterns from Error Knowledge Base.

        Args:
            objective: Task objective
            ctx: Optional run context for journal events

        Returns:
            List of relevant error patterns with suggestions
        """
        journal_path = ctx.run_path if ctx else PROJECT_ROOT / "platform_data"
        trace_id = ctx.trace_id if ctx else None

        error_context = []

        try:
            error_kb = ErrorKnowledgeBase()

            # Get recent error patterns (min 2 occurrences)
            patterns = error_kb.get_error_patterns(min_occurrences=2)

            # Journal: Error KB query
            append_event(
                journal_path,
                "ERROR_KB_QUERY",
                {
                    "patterns_count": len(patterns),
                },
                trace_id=trace_id,
            )

            # Limit to top 5 most frequent patterns
            for pattern in patterns[:5]:
                error_context.append({
                    "error_type": pattern.error_type,
                    "pattern": pattern.error_message_pattern,
                    "occurrences": pattern.occurrence_count,
                    "suggestion": pattern.suggested_fix or self._generate_suggestion(pattern),
                })

            # Also get errors similar to keywords in objective
            keywords = self._extract_keywords(objective)
            for keyword in keywords[:3]:
                similar = error_kb.get_similar_errors(error_message=keyword, limit=2)
                for err in similar:
                    if err.error_type not in [e["error_type"] for e in error_context]:
                        error_context.append({
                            "error_type": err.error_type,
                            "pattern": err.error_message[:100],
                            "occurrences": 1,
                            "suggestion": f"Previous error in step '{err.step}': {err.error_message[:50]}",
                        })
        except Exception:
            pass  # Error KB is optional

        return error_context

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract relevant keywords from text."""
        import re
        # Extract potential file names, module names, function names
        words = re.findall(r'\b[a-z_][a-z0-9_]*\b', text.lower())
        # Filter out common words
        stopwords = {"the", "a", "an", "is", "are", "to", "for", "and", "or", "in", "on", "with"}
        return [w for w in words if w not in stopwords and len(w) > 3]

    def _generate_suggestion(self, pattern) -> str:
        """Generate suggestion for error pattern."""
        suggestions = {
            "syntax_error": "Run syntax check before execution. Use 'ruff check' to validate.",
            "type_error": "Add type hints and run mypy. Check function signatures.",
            "lint_error": "Run 'ruff check --fix' to auto-fix lint issues.",
            "test_failure": "Review test assertions. Check for changed interfaces.",
            "import_error": "Verify import paths. Check if module is installed.",
        }
        return suggestions.get(pattern.error_type, f"Review {pattern.error_type} errors before execution.")

    def _get_system_prompt(
        self,
        relevant_context: list[dict] | None = None,
        impact_warnings: list[str] | None = None,
        error_context: list[dict] | None = None,
    ) -> str:
        """Get system prompt for planning with RAG context."""
        # Include codebase context if available
        codebase_context = self._get_codebase_context()
        context_section = ""
        if codebase_context:
            context_section = f"\n\nYou are working in a codebase with this structure:\n{codebase_context}\n"

        # Include RAG context
        rag_section = ""
        if relevant_context:
            rag_section = "\n\nRelevant Context from Codebase:\n"
            for i, ctx in enumerate(relevant_context[:3], 1):  # Limit to top 3
                metadata = ctx.get("metadata", {})
                file_path = metadata.get("file") or metadata.get("file_path", "")
                doc_preview = ctx.get('document', '')[:500]
                if file_path:
                    rag_section += f"\n[{i}] File: {file_path}\n{doc_preview}...\n"
                else:
                    rag_section += f"\n[{i}] {doc_preview}...\n"

        # Include rules pack (authoritative quality rules)
        rules_section = ""
        rules_text = self._load_rules_pack()
        rules_rag = self._get_rules_rag_context()
        if rules_text:
            rules_section = f"\n\nRules Pack (MUST FOLLOW):\n{rules_text}\n"
        elif rules_rag:
            rules_section = "\n\nRules Pack (from RAG):\n"
            for i, ctx in enumerate(rules_rag[:2], 1):
                doc_preview = ctx.get("document", "")[:800]
                rules_section += f"\n[{i}] {doc_preview}...\n"

        # Include impact warnings
        impact_section = ""
        if impact_warnings:
            impact_section = "\n\nImpact Analysis Warnings:\n" + "\n".join(impact_warnings)

        # Include error history warnings
        error_section = ""
        if error_context:
            error_section = "\n\nKnown Error Patterns (AVOID THESE):\n"
            for _i, err in enumerate(error_context[:5], 1):
                error_section += f"\n[!] {err['error_type']} (seen {err['occurrences']}x): {err['suggestion']}\n"

        return f"""You are a code planning assistant. Analyze the task and generate a JSON plan with:
{{
  "objective": "Clear description of what to do",
  "files": ["list", "of", "file", "paths"],
  "instructions": "Step-by-step instructions",
  "steps": [
    {{"action": "step 1 description", "files": ["file1.py"], "description": "detailed description"}},
    {{"action": "step 2 description", "files": ["file2.py"], "description": "detailed description"}}
  ]
}}

IMPORTANT: The "steps" array is REQUIRED and must contain at least one step. Each step should have:
- "action": A clear action description (e.g., "Create add_numbers.py file")
- "files": List of files this step will create/modify
- "description": Detailed description of what this step does

Identify which files need to be modified based on the task objective.{context_section}{rag_section}{rules_section}{impact_section}{error_section}"""

    def _load_rules_pack(self) -> str:
        """Load rules pack for quality guidance."""
        rules_path = PROJECT_ROOT / "platform_data" / "knowledge" / "Rules" / "YBIS_RULES.md"
        if not rules_path.exists():
            return ""
        try:
            content = rules_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = rules_path.read_text(encoding="utf-8", errors="ignore")
        return content.strip()

    def _get_rules_rag_context(self) -> list[dict]:
        """Query RAG for rules-related context if available."""
        if not self.vector_store:
            return []
        try:
            return self.vector_store.query("knowledge", "YBIS rules quality planning", top_k=2)
        except Exception:
            return []

    def _get_codebase_context(self) -> str:
        """
        Get codebase context for planning.

        Returns:
            Codebase summary string
        """
        try:
            from ..constants import PROJECT_ROOT
            from ..services.knowledge import scan_codebase

            # Scan both src/ybis and src/agentic (legacy)
            ybis_root = PROJECT_ROOT / "src" / "ybis"
            agentic_root = PROJECT_ROOT / "src" / "agentic"

            context_parts = []

            if ybis_root.exists():
                ybis_context = scan_codebase(ybis_root)
                context_parts.append("Current Platform (src/ybis):")
                context_parts.append(ybis_context)

            if agentic_root.exists():
                agentic_context = scan_codebase(agentic_root)
                context_parts.append("\nLegacy Codebase (src/agentic):")
                context_parts.append(agentic_context)

            return "\n".join(context_parts) if context_parts else ""
        except Exception:
            return ""  # Fallback to no context

    def _parse_plan(self, plan_data: dict[str, Any], task: Task) -> Plan:
        """
        Parse LLM response into Plan object.

        Args:
            plan_data: Parsed JSON from LLM
            task: Original task

        Returns:
            Plan object
        """
        # Extract steps from plan_data
        steps = plan_data.get("steps", [])

        # If no steps provided, create a default step from instructions
        if not steps and plan_data.get("instructions"):
            steps = [{
                "action": plan_data.get("instructions", "Execute plan"),
                "files": plan_data.get("files", []),
                "description": plan_data.get("objective", task.objective),
            }]

        # If still no steps, create a minimal step
        if not steps:
            steps = [{
                "action": f"Implement: {task.objective}",
                "files": plan_data.get("files", []),
                "description": task.objective,
            }]

        return Plan(
            objective=plan_data.get("objective", task.objective),
            files=plan_data.get("files", []),
            instructions=plan_data.get("instructions", ""),
            steps=steps,  # Include steps!
        )

    def _heuristic_plan(self, task: Task) -> Plan:
        """
        Fallback heuristic planning.

        Args:
            task: Task to plan

        Returns:
            Plan object
        """
        import re

        # Extract file paths from objective
        files = []
        # Look for common file patterns
        file_patterns = [
            r"(\w+\.py)",
            r"(\w+\.ts)",
            r"(\w+\.js)",
            r"([\w/]+\.\w+)",
        ]

        for pattern in file_patterns:
            matches = re.findall(pattern, task.objective)
            files.extend(matches)

        # Remove duplicates
        files = list(set(files))

        # Create at least one step for heuristic plan
        steps = [{
            "action": f"Implement: {task.title}",
            "files": files if files else [],
            "description": task.objective,
        }]

        return Plan(
            objective=task.objective,
            files=files,
            instructions=f"Execute task: {task.title}",
            steps=steps,  # Include steps!
        )


def plan_task(task: Task, ctx: RunContext | None = None) -> Plan:
    """
    Plan a task using LLM planner.

    Args:
        task: Task to plan
        ctx: Optional run context for journal events

    Returns:
        Plan object
    """
    planner = LLMPlanner()
    return planner.plan(task, ctx)
