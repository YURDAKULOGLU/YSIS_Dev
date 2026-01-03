import os
from typing import List, Optional
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import FileReadTool, FileWriterTool

# Configure LLM (Local or Cloud)
# In production, this should come from a config/env manager
ollama_model = LLM(
    model="ollama/llama3.2:latest",
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

class FileModification(BaseModel):
    file_path: str = Field(..., description="Absolute path to the file to modify")
    instructions: str = Field(..., description="What changes to make to the file")
    context_files: List[str] = Field(default_factory=list, description="List of files to read for context")

class UniversalDevCrew:
    """
    A generic developer crew that can modify any file given a path and instructions.
    """
    def __init__(self):
        # Tools
        self.read_tool = FileReadTool()
        self.write_tool = FileWriterTool()

        # Imagine this as the "Junior Dev" who does the typing
        self.developer = Agent(
            role='Senior Python Developer',
            goal='Implement precise code changes based on instructions.',
            backstory=(
                "You are an expert software engineer. "
                "You are given specific instructions to modify a file. "
                "You explicitly use the FileWriterTool to overwrite/update the file. "
                "You never simply return code in markdown; you MUST save it."
            ),
            verbose=True,
            allow_delegation=False,
            llm=ollama_model,
            tools=[self.read_tool, self.write_tool]
        )

        # Imagine this as the "Tech Lead" who checks the work
        self.qa_engineer = Agent(
            role='Code Reviewer',
            goal='Verify that the file was modified correctly.',
            backstory=(
                "You are a strict code reviewer. "
                "You check if the file exists and if the content matches the instructions. "
                "You verify syntax and logic."
            ),
            verbose=True,
            allow_delegation=False,
            llm=ollama_model,
            tools=[self.read_tool]
        )

    def run(self, inputs: FileModification):
        print(f"--- 🚀 Starting UniversalDevCrew ---")
        print(f"Target: {inputs.file_path}")

        # 1. Developer Task
        devel_task = Task(
            description=f"""
            CONTEXT:
            You need to modify the file: '{inputs.file_path}'.

            INSTRUCTIONS:
            {inputs.instructions}

            Start by reading the file if it exists (use FileReadTool).
            Then, rewrite the file with the changes using FileWriterTool.
            """,
            agent=self.developer,
            expected_output="Confirmation that the file has been successfully written/updated."
        )

        # 2. QA Task
        qa_task = Task(
            description=f"""
            Verify the work done on '{inputs.file_path}'.
            1. Read the file using FileReadTool.
            2. Check if the instructions were followed:
               "{inputs.instructions}"
            3. If the code looks broken or incomplete, report it.
            """,
            agent=self.qa_engineer,
            expected_output="A brief quality report (PASS/FAIL) and summary of changes."
        )

        crew = Crew(
            agents=[self.developer, self.qa_engineer],
            tasks=[devel_task, qa_task],
            verbose=True,
            process=Process.sequential
        )

        return crew.kickoff()

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Run UniversalDevCrew to modify a file.")
    parser.add_argument("file_path", help="Path to the file to modify")
    parser.add_argument("instructions", help="Instructions for modification")
    parser.add_argument("--context", nargs="*", help="Context files", default=[])

    args = parser.parse_args()

    # Ensure absolute path
    abs_path = os.path.abspath(args.file_path)

    input_data = FileModification(
        file_path=abs_path,
        instructions=args.instructions,
        context_files=args.context
    )

    crew = UniversalDevCrew()
    try:
        result = crew.run(input_data)
        print("\n\n########################")
        print("## RESULT ##")
        print(result)
        print("########################\n")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
