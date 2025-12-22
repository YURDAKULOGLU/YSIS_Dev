import os
import subprocess
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.agentic.core.protocols import ExecutorProtocol, Plan, CodeResult
from src.agentic.core.plugins.model_router import default_router

class AiderExecutorEnhanced(ExecutorProtocol):
    """
    Enhanced Executor that enforces YBIS Constitution and Test-First workflow.
    Injects architectural principles and coding standards into every prompt.
    """

    def __init__(self, router=None):
        self.router = router or default_router
        self.constitution_path = "docs/governance/YBIS_CONSTITUTION.md"

    def name(self) -> str:
        return "Aider-Enhanced-Executor"

    async def execute(self, plan: Plan, sandbox_path: str, error_history: List[str] = None, retry_count: int = 0) -> CodeResult:
        """
        Execute the plan with enhanced prompt engineering and strict enforcement.
        """
        model_config = self.router.get_model("CODING")
        print(f"[AiderEnhanced] Using model: {model_config.model_name} ({model_config.provider})")

        # 1. Load Contextual Knowledge
        constitution = ""
        if os.path.exists(self.constitution_path):
            try:
                with open(self.constitution_path, "r", encoding="utf-8") as f:
                    constitution = f.read()
            except Exception:
                pass

        # 2. Construct the Hyper-Prompt
        prompt = "### YBIS ENHANCED EXECUTION PROTOCOL ###\n"
        prompt += "You are an elite autonomous developer in the YBIS Software Factory.\n\n"
        
        if constitution:
            prompt += "## CONSTITUTIONAL MANDATES (FOLLOW STRICTLY):\n"
            prompt += constitution + "\n\n"

        prompt += "## CODE STANDARDS:\n"
        prompt += "- Style: PEP8, snake_case for functions and variables.\n"
        prompt += "- Documentation: Google-style docstrings for all classes and functions.\n"
        prompt += "- Typing: MANDATORY type hints for all parameters and return types.\n"
        prompt += "- Quality: Ensure the code passes 'ruff check' with zero errors.\n\n"

        prompt += "## TEST-FIRST WORKFLOW:\n"
        prompt += "1. Identify the core logic being added or modified.\n"
        prompt += "2. CREATE or UPDATE a unit test in 'tests/unit/' that covers this logic.\n"
        prompt += "3. IMPLEMENT the code to make the test pass.\n"
        prompt += "4. Verification will fail if no tests are added/updated for new features.\n\n"

        if error_history and len(error_history) > 0:
            prompt += "## RECOVERY PROTOCOL (FIX PREVIOUS ERRORS):\n"
            for i, err in enumerate(error_history):
                prompt += f"ERR_{i}: {err}\n"
            prompt += "Analyze why the previous attempt failed and implement a robust fix.\n\n"

        prompt += f"## MISSION OBJECTIVE:\n{plan.objective}\n\n"
        prompt += "## EXECUTION STEPS:\n"
        for i, step in enumerate(plan.steps):
            prompt += f"{i+1}. {step}\n"

        # 3. Handle File Paths
        from src.agentic.core.config import PROJECT_ROOT
        git_root = Path(PROJECT_ROOT).resolve()
        
        files = plan.files_to_modify if plan.files_to_modify else []
        normalized_files = []
        for f in files:
            f_path = Path(f)
            if f_path.is_absolute():
                full_path = f_path
            else:
                full_path = git_root / f_path
            
            try:
                rel_to_root = full_path.relative_to(git_root)
                normalized_files.append(str(rel_to_root))
            except ValueError:
                normalized_files.append(str(full_path))

        # 4. Construct Command
        cmd = ["aider"]
        cmd.extend(normalized_files)
        
        prompt += f"\nNote: All paths provided are relative to the Git Root: {git_root}\n"
        cmd.extend(["--message", prompt])

        model_full_name = model_config.model_name
        if model_config.provider == "ollama":
            model_full_name = f"ollama/{model_config.model_name}"
        cmd.extend(["--model", model_full_name])
        
        cmd.extend([
            "--model-settings-file", "config/aider_model_settings.yml",
            "--no-show-model-warnings",
            "--no-pretty",
            "--no-auto-lint",
            "--no-suggest-shell-commands",
            "--aiderignore", "config/.sandbox_aiderignore",
            "--yes",
            "--no-auto-commits"
        ])

        # 5. Execute Aider
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=None,
                stderr=None,
                cwd=str(git_root),
                env=os.environ
            )
            await process.wait()
            success = (process.returncode == 0)

            # Detect Changes (Optimized filtering)
            actual_files = {}
            try:
                proc = await asyncio.create_subprocess_shell(
                    "git status --porcelain",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(git_root)
                )
                stdout, _ = await proc.communicate()
                for line in stdout.decode('utf-8').splitlines():
                    status_code = line[:2].strip()
                    path = line[3:].strip().replace('"', '')
                    if " -> " in path:
                        path = path.split(" -> ")[-1].strip()
                    
                    # ONLY report changes in allowed directories
                    if path.startswith("src/") or path.startswith("tests/"):
                        abs_path = (git_root / path).resolve()
                        actual_files[str(abs_path)] = status_code
            except Exception:
                # Fallback only to files we intended to modify
                actual_files = {f: "Modified" for f in normalized_files}

            return CodeResult(
                files_modified=actual_files,
                commands_run=[' '.join(cmd)],
                outputs={"status": "Executed"},
                success=success,
                error=None if success else "Aider execution failed (see logs)"
            )

        except Exception as e:
            return CodeResult(
                files_modified={},
                commands_run=[' '.join(cmd)],
                outputs={},
                success=False,
                error=str(e)
            )
