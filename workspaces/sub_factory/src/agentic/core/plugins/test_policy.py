"""
Test Policy Enforcement Gate.

Defines required tests by task type and enforces quality gates before merge.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from src.agentic.core.config import REQUIRE_TESTS
from src.agentic.core.protocols import MIN_TEST_COVERAGE


class TaskType(Enum):
    """Task classification for test requirements."""
    FEATURE = "feature"          # New functionality
    BUGFIX = "bugfix"            # Bug fixes
    REFACTOR = "refactor"        # Code restructuring
    DOCS = "docs"                # Documentation only
    CONFIG = "config"            # Configuration changes
    TEST = "test"                # Test-only changes
    CHORE = "chore"              # Maintenance tasks


@dataclass
class TestPolicy:
    """Test requirements for a task type."""
    unit_tests_required: bool = True
    integration_tests_required: bool = False
    lint_required: bool = True
    min_coverage: float = MIN_TEST_COVERAGE
    allow_skip: bool = False  # If True, tests can be skipped with explicit flag


# Test policies by task type
TASK_POLICIES: dict[TaskType, TestPolicy] = {
    TaskType.FEATURE: TestPolicy(
        unit_tests_required=True,
        integration_tests_required=True,
        lint_required=True,
        min_coverage=0.8,
        allow_skip=False
    ),
    TaskType.BUGFIX: TestPolicy(
        unit_tests_required=True,
        integration_tests_required=False,
        lint_required=True,
        min_coverage=0.7,
        allow_skip=False
    ),
    TaskType.REFACTOR: TestPolicy(
        unit_tests_required=True,
        integration_tests_required=False,
        lint_required=True,
        min_coverage=0.7,
        allow_skip=False
    ),
    TaskType.DOCS: TestPolicy(
        unit_tests_required=False,
        integration_tests_required=False,
        lint_required=False,
        min_coverage=0.0,
        allow_skip=True
    ),
    TaskType.CONFIG: TestPolicy(
        unit_tests_required=False,
        integration_tests_required=False,
        lint_required=True,
        min_coverage=0.0,
        allow_skip=True
    ),
    TaskType.TEST: TestPolicy(
        unit_tests_required=False,  # Tests for tests not required
        integration_tests_required=False,
        lint_required=True,
        min_coverage=0.0,
        allow_skip=True
    ),
    TaskType.CHORE: TestPolicy(
        unit_tests_required=False,
        integration_tests_required=False,
        lint_required=True,
        min_coverage=0.0,
        allow_skip=True
    ),
}


def classify_task(task_id: str, goal: str) -> TaskType:
    """
    Classify task type based on ID prefix and goal keywords.
    
    Convention:
    - FEATURE-*, feat:, add: -> FEATURE
    - FIX-*, fix:, bugfix: -> BUGFIX
    - REFACTOR-*, refactor: -> REFACTOR
    - DOCS-*, docs:, doc: -> DOCS
    - CONFIG-*, config: -> CONFIG
    - TEST-*, test: -> TEST
    - CHORE-*, chore:, maintenance: -> CHORE
    """
    id_lower = task_id.lower()
    goal_lower = goal.lower()
    
    # Check ID prefix first
    if id_lower.startswith("feature-") or id_lower.startswith("feat-"):
        return TaskType.FEATURE
    if id_lower.startswith("fix-") or id_lower.startswith("bugfix-"):
        return TaskType.BUGFIX
    if id_lower.startswith("refactor-"):
        return TaskType.REFACTOR
    if id_lower.startswith("docs-") or id_lower.startswith("doc-"):
        return TaskType.DOCS
    if id_lower.startswith("config-"):
        return TaskType.CONFIG
    if id_lower.startswith("test-"):
        return TaskType.TEST
    if id_lower.startswith("chore-") or id_lower.startswith("maint-"):
        return TaskType.CHORE
    
    # Check goal keywords
    if any(kw in goal_lower for kw in ["add ", "implement ", "create ", "new "]):
        return TaskType.FEATURE
    if any(kw in goal_lower for kw in ["fix ", "bug ", "error ", "issue "]):
        return TaskType.BUGFIX
    if any(kw in goal_lower for kw in ["refactor", "restructure", "reorganize"]):
        return TaskType.REFACTOR
    if any(kw in goal_lower for kw in ["document", "readme", "docs"]):
        return TaskType.DOCS
    if any(kw in goal_lower for kw in ["config", "setting", "environment"]):
        return TaskType.CONFIG
    if any(kw in goal_lower for kw in ["test", "spec", "coverage"]):
        return TaskType.TEST
    
    # Default to FEATURE (strictest policy)
    return TaskType.FEATURE


def get_policy(task_type: TaskType) -> TestPolicy:
    """Get test policy for a task type."""
    return TASK_POLICIES.get(task_type, TASK_POLICIES[TaskType.FEATURE])


@dataclass
class GateResult:
    """Result of test policy enforcement gate."""
    passed: bool
    task_type: TaskType
    policy: TestPolicy
    violations: list[str]
    warnings: list[str]


def enforce_gate(
    task_id: str,
    goal: str,
    lint_passed: bool,
    tests_passed: bool,
    coverage: float,
    skip_tests: bool = False
) -> GateResult:
    """
    Enforce test policy gate for a task.
    
    Args:
        task_id: Task identifier
        goal: Task goal/description
        lint_passed: Whether lint checks passed
        tests_passed: Whether tests passed
        coverage: Test coverage (0.0-1.0)
        skip_tests: If True and policy allows, skip test requirements
        
    Returns:
        GateResult with pass/fail status and details
    """
    if not REQUIRE_TESTS:
        return GateResult(
            passed=True,
            task_type=TaskType.CHORE,
            policy=TestPolicy(allow_skip=True),
            violations=[],
            warnings=["Test enforcement disabled via REQUIRE_TESTS=false"]
        )
    
    task_type = classify_task(task_id, goal)
    policy = get_policy(task_type)
    
    violations = []
    warnings = []
    
    # Check if skip is requested and allowed
    if skip_tests:
        if policy.allow_skip:
            warnings.append(f"Tests skipped for {task_type.value} task (allowed by policy)")
            return GateResult(
                passed=True,
                task_type=task_type,
                policy=policy,
                violations=[],
                warnings=warnings
            )
        else:
            violations.append(f"Cannot skip tests for {task_type.value} task (policy prohibits)")
    
    # Check lint
    if policy.lint_required and not lint_passed:
        violations.append("Lint check failed (required by policy)")
    
    # Check tests
    if policy.unit_tests_required and not tests_passed:
        violations.append("Unit tests failed or not run (required by policy)")
    
    # Check coverage
    if policy.min_coverage > 0 and coverage < policy.min_coverage:
        violations.append(
            f"Coverage {coverage:.1%} below minimum {policy.min_coverage:.1%}"
        )
    
    return GateResult(
        passed=len(violations) == 0,
        task_type=task_type,
        policy=policy,
        violations=violations,
        warnings=warnings
    )
