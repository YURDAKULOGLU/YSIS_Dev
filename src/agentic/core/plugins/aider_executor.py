import os
import subprocess
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from src.agentic.core.protocols import ExecutorProtocol, Plan, CodeResult

class AiderExecutor(ExecutorProtocol):
    """
    Executor that delegates coding tasks to 'aider', a powerful AI pair programmer.
    This acts as a bridge between our Orchestrator and the Aider CLI.
    """

    def name(self) -> str:
        return "Aider-CLI-Executor"

    async def execute(self, plan: Plan, sandbox_path: str) -> CodeResult:
        """
        Execute the plan by constructing a prompt for Aider and running it.
        """
        print(f"[AiderExecutor] Preparing to execute plan with {len(plan.steps)} steps.")

        # 1. Construct the prompt for Aider
        prompt = f"OBJECTIVE: {plan.objective}\n\nPLAN STEPS:\n"
        for i, step in enumerate(plan.steps):
            prompt += f"{i+1}. {step}\n"
        
        prompt += "\nIMPORTANT:\n"
        prompt += "- Implement these changes exactly.\n"
        prompt += "- Use REAL file paths. DO NOT use placeholders.\n"
        prompt += "- Run tests if valid.\n"


        # 2. Identify target files and normalize paths relative to Git Root
        files = plan.files_to_modify if plan.files_to_modify else []
        
        # Calculate Git Root
        current_path = Path(sandbox_path).resolve()
        git_root = current_path
        while not (git_root / ".git").exists() and git_root != git_root.parent:
            git_root = git_root.parent
            
        print(f"[AiderExecutor] Resolved Git Root: {git_root}")
        
        rel_path_from_root = current_path.relative_to(git_root)
        
        normalized_files = []
        for f in files:
            # We want to edit files in the REAL project, not the sandbox.
            # Planner usually returns paths relative to project root (e.g. "src/main.py").
            
            # Treat all paths as relative to git_root unless absolute
            f_path = Path(f)
            if f_path.is_absolute():
                full_path = f_path
            else:
                full_path = git_root / f_path
            
            try:
                # Calculate path relative to Git Root (Aider expects relative paths usually)
                rel_to_root = full_path.relative_to(git_root)
                normalized_files.append(str(rel_to_root))
            except ValueError:
                # If path is not inside git root, use absolute path
                normalized_files.append(str(full_path))
                
        print(f"[AiderExecutor] Normalized Files: {normalized_files}")

        # 3. Construct the command
        cmd = ["aider"]
        cmd.extend(normalized_files)
        
        # Update prompt to be explicit about paths
        prompt += f"\nNOTE: You are running in the Git Root: {git_root}\n"
        prompt += f"My Current Working Directory (Sandbox) is: {current_path}\n"
        prompt += f"Please edit files relative to the Git Root, e.g. {rel_path_from_root}/filename.py\n"

        cmd.extend(["--message", prompt])

        # FORCE LOCAL OLLAMA MODEL (UPGRADED)
        cmd.extend(["--model", "ollama/qwen2.5-coder:32b"])
        # Inject Model Settings to silence warnings
        cmd.extend(["--model-settings-file", ".YBIS_Dev/Veriler/aider_model_settings.yml"])
        cmd.extend(["--no-show-model-warnings"])
        
        # FORCE SANDBOX CONTAINMENT
        # Only allow Aider to see what we explicitly permit
        cmd.extend(["--aiderignore", ".YBIS_Dev/Veriler/.sandbox_aiderignore"])

        cmd.extend(["--yes"])
        cmd.extend(["--no-auto-commits"]) # Let Orchestrator handle commits after verification

        print(f"[AiderExecutor] Running command: {' '.join(cmd)}")

        # 4. Run Aider
        try:
            # We run synchronously for now as subprocess, but wrap in asyncio in real app
            # In a real async app we'd use asyncio.create_subprocess_exec
            process = await asyncio.create_subprocess_exec(
                *cmd,
                # Inherit stdout/stderr so user sees progress in real-time
                stdout=None,
                stderr=None,
                cwd=str(git_root),
                env=os.environ
            )
            
            await process.wait()
            
            success = process.returncode == 0
            output_str = "Output streamed to console."
            
            if success:
                print("[AiderExecutor] Success!")
            else:
                print("[AiderExecutor] Failed!")

            # Detect actually modified files using git
            actual_files = {}
            try:
                # We assume git_root is a git repo
                proc = await asyncio.create_subprocess_shell(
                    "git status --porcelain",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(git_root)
                )
                stdout, _ = await proc.communicate()
                entries = stdout.decode('utf-8').splitlines()
                
                for entry in entries:
                    # Format: " M path/to/file" or "?? path/to/file"
                    # We care about M, A, ??
                    status_code = entry[:2]
                    file_path = entry[3:].strip()
                    if file_path:
                         abs_path = (git_root / file_path).resolve()
                         actual_files[str(abs_path)] = f"Detected change: {status_code}"
            except Exception as git_err:
                 print(f"[AiderExecutor] Failed to detect changes: {git_err}")
                 # Fallback to plan files
                 actual_files = {f: "Modified by Aider (Fallback)" for f in files}

            return CodeResult(
                files_modified=actual_files,
                commands_run=[' '.join(cmd)],
                outputs={"aider": output_str},
                success=success,
                error=None if success else output_str
            )

        except Exception as e:
            return CodeResult(
                files_modified={},
                commands_run=[' '.join(cmd)],
                outputs={},
                success=False,
                error=str(e)
            )
