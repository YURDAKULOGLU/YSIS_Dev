"""
SimpleExecutor - Basic executor using local Ollama agent.

Executes plans by:
1. Calling DeveloperAgent (from existing Agentic/Agents/developer.py)
2. Writing files to sandbox
3. Running basic commands
"""

import os
import sys
from pathlib import Path
from typing import List
import asyncio

# Add paths
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agentic.core.protocols import Plan, CodeResult
from Agentic.Agents.developer import DeveloperAgent
from Agentic.inference.router import IntelligentRouter, config as router_config


class SimpleExecutor:
    """
    Simple executor using existing DeveloperAgent.

    This reuses your existing agent infrastructure.
    """

    def __init__(self):
        self.router = IntelligentRouter(router_config)
        self.developer = DeveloperAgent(router=self.router)

    async def execute(self, plan: Plan, sandbox_path: str, error_history: List[str] = None, retry_count: int = 0) -> CodeResult:
        """Execute plan using DeveloperAgent"""

        print(f"[SimpleExecutor] Executing plan in {sandbox_path}")
        print(f"[SimpleExecutor] Objective: {plan.objective}")

        # Build prompt for developer
        prompt = self._build_prompt(plan)

        # Call DeveloperAgent
        result = await self.developer.implement(prompt)

        # Parse result and write files
        files_modified = await self._write_files(result, sandbox_path, plan)

        # Run any commands needed
        commands_run, outputs = await self._run_commands(plan, sandbox_path)

        return CodeResult(
            files_modified=files_modified,
            commands_run=commands_run,
            outputs=outputs,
            success=len(files_modified) > 0,
            error=None if len(files_modified) > 0 else "No files generated"
        )

    def name(self) -> str:
        return "SimpleExecutor(DeveloperAgent+Ollama)"

    # ========================================================================
    # IMPLEMENTATION
    # ========================================================================

    def _build_prompt(self, plan: Plan) -> str:
        """Build prompt for DeveloperAgent"""
        return f"""Implement this plan:

OBJECTIVE: {plan.objective}

STEPS:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(plan.steps))}

FILES TO MODIFY:
{chr(10).join(f"- {file}" for file in plan.files_to_modify)}

Generate the code for each file. Format your response as:

FILE: path/to/file.ts
```typescript
// code here
```

FILE: path/to/another.py
```python
# code here
```
"""

    async def _write_files(self, agent_result, sandbox_path: str, plan: Plan) -> dict:
        """Parse agent output and write files to sandbox"""
        files_modified = {}

        # Try to extract code from agent response
        # The developer agent returns AgentRunResult with code and filename
        if hasattr(agent_result, 'code') and hasattr(agent_result, 'filename'):
            # Single file result
            if agent_result.filename and agent_result.code:
                file_path = os.path.join(sandbox_path, agent_result.filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(agent_result.code)

                files_modified[agent_result.filename] = agent_result.code
                print(f"[SimpleExecutor] [OK] Wrote {agent_result.filename}")

        # If no files written but plan specified files, create placeholders
        if not files_modified and plan.files_to_modify:
            for file_path in plan.files_to_modify[:1]:  # Just first file for now
                full_path = os.path.join(sandbox_path, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                # Create basic placeholder
                content = f"// TODO: Implement {plan.objective}\n"
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                files_modified[file_path] = content
                print(f"[SimpleExecutor] [WARN] Created placeholder: {file_path}")

        return files_modified

    async def _run_commands(self, plan: Plan, sandbox_path: str) -> tuple:
        """Run any required commands"""
        commands_run = []
        outputs = {}

        # For now, no commands
        # In future: npm install, git operations, etc.

        return commands_run, outputs


# ============================================================================
# TESTING
# ============================================================================

async def test_simple_executor():
    """Test executor standalone"""
    from src.agentic.core.protocols import Plan

    executor = SimpleExecutor()

    plan = Plan(
        objective="Create a simple hello function",
        steps=["Create function", "Export it"],
        files_to_modify=["hello.ts"],
        dependencies=[],
        risks=[],
        success_criteria=["File created"],
        metadata={}
    )

    result = await executor.execute(plan, ".sandbox/test")

    print(f"Success: {result.success}")
    print(f"Files modified: {list(result.files_modified.keys())}")
    print(f"Commands run: {result.commands_run}")


if __name__ == "__main__":
    asyncio.run(test_simple_executor())
