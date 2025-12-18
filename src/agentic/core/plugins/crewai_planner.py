"""
CrewAI Planner - PlannerProtocol implementation using CrewAI.

Uses existing planning_crew.py for multi-agent planning.
Converts CrewAI output to Plan objects.
"""

# Windows compatibility fix for CrewAI
import signal
import sys
import platform

if platform.system() == "Windows":
    # CrewAI tries to use Unix-only signals that don't exist on Windows
    # Mock them all to prevent AttributeError
    unix_signals = {
        'SIGHUP': 1,
        'SIGQUIT': 3,
        'SIGTSTP': 18,
        'SIGCONT': 19,
        'SIGTTIN': 21,
        'SIGTTOU': 22,
        'SIGXCPU': 24,
        'SIGXFSZ': 25,
        'SIGVTALRM': 26,
        'SIGPROF': 27,
        'SIGUSR1': 10,
        'SIGUSR2': 12,
        'SIGPIPE': 13,
        'SIGALRM': 14,
        'SIGCHLD': 17,
        'SIGTERM': 15
    }
    for sig_name, sig_value in unix_signals.items():
        if not hasattr(signal, sig_name):
            setattr(signal, sig_name, sig_value)

import os
from pathlib import Path
from typing import Dict, Any
import json
import re

# Add paths
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agentic.core.protocols import Plan
from Agentic.Crews.planning_crew import PlanningCrew


class CrewAIPlanner:
    """
    CrewAI-based planner using planning_crew.py.

    This is a drop-in replacement for SimplePlanner.
    Uses CrewAI's multi-agent system (Product Owner + Architect).
    """

    def __init__(self):
        self.crew = PlanningCrew()

    async def plan(self, task: str, context: Dict[str, Any]) -> Plan:
        """Generate execution plan using CrewAI"""

        print(f"[CrewAIPlanner] Analyzing task with multi-agent crew...")

        # Run CrewAI crew
        # Note: PlanningCrew.run() is synchronous, not async
        result = self.crew.run(task)

        # Parse CrewAI output into Plan
        plan = self._parse_crewai_output(result, task)

        return plan

    def name(self) -> str:
        return "CrewAIPlanner(ProductOwner+Architect)"

    # ========================================================================
    # IMPLEMENTATION
    # ========================================================================

    def _parse_crewai_output(self, result, task: str) -> Plan:
        """
        Parse CrewAI crew output into Plan object.

        CrewAI returns a CrewOutput object with the final result.
        We need to extract structured plan from it.
        """
        try:
            # CrewOutput has .raw property with full output string
            if hasattr(result, 'raw'):
                result_str = result.raw
            elif hasattr(result, 'output'):
                result_str = result.output
            else:
                result_str = str(result)

            # Debug: print raw output
            print(f"\n[DEBUG] Raw CrewAI output (first 1000 chars):")
            print(result_str[:1000])
            print(f"[DEBUG] Output type: {type(result)}")

            # Try to find JSON in the output
            json_match = re.search(r'\{[\s\S]*\}', result_str)

            if json_match:
                data = json.loads(json_match.group(0))
                return self._create_plan_from_dict(data, task)

            # If no JSON, parse as structured text
            return self._create_plan_from_text(result_str, task)

        except Exception as e:
            print(f"[CrewAIPlanner] Failed to parse output: {e}")
            print(f"[CrewAIPlanner] Raw output: {result_str[:500]}")

            # Fallback: create basic plan
            return Plan(
                objective=task,
                steps=["Analyze requirements", "Design solution", "Implement code"],
                files_to_modify=[],
                dependencies=[],
                risks=["CrewAI output parsing failed - using fallback"],
                success_criteria=["Task completed"],
                metadata={"planner": "CrewAIPlanner", "fallback": True}
            )

    def _create_plan_from_dict(self, data: dict, task: str) -> Plan:
        """Create Plan from parsed JSON dict"""
        return Plan(
            objective=data.get("objective", task),
            steps=data.get("steps", []),
            files_to_modify=data.get("files_to_modify", data.get("files", [])),
            dependencies=data.get("dependencies", []),
            risks=data.get("risks", []),
            success_criteria=data.get("success_criteria", []),
            metadata={"planner": "CrewAIPlanner", "source": "json"}
        )

    def _create_plan_from_text(self, text: str, task: str) -> Plan:
        """Create Plan from unstructured text"""

        # Extract objective (usually first paragraph)
        lines = text.split('\n')
        objective = lines[0].strip() if lines else task

        # Extract steps (lines that start with numbers or bullets)
        steps = []
        for line in lines:
            line = line.strip()
            # Match: "1. Step", "- Step", "* Step"
            if re.match(r'^(\d+\.|-|\*)\s+', line):
                step = re.sub(r'^(\d+\.|-|\*)\s+', '', line)
                if step:
                    steps.append(step)

        # Extract files (lines with file extensions)
        files = []
        for line in lines:
            if any(ext in line for ext in ['.ts', '.tsx', '.py', '.js', '.jsx']):
                # Extract file paths
                matches = re.findall(r'[\w/]+\.(ts|tsx|py|js|jsx)', line)
                files.extend(matches)

        return Plan(
            objective=objective,
            steps=steps if steps else ["Execute task"],
            files_to_modify=files,
            dependencies=[],
            risks=[],
            success_criteria=["All steps completed"],
            metadata={"planner": "CrewAIPlanner", "source": "text_parsing"}
        )


# ============================================================================
# TESTING
# ============================================================================

async def test_crewai_planner():
    """Test CrewAI planner standalone"""
    planner = CrewAIPlanner()

    plan = await planner.plan(
        task="Add user authentication to the mobile app",
        context={"repo": "YBIS", "current_branch": "main"}
    )

    print(f"\n[TEST] CrewAI Planner Result:")
    print(f"Objective: {plan.objective}")
    print(f"Steps ({len(plan.steps)}):")
    for i, step in enumerate(plan.steps, 1):
        print(f"  {i}. {step}")
    print(f"Files to modify: {plan.files_to_modify}")
    print(f"Metadata: {plan.metadata}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_crewai_planner())
