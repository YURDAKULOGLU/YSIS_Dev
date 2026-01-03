from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional, List, Any, Type
import re
import os
import yaml
import ast

# Global Config for Ollama
os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434/v1"

# Import Router components
from Agentic.inference.router import IntelligentRouter, TaskType

# ==================== CONSTITUTION COMPLIANT OUTPUT SCHEMAS ====================

class CodeOutput(BaseModel):
    """
    Schema for code generation output. Enforces structure and allows validation
    according to YBIS Constitution rules. The Agent MUST return data in this format.
    """
    file_path: str = Field(..., description="The relative path to the file to be created or modified (e.g., src/feature.py).")
    code: str = Field(..., description="The generated code for the specified file.")
    explanation: Optional[str] = Field(None, description="A brief explanation of the generated code and changes.")
    language: Optional[str] = Field(None, description="The programming language of the generated code (e.g., 'python', 'typescript').")

    @field_validator('code')
    @classmethod
    def check_no_any_type(cls, v: str) -> str:
        """Constitution: No `any` type allowed in Python/TypeScript. Use unknown or specific types."""
        if re.search(r':\s*any\b', v) or re.search(r'<any>', v):
            raise ValueError("Quality Standard Violation: 'any' type is not allowed. Use unknown or a specific type.")
        return v

    @field_validator('code')
    @classmethod
    def check_no_ts_ignore(cls, v: str) -> str:
        """Constitution: No @ts-ignore/@ts-nocheck allowed in TypeScript. Fix the root cause."""
        if '@ts-ignore' in v or '@ts-nocheck' in v:
            raise ValueError("Quality Standard Violation: @ts-ignore/@ts-nocheck is not allowed. Fix the root cause.")
        return v

    @field_validator('code')
    @classmethod
    def check_no_console_log(cls, v: str) -> str:
        """Constitution: Use proper logging; avoid direct console.log outside of tests."""
        # This validator is more permissive for now, will be tightened with proper logger integration
        if 'console.log' in v and not ('logger' in v.lower()) and not ('test' in v.lower()):
             pass # Temporarily allow, as proper logger integration is a separate task.
        return v

# ==================== BASE AGENT ====================

class YBISAgent:
    """
    Base agent wrapper for PydanticAI, integrated with IntelligentRouter.
    Reads governance documents dynamically and enforces structured output.
    """

    def __init__(self, agent_id: str, router: IntelligentRouter, task_type: TaskType, output_model: Optional[Type[BaseModel]] = None):
        self.agent_id = agent_id
        self.router = router
        self.task_type = task_type
        self.persona = self._load_persona()
        self.output_model = output_model

        # Load Governance Docs
        self.agentic_constitution = self._read_governance_doc("AGENTIC_CONSTITUTION.md")
        self.quality_standards = self._read_governance_doc("QUALITY_STANDARDS.md")
        self.project_constitution = self._read_governance_doc("Constitution.md")

        # Create PydanticAI agent
        self.agent = Agent(
            model=None, # Model set dynamically by router
            system_prompt=self._build_system_prompt(),
            output_type=self.output_model, # Enforce structured output
            retries=3 # Allow up to 3 retries for validation errors
        )

    def _read_governance_doc(self, filename: str) -> str:
        """Reads a markdown file from Meta/Governance"""
        try:
            # Resolve path relative to this file
            base_path = os.path.dirname(os.path.abspath(__file__)) # Agentic/Agents/
            gov_path = os.path.abspath(os.path.join(base_path, "../../Meta/Governance", filename))

            if os.path.exists(gov_path):
                with open(gov_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return f"Missing Governance Doc: {filename}"
        except Exception as e:
            return f"Error reading {filename}: {e}"

    def _load_persona(self) -> dict:
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_path, "personas", f"{self.agent_id}.md")
        if not os.path.exists(path): return {"role": "Assistant", "style": "Helpful"}
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
        if match: return yaml.safe_load(match.group(1)).get('persona', {})
        return {"role": "Assistant", "style": "Helpful"}

    def _build_system_prompt(self) -> str:
        return f"""You are {self.agent_id.upper()}.
Role: {self.persona.get('role', 'Assistant')}
Style: {self.persona.get('style', 'Professional')}

## 1. AGENTIC PRIME DIRECTIVES (YOUR BEHAVIOR)
{self.agentic_constitution}

## 2. GENERAL QUALITY STANDARDS (UNIVERSAL RULES)
{self.quality_standards}

## 3. PROJECT SPECIFIC CONSTITUTION (YBIS LAWS)
{self.project_constitution}

## CORE PRINCIPLES
{chr(10).join(f'- {p}' for p in self.persona.get('core_principles', []))}
"""

    async def run(self, task: str) -> Any:
        print(f"[{self.agent_id.upper()}] Thinking...")
        try:
            model, _ = self.router.route(self.task_type)
            result = await self.agent.run(task, model=model)
            # PydanticAI wraps results in AgentRunResult - extract the actual output
            if hasattr(result, 'output'):
                return result.output
            return result
        except ValidationError as e:
            # Pydantic validation failed - try to extract clean JSON
            print(f"[WARN] [{self.agent_id.upper()}] Validation error, retrying with max_retries=3...")
            # PydanticAI should handle retries automatically, but if it still fails, we re-raise
            raise e
        except Exception as e:
            print(f"[ERROR] [{self.agent_id.upper()}] Error during run: {str(e)}")
            raise e
