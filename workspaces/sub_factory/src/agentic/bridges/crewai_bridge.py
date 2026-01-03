"""
CrewAI Bridge for YBIS
Wraps CrewAI to provide a standardized agent team interface.
Uses local Ollama models by default.
"""

from crewai import Agent, Task, Crew, Process
from langchain_ollama import ChatOllama
import os

class CrewAIBridge:
    def __init__(self, model_name: str = "qwen2.5-coder:32b"):
        # FORCE LOCAL MODE
        os.environ["OPENAI_API_KEY"] = "NA"
        os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
        os.environ["OPENAI_MODEL_NAME"] = model_name

        self.llm = ChatOllama(
            model=model_name,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
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
