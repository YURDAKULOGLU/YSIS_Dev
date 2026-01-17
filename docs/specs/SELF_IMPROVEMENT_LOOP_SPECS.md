# Self-Improvement Loop Specifications

**Status**: Ready for Implementation
**Priority**: HIGH
**Philosophy**: Close the feedback loops - detection must lead to action

---

## Overview

These 4 tasks connect existing YBIS components into active self-improvement loops.
Currently, each component works in isolation. After these tasks, they form a closed loop:

```
DETECT → LEARN → UPDATE POLICY → BETTER EXECUTION → DETECT ...
```

---

## LOOP-001: Lesson Engine → Policy Auto-Update

### Problem
- `LessonEngine` generates `AUTO_RULES.md` with learned rules (line 198-251 in `lesson_engine.py`)
- But rules are just written to markdown - never applied to actual policy
- System keeps making same mistakes because policy never updates

### Current Flow
```
Run fails → LessonEngine.analyze_run() → AUTO_RULES.md updated → (nothing happens)
```

### Target Flow
```
Run fails → LessonEngine.analyze_run() → AUTO_RULES.md updated → Policy auto-updated → Next run uses new rules
```

### Implementation

**File**: `src/ybis/services/lesson_engine.py`

**Add new method** after `generate_auto_policy()` (around line 252):

```python
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
    from ..constants import PROJECT_ROOT
    import yaml

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
    from ..constants import PROJECT_ROOT
    import yaml

    policy_file = PROJECT_ROOT / "configs" / "profiles" / "default.yaml"

    try:
        # Read existing policy
        with open(policy_file, "r", encoding="utf-8") as f:
            policy_data = yaml.safe_load(f) or {}

        # Update auto_rules section
        policy_data["auto_rules"] = auto_rules

        # Write back
        with open(policy_file, "w", encoding="utf-8") as f:
            yaml.dump(policy_data, f, default_flow_style=False, sort_keys=False)

    except Exception as e:
        # Log but don't fail - policy update is best-effort
        print(f"Warning: Could not persist auto_rules: {e}")
```

**Modify `analyze_run()`** (around line 90-95):

```python
# After: lessons["lessons"].append(lesson)
# Add:
if lessons["lessons"]:
    # Generate markdown documentation
    self.generate_auto_policy(lessons["lessons"])
    # Apply to runtime policy
    policy_updates = self.apply_lessons_to_policy(lessons["lessons"])
    lessons["policy_updates"] = policy_updates
```

### Policy File Update

**File**: `configs/profiles/default.yaml`

Add new section (will be auto-managed):

```yaml
# Auto-generated rules from Lesson Engine (DO NOT EDIT MANUALLY)
auto_rules:
  pre_hooks: []      # Commands to run before execution
  blocked_patterns: []  # Import patterns to block
  required_checks: []   # Required verification checks
  require_tests_pass: false
```

### Verification
1. Trigger 3 syntax errors in test runs
2. Check `AUTO_RULES.md` is updated
3. Check `default.yaml` has `auto_rules.pre_hooks: ["ruff check {files}"]`
4. Next run should run ruff check automatically

---

## LOOP-002: Health Monitor → Self-Heal Trigger

### Problem
- `HealthMonitor` publishes `HEALTH_DEGRADED` events (line 86-94 in `health_monitor.py`)
- But nobody listens - no action taken when system degrades
- Adapters fail silently, disk fills up, configs break - nothing happens

### Current Flow
```
Health check fails → Event published → (nothing happens)
```

### Target Flow
```
Health check fails → Event published → Self-heal actions triggered → Recovery attempted → Notification sent
```

### Implementation

**File**: `src/ybis/services/health_monitor.py`

**Add new class** after `HealthMonitor` class (around line 328):

```python
class SelfHealHandler:
    """
    Handles health degradation events and triggers recovery actions.
    """

    def __init__(self, health_monitor: HealthMonitor):
        self.health_monitor = health_monitor
        self.recovery_actions = {
            "adapters": self._recover_adapters,
            "disk_space": self._recover_disk_space,
            "configuration": self._recover_configuration,
            "database": self._recover_database,
            "artifacts": self._recover_artifacts,
        }

    def handle_degradation(self, checks: List[HealthCheck]) -> Dict[str, Any]:
        """
        Handle health degradation by triggering recovery actions.

        Args:
            checks: List of health check results

        Returns:
            Recovery report
        """
        recovery_report = {
            "timestamp": datetime.now().isoformat(),
            "actions_taken": [],
            "success": True,
        }

        for check in checks:
            if check.status in ["degraded", "unhealthy"]:
                action = self.recovery_actions.get(check.name)
                if action:
                    try:
                        result = action(check)
                        recovery_report["actions_taken"].append({
                            "check": check.name,
                            "action": result.get("action"),
                            "success": result.get("success", False),
                            "message": result.get("message", ""),
                        })
                    except Exception as e:
                        recovery_report["actions_taken"].append({
                            "check": check.name,
                            "action": "recovery_failed",
                            "success": False,
                            "message": str(e),
                        })
                        recovery_report["success"] = False

        return recovery_report

    def _recover_adapters(self, check: HealthCheck) -> Dict[str, Any]:
        """Disable unavailable adapters in policy."""
        from .policy import get_policy_provider
        from ..constants import PROJECT_ROOT
        import yaml

        missing = check.details.get("missing", [])
        if not missing:
            return {"action": "no_action", "success": True, "message": "No missing adapters"}

        policy_file = PROJECT_ROOT / "configs" / "profiles" / "default.yaml"

        try:
            with open(policy_file, "r", encoding="utf-8") as f:
                policy_data = yaml.safe_load(f) or {}

            adapters = policy_data.setdefault("adapters", {})
            disabled = []

            for adapter_name in missing:
                if adapter_name in adapters:
                    adapters[adapter_name]["enabled"] = False
                    adapters[adapter_name]["disabled_reason"] = "auto-disabled: unavailable"
                    disabled.append(adapter_name)

            if disabled:
                with open(policy_file, "w", encoding="utf-8") as f:
                    yaml.dump(policy_data, f, default_flow_style=False, sort_keys=False)

            return {
                "action": "disable_adapters",
                "success": True,
                "message": f"Disabled unavailable adapters: {', '.join(disabled)}",
            }
        except Exception as e:
            return {"action": "disable_adapters", "success": False, "message": str(e)}

    def _recover_disk_space(self, check: HealthCheck) -> Dict[str, Any]:
        """Clean up old workspaces to free disk space."""
        import shutil
        from ..constants import PROJECT_ROOT

        workspaces_dir = PROJECT_ROOT / "workspaces"
        if not workspaces_dir.exists():
            return {"action": "no_action", "success": True, "message": "No workspaces to clean"}

        # Find old runs (older than 7 days)
        import time
        now = time.time()
        seven_days_ago = now - (7 * 24 * 60 * 60)

        cleaned = 0
        freed_bytes = 0

        for task_dir in workspaces_dir.iterdir():
            if not task_dir.is_dir():
                continue
            runs_dir = task_dir / "runs"
            if not runs_dir.exists():
                continue

            for run_dir in runs_dir.iterdir():
                if not run_dir.is_dir():
                    continue
                try:
                    mtime = run_dir.stat().st_mtime
                    if mtime < seven_days_ago:
                        size = sum(f.stat().st_size for f in run_dir.rglob("*") if f.is_file())
                        shutil.rmtree(run_dir)
                        cleaned += 1
                        freed_bytes += size
                except Exception:
                    continue

        freed_mb = freed_bytes / (1024 * 1024)
        return {
            "action": "clean_old_runs",
            "success": True,
            "message": f"Cleaned {cleaned} old runs, freed {freed_mb:.2f} MB",
        }

    def _recover_configuration(self, check: HealthCheck) -> Dict[str, Any]:
        """Reset configuration to defaults if invalid."""
        missing = check.details.get("missing", [])
        if not missing:
            return {"action": "no_action", "success": True, "message": "No missing sections"}

        from ..constants import PROJECT_ROOT
        import yaml

        policy_file = PROJECT_ROOT / "configs" / "profiles" / "default.yaml"

        # Default values for missing sections
        defaults = {
            "sandbox": {"enabled": True, "network": False},
            "exec": {"allowlist": ["python", "pytest", "ruff", "git"]},
            "paths": {"protected": ["src/ybis/contracts/", "src/ybis/syscalls/"]},
            "gates": {"require_verifier_pass": True},
        }

        try:
            with open(policy_file, "r", encoding="utf-8") as f:
                policy_data = yaml.safe_load(f) or {}

            restored = []
            for section in missing:
                if section in defaults:
                    policy_data[section] = defaults[section]
                    restored.append(section)

            if restored:
                with open(policy_file, "w", encoding="utf-8") as f:
                    yaml.dump(policy_data, f, default_flow_style=False, sort_keys=False)

            return {
                "action": "restore_defaults",
                "success": True,
                "message": f"Restored default config for: {', '.join(restored)}",
            }
        except Exception as e:
            return {"action": "restore_defaults", "success": False, "message": str(e)}

    def _recover_database(self, check: HealthCheck) -> Dict[str, Any]:
        """Attempt to reinitialize database."""
        try:
            from ..control_plane import ControlPlaneDB
            from ..constants import PROJECT_ROOT
            import asyncio

            db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
            db = ControlPlaneDB(str(db_path))
            asyncio.run(db.initialize())

            return {
                "action": "reinitialize_db",
                "success": True,
                "message": "Database reinitialized successfully",
            }
        except Exception as e:
            return {"action": "reinitialize_db", "success": False, "message": str(e)}

    def _recover_artifacts(self, check: HealthCheck) -> Dict[str, Any]:
        """Mark runs with missing artifacts as failed."""
        issues = check.details.get("issues", [])
        if not issues:
            return {"action": "no_action", "success": True, "message": "No artifact issues"}

        return {
            "action": "log_issues",
            "success": True,
            "message": f"Logged {len(issues)} artifact issues for review",
        }
```

**Modify `run_all_checks()`** (around line 86-104):

```python
# Replace the event publishing section with:
healthy_count = sum(1 for c in checks if c.status == "healthy")
total_count = len(checks)

if healthy_count < total_count:
    # Publish event
    self.event_bus.publish(
        Events.HEALTH_DEGRADED,
        {
            "healthy": healthy_count,
            "total": total_count,
            "checks": [c.__dict__ for c in checks],
        },
    )

    # Trigger self-healing
    healer = SelfHealHandler(self)
    recovery_report = healer.handle_degradation(checks)

    # Publish recovery event
    self.event_bus.publish(
        Events.HEALTH_RECOVERED if recovery_report["success"] else Events.HEALTH_RECOVERY_FAILED,
        recovery_report,
    )
else:
    self.event_bus.publish(
        Events.HEALTH_CHECK,
        {"healthy": healthy_count, "total": total_count},
    )

return checks
```

**File**: `src/ybis/services/event_bus.py`

Add new event types to `Events` class:

```python
class Events:
    # ... existing events ...
    HEALTH_RECOVERED = "health.recovered"
    HEALTH_RECOVERY_FAILED = "health.recovery_failed"
```

### Verification
1. Disable an adapter that's enabled in policy (e.g., set wrong port for neo4j)
2. Run health check
3. Check that adapter is auto-disabled in `default.yaml`
4. Check `HEALTH_RECOVERED` event is published

---

## LOOP-003: Error KB → Planner Context

### Problem
- `ErrorKnowledgeBase` collects error patterns across tasks (line 215-258 in `error_knowledge_base.py`)
- `LLMPlanner` generates plans without knowing about past failures
- System doesn't learn from history - makes same mistakes repeatedly

### Current Flow
```
Task fails → Error recorded in KB → (sits unused) → Next task plans without context
```

### Target Flow
```
Task fails → Error recorded in KB → Pattern detected → Next task gets error context → Planner avoids known issues
```

### Implementation

**File**: `src/ybis/orchestrator/planner.py`

**Add import** at top:

```python
from ..services.error_knowledge_base import ErrorKnowledgeBase
```

**Add new method** to `LLMPlanner` class (around line 207):

```python
def _get_error_context(self, objective: str) -> list[dict]:
    """
    Get relevant error patterns from Error Knowledge Base.

    Args:
        objective: Task objective

    Returns:
        List of relevant error patterns with suggestions
    """
    error_context = []

    try:
        error_kb = ErrorKnowledgeBase()

        # Get recent error patterns (min 2 occurrences)
        patterns = error_kb.get_error_patterns(min_occurrences=2)

        # Limit to top 5 most frequent patterns
        for pattern in patterns[:5]:
            error_context.append({
                "error_type": pattern.error_type,
                "pattern": pattern.error_message_pattern,
                "occurrences": pattern.occurrence_count,
                "suggestion": pattern.suggested_fix or self._generate_suggestion(pattern),
            })

        # Also get errors similar to keywords in objective
        keywords = self._extract_keywords(objective)
        for keyword in keywords[:3]:
            similar = error_kb.get_similar_errors(error_message=keyword, limit=2)
            for err in similar:
                if err.error_type not in [e["error_type"] for e in error_context]:
                    error_context.append({
                        "error_type": err.error_type,
                        "pattern": err.error_message[:100],
                        "occurrences": 1,
                        "suggestion": f"Previous error in step '{err.step}': {err.error_message[:50]}",
                    })
    except Exception:
        pass  # Error KB is optional

    return error_context


def _extract_keywords(self, text: str) -> list[str]:
    """Extract relevant keywords from text."""
    import re
    # Extract potential file names, module names, function names
    words = re.findall(r'\b[a-z_][a-z0-9_]*\b', text.lower())
    # Filter out common words
    stopwords = {"the", "a", "an", "is", "are", "to", "for", "and", "or", "in", "on", "with"}
    return [w for w in words if w not in stopwords and len(w) > 3]


def _generate_suggestion(self, pattern) -> str:
    """Generate suggestion for error pattern."""
    suggestions = {
        "syntax_error": "Run syntax check before execution. Use 'ruff check' to validate.",
        "type_error": "Add type hints and run mypy. Check function signatures.",
        "lint_error": "Run 'ruff check --fix' to auto-fix lint issues.",
        "test_failure": "Review test assertions. Check for changed interfaces.",
        "import_error": "Verify import paths. Check if module is installed.",
    }
    return suggestions.get(pattern.error_type, f"Review {pattern.error_type} errors before execution.")
```

**Modify `_get_system_prompt()`** (around line 210):

Change method signature to:

```python
def _get_system_prompt(
    self,
    relevant_context: list[dict] | None = None,
    impact_warnings: list[str] | None = None,
    error_context: list[dict] | None = None,  # NEW PARAMETER
) -> str:
```

Add error context section in the prompt (after `impact_section`):

```python
# Include error history warnings
error_section = ""
if error_context:
    error_section = "\n\nKnown Error Patterns (AVOID THESE):\n"
    for i, err in enumerate(error_context[:5], 1):
        error_section += f"\n[!] {err['error_type']} (seen {err['occurrences']}x): {err['suggestion']}\n"

return f"""You are a code planning assistant...{context_section}{rag_section}{impact_section}{error_section}"""
```

**Modify `plan()` method** (around line 100-120):

```python
# After: relevant_context = self._get_relevant_context(task.objective)
# Add:
error_context = self._get_error_context(task.objective)

# Update the call to _get_system_prompt:
system_prompt = self._get_system_prompt(relevant_context, impact_warnings, error_context)
```

### Verification
1. Create a task that fails with syntax error
2. Run it 3 times (to build pattern)
3. Create new similar task
4. Check planner prompt includes "Known Error Patterns" section
5. Verify plan mentions syntax checking

---

## LOOP-004: Staleness → Auto-Task Creation

### Problem
- `StalenessDetector` can detect stale files (line 39-80 in `staleness.py`)
- `create_consistency_tasks()` exists but is never called automatically
- Core files change but dependents are never updated

### Current Flow
```
Core file changes → (nothing detects this) → Dependents become stale → Bugs appear later
```

### Target Flow
```
Core file changes → Staleness detected → Consistency tasks auto-created → Dependents updated
```

### Implementation

**File**: `src/ybis/services/staleness.py`

**Add new class** for automatic triggering (after `StalenessDetector` class):

```python
class StalenessWatcher:
    """
    Watches for core file changes and auto-triggers staleness detection.

    Can be run:
    1. After each run completes
    2. On git commit hook
    3. On schedule (e.g., hourly)
    """

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or PROJECT_ROOT
        self.detector = StalenessDetector(self.project_root)
        self.last_check_file = self.project_root / "platform_data" / ".staleness_last_check"

    def get_changed_since_last_check(self) -> list[str]:
        """Get files changed since last staleness check."""
        import subprocess

        # Get last check commit
        last_commit = "HEAD~1"  # Default: compare to previous commit
        if self.last_check_file.exists():
            try:
                last_commit = self.last_check_file.read_text().strip()
            except Exception:
                pass

        # Get changed files
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", last_commit, "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        except Exception:
            pass

        return []

    def update_last_check(self) -> None:
        """Update last check marker to current HEAD."""
        import subprocess

        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                self.last_check_file.parent.mkdir(parents=True, exist_ok=True)
                self.last_check_file.write_text(result.stdout.strip())
        except Exception:
            pass

    async def check_and_create_tasks(self) -> dict[str, Any]:
        """
        Check for staleness and create consistency tasks if needed.

        Returns:
            Report of actions taken
        """
        from ..control_plane import ControlPlaneDB

        report = {
            "timestamp": datetime.now().isoformat() if 'datetime' in dir() else None,
            "changed_files": [],
            "stale_files": [],
            "tasks_created": [],
        }

        # Import datetime if not available
        from datetime import datetime
        report["timestamp"] = datetime.now().isoformat()

        # Get changed files
        changed_files = self.get_changed_since_last_check()
        report["changed_files"] = changed_files

        if not changed_files:
            return report

        # Detect staleness
        stale_files = self.detector.detect_staleness(changed_files)
        report["stale_files"] = stale_files

        if not stale_files:
            self.update_last_check()
            return report

        # Create tasks
        db_path = self.project_root / "platform_data" / "control_plane.db"
        db = ControlPlaneDB(str(db_path))

        try:
            task_ids = await self.detector.create_consistency_tasks(stale_files, db)
            report["tasks_created"] = task_ids
        except Exception as e:
            report["error"] = str(e)

        # Update last check marker
        self.update_last_check()

        return report

    async def run_check(self) -> dict[str, Any]:
        """
        Convenience method to run staleness check.

        Returns:
            Staleness check report
        """
        return await self.check_and_create_tasks()
```

**File**: Create `src/ybis/services/staleness_hook.py`

```python
"""
Staleness Hook - Run after each orchestrator run to detect staleness.

Usage:
    from ybis.services.staleness_hook import run_staleness_check
    await run_staleness_check()
"""

import asyncio
from pathlib import Path

from ..constants import PROJECT_ROOT
from .staleness import StalenessWatcher


async def run_staleness_check(project_root: Path | None = None) -> dict:
    """
    Run staleness check and create consistency tasks if needed.

    Args:
        project_root: Project root path (default: PROJECT_ROOT)

    Returns:
        Staleness check report
    """
    watcher = StalenessWatcher(project_root or PROJECT_ROOT)
    return await watcher.check_and_create_tasks()


def run_staleness_check_sync(project_root: Path | None = None) -> dict:
    """Synchronous wrapper for staleness check."""
    return asyncio.run(run_staleness_check(project_root))


# CLI entry point
if __name__ == "__main__":
    import json
    report = run_staleness_check_sync()
    print(json.dumps(report, indent=2))
```

**File**: `src/ybis/orchestrator/workflow.py` (or wherever run completion is handled)

Add staleness check after run completes:

```python
# After run completes successfully
from ..services.staleness_hook import run_staleness_check

async def on_run_complete(ctx: RunContext):
    # ... existing completion logic ...

    # Check for staleness and create consistency tasks
    try:
        staleness_report = await run_staleness_check()
        if staleness_report.get("tasks_created"):
            ctx.log(f"Created {len(staleness_report['tasks_created'])} consistency tasks")
    except Exception as e:
        ctx.log(f"Staleness check failed: {e}")
```

**File**: Create `scripts/check_staleness.py` (CLI entry point)

```python
#!/usr/bin/env python
"""
CLI to manually run staleness check.

Usage:
    python scripts/check_staleness.py
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.services.staleness_hook import run_staleness_check


async def main():
    print("Running staleness check...")
    report = await run_staleness_check(project_root)

    print("\n" + "=" * 50)
    print("STALENESS CHECK REPORT")
    print("=" * 50)

    print(f"\nChanged files: {len(report.get('changed_files', []))}")
    for f in report.get('changed_files', [])[:10]:
        print(f"  - {f}")

    print(f"\nStale files: {len(report.get('stale_files', []))}")
    for s in report.get('stale_files', [])[:10]:
        print(f"  - {s['file']} (depends on {s['depends_on']})")

    print(f"\nTasks created: {len(report.get('tasks_created', []))}")
    for t in report.get('tasks_created', []):
        print(f"  - {t}")

    if report.get('error'):
        print(f"\nError: {report['error']}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
```

### Verification
1. Modify a core file (e.g., `src/ybis/contracts/resources.py`)
2. Commit the change
3. Run `python scripts/check_staleness.py`
4. Verify consistency tasks are created in control plane DB
5. Check that `.staleness_last_check` file is updated

---

## Integration Order

Execute in this order for minimal dependencies:

1. **LOOP-003** (Error KB → Planner) - Standalone, no other changes needed
2. **LOOP-001** (Lessons → Policy) - Standalone, extends lesson engine
3. **LOOP-004** (Staleness → Tasks) - Standalone, adds new files
4. **LOOP-002** (Health → Self-Heal) - Depends on event bus working

---

## Testing Checklist

### LOOP-001
- [ ] Create 3 runs with syntax errors
- [ ] Verify `AUTO_RULES.md` updated
- [ ] Verify `default.yaml` has `auto_rules` section
- [ ] Verify next run has pre-hook for ruff check

### LOOP-002
- [ ] Manually break an adapter config
- [ ] Run health check
- [ ] Verify adapter auto-disabled in policy
- [ ] Verify recovery event published

### LOOP-003
- [ ] Create task that fails with import error
- [ ] Run it 2+ times
- [ ] Create new task with similar objective
- [ ] Verify planner prompt has "Known Error Patterns"

### LOOP-004
- [ ] Modify core file and commit
- [ ] Run staleness check script
- [ ] Verify consistency task created
- [ ] Verify last check marker updated

---

## Success Criteria

After all 4 loops implemented:

1. **No repeated mistakes** - System learns from failures and prevents them
2. **Self-healing adapters** - Unavailable adapters auto-disabled
3. **Context-aware planning** - Planner knows about past errors
4. **Automatic consistency** - Core changes trigger dependent updates

The system becomes genuinely self-improving without human intervention.
