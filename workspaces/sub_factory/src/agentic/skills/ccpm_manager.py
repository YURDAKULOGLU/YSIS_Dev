"""
CCPM (Claude Code PM) Manager Skill
Integrates industrial-grade project management into YBIS.
Uses Git Worktrees for 100% agent isolation.
"""

import subprocess
import os
import json
from pathlib import Path
from typing import Dict, Any, List

class CCPMManager:
    def __init__(self, tools_dir: str = "tools/ccpm"):
        self.tools_dir = Path(tools_dir)
        self.worktree_base = Path("workspaces/worktrees")
        self.worktree_base.mkdir(parents=True, exist_ok=True)

    def create_worktree(self, task_id: str, branch_name: str) -> Dict[str, Any]:
        """Create a new git worktree for a specific task"""
        target_path = self.worktree_base / task_id
        print(f"🚜 Creating worktree at: {target_path}")
        
        try:
            # 1. Create branch
            subprocess.run(["git", "checkout", "-b", branch_name], capture_output=True)
            
            # 2. Add worktree
            cmd = ["git", "worktree", "add", str(target_path), branch_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            return {
                "success": result.returncode == 0,
                "path": str(target_path),
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def sync_github_issue(self, task_id: str, title: str, body: str):
        """Placeholder for CCPM GitHub sync (Future integration)"""
        print(f"🔗 Syncing Task {task_id} to GitHub via CCPM logic...")
        # CCPM logic would run here to map local task -> github issue
        return True

    def cleanup_worktree(self, task_id: str):
        """Safely remove a worktree after task completion"""
        target_path = self.worktree_base / task_id
        subprocess.run(["git", "worktree", "remove", str(target_path)], capture_output=True)
        print(f"🧹 Worktree cleaned for {task_id}")
