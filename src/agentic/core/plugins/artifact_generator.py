import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict

from src.agentic.core.config import PROJECT_ROOT
from src.agentic.core.protocols import TaskState


class ArtifactGenerator:
    """
    Generates documentation and logs for completed tasks using Pydantic State.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger("ArtifactGen")

    def name(self) -> str:
        return "ArtifactGenerator"

    def _workspace_root(self, state: TaskState) -> Path:
        return Path(state.artifacts_path).resolve().parent

    def _read_existing(self, path: Path) -> str | None:
        if path.exists():
            content = path.read_text(encoding="utf-8").strip()
            return content if content else None
        return None

    def _normalize_paths(self, paths: list[str]) -> list[str]:
        root = Path(PROJECT_ROOT).resolve()
        normalized: list[str] = []
        for path in paths:
            try:
                normalized.append(str(Path(path).resolve().relative_to(root)))
            except ValueError:
                normalized.append(str(Path(path)))
        return normalized

    def _build_plan(self, state: TaskState) -> str:
        plan = state.plan
        steps = plan.steps if plan else []
        files_to_modify = plan.files_to_modify if plan else []
        risks = plan.risks if plan else []
        success = plan.success_criteria if plan else []

        frontmatter = (
            "---\n"
            f"id: {state.task_id}\n"
            "type: PLAN\n"
            "status: FINAL\n"
            f"created_at: {(state.started_at or datetime.now()).isoformat()}\n"
            "token_budget: 2000\n"
            "target_files:\n"
        )
        for file in files_to_modify:
            frontmatter += f"- {file}\n"
        frontmatter += "---\n"

        body = f"# Task: {state.task_description or state.task_id}\n\n"
        body += "## Objective\n"
        body += f"{plan.objective if plan else ''}\n\n"
        body += "## Steps\n"
        if steps:
            for idx, step in enumerate(steps, start=1):
                body += f"{idx}. {step}\n"
        else:
            body += "1. \n"
        body += "\n## Risks & Mitigations\n"
        if risks:
            for item in risks:
                body += f"- {item}\n"
        else:
            body += "- None noted.\n"
        body += "\n## Success Criteria\n"
        if success:
            for item in success:
                body += f"- {item}\n"
        else:
            body += "- Protocol check passes.\n"

        return frontmatter + body

    def _build_runbook(self, state: TaskState) -> str:
        commands: list[str] = []
        if state.code_result and state.code_result.commands_run:
            commands.extend(state.code_result.commands_run)
        if not commands:
            return ""
        return "\n".join(commands) + "\n"

    def _build_result(self, state: TaskState) -> str:
        files = self._normalize_paths(state.files_modified or [])
        verification = state.verification
        lint_status = "PASS" if verification and verification.lint_passed else "FAIL"
        test_status = "PASS" if verification and verification.tests_passed else "FAIL"

        frontmatter = (
            "---\n"
            f"id: {state.task_id}\n"
            "type: RESULT\n"
            f"status: {state.final_status}\n"
            f"completed_at: {(state.completed_at or datetime.now()).isoformat()}\n"
            "token_budget: 2000\n"
            "---\n"
        )

        body = f"# Task Result: {state.task_description or state.task_id}\n\n"
        body += "## Summary\n"
        body += f"- Status: {state.final_status}\n"
        if state.error_history:
            body += "- Notes: Errors recorded during execution.\n"
        body += "\n## Changes Made\n"
        if state.plan:
            body += f"- Objective: {state.plan.objective}\n"
        else:
            body += "- Objective: Not recorded.\n"

        body += "\n## Files Modified\n"
        if files:
            for item in files:
                body += f"- {item}\n"
        else:
            body += "- None recorded.\n"

        body += "\n## Tests Run\n"
        body += f"- Lint: {lint_status}\n"
        body += f"- Tests: {test_status}\n"

        body += "\n## Verification\n"
        if verification and verification.warnings:
            for warning in verification.warnings:
                body += f"- Warning: {warning}\n"
        else:
            body += "- No warnings.\n"

        if state.error_history:
            body += "\n## Notes\n"
            for err in state.error_history:
                body += f"- {err}\n"

        return frontmatter + body

    def _build_changes(self, state: TaskState) -> str:
        files_modified = state.code_result.files_modified if state.code_result else {}
        normalized = self._normalize_paths(list(files_modified.keys()))
        statuses = list(files_modified.values())
        entries = []
        for idx, path in enumerate(normalized):
            status = statuses[idx] if idx < len(statuses) else "M"
            entries.append({
                "path": path,
                "status": status,
                "purpose": "modified by task"
            })

        payload = {
            "task_id": state.task_id,
            "generated_at": datetime.now().isoformat(),
            "changed_files": entries
        }
        return json.dumps(payload, indent=2)

    def _build_meta(self, state: TaskState) -> str:
        payload = {
            "task_id": state.task_id,
            "status": state.final_status,
            "phase": state.phase,
            "started_at": state.started_at.isoformat() if state.started_at else None,
            "completed_at": state.completed_at.isoformat() if state.completed_at else None,
            "quality_score": state.quality_score,
            "files_modified": self._normalize_paths(state.files_modified or []),
            "constitution_tags": ["\u00a71", "\u00a73", "\u00a74", "\u00a75"],
        }
        if state.verification:
            payload["verification"] = {
                "lint_passed": state.verification.lint_passed,
                "tests_passed": state.verification.tests_passed,
                "warnings": state.verification.warnings,
                "errors": state.verification.errors,
            }
        if state.plan:
            payload["plan"] = {
                "objective": state.plan.objective,
                "steps": state.plan.steps,
                "files_to_modify": state.plan.files_to_modify,
            }
        return json.dumps(payload, indent=2)

    async def generate(self, state: TaskState) -> Dict[str, str]:
        root = self._workspace_root(state)
        outputs: dict[str, str] = {}

        plan_path = root / "docs" / "PLAN.md"
        runbook_path = root / "docs" / "RUNBOOK.md"
        result_path = root / "artifacts" / "RESULT.md"
        meta_path = root / "META.json"
        changes_path = root / "CHANGES" / "changed_files.json"

        outputs["docs/PLAN.md"] = self._read_existing(plan_path) or self._build_plan(state)
        outputs["docs/RUNBOOK.md"] = self._read_existing(runbook_path) or self._build_runbook(state)
        outputs["artifacts/RESULT.md"] = self._read_existing(result_path) or self._build_result(state)
        outputs["META.json"] = self._read_existing(meta_path) or self._build_meta(state)
        outputs["CHANGES/changed_files.json"] = self._read_existing(changes_path) or self._build_changes(state)

        return outputs
