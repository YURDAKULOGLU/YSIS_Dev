"""
Error Knowledge Base - Centralized task error collection and analysis.

Collects errors from all tasks, analyzes patterns, and provides insights
for future task execution.
"""

import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT
from ..contracts import RunContext, VerifierReport
from ..syscalls.journal import append_event


@dataclass
class TaskError:
    """Single error from a task execution."""
    
    task_id: str
    run_id: str
    error_type: str  # "syntax", "test_failure", "lint_error", "gate_block", etc.
    error_message: str
    error_location: str | None = None  # File path, line number, etc.
    step: str | None = None  # "spec", "plan", "execute", "verify", "gate"
    timestamp: str = ""
    context: dict[str, Any] | None = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


@dataclass
class ErrorPattern:
    """Pattern extracted from multiple errors."""
    
    pattern_id: str
    error_type: str
    error_message_pattern: str
    occurrence_count: int
    first_seen: str
    last_seen: str
    affected_tasks: list[str]
    affected_runs: list[str]
    common_context: dict[str, Any]
    suggested_fix: str | None = None


class ErrorKnowledgeBase:
    """
    Centralized error knowledge base for cross-task learning.
    
    Collects errors from all tasks, analyzes patterns, and provides
    insights for future task execution.
    """
    
    def __init__(self, storage_path: Path | None = None, run_path: Path | None = None, trace_id: str | None = None):
        """
        Initialize error knowledge base.
        
        Args:
            storage_path: Path to store error database (default: platform_data/error_kb/)
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        if storage_path is None:
            storage_path = PROJECT_ROOT / "platform_data" / "error_kb"
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.run_path = run_path
        self.trace_id = trace_id
        
        # Error storage files
        self.errors_file = self.storage_path / "errors.jsonl"  # One error per line
        self.patterns_file = self.storage_path / "patterns.json"
        self.stats_file = self.storage_path / "stats.json"
        
        # In-memory cache
        self._errors: list[TaskError] = []
        self._patterns: dict[str, ErrorPattern] = {}
        self._load_cache()
    
    def _load_cache(self):
        """Load errors and patterns from disk."""
        # Load errors
        if self.errors_file.exists():
            self._errors = []
            with open(self.errors_file, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            data = json.loads(line)
                            self._errors.append(TaskError(**data))
                        except Exception:
                            pass
        
        # Load patterns
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, encoding="utf-8") as f:
                    patterns_data = json.load(f)
                    self._patterns = {
                        pid: ErrorPattern(**pdata)
                        for pid, pdata in patterns_data.items()
                    }
            except Exception:
                self._patterns = {}
    
    def _save_error(self, error: TaskError):
        """Save error to JSONL file."""
        with open(self.errors_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(error), ensure_ascii=False) + "\n")
        self._errors.append(error)
    
    def _save_patterns(self):
        """Save patterns to JSON file."""
        patterns_data = {
            pid: asdict(pattern)
            for pid, pattern in self._patterns.items()
        }
        with open(self.patterns_file, "w", encoding="utf-8") as f:
            json.dump(patterns_data, f, indent=2, ensure_ascii=False)
    
    def record_error(
        self,
        task_id: str,
        run_id: str,
        error_type: str,
        error_message: str,
        error_location: str | None = None,
        step: str | None = None,
        context: dict[str, Any] | None = None,
    ):
        """
        Record an error from a task execution.
        
        Args:
            task_id: Task identifier
            run_id: Run identifier
            error_type: Type of error (e.g., "syntax", "test_failure")
            error_message: Error message
            error_location: File path, line number, etc.
            step: Workflow step where error occurred
            context: Additional context (files modified, etc.)
        """
        error = TaskError(
            task_id=task_id,
            run_id=run_id,
            error_type=error_type,
            error_message=error_message,
            error_location=error_location,
            step=step,
            context=context or {},
        )
        self._save_error(error)
        
        # Journal: Error recorded
        if self.run_path:
            append_event(
                self.run_path,
                "ERROR_KB_RECORD",
                {
                    "error_type": error_type,
                    "task_id": task_id,
                    "step": step or "unknown",
                },
                trace_id=self.trace_id,
            )
        
        # Trigger pattern analysis
        self._analyze_patterns()
    
    def record_from_verifier_report(self, ctx: RunContext, verifier_report: VerifierReport):
        """
        Record errors from a verifier report.
        
        Args:
            ctx: Run context
            verifier_report: Verifier report with errors
        """
        # Record lint errors
        if hasattr(verifier_report, 'lint_errors') and verifier_report.lint_errors:
            for lint_error in verifier_report.lint_errors:
                self.record_error(
                    task_id=ctx.task_id,
                    run_id=ctx.run_id,
                    error_type="lint_error",
                    error_message=str(lint_error),
                    step="verify",
                    context={"lint_passed": verifier_report.lint_passed},
                )
        
        # Record test failures
        if hasattr(verifier_report, 'test_failures') and verifier_report.test_failures:
            for test_failure in verifier_report.test_failures:
                self.record_error(
                    task_id=ctx.task_id,
                    run_id=ctx.run_id,
                    error_type="test_failure",
                    error_message=str(test_failure),
                    step="verify",
                    context={"tests_passed": verifier_report.tests_passed},
                )
        
        # Record general errors
        if verifier_report.errors:
            for error in verifier_report.errors:
                self.record_error(
                    task_id=ctx.task_id,
                    run_id=ctx.run_id,
                    error_type="verifier_error",
                    error_message=str(error),
                    step="verify",
                )
        
        # Record warnings as errors too (for pattern detection)
        if verifier_report.warnings:
            for warning in verifier_report.warnings:
                self.record_error(
                    task_id=ctx.task_id,
                    run_id=ctx.run_id,
                    error_type="verifier_warning",
                    error_message=str(warning),
                    step="verify",
                    context={"lint_passed": verifier_report.lint_passed, "tests_passed": verifier_report.tests_passed},
                )
    
    def _analyze_patterns(self):
        """Analyze errors to extract patterns."""
        # Group errors by type and message pattern
        error_groups: dict[str, list[TaskError]] = defaultdict(list)
        
        for error in self._errors:
            # Create pattern key from error type and message
            pattern_key = f"{error.error_type}:{self._normalize_message(error.error_message)}"
            error_groups[pattern_key].append(error)
        
        # Create patterns for groups with 2+ occurrences
        for pattern_key, errors in error_groups.items():
            if len(errors) >= 2:
                pattern_id = f"pattern_{hash(pattern_key) % 1000000}"
                
                # Extract common context
                common_context = {}
                if errors[0].context:
                    common_context = errors[0].context.copy()
                
                # Find common elements in context
                for error in errors[1:]:
                    if error.context:
                        common_context = {
                            k: v
                            for k, v in common_context.items()
                            if k in error.context and error.context[k] == v
                        }
                
                pattern = ErrorPattern(
                    pattern_id=pattern_id,
                    error_type=errors[0].error_type,
                    error_message_pattern=self._normalize_message(errors[0].error_message),
                    occurrence_count=len(errors),
                    first_seen=min(e.timestamp for e in errors),
                    last_seen=max(e.timestamp for e in errors),
                    affected_tasks=list(set(e.task_id for e in errors)),
                    affected_runs=list(set(e.run_id for e in errors)),
                    common_context=common_context,
                )
                
                self._patterns[pattern_id] = pattern
                
                # Journal: Pattern detected
                if self.run_path:
                    append_event(
                        self.run_path,
                        "ERROR_KB_PATTERN_DETECTED",
                        {
                            "error_type": pattern.error_type,
                            "occurrences": pattern.occurrence_count,
                        },
                        trace_id=self.trace_id,
                    )
        
        self._save_patterns()
    
    def _normalize_message(self, message: str) -> str:
        """Normalize error message for pattern matching."""
        # Remove file paths, line numbers, etc.
        import re
        # Remove absolute paths
        message = re.sub(r'[A-Z]:\\[^\s]+', '<path>', message)
        message = re.sub(r'/[^\s]+', '<path>', message)
        # Remove line numbers
        message = re.sub(r':\d+', ':N', message)
        # Remove timestamps
        message = re.sub(r'\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}', '<timestamp>', message)
        return message.strip()
    
    def get_similar_errors(
        self,
        error_type: str | None = None,
        error_message: str | None = None,
        step: str | None = None,
        limit: int = 10,
    ) -> list[TaskError]:
        """
        Get similar errors from history.
        
        Args:
            error_type: Filter by error type
            error_message: Filter by error message (partial match)
            step: Filter by workflow step
            limit: Maximum number of results
            
        Returns:
            List of similar errors
        """
        results = []
        
        for error in self._errors:
            if error_type and error.error_type != error_type:
                continue
            if step and error.step != step:
                continue
            if error_message and error_message.lower() not in error.error_message.lower():
                continue
            
            results.append(error)
            if len(results) >= limit:
                break
        
        return results
    
    def get_error_patterns(
        self,
        error_type: str | None = None,
        min_occurrences: int = 2,
    ) -> list[ErrorPattern]:
        """
        Get error patterns.
        
        Args:
            error_type: Filter by error type
            min_occurrences: Minimum number of occurrences
            
        Returns:
            List of error patterns
        """
        patterns = list(self._patterns.values())
        
        if error_type:
            patterns = [p for p in patterns if p.error_type == error_type]
        
        patterns = [p for p in patterns if p.occurrence_count >= min_occurrences]
        
        # Sort by occurrence count (descending)
        patterns.sort(key=lambda p: p.occurrence_count, reverse=True)
        
        # Journal: Query executed
        if self.run_path:
            append_event(
                self.run_path,
                "ERROR_KB_QUERY",
                {
                    "query_type": "get_error_patterns",
                    "results_count": len(patterns),
                },
                trace_id=self.trace_id,
            )
        
        return patterns
    
    def get_insights_for_task(self, task_id: str) -> dict[str, Any]:
        """
        Get error insights for a specific task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Dictionary with insights
        """
        task_errors = [e for e in self._errors if e.task_id == task_id]
        
        if not task_errors:
            return {
                "task_id": task_id,
                "error_count": 0,
                "patterns": [],
                "suggestions": [],
            }
        
        # Find patterns that affected this task
        relevant_patterns = []
        for pattern in self._patterns.values():
            if task_id in pattern.affected_tasks:
                relevant_patterns.append(pattern)
        
        # Generate suggestions
        suggestions = []
        for pattern in relevant_patterns:
            if pattern.suggested_fix:
                suggestions.append({
                    "pattern": pattern.pattern_id,
                    "error_type": pattern.error_type,
                    "suggestion": pattern.suggested_fix,
                })
        
        return {
            "task_id": task_id,
            "error_count": len(task_errors),
            "error_types": list(set(e.error_type for e in task_errors)),
            "patterns": [asdict(p) for p in relevant_patterns],
            "suggestions": suggestions,
        }
    
    def get_statistics(self) -> dict[str, Any]:
        """Get error statistics."""
        if not self._errors:
            return {
                "total_errors": 0,
                "error_types": {},
                "steps": {},
                "patterns": 0,
            }
        
        error_types = defaultdict(int)
        steps = defaultdict(int)
        
        for error in self._errors:
            error_types[error.error_type] += 1
            if error.step:
                steps[error.step] += 1
        
        return {
            "total_errors": len(self._errors),
            "error_types": dict(error_types),
            "steps": dict(steps),
            "patterns": len(self._patterns),
            "unique_tasks": len(set(e.task_id for e in self._errors)),
            "unique_runs": len(set(e.run_id for e in self._errors)),
        }

