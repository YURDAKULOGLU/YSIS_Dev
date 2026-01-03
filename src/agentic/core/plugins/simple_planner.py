"""
SimplePlanner - Fallback planner with zero framework dependencies.

Uses direct Ollama API calls (via requests) to generate plans.
No CrewAI, no LangChain, no heavy dependencies.
"""

import json
import os
from typing import Dict, Any
from pathlib import Path
import asyncio
import httpx
from src.agentic.core.utils.logging_utils import log_event

from src.agentic.core.protocols import Plan
from src.agentic.core.config import CONSTITUTION_PATH
from src.agentic.core.plugins.model_router import default_router
from src.agentic.infrastructure.graph_db import GraphDB


class SimplePlanner:
    """
    Simple planner using direct Ollama API calls via ModelRouter.

    This is the fallback planner - works without any framework.
    """

    def __init__(self, router=None, base_url: str = None):
        self.router = router or default_router
        # Get the planning model config from router
        self.model_config = self.router.get_model("PLANNING")

        # Support Docker -> Host connection via environment variable
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    async def plan(self, task: str, context: Dict[str, Any]) -> Plan:
        """Generate execution plan using Ollama with dependency awareness"""
        log_event(f"Planning task: {task}", component="simple_planner")

        # NEW: Check dependency impact BEFORE planning (GAP 2 FIX)
        impact_analysis = self._check_dependency_impact(context)

        # Enhance context with impact analysis
        if impact_analysis:
            context['dependency_impact'] = impact_analysis

        prompt = self._build_prompt(task, context)

        # Call Ollama API
        response = await self._call_ollama(prompt)

        # Parse response into Plan
        plan = self._parse_response(response, task)

        return plan

    def name(self) -> str:
        return f"SimplePlanner({self.model_config.model_name})"

    # ========================================================================
    # IMPLEMENTATION
    # ========================================================================

    def _check_dependency_impact(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check dependency impact using Neo4j graph (GAP 2 FIX).

        Analyzes which files will be affected by changes mentioned in the context.
        This makes the planner AWARE of consequences before creating a plan.
        """
        try:
            # Extract file paths from context if available
            target_files = context.get('target_files', [])
            if not target_files:
                # Try to extract from task description
                task_desc = context.get('task', '')
                # Simple heuristic: look for file paths in task
                import re
                found_files = re.findall(r'src/[a-zA-Z0-9/_]+\.py', task_desc)
                target_files = found_files

            if not target_files:
                return None  # No files to analyze

            # Query Neo4j for impact
            impact_results = {}
            with GraphDB() as db:
                for file_path in target_files[:3]:  # Limit to first 3 files
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
            # Don't fail planning if impact check fails - just log it
            log_event(f"Impact check failed: {e}", component="simple_planner", level="warning")
            return {
                'checked': False,
                'error': str(e),
                'warning': 'Could not check dependencies - proceed with caution'
            }

    def _read_constitution(self) -> str:
        """Read YBIS Constitution and Auto-generated rules."""
        context = ""
        try:
            if CONSTITUTION_PATH.exists():
                with open(CONSTITUTION_PATH, "r", encoding="utf-8") as f:
                    context += f"### CONSTITUTION:\n{f.read()}\n\n"

            # Add Auto Rules if they exist
            auto_rules_path = CONSTITUTION_PATH.parent.parent / "AUTO_RULES.md"
            if auto_rules_path.exists():
                with open(auto_rules_path, "r", encoding="utf-8") as f:
                    context += f"### AUTOMATED LESSONS & RULES:\n{f.read()}\n\n"

            return context if context else "Constitution not found. Follow standard best practices."
        except Exception:
            return "Error reading constitution or rules."

    def _build_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Build planning prompt with Constitution injection"""
        constitution = self._read_constitution()

        return f"""You are a software architect. Analyze this task and create a detailed execution plan.

### SYSTEM CONSTITUTION (MUST FOLLOW):
{constitution}

TASK: {task}

CONTEXT:
{json.dumps(context, indent=2)}

Generate a plan with the following structure (respond ONLY with valid JSON):

{{
  "objective": "clear one-sentence goal",
  "steps": ["step 1", "step 2", "step 3"],
  "files_to_modify": ["path/to/file1.ts", "path/to/file2.py"],
  "dependencies": ["required tools or packages"],
  "risks": ["potential risk 1", "risk 2"],
  "success_criteria": ["criterion 1", "criterion 2"]
}}

Respond ONLY with the JSON object, no additional text."""

    async def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API directly"""
        # Remove /v1 suffix if present (Ollama API is at /api/generate)
        base = self.base_url.rstrip('/').replace('/v1', '')
        url = f"{base}/api/generate"

        payload = {
            "model": self.model_config.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.model_config.temperature,  # Use router config
                "num_predict": 2048, # Increased context for better plans
                "num_ctx": self.model_config.context_window
            }
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()

            data = response.json()
            return data.get("response", "")

    def _parse_response(self, response: str, task: str) -> Plan:
        """Parse LLM response into Plan object"""
        try:
            # Try to extract JSON from response
            response = response.strip()

            # Sometimes LLM adds markdown code blocks
            if response.startswith("```"):
                # Extract JSON from code block
                lines = response.split("\n")
                response = "\n".join(lines[1:-1])  # Remove first and last line

            data = json.loads(response)

            return Plan(
                objective=data.get("objective", task),
                steps=data.get("steps", []),
                files_to_modify=data.get("files_to_modify", []),
                dependencies=data.get("dependencies", []),
                risks=data.get("risks", []),
                success_criteria=data.get("success_criteria", []),
                metadata={"model": self.model_config.model_name, "planner": "SimplePlanner"}
            )

        except json.JSONDecodeError as e:
            # Fallback: create basic plan from task description
            log_event(f"Failed to parse JSON: {e}", component="simple_planner", level="warning")
            log_event(f"Response was: {response[:200]}", component="simple_planner", level="warning")

            return Plan(
                objective=task,
                steps=["Analyze requirements", "Implement solution", "Test changes"],
                files_to_modify=[],
                dependencies=[],
                risks=["Plan parsing failed - using fallback"],
                success_criteria=["Task completed"],
                metadata={"model": self.model, "planner": "SimplePlanner", "fallback": True}
            )


# ============================================================================
# TESTING
# ============================================================================

async def test_simple_planner():
    """Test planner standalone"""
    planner = SimplePlanner()

    plan = await planner.plan(
        task="Add a new Button component to packages/ui",
        context={"repo": "YBIS", "current_branch": "main"}
    )

    log_event(f"Objective: {plan.objective}", component="simple_planner_test")
    log_event(f"Steps ({len(plan.steps)}):", component="simple_planner_test")
    for i, step in enumerate(plan.steps, 1):
        log_event(f"  {i}. {step}", component="simple_planner_test")
    log_event(f"Files to modify: {plan.files_to_modify}", component="simple_planner_test")


if __name__ == "__main__":
    asyncio.run(test_simple_planner())
