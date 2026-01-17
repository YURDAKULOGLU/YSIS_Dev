"""
SimplePlanner V2 - Universal AI Provider Support
Uses LiteLLM for multi-provider support with caching and fallbacks.
"""

import json
import os
from typing import Dict, Any
from pathlib import Path
import asyncio
import time
from src.agentic.core.utils.logging_utils import log_event

from src.agentic.core.protocols import Plan
from src.agentic.core.config import CONSTITUTION_PATH, ENABLE_METRICS
from src.agentic.core.llm import get_provider
from src.agentic.infrastructure.graph_db import GraphDB
from src.agentic.core.metrics import get_metrics


class SimplePlannerV2:
    """
    Universal AI Planner using LiteLLM.

    Features:
    - Multi-provider support (Claude, GPT, Gemini, DeepSeek, Ollama)
    - Automatic fallbacks (API -> Local)
    - Prompt caching (90% cost savings on Claude)
    - Structured outputs (zero JSON errors)
    - Dependency awareness (Neo4j integration)
    """

    def __init__(self, model: str = None, quality: str = "high"):
        """
        Initialize planner with LiteLLM.

        Args:
            model: Specific model to use (auto-selects if None)
            quality: "high", "medium", "low" (affects model selection)
        """
        self.provider = get_provider()
        self.model = model
        self.quality = quality

    async def plan(self, task: str, context: Dict[str, Any]) -> Plan:
        """Generate execution plan using Universal AI Provider"""

        # Check dependency impact BEFORE planning
        impact_analysis = self._check_dependency_impact(context)
        if impact_analysis:
            context['dependency_impact'] = impact_analysis

        # Build prompt with constitution
        prompt = self._build_prompt(task, context)

        # Select best model if not specified
        model = self.model or self.provider.select_best_model(
            task_type="planning",
            quality=self.quality
        )

        # Track latency
        start_time = time.time()

        # Generate plan with LiteLLM
        response = await self.provider.generate(
            prompt=prompt,
            model=model,
            use_caching=True,  # Enable prompt caching
            use_structured_output=True,  # Enable structured output
            response_schema=self._get_plan_schema(),
            temperature=0.0
        )

        latency_ms = (time.time() - start_time) * 1000

        # Parse response into Plan
        parse_success = True
        try:
            plan = self._parse_response(response["content"], task)
        except Exception as e:
            parse_success = False
            log_event(f"Parse error: {e}", component="simple_planner_v2", level="warning")
            # Still create fallback plan
            plan = Plan(
                objective=task,
                steps=["Parse failed - using fallback"],
                files_to_modify=[],
                dependencies=[],
                risks=["Plan parsing failed"],
                success_criteria=["Task completed"],
                metadata={"planner": "SimplePlannerV2", "fallback": True}
            )

        # Add metadata
        plan.metadata.update({
            "model": response["model"],
            "provider": response["provider"],
            "cached": response["cached"],
            "cost": response["cost"],
            "latency_ms": latency_ms,
            "planner": "SimplePlannerV2"
        })

        # Record metrics (if enabled)
        if ENABLE_METRICS:
            metrics = get_metrics()
            metrics.record_request(
                provider=response["provider"],
                cost=response["cost"],
                latency_ms=latency_ms,
                cached=response["cached"],
                parse_success=parse_success,
                used_caching=True,
                used_structured=True,
                used_thinking=False  # Can be detected from model capabilities
            )

        return plan

    def name(self) -> str:
        return f"SimplePlannerV2(provider={self.provider.__class__.__name__})"

    def _check_dependency_impact(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check dependency impact using Neo4j graph.
        Makes planner AWARE of consequences before creating plan.
        """
        try:
            target_files = context.get('target_files', [])
            if not target_files:
                # Try to extract from task description
                task_desc = context.get('task', '')
                import re
                found_files = re.findall(r'src/[a-zA-Z0-9/_]+\.py', task_desc)
                target_files = found_files

            if not target_files:
                return None

            # Query Neo4j for impact
            impact_results = {}
            with GraphDB() as db:
                for file_path in target_files[:3]:  # Limit to first 3
                    impact = db.impact_analysis(file_path, max_depth=2)
                    if impact:
                        impact_results[file_path] = {
                            'affected_files': impact.get('affected_files', []),
                            'risk_level': impact.get('risk_level', 'UNKNOWN'),
                            'dependents_count': len(impact.get('affected_files', []))
                        }

            if impact_results:
                return {
                    'checked': True,
                    'analysis': impact_results,
                    'warning': 'Some files have dependents - changes may have ripple effects'
                }

            return None

        except Exception as e:
            log_event(f"Impact check failed: {e}", component="simple_planner_v2", level="warning")
            return {
                'checked': False,
                'error': str(e),
                'warning': 'Could not check dependencies - proceed with caution'
            }

    def _read_constitution(self) -> str:
        """Read YBIS Constitution"""
        try:
            if CONSTITUTION_PATH.exists():
                with open(CONSTITUTION_PATH, "r", encoding="utf-8") as f:
                    return f.read()
            return "Constitution not found. Follow standard best practices."
        except Exception:
            return "Error reading constitution."

    def _build_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Build planning prompt with Constitution and RAG Context"""
        constitution = self._read_constitution()
        
        # Extract RAG context if available
        rag_section = ""
        if "rag_context" in context:
            rag_section = f"\n### RELEVANT KNOWLEDGE (RAG):\n{context['rag_context']}\n"

        return f"""You are a software architect. Analyze this task and create a detailed execution plan.

### SYSTEM CONSTITUTION (MUST FOLLOW):
{constitution}
{rag_section}
TASK: {task}

CONTEXT:
{json.dumps(context, indent=2)}

Generate a plan with the following structure (respond ONLY with valid JSON):

{{
  "objective": "clear one-sentence goal",
  "steps": ["step 1", "step 2", "step 3"],
  "files_to_modify": ["path/to/file1.py", "path/to/file2.py"],
  "dependencies": ["required tools or packages"],
  "risks": ["potential risk 1", "risk 2"],
  "success_criteria": ["criterion 1", "criterion 2"]
}}

Respond ONLY with the JSON object, no additional text."""

    def _get_plan_schema(self) -> Dict[str, Any]:
        """Get JSON schema for Plan (for structured output)"""
        return {
            "type": "object",
            "properties": {
                "objective": {"type": "string"},
                "steps": {"type": "array", "items": {"type": "string"}},
                "files_to_modify": {"type": "array", "items": {"type": "string"}},
                "dependencies": {"type": "array", "items": {"type": "string"}},
                "risks": {"type": "array", "items": {"type": "string"}},
                "success_criteria": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["objective", "steps"]
        }

    def _parse_response(self, response: str, task: str) -> Plan:
        """Parse LLM response into Plan object"""
        try:
            # Try to extract JSON from response
            response = response.strip()

            # Sometimes LLM adds markdown code blocks
            if response.startswith("```"):
                lines = response.split("\n")
                response = "\n".join(lines[1:-1])

            data = json.loads(response)

            return Plan(
                objective=data.get("objective", task),
                steps=data.get("steps", []),
                files_to_modify=data.get("files_to_modify", []),
                dependencies=data.get("dependencies", []),
                risks=data.get("risks", []),
                success_criteria=data.get("success_criteria", []),
                metadata={}
            )

        except json.JSONDecodeError as e:
            # Fallback: create basic plan
            log_event(f"Failed to parse JSON: {e}", component="simple_planner_v2", level="warning")
            log_event(f"Response was: {response[:200]}", component="simple_planner_v2", level="warning")

            return Plan(
                objective=task,
                steps=["Analyze requirements", "Implement solution", "Test changes"],
                files_to_modify=[],
                dependencies=[],
                risks=["Plan parsing failed - using fallback"],
                success_criteria=["Task completed"],
                metadata={"planner": "SimplePlannerV2", "fallback": True}
            )


# ============================================================================
# TESTING
# ============================================================================

async def test_universal_planner():
    """Test planner with different providers"""
    planner = SimplePlannerV2(quality="high")

    # Show available providers
    provider = get_provider()
    log_event("Available providers:", component="simple_planner_v2_test")
    for name in provider.get_available_providers():
        log_event(f"  - {name}", component="simple_planner_v2_test")

    # Test planning
    plan = await planner.plan(
        task="Add a new Button component to packages/ui",
        context={"repo": "YBIS", "current_branch": "main"}
    )

    log_event(f"Objective: {plan.objective}", component="simple_planner_v2_test")
    log_event(f"Steps ({len(plan.steps)}):", component="simple_planner_v2_test")
    for i, step in enumerate(plan.steps, 1):
        log_event(f"  {i}. {step}", component="simple_planner_v2_test")
    log_event(f"Files to modify: {plan.files_to_modify}", component="simple_planner_v2_test")
    log_event("Metadata:", component="simple_planner_v2_test")
    log_event(f"  Model: {plan.metadata.get('model')}", component="simple_planner_v2_test")
    log_event(f"  Provider: {plan.metadata.get('provider')}", component="simple_planner_v2_test")
    log_event(f"  Cached: {plan.metadata.get('cached')}", component="simple_planner_v2_test")
    log_event(f"  Cost: ${plan.metadata.get('cost', 0):.4f}", component="simple_planner_v2_test")


if __name__ == "__main__":
    asyncio.run(test_universal_planner())
