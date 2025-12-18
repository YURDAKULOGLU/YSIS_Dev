"""
ArtifactGenerator - Generates all documentation artifacts.

Creates:
- STATE_SNAPSHOT.json
- PLAN.md
- RUNBOOK.md
- DECISIONS.json
- EVIDENCE/lint.log, test.log, smoke.log
"""

import json
import os
from datetime import datetime
from typing import Dict

from src.agentic.core.protocols import TaskState


class ArtifactGenerator:
    """Generates deterministic artifacts for every task execution"""

    async def generate(self, state: TaskState) -> Dict[str, str]:
        """
        Generate all artifacts.

        Returns:
            Dict of {relative_path: content}
        """
        artifacts = {}

        # STATE_SNAPSHOT.json
        artifacts["STATE_SNAPSHOT.json"] = self._generate_state_snapshot(state)

        # PLAN.md (if plan exists)
        if state.plan:
            artifacts["PLAN.md"] = self._generate_plan_md(state)

        # RUNBOOK.md
        artifacts["RUNBOOK.md"] = self._generate_runbook_md(state)

        # DECISIONS.json (if any decisions made)
        artifacts["DECISIONS.json"] = self._generate_decisions_json(state)

        # EVIDENCE/logs
        if state.verification:
            for log_name, log_content in state.verification.logs.items():
                artifacts[f"EVIDENCE/{log_name}.log"] = log_content

        return artifacts

    # ========================================================================
    # GENERATORS
    # ========================================================================

    def _generate_state_snapshot(self, state: TaskState) -> str:
        """Generate STATE_SNAPSHOT.json"""
        snapshot = {
            "task_id": state.task_id,
            "phase": state.phase,
            "started_at": state.started_at.isoformat() if state.started_at else None,
            "completed_at": state.completed_at.isoformat() if state.completed_at else None,
            "retry_count": state.retry_count,
            "max_retries": state.max_retries,
            "error": state.error,
            "success": state.phase == "done",
        }
        return json.dumps(snapshot, indent=2)

    def _generate_plan_md(self, state: TaskState) -> str:
        """Generate PLAN.md"""
        plan = state.plan

        md = f"""# Task: {state.task_id}

## Objective
{plan.objective}

## Task Description
{state.task_description}

## Execution Steps
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(plan.steps))}

## Files to Modify
{chr(10).join(f"- `{file}`" for file in plan.files_to_modify)}

## Dependencies
{chr(10).join(f"- {dep}" for dep in plan.dependencies) if plan.dependencies else "None"}

## Risks
{chr(10).join(f"- {risk}" for risk in plan.risks) if plan.risks else "None"}

## Success Criteria
{chr(10).join(f"- [ ] {criterion}" for criterion in plan.success_criteria)}

## Metadata
```json
{json.dumps(plan.metadata, indent=2)}
```

---
*Generated: {datetime.now().isoformat()}*
"""
        return md

    def _generate_runbook_md(self, state: TaskState) -> str:
        """Generate RUNBOOK.md"""
        md = f"""# Execution Log: {state.task_id}

## Task
{state.task_description}

## Timeline
- **Started:** {state.started_at.isoformat() if state.started_at else 'N/A'}
- **Completed:** {state.completed_at.isoformat() if state.completed_at else 'In progress'}
- **Duration:** {self._format_duration(state)}

## Execution Phases

### Phase: INIT
- Sandbox setup at `{state.artifacts_path}`
- Context loaded

### Phase: PLAN
"""
        if state.plan:
            md += f"""- Objective: {state.plan.objective}
- Steps: {len(state.plan.steps)}
- Files: {len(state.plan.files_to_modify)}
- Gate: {'[OK] PASSED' if state.phase != 'plan' else '[WARN] IN PROGRESS'}

"""

        md += """### Phase: EXECUTE
"""
        if state.code_result:
            md += f"""- Files modified: {len(state.code_result.files_modified)}
- Commands run: {len(state.code_result.commands_run)}
- Success: {state.code_result.success}
- Gate: {'[OK] PASSED' if state.phase not in ['plan', 'execute'] else '[WARN] IN PROGRESS'}

#### Files Generated:
{chr(10).join(f"- `{file}`" for file in state.code_result.files_modified.keys())}

"""

        md += """### Phase: VERIFY
"""
        if state.verification:
            md += f"""- Lint: {'[OK] PASSED' if state.verification.lint_passed else '[X] FAILED'}
- Tests: {'[OK] PASSED' if state.verification.tests_passed else '[X] FAILED'}
- Coverage: {state.verification.coverage:.1%}
- Gate: {'[OK] PASSED' if state.phase == 'commit' or state.phase == 'done' else '[X] FAILED'}

"""

        md += f"""### Phase: COMMIT
- Status: {'[OK] COMPLETED' if state.phase == 'done' else 'Pending'}

## Final Status
**{state.phase.upper()}**

"""
        if state.error:
            md += f"""## Error
```
{state.error}
```

"""

        md += f"""---
*Generated: {datetime.now().isoformat()}*
"""
        return md

    def _generate_decisions_json(self, state: TaskState) -> str:
        """Generate DECISIONS.json"""
        decisions = {
            "task_id": state.task_id,
            "timestamp": datetime.now().isoformat(),
            "decisions": [
                # For now, just track retry decisions
                {
                    "question": "Should retry after failure?",
                    "chosen": f"Yes ({state.retry_count}/{state.max_retries})" if state.retry_count > 0 else "N/A",
                    "rationale": "Gate validation failed"
                }
            ],
            "config": {
                "max_retries": state.max_retries,
                "retry_count": state.retry_count,
                "sandbox_path": state.artifacts_path
            }
        }
        return json.dumps(decisions, indent=2)

    def _format_duration(self, state: TaskState) -> str:
        """Format task duration"""
        if not state.started_at:
            return "N/A"
        if not state.completed_at:
            delta = datetime.now() - state.started_at
        else:
            delta = state.completed_at - state.started_at

        return f"{delta.total_seconds():.1f}s"
