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

    def _read_constitution(self) -> str:
        """Read YBIS Constitution from project root."""
        try:
            if CONSTITUTION_PATH.exists():
                with open(CONSTITUTION_PATH, "r", encoding="utf-8") as f:
                    return f.read()
            return "Constitution not found. Follow standard best practices."
        except Exception:
            return "Error reading constitution."

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
            print(f"[SimplePlanner] Failed to parse JSON: {e}")
            print(f"[SimplePlanner] Response was: {response[:200]}")

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

    print(f"Objective: {plan.objective}")
    print(f"Steps ({len(plan.steps)}):")
    for i, step in enumerate(plan.steps, 1):
        print(f"  {i}. {step}")
    print(f"Files to modify: {plan.files_to_modify}")


if __name__ == "__main__":
    asyncio.run(test_simple_planner())
