"""
CrewAI Bridge for YBIS
Wraps CrewAI to provide a standardized agent team interface.
Uses local Ollama models by default.
"""

import os

_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
_OPENAI_BASE = f"{_BASE_URL}/v1"
os.environ.setdefault("OPENAI_API_KEY", "NA")
os.environ.setdefault("OPENAI_API_BASE", _OPENAI_BASE)
os.environ.setdefault("OPENAI_BASE_URL", _OPENAI_BASE)

from crewai import Agent, Task, Crew, Process, LLM

class CrewAIBridge:
    def __init__(self, model_name: str = "qwen2.5-coder:32b"):
        # FORCE LOCAL MODE
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        openai_base = f"{base_url}/v1"
        os.environ["OPENAI_API_KEY"] = "NA"
        os.environ["OPENAI_API_BASE"] = openai_base
        os.environ["OPENAI_BASE_URL"] = openai_base
        os.environ["OPENAI_MODEL_NAME"] = model_name
        os.environ["MODEL"] = f"ollama/{model_name}"
        os.environ["MODEL_NAME"] = f"ollama/{model_name}"
        os.environ["BASE_URL"] = base_url

        self.llm = LLM(
            model=f"ollama/{model_name}",
            base_url=base_url
        )
        print(f"[CrewAIBridge] Initialized with model: {model_name}")

    def create_research_crew(self, topic: str) -> str:
        """
        Creates a simple researcher crew to analyze a topic.
        This is a 'Golden Task' for CrewAI.
        """
        # 1. Agents
        researcher = Agent(
            role='Senior Researcher',
            goal='Uncover groundbreaking technologies',
            backstory='Driven by curiosity, you explore the depths of AI.',
            llm=self.llm,
            verbose=True
        )

        writer = Agent(
            role='Technical Writer',
            goal='Summarize findings concisely',
            backstory='You simplify complex topics.',
            llm=self.llm,
            verbose=True
        )

        # 2. Tasks
        task1 = Task(
            description=f'Research about {topic}. Focus on key benefits.',
            expected_output='A bullet point list of benefits.',
            agent=researcher
        )

        task2 = Task(
            description='Write a short paragraph summary based on the research.',
            expected_output='A 3-sentence summary.',
            agent=writer
        )

        # 3. Crew
        crew = Crew(
            agents=[researcher, writer],
            tasks=[task1, task2],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        return str(result)
