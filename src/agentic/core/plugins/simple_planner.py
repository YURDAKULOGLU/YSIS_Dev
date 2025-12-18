"""
SimplePlanner - Fallback planner with zero framework dependencies.

Uses direct Ollama API calls (via requests) to generate plans.
No CrewAI, no LangChain, no heavy dependencies.
"""

import json
import os
from typing import Dict, Any
import asyncio
import httpx

from src.agentic.core.protocols import Plan


class SimplePlanner:
    """
    Simple planner using direct Ollama API calls.

    This is the fallback planner - works without any framework.
    """

    def __init__(self, model: str = "qwen2.5-coder:14b", base_url: str = None):
        self.model = model
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    async def plan(self, task: str, context: Dict[str, Any]) -> Plan:
        """Generate execution plan using Ollama"""

        prompt = self._build_prompt(task, context)

        # Call Ollama API
        response = await self._call_ollama(prompt)

        # Parse response into Plan
        plan = self._parse_response(response, task)

        return plan

    def name(self) -> str:
        return f"SimplePlanner({self.model})"

    # ========================================================================
    # IMPLEMENTATION
    # ========================================================================

    def _build_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Build planning prompt"""
        return f"""You are a software architect. Analyze this task and create a detailed execution plan.

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
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # Low temperature for structured output
                "num_predict": 1000,
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
                metadata={"model": self.model, "planner": "SimplePlanner"}
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
