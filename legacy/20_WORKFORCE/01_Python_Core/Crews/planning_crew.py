# Windows compatibility fix for CrewAI
import signal
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

from crewai import Agent, Task, Crew, Process, LLM
from src.modules.memory.RAGMemory import RAGMemory
import os

# Set dummy API key for local Ollama (doesn't use authentication)
os.environ.setdefault("OPENAI_API_KEY", "sk-dummy-key-for-local-ollama")

# Configure Ollama using CrewAI's native LLM class
# Use OpenAI-compatible endpoint (without "ollama/" prefix)
# Model name without prefix makes LiteLLM use /v1/chat/completions endpoint
ollama_model = LLM(
    model="llama3.2:latest",
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
    # Disable telemetry to avoid emoji encoding errors on Windows
    callbacks=[]
)

class PlanningCrew:
    def __init__(self):
        self.model = ollama_model
        self.rag_memory = RAGMemory()

        self.product_owner = Agent(
            role='Technical Product Owner',
            goal='Analyze requirements and define clear acceptance criteria.',
            backstory='You are an experienced PO who ensures that what we build actually solves the user problem.',
            verbose=True,
            allow_delegation=False,
            llm=ollama_model
        )

        self.architect = Agent(
            role='Senior Software Architect',
            goal='Design robust, scalable, and maintainable software solutions.',
            backstory='You are a pragmatic architect. You prefer simple, proven solutions over complex ones. You love SOLID principles.',
            verbose=True,
            allow_delegation=False,
            llm=ollama_model
        )

    def run(self, requirement: str):
        print(f"--- Starting Planning Crew for: {requirement[:50]}... ---")

        # RAGMemory'den bilgi al
        additional_info = self.rag_memory.retrieve_information(requirement)
        enriched_requirement = f"{requirement} {additional_info}"

        task_analysis = Task(
            description=f"""
            Analyze the following requirement:
            "{requirement}"

            Identify key technical challenges, necessary components, and potential risks.
            """,
            agent=self.product_owner,
            expected_output="A summary of technical requirements and risks."
        )

        task_design = Task(
            description=f"""
            Based on the analysis, create a step-by-step implementation plan.
            The plan must be feasible for a single developer to execute.

            Requirement: "{requirement}"

            Output MUST be a JSON object with this structure:
            {{
                "technical_requirements": ["req1", "req2"],
                "step_by_step_plan": ["step1", "step2"],
                "files_to_create_modify": ["file1.py", "file2.ts"]
            }}
            """,
            agent=self.architect,
            expected_output="A JSON object containing the implementation plan."
        )

        crew = Crew(
            agents=[self.product_owner, self.architect],
            tasks=[task_analysis, task_design],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        return result
