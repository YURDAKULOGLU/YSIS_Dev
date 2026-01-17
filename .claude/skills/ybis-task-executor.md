---
# YBIS Task Executor Skill - Limit Test
# Bu skill, Claude Code skill sisteminin TÜM özelliklerini kullanır

# Skill metadata
name: "ybis-task-executor"
version: "1.0.0"
description: "YBIS task execution skill - otomatik task detection ve execution"

# Trigger conditions - bu koşullardan biri sağlandığında skill aktive olur
triggers:
  # Pattern-based triggers (regex)
  patterns:
    - "(?i)ybis\\s+task"
    - "(?i)run\\s+task\\s+[A-Z]+-\\d+"
    - "(?i)execute\\s+[A-Z]+-[a-f0-9]+"
    - "(?i)claim\\s+(next\\s+)?task"
    - "(?i)complete\\s+task"

  # File-based triggers - bu dosyalar context'te olduğunda
  files:
    - "platform_data/control_plane.db"
    - "workspaces/active/**/PLAN.md"
    - "workspaces/active/**/RESULT.md"

  # Keyword triggers - bu kelimeler geçtiğinde
  keywords:
    - "YBIS"
    - "task execution"
    - "workflow run"
    - "claim task"

  # Context triggers - belirli context durumlarında
  context:
    - type: "mcp_available"
      server: "ybis"
    - type: "file_exists"
      path: "src/ybis/orchestrator/graph.py"

# Priority - aynı anda birden fazla skill match ederse
priority: 100

# Auto-invoke - trigger olunca otomatik çalış (false ise öneri göster)
auto_invoke: false

# Confirmation required - çalışmadan önce onay iste
requires_confirmation: true
confirmation_message: "YBIS task executor'ı çalıştırmak istiyor musunuz?"

# Tool restrictions
allowed_tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - TodoWrite
  - mcp__ybis__*

# Model preference
preferred_model: "sonnet"

# Timeout (ms)
timeout: 300000

# Max turns
max_turns: 30

# Tags for categorization
tags:
  - "automation"
  - "task-management"
  - "ybis"
  - "workflow"
---

# YBIS Task Executor Skill

## Overview

Bu skill, YBIS platformundaki task'ları otomatik olarak algılar ve execute eder.
User YBIS task'larından bahsettiğinde bu skill aktive olur.

## Capabilities

### 1. Task Detection
- Conversation'da task ID pattern'ları algıla
- YBIS database'inden task bilgilerini çek
- Task durumunu ve gereksinimlerini analiz et

### 2. Task Claiming
- Pending task'ları listele
- Uygun task'ı otomatik claim et
- Lease management (timeout handling)

### 3. Execution Orchestration
- Task objective'e göre execution plan oluştur
- LangGraph workflow'unu tetikle
- Progress tracking ve reporting

### 4. Verification
- Test execution
- Lint checking
- Security scanning
- Gate evaluation

### 5. Completion
- Artifact generation (PLAN.md, RESULT.md)
- Task status update
- Lease release

## Activation Logic

```python
def should_activate(context):
    """Skill aktivasyon logic'i"""

    # 1. Pattern check
    message = context.last_user_message
    patterns = [
        r"(?i)ybis\s+task",
        r"(?i)run\s+task\s+[A-Z]+-\d+",
        r"(?i)execute\s+[A-Z]+-[a-f0-9]+",
    ]
    for pattern in patterns:
        if re.search(pattern, message):
            return True

    # 2. MCP server check
    if "ybis" in context.available_mcp_servers:
        # YBIS MCP available, check for task keywords
        keywords = ["task", "workflow", "claim", "execute"]
        if any(kw in message.lower() for kw in keywords):
            return True

    # 3. File context check
    if any("PLAN.md" in f or "RESULT.md" in f for f in context.recent_files):
        return True

    return False
```

## Execution Flow

### Phase 1: Context Gathering
```yaml
actions:
  - tool: mcp__ybis__get_tasks
    params:
      status: "pending"
      limit: 10
    output: pending_tasks

  - tool: Read
    params:
      file_path: "docs/governance/YBIS_CONSTITUTION.md"
    output: governance_rules

  - tool: Glob
    params:
      pattern: "src/ybis/**/*.py"
    output: source_files
```

### Phase 2: Task Selection
```yaml
logic: |
  IF user specified task_id:
    selected_task = task_id
  ELIF pending_tasks not empty:
    selected_task = pending_tasks[0]  # Priority-sorted
  ELSE:
    ASK user for task details
    CREATE new task

actions:
  - tool: mcp__ybis__claim_task
    params:
      task_id: "${selected_task}"
      worker_id: "claude-code-skill"
```

### Phase 3: Planning
```yaml
actions:
  - tool: Task
    params:
      subagent_type: "Plan"
      prompt: "Plan implementation for: ${task.objective}"
    output: implementation_plan

  - tool: Write
    params:
      file_path: "workspaces/active/${task_id}/docs/PLAN.md"
      content: "${implementation_plan}"
```

### Phase 4: Implementation
```yaml
loop:
  for_each: implementation_plan.steps
  actions:
    - tool: TodoWrite
      params:
        todos:
          - content: "${step.description}"
            status: "in_progress"

    - tool: Edit
      params:
        file_path: "${step.file}"
        changes: "${step.changes}"

    - tool: TodoWrite
      params:
        todos:
          - content: "${step.description}"
            status: "completed"
```

### Phase 5: Verification
```yaml
actions:
  - tool: Bash
    params:
      command: "cd ${PROJECT_ROOT} && python -m pytest tests/ -v"
    output: test_results
    on_failure: "retry_with_fix"

  - tool: Bash
    params:
      command: "cd ${PROJECT_ROOT} && ruff check src/"
    output: lint_results
```

### Phase 6: Completion
```yaml
actions:
  - tool: mcp__ybis__artifact_write
    params:
      task_id: "${task_id}"
      artifact_type: "RESULT"
      content: "${generate_result_md()}"

  - tool: mcp__ybis__task_complete
    params:
      task_id: "${task_id}"
      status: "completed"
      result_summary: "${summary}"
```

## Error Handling

```yaml
error_handlers:
  - error: "TaskAlreadyClaimed"
    action: "select_next_pending_task"
    max_retries: 3

  - error: "TestFailure"
    action: "analyze_and_fix"
    max_retries: 2

  - error: "LintError"
    action: "auto_fix_lint"
    max_retries: 1

  - error: "Timeout"
    action: "save_progress_and_report"

  - error: "*"
    action: "report_failure_and_release_lease"
```

## Output Templates

### Success Output
```markdown
## YBIS Task Execution Complete

**Task:** ${task_id} - ${task.title}
**Status:** ${final_status}
**Duration:** ${duration}

### Changes Made
${changes_summary}

### Test Results
- Passed: ${tests.passed}
- Failed: ${tests.failed}
- Skipped: ${tests.skipped}

### Verification
- Lint: ${lint_status}
- Types: ${type_status}
- Security: ${security_status}

### Artifacts
- [PLAN.md](workspaces/active/${task_id}/docs/PLAN.md)
- [RESULT.md](workspaces/active/${task_id}/artifacts/RESULT.md)

### Next Steps
${next_steps}
```

### Failure Output
```markdown
## YBIS Task Execution Failed

**Task:** ${task_id} - ${task.title}
**Status:** FAILED
**Failed At:** Phase ${failed_phase}

### Error Details
${error_message}

### Partial Progress
${partial_progress}

### Recovery Options
1. ${recovery_option_1}
2. ${recovery_option_2}

### Debug Info
${debug_info}
```

## Integration Points

### MCP Tools Used
- `mcp__ybis__get_tasks` - Task listing
- `mcp__ybis__task_status` - Task details
- `mcp__ybis__claim_task` - Task claiming
- `mcp__ybis__task_run` - Workflow execution
- `mcp__ybis__task_complete` - Task completion
- `mcp__ybis__artifact_write` - Artifact storage
- `mcp__ybis__artifact_read` - Artifact retrieval

### Subagents Used
- `Explore` - Codebase exploration
- `Plan` - Implementation planning
- `Bash` - Command execution

### Hooks Integration
- Triggers `PreToolUse` hooks before MCP calls
- Respects `PostToolUse` hooks for logging

## Configuration

User can override skill behavior in `.claude/settings.json`:

```json
{
  "skills": {
    "ybis-task-executor": {
      "enabled": true,
      "auto_invoke": false,
      "preferred_model": "opus",
      "timeout": 600000,
      "custom_settings": {
        "max_test_retries": 3,
        "auto_commit": false,
        "notify_on_complete": true
      }
    }
  }
}
```

## Examples

### Example 1: Execute specific task
```
User: "YBIS task T-abc123'ü çalıştır"
Skill: Activates, claims task, executes full cycle
```

### Example 2: Claim next task
```
User: "Claim next pending task from YBIS"
Skill: Lists pending, claims first, starts execution
```

### Example 3: Task status check
```
User: "YBIS task durumunu kontrol et"
Skill: Partial activation, shows status only
```
