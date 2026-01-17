"""
Lesson Engine - Self-supervised governance.

Automatically updates policies based on past failures to prevent recurring errors.
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT
from ..contracts import RunContext
from ..syscalls.journal import append_event


class LessonEngine:
    """
    Lesson Engine - Learns from failures and generates auto-policies.

    Tracks recurring errors and generates rules to prevent them.
    """

    def __init__(self, auto_rules_path: Path | None = None, run_path: Path | None = None, trace_id: str | None = None):
        """
        Initialize lesson engine.

        Args:
            auto_rules_path: Path to AUTO_RULES.md (defaults to docs/governance/AUTO_RULES.md)
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        self.auto_rules_path = auto_rules_path or PROJECT_ROOT / "docs" / "governance" / "AUTO_RULES.md"
        self.error_history: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.run_path = run_path
        self.trace_id = trace_id

    def analyze_run(self, ctx: RunContext) -> dict[str, Any]:
        """
        Analyze a run and extract lessons.

        Args:
            ctx: Run context

        Returns:
            Analysis result with lessons learned
        """
        lessons = {
            "run_id": ctx.run_id,
            "task_id": ctx.task_id,
            "status": "unknown",
            "errors": [],
            "warnings": [],
            "lessons": [],
        }

        # Load verifier report
        verifier_path = ctx.verifier_report_path
        if verifier_path.exists():
            try:
                verifier_data = json.loads(verifier_path.read_text())
                lessons["errors"] = verifier_data.get("errors", [])
                lessons["warnings"] = verifier_data.get("warnings", [])
            except Exception:
                pass

        # Load gate report
        gate_path = ctx.gate_report_path
        if gate_path.exists():
            try:
                gate_data = json.loads(gate_path.read_text())
                decision = gate_data.get("decision", {})
                if isinstance(decision, dict):
                    decision = decision.get("value", "")
                lessons["status"] = decision
            except Exception:
                pass

        # Extract error patterns
        for error in lessons["errors"]:
            error_pattern = self._extract_error_pattern(error)
            if error_pattern:
                self.error_history[error_pattern].append(
                    {
                        "run_id": ctx.run_id,
                        "task_id": ctx.task_id,
                        "error": error,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        # Check if any error pattern has occurred 3+ times
        for pattern, occurrences in self.error_history.items():
            if len(occurrences) >= 3:
                lesson = self._generate_lesson(pattern, occurrences)
                if lesson:
                    lessons["lessons"].append(lesson)

        # Apply lessons to policy if any were learned
        if lessons["lessons"]:
            # Journal: Lesson recorded
            if self.run_path:
                for lesson in lessons["lessons"]:
                    append_event(
                        self.run_path,
                        "LESSON_RECORD",
                        {
                            "lesson_type": lesson.get("pattern", "unknown"),
                            "source": ctx.task_id,
                        },
                        trace_id=self.trace_id,
                    )
            
            # Generate markdown documentation
            self.generate_auto_policy(lessons["lessons"])
            # Apply to runtime policy
            policy_updates = self.apply_lessons_to_policy(lessons["lessons"])
            lessons["policy_updates"] = policy_updates
            
            # Journal: Lesson applied
            if self.run_path:
                for update in policy_updates.get("updates", []):
                    append_event(
                        self.run_path,
                        "LESSON_APPLY",
                        {
                            "lesson_id": update.get("type", "unknown"),
                            "target": "policy",
                        },
                        trace_id=self.trace_id,
                    )

        return lessons

    def _extract_error_pattern(self, error: str) -> str | None:
        """
        Extract error pattern from error message.

        Args:
            error: Error message

        Returns:
            Error pattern (normalized) or None
        """
        # Normalize common error patterns
        error_lower = error.lower()

        # Import errors
        if "import" in error_lower and ("cannot" in error_lower or "no module" in error_lower):
            # Extract module name if possible
            if "no module named" in error_lower:
                parts = error_lower.split("no module named")
                if len(parts) > 1:
                    module = parts[1].strip().split()[0]
                    return f"missing_import:{module}"
            return "missing_import:unknown"

        # Syntax errors
        if "syntax error" in error_lower:
            return "syntax_error"

        # Type errors
        if "type error" in error_lower or "typeerror" in error_lower:
            return "type_error"

        # Attribute errors
        if "attribute error" in error_lower or "attributeerror" in error_lower:
            return "attribute_error"

        # Lint errors
        if "ruff" in error_lower or "lint" in error_lower:
            return "lint_error"

        # Test failures
        if "test" in error_lower and ("fail" in error_lower or "error" in error_lower):
            return "test_failure"

        return None

    def _generate_lesson(self, pattern: str, occurrences: list[dict[str, Any]]) -> dict[str, Any] | None:
        """
        Generate a lesson (auto-rule) from recurring error pattern.

        Args:
            pattern: Error pattern
            occurrences: List of occurrences

        Returns:
            Lesson dict or None
        """
        if len(occurrences) < 3:
            return None

        # Generate rule based on pattern
        rule = {
            "pattern": pattern,
            "count": len(occurrences),
            "first_seen": occurrences[0]["timestamp"],
            "last_seen": occurrences[-1]["timestamp"],
            "rule": self._create_rule(pattern),
        }

        return rule

    def _create_rule(self, pattern: str) -> str:
        """
        Create a rule text for a given error pattern.

        Args:
            pattern: Error pattern

        Returns:
            Rule text
        """
        if pattern.startswith("missing_import:"):
            module = pattern.split(":")[1]
            return f"Always check for '{module}' import before using it. Add import validation in pre-commit or gate checks."

        if pattern == "syntax_error":
            return "Run syntax check (ruff check) before executing code. Block runs with syntax errors immediately."

        if pattern == "type_error":
            return "Enable strict type checking (mypy) in verification phase. Type errors should block runs."

        if pattern == "attribute_error":
            return "Add attribute existence checks before accessing object attributes. Use hasattr() or try/except."

        if pattern == "lint_error":
            return "Lint errors must be fixed before proceeding. Auto-fix with 'ruff check --fix' if possible."

        if pattern == "test_failure":
            return "All tests must pass before completion. Review test failures and fix root cause."

        return f"Recurring error pattern detected: {pattern}. Review and add preventive measures."

    def generate_auto_policy(self, lessons: list[dict[str, Any]]) -> None:
        """
        Generate AUTO_RULES.md from lessons.

        Args:
            lessons: List of lessons learned
        """
        if not lessons:
            return

        # Ensure directory exists
        self.auto_rules_path.parent.mkdir(parents=True, exist_ok=True)

        # Read existing rules if any
        existing_rules = []
        if self.auto_rules_path.exists():
            try:
                content = self.auto_rules_path.read_text(encoding="utf-8")
                # Parse existing rules (simple markdown parsing)
                # In production, use proper markdown parser
                existing_rules = [line.strip() for line in content.split("\n") if line.strip() and not line.startswith("#")]
            except Exception:
                pass

        # Generate new rules section
        new_rules = []
        new_rules.append("# AUTO_RULES.md - Auto-Generated Governance Rules")
        new_rules.append("")
        new_rules.append("**Generated:** " + datetime.now().isoformat())
        new_rules.append("")
        new_rules.append("These rules are automatically generated by the Lesson Engine based on recurring errors.")
        new_rules.append("")
        new_rules.append("## Rules")
        new_rules.append("")

        # Add existing rules
        if existing_rules:
            new_rules.extend(existing_rules)
            new_rules.append("")

        # Add new lessons
        for lesson in lessons:
            new_rules.append(f"### {lesson['pattern']} (Seen {lesson['count']} times)")
            new_rules.append("")
            new_rules.append(f"**First Seen:** {lesson['first_seen']}")
            new_rules.append(f"**Last Seen:** {lesson['last_seen']}")
            new_rules.append("")
            new_rules.append(f"**Rule:** {lesson['rule']}")
            new_rules.append("")
            new_rules.append("---")
            new_rules.append("")

        # Write to file
        self.auto_rules_path.write_text("\n".join(new_rules), encoding="utf-8")

    def apply_lessons_to_policy(self, lessons: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Apply lessons to runtime policy configuration.

        Args:
            lessons: List of lessons learned

        Returns:
            Dictionary of policy updates applied
        """
        if not lessons:
            return {"updates": []}


        from .policy import get_policy_provider

        policy_provider = get_policy_provider()
        policy = policy_provider.get_policy()
        updates = []

        # Get or create auto_rules section in policy
        auto_rules = policy.get("auto_rules", {
            "pre_hooks": [],
            "blocked_patterns": [],
            "required_checks": []
        })

        for lesson in lessons:
            pattern = lesson.get("pattern", "")
            rule = lesson.get("rule", "")

            # Map patterns to policy updates
            if pattern == "syntax_error":
                if "ruff check" not in auto_rules.get("pre_hooks", []):
                    auto_rules.setdefault("pre_hooks", []).append("ruff check {files}")
                    updates.append({"type": "pre_hook", "value": "ruff check"})

            elif pattern == "type_error":
                if "mypy" not in auto_rules.get("pre_hooks", []):
                    auto_rules.setdefault("pre_hooks", []).append("mypy {files}")
                    updates.append({"type": "pre_hook", "value": "mypy"})

            elif pattern == "lint_error":
                if "ruff" not in str(auto_rules.get("pre_hooks", [])):
                    auto_rules.setdefault("pre_hooks", []).append("ruff check --fix {files}")
                    updates.append({"type": "pre_hook", "value": "ruff --fix"})

            elif pattern == "test_failure":
                auto_rules["require_tests_pass"] = True
                updates.append({"type": "gate_rule", "value": "require_tests_pass"})

            elif pattern.startswith("missing_import:"):
                module = pattern.split(":")[1]
                blocked = auto_rules.setdefault("blocked_patterns", [])
                if module not in blocked:
                    blocked.append(f"import {module}")
                    updates.append({"type": "blocked_pattern", "value": f"import {module}"})

        # Update policy in memory
        policy["auto_rules"] = auto_rules

        # Persist to default.yaml (append auto_rules section)
        if updates:
            self._persist_auto_rules(auto_rules)

        return {"updates": updates, "auto_rules": auto_rules}

    def _persist_auto_rules(self, auto_rules: dict[str, Any]) -> None:
        """Persist auto_rules to policy file."""
        import yaml

        from ..constants import PROJECT_ROOT

        policy_file = PROJECT_ROOT / "configs" / "profiles" / "default.yaml"

        try:
            # Read existing policy
            with open(policy_file, encoding="utf-8") as f:
                policy_data = yaml.safe_load(f) or {}

            # Update auto_rules section
            policy_data["auto_rules"] = auto_rules

            # Write back
            with open(policy_file, "w", encoding="utf-8") as f:
                yaml.dump(policy_data, f, default_flow_style=False, sort_keys=False)

        except Exception as e:
            # Log but don't fail - policy update is best-effort
            print(f"Warning: Could not persist auto_rules: {e}")

