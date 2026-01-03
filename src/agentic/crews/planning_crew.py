"""
PlanningCrew - Multi-agent planning via CrewAI.

Restored from legacy/20_WORKFORCE/01_Python_Core/Crews/planning_crew.py
Uses Product Owner + Architect agents for robust planning.
"""

# Windows compatibility fix for CrewAI
import platform
import signal

if platform.system() == "Windows":
    # CrewAI tries to use Unix-only signals that don't exist on Windows
    unix_signals = {
        'SIGHUP': 1, 'SIGQUIT': 3, 'SIGTSTP': 18, 'SIGCONT': 19,
        'SIGTTIN': 21, 'SIGTTOU': 22, 'SIGXCPU': 24, 'SIGXFSZ': 25,
        'SIGVTALRM': 26, 'SIGPROF': 27, 'SIGUSR1': 10, 'SIGUSR2': 12,
        'SIGPIPE': 13, 'SIGALRM': 14, 'SIGCHLD': 17, 'SIGTERM': 15
    }
    for sig_name, sig_value in unix_signals.items():
        if not hasattr(signal, sig_name):
            setattr(signal, sig_name, sig_value)

import json
import os
from typing import Any

# Optional CrewAI import
try:
    from crewai import LLM, Agent, Crew, Process, Task
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    print("[PlanningCrew] CrewAI not installed. Run: pip install crewai")

from src.agentic.core.config import CONSTITUTION_PATH
from src.agentic.core.protocols import Plan


def get_ollama_llm() -> Any | None:
    """Get Ollama LLM configured for CrewAI."""
    if not CREWAI_AVAILABLE:
        return None

    # Set dummy API key for local Ollama
    os.environ.setdefault("OPENAI_API_KEY", "sk-dummy-key-for-local-ollama")

    return LLM(
        model="qwen2.5-coder:32b",
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        callbacks=[]  # Disable telemetry
    )


class PlanningCrew:
    """
    Multi-agent planning crew using CrewAI.

    Agents:
    - Product Owner: Analyzes requirements, defines acceptance criteria
    - Architect: Designs implementation, creates step-by-step plan
    """

    def __init__(self, llm=None):
        if not CREWAI_AVAILABLE:
            raise RuntimeError("CrewAI not available. Install with: pip install crewai")

        self.llm = llm or get_ollama_llm()
        self._setup_agents()

    def _setup_agents(self):
        """Initialize the crew agents."""
        self.product_owner = Agent(
            role='Technical Product Owner',
            goal='Analyze requirements and define clear acceptance criteria.',
            backstory=(
                'You are an experienced PO who ensures that what we build '
                'actually solves the user problem. You focus on clarity and feasibility.'
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        self.architect = Agent(
            role='Senior Software Architect',
            goal='Design robust, scalable, and maintainable software solutions.',
            backstory=(
                'You are a pragmatic architect. You prefer simple, proven solutions '
                'over complex ones. You love SOLID principles and clean code.'
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def _read_constitution(self) -> str:
        """Read YBIS Constitution for context."""
        try:
            if CONSTITUTION_PATH.exists():
                return CONSTITUTION_PATH.read_text(encoding='utf-8')
        except Exception:
            pass
        return ""

    def plan(self, task_description: str, context: dict[str, Any] = None) -> Plan:
        """
        Generate a plan using multi-agent collaboration.

        Args:
            task_description: What needs to be done
            context: Additional context (RAG results, repo tree, etc.)

        Returns:
            Plan object with steps, files, risks, etc.
        """
        context = context or {}
        constitution = self._read_constitution()

        # Build enriched requirement
        enriched_req = f"TASK: {task_description}\n"
        if constitution:
            enriched_req += f"\nCONSTITUTION (must follow):\n{constitution[:2000]}...\n"
        if context.get('rag_context'):
            enriched_req += f"\nRELEVANT CODE CONTEXT:\n{context['rag_context']}\n"
        if context.get('repo_tree'):
            enriched_req += f"\nREPO STRUCTURE:\n{context['repo_tree']}\n"

        # Task 1: Analysis by Product Owner
        task_analysis = Task(
            description=f"""
            Analyze the following requirement:
            "{task_description}"

            Context:
            {json.dumps(context, indent=2, default=str)[:1000]}

            Identify:
            1. Key technical challenges
            2. Necessary components
            3. Potential risks
            4. Success criteria
            """,
            agent=self.product_owner,
            expected_output="A summary of technical requirements, risks, and success criteria."
        )

        # Task 2: Design by Architect
        task_design = Task(
            description=f"""
            Based on the analysis, create a step-by-step implementation plan.
            The plan must be feasible for a single developer to execute.

            Requirement: "{task_description}"

            Output MUST be a JSON object with this structure:
            {{
                "objective": "clear one-sentence goal",
                "steps": ["step1", "step2", "step3"],
                "files_to_modify": ["path/to/file1.py", "path/to/file2.py"],
                "dependencies": ["required packages"],
                "risks": ["risk1", "risk2"],
                "success_criteria": ["criterion1", "criterion2"]
            }}

            IMPORTANT: Output ONLY the JSON, no markdown or explanation.
            """,
            agent=self.architect,
            expected_output="A JSON object containing the implementation plan."
        )

        # Run the crew
        crew = Crew(
            agents=[self.product_owner, self.architect],
            tasks=[task_analysis, task_design],
            verbose=True,
            process=Process.sequential
        )

        try:
            result = crew.kickoff()
            return self._parse_crew_output(result, task_description)
        except Exception as e:
            print(f"[PlanningCrew] Crew failed: {e}")
            return self._fallback_plan(task_description)

    def _parse_crew_output(self, result: Any, task_description: str) -> Plan:
        """Parse CrewAI output into Plan object with robust JSON handling."""
        result_str = str(result)

        # Try multiple JSON extraction strategies
        json_str = self._extract_json(result_str)

        if json_str:
            try:
                # Try to repair common JSON issues
                repaired = self._repair_json(json_str)
                data = json.loads(repaired)

                files = data.get('files_to_modify', [])
                # If no files specified, infer from task
                if not files:
                    files = self._infer_files(task_description)

                return Plan(
                    objective=data.get('objective', task_description),
                    steps=data.get('steps', []),
                    files_to_modify=files,
                    dependencies=data.get('dependencies', []),
                    risks=data.get('risks', []),
                    success_criteria=data.get('success_criteria', []),
                    metadata={'source': 'CrewAI', 'raw_output': result_str[:500]}
                )
            except json.JSONDecodeError as e:
                print(f"[PlanningCrew] Parse failed: {e}")

        return self._fallback_plan(task_description)

    def _extract_json(self, text: str) -> str | None:
        """Extract JSON from text with multiple strategies."""
        import re

        # Strategy 1: Find outermost { }
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            return text[start:end]

        # Strategy 2: Look for ```json blocks
        match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            return match.group(1).strip()

        return None

    def _repair_json(self, json_str: str) -> str:
        """Attempt to repair common JSON issues."""
        import re

        repaired = json_str

        # Remove trailing commas before ] or }
        repaired = re.sub(r',\s*([}\]])', r'\1', repaired)

        # Fix unescaped newlines in strings
        repaired = re.sub(r'(?<!\\)\n(?=[^"]*"[^"]*$)', r'\\n', repaired)

        # Remove control characters
        repaired = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', repaired)

        return repaired

    def _infer_files(self, task_description: str) -> list[str]:
        """Infer target files from task description."""
        import re
        files = []

        # Look for file paths in description
        patterns = [
            r'(src/[a-zA-Z0-9_/]+\.py)',
            r'(tests/[a-zA-Z0-9_/]+\.py)',
            r'([a-zA-Z0-9_]+\.py)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, task_description)
            files.extend(matches)

        # Deduplicate
        return list(dict.fromkeys(files))

    def _fallback_plan(self, task_description: str) -> Plan:
        """Generate fallback plan when crew fails."""
        # Try to infer files from task description
        inferred_files = self._infer_files(task_description)

        return Plan(
            objective=task_description,
            steps=[
                "Analyze the requirements",
                "Implement the solution",
                "Write tests",
                "Verify changes"
            ],
            files_to_modify=inferred_files,
            dependencies=[],
            risks=["Plan generated from fallback - manual review recommended"],
            success_criteria=["Task completed successfully"],
            metadata={'source': 'fallback', 'files_inferred': bool(inferred_files)}
        )

    def name(self) -> str:
        return "PlanningCrew(CrewAI)"


# Convenience function
def create_planning_crew() -> PlanningCrew | None:
    """Create a PlanningCrew instance if CrewAI is available."""
    if not CREWAI_AVAILABLE:
        return None
    try:
        return PlanningCrew()
    except Exception as e:
        print(f"[PlanningCrew] Failed to create crew: {e}")
        return None
