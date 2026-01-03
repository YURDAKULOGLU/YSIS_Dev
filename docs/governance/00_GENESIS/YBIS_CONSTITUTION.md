# YBIS SYSTEM CONSTITUTION (V1.1)

> "Dog Scales Dog"
> *We define the system that builds the system.*

This document establishes the supreme laws governing the YBIS_Dev autonomous development environment. All agents (biological or synthetic) operating within this jurisdiction must adhere to this modular constitution.

---

## TABLE OF CONTENTS

### [ARTICLE 1: THE PRIME DIRECTIVES (Manifesto)](../10_META/Governance/1_PRINCIPLES.md)
*The core philosophy. Why we exist, and the "Iron Chain" rule.*

### [ARTICLE 2: CORPORATE HIERARCHY (Roles)](../10_META/Governance/2_ROLES.md)
*Who is in charge? The relationship between The Chairman (Human), The Strategist (Meta-Agent), and The Workforce.*

### [ARTICLE 3: OPERATIONAL PROTOCOLS (The "How")](../10_META/Governance/3_PROTOCOLS.md)
*How work gets done. Spec-Driven Development, Onboarding, and the Definition of Done.*
- **Commit Discipline:** All commits must run inside the active worktree (`YBIS_CODE_ROOT`), with zero unstaged files and passing pre-commit hooks. No bypass flags.
- **Allowed-File Gate:** Only files explicitly allowed by the plan may be staged or committed. Any extra staged, unstaged, or untracked files must fail the task.
- **Observability Standard:** Core modules must log to both terminal and file (see `docs/governance/00_GENESIS/CODE_STANDARDS.md`).
- **Adapter-First Rule:** Any external framework must integrate through an adapter in the spine. A native equivalent must be scheduled in the backlog, with explicit deprecation criteria for the adapter.

### [ARTICLE 4: SECURITY & BOUNDARIES (Red Lines)](../10_META/Governance/4_SECURITY.md)
*What is strictly forbidden. File system limits and safety checks.*

### [ARTICLE 5: RISK & QUALITY GATES](../RISK_MATRIX.md)
*   **[Risk Classification Matrix](../RISK_MATRIX.md)**
*   **[Verification Standards](../VERIFICATION_STANDARDS.md)**
*   **[Framework Governance](../FRAMEWORK_TIERS.md)**

### [ARTICLE 6: TOKEN ECONOMY & SLIM REPORTING](../TAGGING_STANDARD.md)
*   **[SLIM Templates](../templates/SLIM_RESULT.md)**
*   **[Tagging Standard (§-Symbols)](../TAGGING_STANDARD.md)**
*   **LiteLLM Policy:** LiteLLM is **OPTIONAL**. Local Ollama is the default. Feature flags required.

### ARTICLE 7: SELF-HEALING & EXTENSIBILITY

> "Observe -> Detect -> Debate -> Decide -> Apply -> Verify -> Learn"

#### 7.1 Observability (MANDATORY)
- **Structured Logging:** JSON format, context-aware, severity levels
- **Metrics:** Success rate, latency, error patterns tracked
- **Event Bus:** All significant events published via Redis pub/sub
- **Health Endpoints:** Each component reports its own health
- **Tracing:** Task flow visibility end-to-end

#### 7.2 Solution Space Hierarchy
When solving problems, follow this priority order:
1. **FRAMEWORK** - Is there an open-source solution? (HIGHEST PRIORITY)
2. **LIBRARY** - Can we add a library?
3. **CONFIG** - Can we change configuration?
4. **TWEAK** - Small code modification?
5. **PATTERN** - Apply design pattern?
6. **CUSTOM** - Write from scratch (LAST RESORT)

#### 7.3 Framework Integration Rules
- **NEVER** fork or modify framework code directly
- **ALWAYS** use adapter/bridge pattern
- **ALWAYS** implement fallback mechanism
- **ALWAYS** pin versions with update policy
- **ALWAYS** write contract tests

#### 7.4 Extensibility Principles
- **Plugin Architecture:** Everything is a plugin, core is minimal
- **Protocol-First:** Depend on abstractions, not concretions
- **Hot-Swap Ready:** Plugins replaceable at runtime
- **Contract Testing:** Plugin behavior guaranteed by tests

#### 7.5 Self-Healing Loop
```
1. OBSERVE  -> Metrics, logs, events continuously collected
2. DETECT   -> Anomaly/error patterns identified
3. DEBATE   -> Solution space explored (framework? tweak?)
4. DECIDE   -> Best solution selected
5. APPLY    -> Solution implemented (code/config/framework)
6. VERIFY   -> Solution tested
7. LEARN    -> Pattern added to Knowledge Base
```

---

## QUICK START
If you are a new agent, acknowledge this Constitution and proceed immediately to:
👉 **[00_GENESIS/ONBOARDING.md](../00_GENESIS/ONBOARDING.md)**
