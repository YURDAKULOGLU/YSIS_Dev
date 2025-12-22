import subprocess
import logging
import os
from typing import Dict, Any
from pathlib import Path

class GitManager:
    """
    The Git Giant. 
    Handles automatic commits and pushes to keep the workspace clean.
    """
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.logger = logging.getLogger("GitManager")

    def run_git(self, args: list) -> str:
        """Executes a git command and returns output."""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git Error: {e.stderr}")
            raise Exception(f"Git command failed: {e.stderr}")

    async def commit_task(self, task_id: str, message: str) -> bool:
        """Stages relevant changes and commits them."""
        try:
            print(f"[GitManager] Cleaning up workspace for {task_id}...")
            
            # 1. Stage only relevant directories to avoid 'nul' file errors
            # We focus on the areas the factory actually works in
            for folder in ["src", "tests", "config", "scripts", "Knowledge", "docs"]:
                if os.path.exists(self.project_root / folder):
                    self.run_git(["add", folder])
            
            # Also add root markdown files if any changed
            self.run_git(["add", "*.md"])
            
            # 2. Check status
            status = self.run_git(["status", "--porcelain"])
            if not status:
                print("[GitManager] No relevant changes to commit.")
                return True

            # 3. Commit
            full_message = f"AUTO-COMMIT [{task_id}]: {message}"
            self.run_git(["commit", "-m", full_message])
            print(f"[GitManager] Successfully committed: {full_message}")
            return True
        except Exception as e:
            print(f"[GitManager] [!] Commit failed: {e}")
            return False

    async def push_changes(self):
        """Pushes changes to remote."""
        try:
            print("[GitManager] Pushing to remote...")
            self.run_git(["push"])
            return True
        except Exception as e:
            print(f"[GitManager] [!] Push failed: {e}")
            return False

    def name(self) -> str:
        return "Git-Giant-Manager"
