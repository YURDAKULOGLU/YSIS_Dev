import os
import re
from datetime import datetime
from pathlib import Path
from src.orchestrator.config import PROJECT_ROOT

class WorkspaceManager:
    """
    Handles all workspace lifecycle tasks: creation, stub generation, and metadata parsing.
    Moved out of the God Object for a cleaner architecture.
    """
    
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.root = PROJECT_ROOT / "workspaces" / "active" / task_id
        self.docs_dir = self.root / "docs"
        self.artifacts_dir = self.root / "artifacts"

    def ensure_directories(self) -> tuple[Path, Path, Path]:
        """Creates the task workspace structure."""
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        return self.root, self.docs_dir, self.artifacts_dir

    def write_plan_stub(self, task_goal: str):
        """Generates the initial PLAN.md for the task."""
        plan_path = self.docs_dir / "PLAN.md"
        if plan_path.exists():
            return
        
        frontmatter = f"""---
id: {self.task_id}
type: PLAN
status: DRAFT
created_at: {datetime.now().isoformat()}
token_budget: 2000
target_files: []
---
# Task: {task_goal}

## Objective
{task_goal}

## Approach
Describe the architectural approach here.

## Steps
1. Initial Analysis
2. Implementation
3. Verification

## Risks & Mitigations
- Regressions: Covered by unit tests.

## Success Criteria
- Code passes linting.
- Tests pass.
"""
        plan_path.write_text(frontmatter, encoding="utf-8")

    def write_result_stub(self, task_goal: str, status: str = "COMPLETED"):
        """Generates the final RESULT.md summary."""
        result_path = self.artifacts_dir / "RESULT.md"
        if result_path.exists() and result_path.read_text(encoding="utf-8").strip():
            return
            
        frontmatter = f"""---
id: {self.task_id}
type: RESULT
status: {status}
completed_at: {datetime.now().isoformat()}
token_budget: 2000
---
# Task Result: {task_goal}

## Summary
Brief summary of the changes.

## Changes Made
- Implement feature X
- Fix bug Y

## Files Modified
- src/...

## Tests Run
- tests/...

## Verification
- Ruff: OK
- Pytest: OK
"""
        result_path.write_text(frontmatter, encoding="utf-8")

    @staticmethod
    def parse_frontmatter(content: str) -> dict[str, str]:
        """Helper to extract metadata from markdown files."""
        if not content.startswith("---"):
            return {}
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}
        _, fm_text, _ = parts
        fm = {}
        for line in fm_text.strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                fm[key.strip()] = value.strip()
        return fm
