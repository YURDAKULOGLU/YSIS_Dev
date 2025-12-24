from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileWriterTool
import os
from src.services.IntegrationService import IntegrationService

# Configure Ollama
ollama_model = LLM(
    model="ollama/llama3.2:latest",
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

# Use Standard Tool
file_writer = FileWriterTool()

class DevCrew:
    def __init__(self):
        self.developer = Agent(
            role='Senior Python Developer',
            goal='Write clean, efficient, and typed Python code.',
            backstory='You are a Python expert. You write code that is easy to read and test. You strictly follow instructions.',
            verbose=True,
            allow_delegation=False,
            llm=ollama_model,
            tools=[file_writer] # Use standard tool
        )
        
        self.qa_engineer = Agent(
            role='QA Automation Engineer',
            goal='Ensure code quality and correctness.',
            backstory='You catch bugs before they happen. You are critical and detail-oriented.',
            verbose=True,
            allow_delegation=False,
            llm=ollama_model
        )
        self.integration_service = IntegrationService()

    def run(self, context: dict):
        print(f"--- Starting Dev Crew Execution ---")
        
        # Parse context
        plan = context.get('plan', str(context))
        
        query = "Bilgi almak için sorgu"
        retrieved_data = self.integration_service.retrieve_data(query)
        print(f"Alınan veri: {retrieved_data}")
        
        task_code = Task(
            description=f"""
            Execute the following technical plan:
            {plan}
            
            Write the optimized code.
            IMPORTANT: Use the 'FileWriterTool' to save the code directly to 'Agentic/Core/orchestrator_hybrid_optimized.py'.
            Do NOT return the code in the final answer, just confirm it was saved.
            
            Retrieved Data: {retrieved_data}
            """,
            agent=self.developer,
            expected_output="Confirmation that the file was saved using the tool."
        )
        
        task_review = Task(
            description=f"""
            Review the actions taken by the Developer.
            Check if the file 'Agentic/Core/orchestrator_hybrid_optimized.py' was created/updated (assume success if Developer said so).
            
            Provide a summary of the optimization.
            
            Retrieved Data: {retrieved_data}
            """,
            agent=self.qa_engineer,
            expected_output="QA Report confirming file creation."
        )
        
        crew = Crew(
            agents=[self.developer, self.qa_engineer],
            tasks=[task_code, task_review],
            verbose=True,
            process=Process.sequential
        )
        
        return crew.kickoff()
