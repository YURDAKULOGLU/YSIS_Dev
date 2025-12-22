from .base_agent import YBISAgent
from Agentic.inference.router import IntelligentRouter, TaskType
from pydantic import BaseModel, Field
from typing import List, Optional

class QAValidationResult(BaseModel):
    """Structured output for QA Agent validation."""
    passed: bool = Field(..., description="True if code passes QA, False otherwise")
    issues: List[str] = Field(default_factory=list, description="List of issues found in the code")
    fix_suggestion: str = Field(default="", description="Suggestion on how to fix the issues")

class QAAgent(YBISAgent):
    def __init__(self, router: IntelligentRouter):
        super().__init__(
            agent_id="qa",
            router=router,
            task_type=TaskType.CODE_REVIEW,
            output_model=QAValidationResult
        )

    async def validate(self, code: str, requirements: str) -> QAValidationResult:
        prompt = f"""Review this code against requirements and output ONLY a JSON object.

Requirements:
{requirements}

Code to review:
```
{code}
```

Output a JSON object with these fields:
- "passed": true/false (boolean)
- "issues": [] (array of strings, empty if passed)
- "fix_suggestion": "" (string, empty if passed)

Examples:

If code is GOOD:
{{"passed": true, "issues": [], "fix_suggestion": ""}}

If code has ISSUES:
{{"passed": false, "issues": ["Syntax error on line 11", "Missing error handling"], "fix_suggestion": "Add try-catch and fix db.find_one() call"}}

Check for:
1. Syntax errors
2. Security issues (SQL injection, XSS, etc.)
3. Missing error handling
4. Code quality (proper naming, no console.log, etc.)

Output ONLY the JSON object, nothing else:"""

        try:
            validation_result = await self.run(prompt)
            print(f"[DEBUG] QA validation_result type: {type(validation_result)}")
            print(f"[DEBUG] QA validation_result: {validation_result}")
            return validation_result

        except Exception as e:
            print(f"[ERROR] [QA] Error during validation: {e}")
            raise e
