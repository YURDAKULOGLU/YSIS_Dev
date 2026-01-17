import os
from textwrap import dedent
from typing import Any, List

from crewai import Agent, Crew, Process, Task
from langchain_openai import ChatOpenAI

from src.agentic.core.protocols import PlannerProtocol, Plan
from src.agentic.core.config import PROJECT_ROOT

class PlanningCrew(PlannerProtocol):
    """
    Advanced Planning Crew powered by CrewAI.
    Replaces SimplePlanner with a multi-agent architectural council.
    """

    def __init__(self, model_name: str = "ollama/qwen2.5-coder:32b"):
        self.model_name = model_name
        # Use LiteLLM via ChatOpenAI wrapper if needed, or direct Ollama
        # For now, assuming local Ollama
        self.llm = ChatOpenAI(
            model=model_name,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key="ollama"
        )

    def name(self) -> str:
        return "CrewAI-Planning-Squad"

    async def plan(self, task_description: str, context: dict[str, Any]) -> Plan:
        """
        Orchestrates the planning process using a crew of specialized agents.
        """
        
        # 1. AGENTS
        architect = Agent(
            role='Senior Systems Architect',
            goal='Design robust, scalable, and secure system architectures.',
            backstory=dedent("""
                You are the guardian of the YBIS Architecture. You know the Constitution 
                and the ARCHITECTURE_V2.md by heart. You despise spaghetti code.
            """),
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )

        tech_lead = Agent(
            role='Technical Lead',
            goal='Translate architectural vision into concrete implementation steps.',
            backstory=dedent("""
                You are a pragmatic coder. You know the file structure, the libraries, 
                and the "Steward OroYstein" philosophy. You ensure the plan is actionable.
            """),
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )

        qa_specialist = Agent(
            role='QA Engineer',
            goal='Ensure every plan includes comprehensive verification strategies.',
            backstory=dedent("""
                You don't trust code until it's tested. Your job is to make sure 
                tests are written BEFORE the code (TDD).
            """),
            allow_delegation=False,
            verbose=True,
            llm=self.llm
        )

        # 2. TASKS
        context_str = str(context)
        
        analysis_task = Task(
            description=dedent(f"""
                Analyze the following user request: "{task_description}"
                Context: {context_str}
                
                Identify:
                1. Which core components are affected?
                2. Are there any architectural risks?
                3. What is the high-level strategy?
            """),
            agent=architect,
            expected_output="A high-level architectural analysis."
        )

        spec_task = Task(
            description=dedent("""
                Based on the architect's analysis, create a detailed implementation specification.
                List exactly which files need to be created or modified.
                Define the dependencies.
            """),
            agent=tech_lead,
            context=[analysis_task],
            expected_output="A list of files and implementation steps."
        )

        plan_task = Task(
            description=dedent("""
                Consolidate the analysis and specification into a final JSON Plan.
                The format MUST be:
                {
                    "objective": "...",
                    "steps": ["step1", "step2"],
                    "files_to_modify": ["src/..."],
                    "success_criteria": ["..."]
                }
                Ensure Test-Driven Development (TDD) steps are included.
            """),
            agent=qa_specialist,
            context=[analysis_task, spec_task],
            expected_output="A valid JSON object representing the Plan."
        )

        # 3. CREW EXECUTION
        crew = Crew(
            agents=[architect, tech_lead, qa_specialist],
            tasks=[analysis_task, spec_task, plan_task],
            process=Process.sequential,
            verbose=True
        )

        # Run (Synchronous for now, wrapped in async)
        # Note: CrewAI is sync by default.
        import json
        try:
            result_str = crew.kickoff()
            # Parse JSON from result
            # Cleanup markdown code blocks if present
            cleaned = result_str.raw.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned)
            
            return Plan(
                objective=data.get("objective", task_description),
                steps=data.get("steps", []),
                files_to_modify=data.get("files_to_modify", []),
                success_criteria=data.get("success_criteria", []),
                metadata={"planner": "CrewAI"}
            )
        except Exception as e:
            print(f"[ERROR] CrewAI Planning Failed: {e}")
            # Fallback to a basic plan
            return Plan(
                objective=task_description,
                steps=["Analyze", "Implement", "Verify"],
                files_to_modify=[],
                metadata={"planner": "Fallback", "error": str(e)}
            )