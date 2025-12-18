from .base_agent import YBISAgent
from Agentic.inference.router import IntelligentRouter, TaskType
from pydantic import BaseModel, ValidationError
from typing import List
import json # Moved here for correct scope
import re
import ast

class ArchitectPlan(BaseModel):
    """Architect's output plan structure."""
    technical_requirements: List[str]
    step_by_step_plan: List[str]
    files_to_create_modify: List[str]
    explanation: str

class ArchitectAgent(YBISAgent):
    def __init__(self, router: IntelligentRouter):
        super().__init__(
            agent_id="architect", 
            router=router, 
            task_type=TaskType.ARCHITECTURE,
            output_model=ArchitectPlan # Use output_model for structured output
        )

    # _extract_json method is no longer needed as output_model handles parsing

    async def analyze(self, task: str) -> ArchitectPlan:
        # ArchitectPlan'ın JSON Schema'sını al
        architect_plan_schema = ArchitectPlan.model_json_schema()

        prompt = f"""You are an Architect Agent. Your goal is to analyze the given task and create a detailed plan.
        Your response MUST be a JSON object that strictly adheres to the ArchitectPlan Pydantic model.

        The JSON schema for ArchitectPlan is:
        {json.dumps(architect_plan_schema, indent=2)}

        Example of a valid ArchitectPlan JSON output:
        ```json
        {{
          "technical_requirements": [
            "Implement a new feature to handle user authentication.",
            "Integrate with existing user database."
          ],
          "step_by_step_plan": [
            "1. Design database schema for user credentials.",
            "2. Implement API endpoints for login and registration.",
            "3. Develop UI components for login and registration forms."
          ],
          "files_to_create_modify": [
            "database/users_schema.sql",
            "api/auth_routes.py",
            "frontend/components/LoginForm.tsx"
          ],
          "explanation": "Plan for implementing user authentication feature."
        }}
        ```
        CRITICAL: If your output does not strictly conform to the ArchitectPlan Pydantic model and its JSON schema, the entire system will fail. You MUST produce a valid JSON object.
        """
        
        try:
            plan: ArchitectPlan = await self.run(prompt)
            return plan
        except ValidationError as ve:
            print(f"[ERROR] [Architect] Pydantic Validation Error: LLM output did not conform to schema: {ve}")
            raise ve
        except Exception as e:
            print(f"[ERROR] [Architect] Error during analysis: {e}")
            raise e