---
id: TASK-New-686
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-28T00:46:39.151260
updated_at: 2025-12-28T01:00:45
assignee: claude-code
priority: HIGH
target_files:
  - src/agentic/mcp_server.py
  - src/agentic/infrastructure/sandbox.py
  - src/agentic/infrastructure/command_validator.py
  - docker-compose.yml
---

# INFRA-V5-OPEN-INTERPRETER: Integrate Open Interpreter Core

## Objective

Integrate Open Interpreter to give agents **safe, controlled OS-level execution** capabilities through MCP tools. This enables agents to perform system operations like "Fix WiFi", "Install Docker", or "Restart service" - but ONLY through a security-hardened wrapper.

## Research Findings (Phase 1 - COMPLETE)

### Open Interpreter Reality Check
- **Architecture**: LLM + exec() function running code DIRECTLY on machine
- **Access**: Full internet, all installed packages, no isolation by default
- **Current Safety**: Manual approval + experimental semgrep scanning
- **Sandboxing**: Docker (experimental), E2B cloud (Python only)

### Security Assessment: HIGH RISK ⚠️
- Direct code execution without filtering
- Full system access
- Experimental sandboxing only
- No built-in audit trail

**Conclusion**: We CANNOT use raw Open Interpreter. Must build custom safety layer.

## Approach: Security-First Integration

### Phase 1: Docker Sandbox (Week 1)
Build isolated execution environment:
- Dedicated Docker container for code execution
- No network access by default
- Read-only filesystem (except /workspace)
- Resource limits (CPU, memory, time)
- Container restart after each execution

### Phase 2: Command Validation (Week 1-2)
Build validation layer BEFORE execution:
- **Allowlist**: Safe commands (ls, cat, grep, basic Python)
- **Blocklist**: Dangerous operations (rm -rf, dd, fork bombs, network calls)
- **Context-aware**: Different rules for different agents
- Semgrep + AST analysis for Python code
- Shell command parser for bash

### Phase 3: MCP Tool Wrapper (Week 2)
Create controlled interface:
```python
execute_os_command(
    command: str,
    agent_id: str,
    justification: str,
    timeout: int = 30,
    require_approval: bool = True
)
```
- Validates via Phase 2
- Executes in Phase 1 sandbox
- Logs to Phase 4 audit trail
- Returns: stdout, stderr, exit_code, risk_score

### Phase 4: Neo4j Audit Trail (Week 2-3)
Log EVERYTHING:
- Who executed what command
- When, why (justification)
- Result (success/failure)
- Risk score from validator
- Graph relationships: Agent→Command→File→Result

### Phase 5: Sentinel++ Monitoring (Week 3)
Real-time anomaly detection:
- Unusual command patterns
- Repeated failures
- Escalation attempts (sudo, privilege escalation)
- Resource abuse
- Alert via messaging system

### Phase 6: Gradual Rollout (Week 4)
1. Test environment only
2. Claude only (infrastructure tasks)
3. All agents (approved commands only)
4. Expand allowlist based on usage patterns

## Implementation Steps

### 1. Docker Sandbox Infrastructure ✅ (In Progress)
```yaml
# docker-compose.yml
services:
  sandbox:
    image: python:3.12-slim
    container_name: ybis-sandbox
    networks:
      - isolated
    volumes:
      - ./workspaces/sandbox:/workspace:rw
    cap_drop:
      - ALL
    cap_add:
      - CHOWN  # Only safe capabilities
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp:size=100M
    mem_limit: 512m
    cpus: 0.5
```

### 2. Command Validator (src/agentic/infrastructure/command_validator.py)
```python
class CommandValidator:
    ALLOWLIST = [
        r'^ls(\s+-[lah]+)?(\s+\S+)?$',  # ls with flags
        r'^cat\s+[\w/.-]+$',             # cat specific file
        r'^grep\s+.+$',                  # grep
        r'^python3?\s+-c\s+.+$',         # python -c (with AST validation)
    ]

    BLOCKLIST = [
        r'rm\s+-rf',
        r'\bsudo\b',
        r'\bsu\b',
        r'>\s*/dev/',
        r'fork\(',
        r'eval\(',
        r'exec\(',
    ]

    def validate(self, command: str) -> ValidationResult:
        # Check blocklist first
        # Check allowlist
        # For Python: AST analysis
        # Return: allowed, risk_score, reason
```

### 3. MCP Tool (src/agentic/mcp_server.py)
```python
@server.call_tool()
async def execute_os_command(
    command: str,
    agent_id: str,
    justification: str,
    timeout: int = 30,
) -> List[types.TextContent]:
    # 1. Validate
    validation = validator.validate(command)
    if not validation.allowed:
        return error(validation.reason)

    # 2. Log to Neo4j (pre-execution)
    audit_id = graph.log_command_attempt(agent_id, command, justification)

    # 3. Execute in Docker
    result = await docker_sandbox.execute(command, timeout)

    # 4. Log to Neo4j (post-execution)
    graph.log_command_result(audit_id, result)

    # 5. Check for anomalies
    if sentinel.detect_anomaly(agent_id, command, result):
        messaging.alert("Anomalous command detected", ...)

    return result
```

### 4. Neo4j Audit Schema
```cypher
CREATE (cmd:OSCommand {
    id: 'CMD-12345',
    command: 'ls -la /etc',
    timestamp: datetime(),
    risk_score: 0.1
})
CREATE (agent:Agent {id: 'claude-code'})
CREATE (agent)-[:EXECUTED {justification: 'Debug config'}]->(cmd)
CREATE (cmd)-[:RESULTED_IN {
    exit_code: 0,
    duration_ms: 45
}]->(result:CommandResult)
```

### 5. Sentinel++ Rules
```python
# sentinel_rules.py
ANOMALY_RULES = [
    {
        'name': 'repeated_failures',
        'condition': 'same_command_failed_3_times_in_1_hour',
        'severity': 'MEDIUM',
        'action': 'alert'
    },
    {
        'name': 'privilege_escalation_attempt',
        'condition': 'blocked_command_contains_sudo_or_su',
        'severity': 'HIGH',
        'action': 'alert_and_log'
    },
]
```

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Sandbox escape | CRITICAL | Use Docker security features, minimal capabilities, read-only FS |
| Command injection | HIGH | Strict regex validation, no shell=True, parameterized execution |
| Resource exhaustion | MEDIUM | CPU/memory/time limits, container restart |
| Audit trail tampering | MEDIUM | Neo4j access control, immutable logs |
| False positives blocking work | LOW | Start with permissive allowlist, expand based on usage |

## Success Criteria

### Phase 1 (Sandbox)
- [ ] Docker sandbox container running
- [ ] Command execution isolated
- [ ] Resource limits enforced
- [ ] Container auto-restart working

### Phase 2 (Validation)
- [ ] Allowlist/blocklist implemented
- [ ] Python AST validation working
- [ ] 0 false negatives (no dangerous commands pass)
- [ ] <5% false positives (safe commands blocked)

### Phase 3 (MCP Tool)
- [ ] `execute_os_command` MCP tool registered
- [ ] Returns structured results
- [ ] Error handling robust
- [ ] Timeout enforcement working

### Phase 4 (Audit)
- [ ] All commands logged to Neo4j
- [ ] Graph relationships queryable
- [ ] Audit trail immutable
- [ ] Query: "Show all commands by agent X"

### Phase 5 (Monitoring)
- [ ] Sentinel++ rules active
- [ ] Anomaly alerts working
- [ ] False positive rate <1%
- [ ] Response time <10s

### Phase 6 (Rollout)
- [ ] Tested with 100 commands (0 escapes)
- [ ] Claude using in production
- [ ] Documentation complete
- [ ] Usage metrics dashboard

## Dependencies

- Docker (already installed)
- Neo4j (already running)
- Sentinel (exists, needs rules)
- MCP server (running)
- Open Interpreter library (NOT INSTALLED - may not need full package)

## Timeline

- Week 1: Sandbox + Validator (80% done)
- Week 2: MCP Tool + Audit Trail
- Week 3: Sentinel Integration + Testing
- Week 4: Rollout + Documentation

**Target Completion**: 2025-01-24

## Notes

- **DO NOT install raw open-interpreter package** - extract concepts only
- Security > Functionality - block if uncertain
- Start restrictive, expand based on real usage
- Every execution is logged, auditable, reversible
- This is NOT autopilot - agents request, we validate, then execute

## Sources

- Open Interpreter Docs: https://docs.openinterpreter.com/safety/introduction
- Isolation Guide: https://docs.openinterpreter.com/safety/isolation
- Security Issues: https://github.com/OpenInterpreter/open-interpreter/issues/1536
