"""
SpecFirstWorkflow - End-to-end Spec-Driven Development orchestration

Implements the complete spec-first workflow:
1. Generate SPEC.md (if missing)
2. Validate spec exists
3. Create PLAN.md
4. Validate plan against spec
5. Execute plan
6. Validate implementation against spec
7. Generate compliance report
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime

from src.agentic.core.plugins.spec_writer_agent import SpecWriterAgent, SpecContent
from src.agentic.core.plugins.spec_validator import SpecValidator, ParsedSpec, ValidationResult
from src.agentic.core.config import USE_LITELLM, LITELLM_QUALITY
from src.agentic.core.utils.logging_utils import log_event


@dataclass
class WorkflowConfig:
    """Configuration for spec-first workflow"""
    require_spec: bool = True  # Block if spec missing
    validate_plan: bool = True  # Validate plan against spec
    validate_implementation: bool = True  # Validate code against spec
    use_llm_validation: bool = True  # Use LLM for semantic validation
    min_plan_score: float = 0.7  # Minimum plan compliance score
    min_impl_score: float = 0.7  # Minimum implementation compliance score
    auto_generate_spec: bool = True  # Auto-generate spec if missing
    interactive_review: bool = False  # Prompt user for spec review


@dataclass
class WorkflowResult:
    """Result of spec-first workflow execution"""
    success: bool
    phase: str  # Last completed phase
    spec_path: Optional[Path] = None
    plan_path: Optional[Path] = None
    spec_validation: Optional[ValidationResult] = None
    plan_validation: Optional[ValidationResult] = None
    impl_validation: Optional[ValidationResult] = None
    error: Optional[str] = None
    warnings: List[str] = None
    artifacts: Dict[str, Path] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
        if self.artifacts is None:
            self.artifacts = {}


def _log(message: str) -> None:
    log_event(message, component="spec_first_workflow")


class SpecFirstWorkflow:
    """
    Orchestrates the complete Spec-Driven Development workflow.

    Workflow phases:
    1. SPEC GENERATION: Generate or validate SPEC.md exists
    2. SPEC VALIDATION: Parse and validate spec completeness
    3. PLAN CREATION: Create PLAN.md (existing planner)
    4. PLAN VALIDATION: Validate plan against spec requirements
    5. IMPLEMENTATION: Execute plan (existing executor)
    6. IMPL VALIDATION: Validate implementation against spec
    7. REPORTING: Generate compliance report

    Features:
    - Enforces spec-first discipline (SPEC.md required)
    - Validates at each gate (spec → plan → implementation)
    - Blocks on validation failures (configurable)
    - Generates compliance reports
    - Integrates with existing SimplePlannerV2 and executors
    """

    def __init__(
        self,
        config: Optional[WorkflowConfig] = None,
        llm_provider=None
    ):
        """
        Initialize SpecFirstWorkflow.

        Args:
            config: Workflow configuration
            llm_provider: LLM provider for spec generation/validation
        """
        self.config = config or WorkflowConfig()
        self.llm_provider = llm_provider
        self.spec_writer = SpecWriterAgent(llm_provider=llm_provider)
        self.spec_validator = SpecValidator(llm_provider=llm_provider)

    async def execute(
        self,
        task_id: str,
        goal: str,
        details: str = "",
        workspace_path: Optional[Path] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Execute complete spec-first workflow for a task.

        Args:
            task_id: Task identifier
            goal: Task goal/title
            details: Additional task details
            workspace_path: Workspace directory (auto-created)
            context: Additional context for spec generation

        Returns:
            WorkflowResult with success status and artifacts
        """
        # Setup workspace
        if workspace_path is None:
            workspace_path = Path(f"workspaces/active/{task_id}")
        workspace_path = Path(workspace_path)
        workspace_path.mkdir(parents=True, exist_ok=True)

        _log(f"\n{'='*60}")
        _log(f"SPEC-FIRST WORKFLOW: {task_id}")
        _log(f"{'='*60}\n")

        result = WorkflowResult(success=False, phase="INIT")

        try:
            # Phase 1: SPEC GENERATION/VALIDATION
            _log("[Phase 1] SPEC GENERATION/VALIDATION")
            spec_path = workspace_path / "SPEC.md"

            if not spec_path.exists():
                if self.config.auto_generate_spec:
                    _log("  → SPEC.md missing, generating...")
                    spec_content, spec_path = await self.spec_writer.generate_and_save(
                        task_id=task_id,
                        goal=goal,
                        details=details,
                        workspace_path=workspace_path,
                        context=context
                    )
                    _log(f"  Generated SPEC.md ({len(spec_content.content)} chars)")

                    if spec_content.warnings:
                        result.warnings.extend(spec_content.warnings)
                elif self.config.require_spec:
                    result.error = "SPEC.md required but missing (auto-generation disabled)"
                    return result
                else:
                    result.warnings.append("SPEC.md missing, proceeding without spec validation")
                    result.spec_path = None
                    result.phase = "SPEC_SKIPPED"
                    # Continue without spec
                    return await self._execute_without_spec(task_id, goal, details, workspace_path, result)
            else:
                _log("  Found existing SPEC.md")

            result.spec_path = spec_path
            result.artifacts["spec"] = spec_path

            # Phase 2: SPEC PARSING
            _log("\n[Phase 2] SPEC PARSING")
            try:
                parsed_spec = self.spec_validator.parse_spec(spec_path)
                _log(f"  Parsed spec (type: {parsed_spec.spec_type})")
                _log(f"     - Requirements: {len(parsed_spec.requirements)}")
                _log(f"     - Success Criteria: {len(parsed_spec.success_criteria)}")
                _log(f"     - Implementation Steps: {len(parsed_spec.implementation_steps)}")
                result.phase = "SPEC_PARSED"
            except Exception as e:
                result.error = f"Failed to parse SPEC.md: {e}"
                return result

            # Phase 3: PLAN CREATION
            _log("\n[Phase 3] PLAN CREATION")
            plan_path = workspace_path / "docs" / "PLAN.md"

            if not plan_path.exists():
                _log("  → PLAN.md missing, delegating to planner...")
                # NOTE: This should be handled by external planner (SimplePlannerV2)
                # For now, we just validate if plan exists after this workflow
                result.warnings.append("PLAN.md should be created by SimplePlannerV2 before validation")
                result.phase = "PLAN_PENDING"
                # Store spec info for planner to use
                result.artifacts["parsed_spec"] = parsed_spec
                return result
            else:
                _log("  Found existing PLAN.md")

            result.plan_path = plan_path
            result.artifacts["plan"] = plan_path

            # Phase 4: PLAN VALIDATION
            if self.config.validate_plan:
                _log("\n[Phase 4] PLAN VALIDATION")
                plan_content = plan_path.read_text(encoding='utf-8')

                plan_validation = await self.spec_validator.validate_plan(
                    spec=parsed_spec,
                    plan_content=plan_content,
                    use_llm=self.config.use_llm_validation
                )

                _log(f"  → Plan Validation Score: {plan_validation.score:.2%}")
                _log(f"  → Requirements Met: {plan_validation.requirements_met}/{plan_validation.requirements_total}")
                _log(f"  → Errors: {len(plan_validation.errors)}")
                _log(f"  → Warnings: {len(plan_validation.warnings)}")

                result.plan_validation = plan_validation

                if not plan_validation.passed:
                    if plan_validation.score < self.config.min_plan_score:
                        result.error = f"Plan validation failed (score: {plan_validation.score:.2%} < {self.config.min_plan_score:.2%})"
                        _log(f"  ERROR: {result.error}")

                        # Print errors
                        for error in plan_validation.errors[:5]:
                            _log(f"     ERROR: {error.message}")

                        return result
                    else:
                        result.warnings.append(f"Plan has validation issues but score acceptable ({plan_validation.score:.2%})")

                _log("  Plan validation passed")
                result.phase = "PLAN_VALIDATED"

            # Phase 5: IMPLEMENTATION
            _log("\n[Phase 5] IMPLEMENTATION")
            _log("  → Execution delegated to AiderExecutorEnhanced")
            _log("  → (This workflow validates implementation after execution)")
            result.phase = "IMPLEMENTATION_PENDING"

            # At this point, implementation would be done by external executor
            # Workflow returns here, and implementation validation happens after execution

            result.success = True
            return result

        except Exception as e:
            result.error = f"Workflow error in phase {result.phase}: {e}"
            _log(f"  ERROR: {result.error}")
            return result

    async def validate_implementation(
        self,
        task_id: str,
        workspace_path: Path,
        changed_files: List[str],
        file_contents: Optional[Dict[str, str]] = None
    ) -> WorkflowResult:
        """
        Validate implementation against spec (called after execution).

        Args:
            task_id: Task identifier
            workspace_path: Workspace directory
            changed_files: List of modified file paths
            file_contents: Optional dict of file contents (will read if not provided)

        Returns:
            WorkflowResult with implementation validation
        """
        workspace_path = Path(workspace_path)
        result = WorkflowResult(success=False, phase="IMPL_VALIDATION")

        _log(f"\n{'='*60}")
        _log(f"IMPLEMENTATION VALIDATION: {task_id}")
        _log(f"{'='*60}\n")

        try:
            # Load spec
            spec_path = workspace_path / "SPEC.md"
            if not spec_path.exists():
                result.warnings.append("SPEC.md not found, skipping validation")
                result.success = True
                return result

            parsed_spec = self.spec_validator.parse_spec(spec_path)
            _log(f"[Spec] Loaded {parsed_spec.spec_type} spec")

            # Load file contents if not provided
            if file_contents is None:
                file_contents = {}
                for file_path in changed_files:
                    try:
                        path = Path(file_path)
                        if path.exists():
                            file_contents[file_path] = path.read_text(encoding='utf-8')
                    except Exception as e:
                        _log(f"  Warning: Could not read {file_path}: {e}")

            _log(f"[Files] Validating {len(file_contents)} changed files")

            # Validate implementation
            impl_validation = await self.spec_validator.validate_implementation(
                spec=parsed_spec,
                changed_files=changed_files,
                file_contents=file_contents,
                use_llm=self.config.use_llm_validation
            )

            _log(f"\n[Validation Results]")
            _log(f"  Score: {impl_validation.score:.2%}")
            _log(f"  Requirements Met: {impl_validation.requirements_met}/{impl_validation.requirements_total}")
            _log(f"  Criteria Met: {impl_validation.criteria_met}/{impl_validation.criteria_total}")
            _log(f"  Errors: {len(impl_validation.errors)}")
            _log(f"  Warnings: {len(impl_validation.warnings)}")

            result.impl_validation = impl_validation

            if impl_validation.score < self.config.min_impl_score:
                result.error = f"Implementation validation failed (score: {impl_validation.score:.2%})"
                _log(f"\n  ERROR: {result.error}")

                # Print errors
                for error in impl_validation.errors[:5]:
                    _log(f"     ERROR: {error.message}")

                result.success = False
            else:
                _log("\n  Implementation validation passed")
                result.success = True

            result.phase = "IMPL_VALIDATED"

            # Generate report
            await self._generate_compliance_report(
                workspace_path=workspace_path,
                parsed_spec=parsed_spec,
                impl_validation=impl_validation
            )

            return result

        except Exception as e:
            result.error = f"Implementation validation error: {e}"
            _log(f"  ERROR: {result.error}")
            return result

    async def _execute_without_spec(
        self,
        task_id: str,
        goal: str,
        details: str,
        workspace_path: Path,
        result: WorkflowResult
    ) -> WorkflowResult:
        """Execute workflow without spec (fallback mode)"""
        _log("\n[Fallback] Proceeding without SPEC.md")
        result.warnings.append("Running in spec-less mode (not recommended)")
        result.success = True
        result.phase = "NO_SPEC"
        return result

    async def _generate_compliance_report(
        self,
        workspace_path: Path,
        parsed_spec: ParsedSpec,
        impl_validation: ValidationResult
    ):
        """Generate compliance report"""
        report_path = workspace_path / "artifacts" / "COMPLIANCE_REPORT.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        report = f"""# Specification Compliance Report

**Generated:** {datetime.now().isoformat()}
**Task:** {parsed_spec.task_id}
**Spec Type:** {parsed_spec.spec_type}

## Summary

**Overall Score:** {impl_validation.score:.2%}
**Status:** {'PASSED' if impl_validation.passed else 'FAILED'}

## Requirements Compliance

**Total Requirements:** {impl_validation.requirements_total}
**Requirements Met:** {impl_validation.requirements_met}
**Coverage:** {impl_validation.requirements_met / max(impl_validation.requirements_total, 1):.2%}

## Success Criteria Compliance

**Total Criteria:** {impl_validation.criteria_total}
**Criteria Met:** {impl_validation.criteria_met}
**Coverage:** {impl_validation.criteria_met / max(impl_validation.criteria_total, 1):.2%}

## Issues

### Errors ({len(impl_validation.errors)})

"""

        for error in impl_validation.errors:
            report += f"**[{error.section}]** {error.message}\n"
            if error.suggestion:
                report += f"  → Suggestion: {error.suggestion}\n"
            report += "\n"

        report += f"\n### Warnings ({len(impl_validation.warnings)})\n\n"

        for warning in impl_validation.warnings:
            report += f"**[{warning.section}]** {warning.message}\n"
            if warning.suggestion:
                report += f"  → Suggestion: {warning.suggestion}\n"
            report += "\n"

        report += f"\n## Detailed Summary\n\n{impl_validation.summary}\n"

        report_path.write_text(report, encoding='utf-8')
        _log(f"\n[Report] Generated compliance report: {report_path}")

    def get_config(self) -> WorkflowConfig:
        """Get current workflow configuration"""
        return self.config

    def update_config(self, **kwargs):
        """Update workflow configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)


__all__ = [
    "SpecFirstWorkflow",
    "WorkflowConfig",
    "WorkflowResult"
]

