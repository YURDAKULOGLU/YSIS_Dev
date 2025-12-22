"""
PROJECT MIRROR: Self-Investigation Module
Uses CrewAI to analyze the current system state and suggest strategic upgrades.
"""

import os
from crewai import Agent, Task, Crew, Process, LLM

class InvestigatorBridge:
    def __init__(self, model_name: str = "qwen2.5-coder:32b"):
        # FORCE LOCAL MODE
        os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
        os.environ["OPENAI_API_KEY"] = "NA"
        
        # CrewAI native LLM (via LiteLLM)
        # Must prefix with 'ollama/' for local models
        self.llm = LLM(
            model=f"ollama/{model_name}",
            base_url="http://localhost:11434"
        )

    def run_audit(self, project_root: str) -> str:
        """
        Conducts a full self-audit of the YBIS system.
        """
        
        # 1. Gather Context (What do we have?)
        req_path = os.path.join(project_root, "requirements.txt")
        tree_context = self._get_tree_structure(project_root)
        
        with open(req_path, "r", encoding="utf-8") as f:
            installed_libs = f.read()

        # 2. Define Agents
        auditor = Agent(
            role='System Architect',
            goal='Analyze the current codebase structure and installed libraries.',
            backstory='You are a strict code auditor. You look for gaps, spaghetti code, and missing standards.',
            llm=self.llm,
            verbose=True
        )
        
        scout = Agent(
            role='Tech Futurist',
            goal='Recommend cutting-edge frameworks to reach AGI level.',
            backstory='You know every new AI tool (AutoGPT, BabyAGI, Semantic Kernel, FastAPI, Vector DBs). You hate obsolescence.',
            llm=self.llm,
            verbose=True
        )

        # 3. Define Tasks
        task_audit = Task(
            description=f"""
            Analyze the current system state based on this context: 
            
            INSTALLED LIBRARIES:
            {installed_libs}
            
            FILE STRUCTURE:
            {tree_context}
            
            Identify what kind of system this is (Agentic Factory?).
            List the core capabilities we currently have (e.g., Memory, Orchestration).
            """,
            expected_output='A summary of Current Capabilities and Architecture.',
            agent=auditor
        )
        
        task_recommend = Task(
            description="""
            Based on the Auditor's analysis, recommend 3-5 CRITICAL frameworks or tools we are missing.
            Focus on:
            1. Multi-modality (Vision, Voice? We are text-only now).
            2. Web Interface (Do we have a UI? FastUI/Streamlit?).
            3. Advanced Reasoning (Do we need specialized math/logic solvers?).
            4. Robustness (Testing frameworks?).
            
            Explain WHY we need them.
            """,
            expected_output='A strategic "MISSING TECHNOLOGIES" report with installation commands.',
            agent=scout
        )

        # 4. Crew
        crew = Crew(
            agents=[auditor, scout],
            tasks=[task_audit, task_recommend],
            verbose=True,
            process=Process.sequential
        )

        return crew.kickoff()

    def _get_tree_structure(self, root_dir: str) -> str:
        """Simple helper to get file structure for context."""
        tree = []
        for root, dirs, files in os.walk(root_dir):
            if any(x in root for x in ["legacy", ".git", "__pycache__", "node_modules", ".sandbox"]):
                continue
            level = root.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * (level)
            tree.append(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                tree.append(f'{subindent}{f}')
        return "\n".join(tree[:100]) # Limit to top 100 lines to save context
