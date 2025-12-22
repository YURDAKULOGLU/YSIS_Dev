import os
import logging
from typing import Dict, Any
from dataclasses import asdict

class ArtifactGenerator:
    """
    Generates documentation and logs for completed tasks.
    """
    def __init__(self):
        self.logger = logging.getLogger("ArtifactGen")

import os
import logging
from typing import Dict, Any
from src.agentic.core.protocols import TaskState

class ArtifactGenerator:
    """
    Generates documentation and logs for completed tasks using Pydantic State.
    """
    def __init__(self):
        self.logger = logging.getLogger("ArtifactGen")

    async def generate(self, state: TaskState) -> Dict[str, str]:
        """
        Create a report of what was done.
        Returns a dict of {filename: content} as per protocol.
        """
        task_id = state.task_id
        plan = state.plan
        files = state.files_modified
        
        report_content = f"# Task Execution Report: {task_id}\n\n"
        report_content += f"## Status: {state.final_status}\n\n"
        
        report_content += f"## Files Modified:\n"
        if files:
            for file in files:
                report_content += f"- {file}\n"
        else:
            report_content += "No files recorded.\n"
        
        report_content += f"\n## Plan Executed:\n"
        if plan:
            for step in plan.steps:
                report_content += f"- {step}\n"
        else:
            report_content += "No plan recorded.\n"

        if state.error_history:
            report_content += f"\n## Error History:\n"
            for err in state.error_history:
                report_content += f"- {err}\n"

        return {"SUMMARY.md": report_content}

    def name(self) -> str:
        return "ArtifactGenerator"

    def name(self) -> str:
        return "ArtifactGenerator"