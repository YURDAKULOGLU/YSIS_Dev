from .base_agent import YBISAgent, CodeOutput # Changed ConstitutionCompliantCode to CodeOutput
from ..Tools.code_exec import code_exec
import re
import os
import json # Add json import
from Agentic.inference.router import IntelligentRouter, TaskType
from pydantic import ValidationError # Import for explicit ValidationError handling

class DeveloperAgent(YBISAgent):
    def __init__(self, router: IntelligentRouter):
        super().__init__(
            agent_id="developer",
            router=router,
            task_type=TaskType.CODE_GENERATION,
            output_model=CodeOutput # Enforce Pydantic output
        )

    async def verify_code(self, file_path: str, code: str) -> str:
        """Try to execute/compile the code to check for syntax errors."""
        temp_dir = os.path.join(os.path.dirname(__file__), "../../.temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, os.path.basename(file_path))

        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(code)

            result = "Skipped verification (unsupported type)"

            if file_path.endswith(".py"):
                result = code_exec.run_python(code)

            return result
        except Exception as e:
            return f"Error during code verification: {e}"
        finally:
            if os.path.exists(temp_path):
                try: os.remove(temp_path)
                except: pass

    # Removed _parse_raw_response as Pydantic handles it now

    async def implement(self, spec: str) -> CodeOutput: # Changed return type
        # Extract task from spec
        task_line = spec.split('\n')[0] if '\n' in spec else spec

        # Get schema
        output_schema = CodeOutput.model_json_schema()

        prompt = f"""You are a code generator.
Your goal is to implement the given specification as code.
You MUST return your response as a JSON object that strictly adheres to the CodeOutput Pydantic model.

The JSON schema for CodeOutput is:
{json.dumps(output_schema, indent=2)}

Example of valid JSON output:
```json
{{
  "file_path": "src/hello.py",
  "code": "def hello():\\n    print('Hello World')",
  "explanation": "Implemented hello world function",
  "language": "python"
}}
```

Specification: {task_line}

Rules for code generation:
1. ONLY write Python code.
2. Output MUST be a valid JSON object matching the CodeOutput schema.
3. No additional text, explanations, or markdown outside the JSON object.
"""

        try:
            raw_result = await self.run(prompt)
            print(f"[DEBUG] Raw LLM output from Developer: {raw_result}") # DEBUG PRINT
            # Result is already unwrapped by base_agent.py
            code_obj: CodeOutput = raw_result

            print(f"[DEBUG] Developer Pydantic output: {code_obj}")

            # Self-Verification
            if code_obj.file_path and code_obj.code:
                verification_result = await self.verify_code(code_obj.file_path, code_obj.code)
                if "Error" in verification_result:
                    print(f"[WARNING] [Developer] Self-Verification Warning: {verification_result}")

            return code_obj

        except ValidationError as ve:
            print(f"[ERROR] [Developer] Pydantic Validation Error: LLM output did not conform to schema: {ve}")
            # The LLM output did not conform to the CodeOutput schema.
            # We could implement a retry mechanism here to prompt the LLM again with error feedback.
            raise ve # Re-raise to fail the task for now
        except Exception as e:
            print(f"[ERROR] [Developer] Error during implementation: {e}")
            raise e # Re-raise to fail the task

developer = DeveloperAgent(None)
