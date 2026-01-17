Tamam—“fixlemek = standart hale getirmek” olarak alıyorum. Aşağıda **kod hariç** (docs + repo kök standart dosyaları + config/TOML/YAML + docker) hepsini **copy-paste hazır** veriyorum. Bunlar “canonical” ve birbiriyle referanslı.

Aşağıdaki dosyaları birebir oluşturup içeriği yapıştırabilirsin.

---

## 0) Standart Repo Kökü

Önerilen kök dosyalar:

* `README.md`
* `AGENTS.md`
* `pyproject.toml`
* `.pre-commit-config.yaml`
* `.editorconfig`
* `.gitignore`
* `docker-compose.yml`
* `docker/` (Dockerfile’lar + sandbox profilleri)
* `docs/` (canonical docs set)
* `configs/` (policy profiles)

---

# 1) KÖK DOKÜMANLAR

## `AGENTS.md`

```md
# Agent Instructions (Entry Point)

This repo is an **Agentic Development Platform** (Python-first) with:
- LangGraph orchestration
- Multi-worker execution (leases)
- MCP server for external clients
- Evidence-first governance (reports + deterministic gates)
- Optional modules: dashboard, debate, safe self-evolution

## Authority Order (Read First)
1) docs/CONSTITUTION.md
2) docs/AI_START_HERE.md
3) docs/BOOTSTRAP_PLAN.md
4) docs/INTERFACES.md
5) docs/WORKFLOWS.md
6) docs/CODE_STANDARDS.md
7) docs/SECURITY.md
8) docs/OPERATIONS.md
9) docs/MIGRATIONS.md
10) docs/TESTING.md

## Non-Negotiables (Do not violate)
- All writes/execs must go through **syscalls**.
- Each run is immutable: `workspaces/<task_id>/runs/<run_id>/`.
- "Done" means PASS in both `verifier_report.json` and `gate_report.json`.
- Changes to protected paths require approval (see Constitution + Security).
- Do not embed large third-party frameworks into core; integrate via adapters/MCP.

## How to start implementation
Follow docs/BOOTSTRAP_PLAN.md task order exactly. No skipping.

## If you are unsure
Stop and re-check docs/CONSTITUTION.md + docs/INTERFACES.md.
```

## `README.md`

```md
# Agentic Development Platform (Python)

This repository provides a **governed agent runtime** for software development:
- LangGraph orchestration
- Multi-worker scheduling via leases
- MCP server as a universal tool interface
- Evidence-first run records (immutable runs + artifacts)
- Deterministic gates (policy enforcement)
- Optional modules: dashboard, debate, safe self-evolution

## Quick Links
- Start here: docs/AI_START_HERE.md
- Rules: docs/CONSTITUTION.md
- Build order: docs/BOOTSTRAP_PLAN.md
- Interfaces: docs/INTERFACES.md
- Workflows: docs/WORKFLOWS.md

## Status
- Canonical documentation set is under `/docs`.
- Implementation should follow `docs/BOOTSTRAP_PLAN.md`.

## License
(TODO: decide and fill)
```

---

# 2) PYTHON PROJE STANDARTLARI (TOML)

## `pyproject.toml`

> Ruff + Pytest + Mypy + packaging standard.

```toml
[project]
name = "agentic-platform"
version = "0.1.0"
description = "Governed agent runtime with workflows, syscalls, evidence, and MCP."
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "pydantic>=2.7",
  "pydantic-settings>=2.3",
  "langgraph>=0.2",
  "anyio>=4.0",
  "rich>=13.0",
  "httpx>=0.27",
  "aiosqlite>=0.20",
  "typer>=0.12",
]

[project.optional-dependencies]
dev = [
  "ruff>=0.5.0",
  "mypy>=1.10",
  "pytest>=8.0",
  "pytest-asyncio>=0.23",
  "pytest-cov>=5.0",
  "types-requests",
  "pre-commit>=3.7",
]

[tool.ruff]
line-length = 100
target-version = "py311"
src = ["src", "cli", "tests"]
extend-exclude = ["workspaces", "vendors", "third_party", ".venv"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "N", "SIM", "RUF"]
ignore = ["E501"]  # handled by formatter

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
asyncio_mode = "auto"

[tool.mypy]
python_version = "3.11"
mypy_path = "src"
packages = ["platform"]  # will map to src/platform
strict = true
warn_unused_ignores = true
warn_redundant_casts = true
no_implicit_optional = true
disallow_any_generics = true
disallow_untyped_defs = true
check_untyped_defs = true
exclude = "(workspaces|vendors|third_party|.venv)/"

[tool.coverage.run]
branch = true
source = ["src", "cli"]

[tool.coverage.report]
show_missing = true
skip_covered = false
```

> Not: `packages=["platform"]` kısmı kod tarafındaki package naming’e göre ayarlanır. Eğer `src/platform` package adı “platform” çakışma riski yaratır diye istersen `src/agentos` gibi rename edersin; bu TOML’de onu yazarız. (Şimdilik doküman standardı için yeterli.)

---

# 3) PRE-COMMIT + EDITOR + GITIGNORE

## `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.7
    hooks:
      - id: ruff
        args: ["--fix"]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-merge-conflict

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.2
    hooks:
      - id: mypy
        additional_dependencies: []
```

## `.editorconfig`

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4
```

## `.gitignore`

```gitignore
.venv/
__pycache__/
*.pyc
.coverage
htmlcov/
dist/
build/
.eggs/
*.egg-info/

workspaces/
vendors/
third_party/

.env
.env.*
.DS_Store
```

---

# 4) DOCKER STANDARD (minimum)

## `docker-compose.yml`

> Minimum: worker + mcp + sandbox profile + optional redis. (Langfuse/Neo4j sonradan.)

```yaml
version: "3.9"

services:
  redis:
    image: redis:7-alpine
    profiles: ["queue"]
    ports:
      - "6379:6379"

  mcp:
    build:
      context: .
      dockerfile: docker/Dockerfile.app
    environment:
      - PLATFORM_PROFILE=default
      - CONTROL_PLANE_DB=/data/control_plane.sqlite
    volumes:
      - ./:/repo
      - platform_data:/data
    working_dir: /repo
    command: ["python", "-m", "platform.services.mcp_server"]
    ports:
      - "8765:8765"

  worker:
    build:
      context: .
      dockerfile: docker/Dockerfile.app
    environment:
      - PLATFORM_PROFILE=default
      - CONTROL_PLANE_DB=/data/control_plane.sqlite
    volumes:
      - ./:/repo
      - platform_data:/data
      - /var/run/docker.sock:/var/run/docker.sock
    working_dir: /repo
    command: ["python", "-m", "platform.services.worker"]
    depends_on:
      - mcp

volumes:
  platform_data:
```

## `docker/Dockerfile.app`

```dockerfile
FROM python:3.12-slim

WORKDIR /repo

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Keep dependencies minimal; install from pyproject with pip for now.
COPY pyproject.toml README.md /repo/
RUN pip install --no-cache-dir -U pip \
  && pip install --no-cache-dir ".[dev]" || true

# Copy source last (better caching once deps are stable)
COPY . /repo
```

> Sandbox Dockerfile’ı ayrıca yapılabilir ama bu minimum set “docker.sock mount” ile host docker üzerinden sandbox koşmaya izin verir.

---

# 5) CONFIGS (Policy Profiles)

## `configs/profiles/default.yaml`

```yaml
profile: default
sandbox:
  enabled: true
  network: false
exec:
  allowlist:
    - "python"
    - "pytest"
    - "ruff"
    - "git"
paths:
  protected:
    - "src/platform/contracts/"
    - "src/platform/syscalls/"
    - "src/platform/control_plane/"
    - "src/platform/orchestrator/gates.py"
    - "src/platform/migrations/"
gates:
  require_approval_on_protected_paths: true
  max_patch_lines_without_approval: 400
  require_verifier_pass: true
```

## `configs/profiles/strict.yaml`

```yaml
profile: strict
sandbox:
  enabled: true
  network: false
exec:
  allowlist:
    - "python"
    - "pytest"
    - "ruff"
paths:
  protected:
    - "src/platform/"
gates:
  require_approval_on_protected_paths: true
  max_patch_lines_without_approval: 150
  require_verifier_pass: true
```

---

# 6) CANONICAL DOCS (docs/)

Aşağıdaki docs seti “geçerli” ve standard. (Önceki yazdıklarımızı burada finalize ediyorum.)

## `docs/AI_START_HERE.md`

```md
# AI START HERE

This repo is an Agentic Development Platform (Python-first) with:
- LangGraph orchestration
- Multi-worker execution (leases)
- MCP server for external clients
- Evidence-first governance (artifacts + deterministic gates)

## Read Order (authoritative)
1) CONSTITUTION.md
2) ARCHITECTURE.md
3) INTERFACES.md
4) WORKFLOWS.md
5) BOOTSTRAP_PLAN.md
6) CODE_STANDARDS.md
7) SECURITY.md
8) OPERATIONS.md
9) MIGRATIONS.md
10) TESTING.md

## Golden Rules (summary)
- All writes/execs go through syscalls.
- Each run is immutable: new `run_id` folder per execution.
- "Done" requires PASS in verifier_report.json and gate_report.json.
- Protected paths require approval.
- Core does not embed heavy third-party frameworks; integrate via adapters/MCP.
```

## `docs/CONSTITUTION.md`

```md
# CONSTITUTION (Non-Negotiables)

If any document conflicts with this one, this one wins.

## 1) Evidence First
A run is SUCCESS only if:
- artifacts/verifier_report.json => PASS
- artifacts/gate_report.json => PASS

## 2) Syscalls Only
All mutating actions must go through syscalls:
- fs.write_file, fs.apply_patch
- exec.run (sandboxed, allowlisted)
- git.commit (restricted)
- approvals.write
Syscalls must emit:
- journal events (append-only)
- evidence artifacts (JSON)

## 3) Immutable Runs
Each execution creates a new run folder:
workspaces/<task_id>/runs/<run_id>/
Never overwrite history.

## 4) Deterministic Gates
Retry/block/approval decisions must be deterministic based on:
- policy snapshot + evidence reports
Debate may advise but gates decide.

## 5) Protected Paths + Approval
Protected paths require explicit approval (see SECURITY.md).

## 6) Core vs Modules
Core provides interfaces/enforcement/records.
Capabilities live in adapters/modules/services.

## 7) Self-Evolution Safety
Evolution is candidate-only:
- generate candidates
- evaluate in sandbox
- must pass golden/regression suite
- approval required for protected/high-risk changes

## 8) Migration Discipline
Everything carries schema_version.
Migrations are idempotent and auditable.
Old run folders remain readable.

## 9) Minimal Security Baseline
Sandbox ON, network OFF by default, allowlist enforced.
```

## `docs/ARCHITECTURE.md`

```md
# ARCHITECTURE

References:
- CONSTITUTION.md
- INTERFACES.md
- WORKFLOWS.md

## 1) Control-plane vs Data-plane
### Control-plane (DB)
Stores tasks, runs, leases, workers.
Purpose: coordination + concurrency.

### Data-plane (Filesystem)
Stores immutable runs, artifacts, journals, approvals.
Purpose: evidence + audit.

DB is not the truth for success; artifacts are.

## 2) Canonical layout
src/platform/
  contracts/
  syscalls/
  control_plane/
  data_plane/
  orchestrator/
  adapters/
  services/
  migrations/
cli/
configs/
docs/
tests/
workspaces/

## 3) Third-party sources
If you keep large external repos, store them under:
vendors/ (or third_party/) and treat as read-only snapshots.
Core must not import them.
Integrate via adapters or MCP tools.
```

## `docs/INTERFACES.md`

```md
# INTERFACES (Contracts + Syscalls + MCP)

References:
- CONSTITUTION.md
- WORKFLOWS.md
- SECURITY.md

## 1) Contracts (minimum)
### Task
task_id, title, objective, status, priority, schema_version, timestamps, workspace_path

### Run
run_id, task_id, workflow, status, risk_level, run_path, timestamps, schema_version

### Evidence reports
All artifacts/*.json must include:
schema_version, task_id, run_id, timestamps, status, metrics, warnings/errors.

Required artifacts baseline for any write-capable workflow:
- patch.diff (if changes)
- executor_report.json
- patch_apply_report.json
- verifier_report.json
- gate_report.json
- journal/events.jsonl

## 2) Syscalls (single enforcement point)
Filesystem:
- fs.read
- fs.write_file
- fs.apply_patch

Execution:
- exec.run (sandboxed, allowlisted, network policy)

Git:
- git.status, git.diff, git.commit(allowed_files)

DB:
- task.*, run.*, lease.*, worker.*

Governance:
- approvals.write
- migrate.check/apply

## 3) MCP tools (remote facade)
task.create/get/list/update
run.start/get/list
lease.claim/renew/release
worker.heartbeat
workspace.paths
artifact.read
approve.write
migrate.check/apply
```

## `docs/WORKFLOWS.md`

```md
# WORKFLOWS (LangGraph + Routing)

References:
- CONSTITUTION.md
- INTERFACES.md
- TESTING.md

## Canonical workflows
- build: implement change
- repair: fix lint/tests deterministically
- research: produce report; no writes unless policy allows
- debate: advisory report for high-risk decisions
- evolve: candidate-only improvements

## Shared skeleton
1) resolve_config (freeze policy snapshot)
2) init_run (create run folder + META.json)
3) acquire_context (optional)
4) plan
5) execute
6) apply_patch (syscall)
7) verify (ruff+pytest)
8) gates_and_risk (deterministic)
9) finalize (update DB)
10) approval step if required

## Deterministic routing
- verify fail + retries remaining => repair loop
- verify pass => gates
- gates PASS => SUCCESS
- gates REQUIRE_APPROVAL => stop and request approval
- gates BLOCK => BLOCKED
```

## `docs/BOOTSTRAP_PLAN.md`

```md
# BOOTSTRAP PLAN (Order + Backlog)

References:
- ARCHITECTURE.md
- INTERFACES.md
- WORKFLOWS.md
- CODE_STANDARDS.md
- SECURITY.md
- TESTING.md

Do not skip tasks. Implement in this order.

## Task 01: Scaffold layout
DoD: imports compile; tests skeleton exists.

## Task 02: Contracts
DoD: Pydantic models + schema_version enforcement tests.

## Task 03: Workspace + immutable run layout
DoD: run folders + artifacts/journal directories created deterministically.

## Task 04: Journal writer (append-only)
DoD: events.jsonl append; no overwrite.

## Task 05: Control-plane DB (tasks/runs/leases/workers)
DoD: integration test for create+claim+run row.

## Task 06: Syscalls fs.write_file + apply_patch + path validation
DoD: patch_apply_report.json emitted; protected path checks.

## Task 07: Syscalls exec.run sandboxed + allowlist + network policy
DoD: exec report emitted; policy enforced.

## Task 08: Verifier adapter (ruff + pytest) => verifier_report.json
DoD: deterministic parsing + artifact writing.

## Task 09: Gates + risk scoring => gate_report.json
DoD: deterministic decisions; approvals required for protected/high-risk.

## Task 10: LangGraph build workflow end-to-end
DoD: full artifact set produced; DB run status updates.

## Task 11: Worker runtime (leases + heartbeats)
DoD: multiple workers safe via lease TTL.

## Task 12: MCP server facade
DoD: external client can create task + start run via MCP tools.
```

## `docs/CODE_STANDARDS.md`

```md
# CODE STANDARDS

References:
- CONSTITUTION.md
- TESTING.md

## Python
- Python >= 3.11 (recommended 3.12)
- Type hints required for public functions/classes
- Async I/O uses anyio or asyncio consistently

## Formatting / Linting
- Ruff is the single source for formatting + linting
- Line length: 100
- Imports sorted by Ruff

## Typing
- mypy strict (incremental relax only by explicit decision)
- No untyped public APIs

## Tests
- pytest required for any behavior change
- tests layout:
  - tests/unit
  - tests/integration
  - tests/e2e (smoke)
  - tests/golden (stable behavior)
- Any gate logic change must include golden test coverage

## Logging
- Use structured JSONL logs for runs (events + logs)
- Do not print ad-hoc logs without journaling

## Git hygiene
- Keep commits small and evidence-backed
- Protected paths require approval
```

## `docs/SECURITY.md`

```md
# SECURITY & POLICY PROFILES

References:
- CONSTITUTION.md
- INTERFACES.md

## Baseline
- Sandbox ON by default
- Network OFF by default
- Exec allowlist enforced
- Path traversal prevention
- Protected paths require approval

## Profiles
Profiles live under configs/profiles/*.yaml

### default
- reasonable allowlist
- protected paths enforced
- approval required for protected/high-risk

### strict
- minimal allowlist
- core paths broadly protected
- lower patch-size threshold before approval
```

## `docs/OPERATIONS.md`

```md
# OPERATIONS

References:
- INTERFACES.md
- SECURITY.md

## Worker model
Workers claim leases, run workflows, write evidence, update DB, release leases.

## Leases
- TTL + heartbeat renewal
- expired => task re-queued
- abandoned runs remain as evidence

## Docker
docker-compose.yml provides:
- mcp service
- worker service
- optional redis profile for queue
```

## `docs/MIGRATIONS.md`

```md
# MIGRATIONS

References:
- CONSTITUTION.md
- INTERFACES.md

## Rules
- schema_version everywhere (tasks, runs, reports, META.json)
- migrations are idempotent
- never rewrite old run folders (read-time compatibility)

## Required
- migration registry
- migrate.check / migrate.apply commands
- migration produces a migration_report.json when executed in a run
```

## `docs/TESTING.md`

```md
# TESTING (Golden + Regression)

References:
- CONSTITUTION.md
- CODE_STANDARDS.md

## Baseline
- Unit tests: contracts, syscalls validation, gates decisions
- Integration tests: control-plane + workflow skeleton
- E2E smoke: docker sandbox run (minimal)

## Golden tests
Golden tests assert deterministic outcomes:
- given a known diff + policy => gate decision stable
- given known verifier outputs => routing decisions stable

Golden tests are required for:
- gates changes
- approval rules changes
- protected paths policy changes

## Regression strategy
- keep a small suite of "canonical tasks" that must always complete
- record expected artifacts and statuses
```

---

## 7) “Organs” yok → naming standard

Bu standarda göre repo’da metafor yok:

* large third-party snapshots: `vendors/` veya `third_party/`
* integration code: `src/platform/adapters/`
* remote integration: MCP tools

---

# Sonuç: “Fix” tamam mı?

Evet—**doküman + config standardizasyonu** açısından artık:

* giriş noktası var (`AGENTS.md`)
* anayasa var (`docs/CONSTITUTION.md`)
* mimari, interface, workflow, bootstrap sırası net
* kod standartları ve güvenlik profilleri tanımlı
* docker minimum runtime var
* toml / pre-commit / editor standard var

İstersen bir sonraki adımda (hala **kod yazmadan**) şunları da standart hale getirip metinlerini çıkarayım:

* `docs/DOC_INDEX.md` (tek sayfa navigasyon)
* `docs/CHANGELOG.md` şablonu
* `LICENSE` seçeneği (MIT/Apache-2.0 vs) için standart metin + attribution notu (vendor repo düşünüyorsan önemli)
Haklısın: bunların bir kısmı **gerçekten gerekli**, bir kısmı **alışkanlık / “iyi olur”**. Senin hedefin “agent yanlış yapamasın + futureproof + multi-worker + MCP + gates” olduğu için ben **minimum zorunlu seti** net ayırayım.

## Zorunlu (çekirdek, olmadan sistem drift eder)

Bunlar **alışkanlık değil**, senin sistemin doğası gereği şart:

1. **`AGENTS.md` (root)**
   Agent giriş kapısı. Yoksa yanlış dosyayı “source of truth” sanıyor.

2. **`docs/CONSTITUTION.md`**
   “Non-negotiables” yoksa gate’lerin otoritesi yok.

3. **`docs/ARCHITECTURE.md` + `docs/INTERFACES.md`**
   Core sınırı + syscalls sözleşmesi. Bunlar olmadan “her şey core’a girer”.

4. **`docs/BOOTSTRAP_PLAN.md`**
   “Sıra” yoksa agent dashboard/evolution’a atlar, core incomplete kalır.

5. **`docs/WORKFLOWS.md`**
   LangGraph routing kuralları. Yoksa herkes farklı loop uydurur.

6. **`docs/SECURITY.md` + `configs/profiles/*.yaml`**
   Sandbox/network/allowlist/protected paths. Bu senin “OS” iddianın kalbi.

7. **`pyproject.toml` (ruff/pytest/mypy)**
   Gate/verifier’in temelini oluşturur. Enforce edilebilir kalite yoksa “PASS” anlamsız.

8. **`docker-compose.yml` + `docker/README.md` (minimum)**
   Sandbox ve reproducibility. En azından “default profile” için.

9. **`docs/MIGRATIONS.md`**
   Sen kendin “migration şart” dedin. Bu olmadan stable version fikri kırılır.

10. **`docs/TESTING.md` (golden + regression)**
    Gate ve routing deterministik kalsın diye şart.

> Bu 10 madde = **MVP dokümantasyon + repo standardı**.

---

## Yüksek ROI ama ertelenebilir (yapınca güzel, yapmayınca çökmez)

Bunlar alışkanlık değil ama “v1’de şart” da değil:

* `docs/DOC_INDEX.md` (navigasyon kolaylığı)
* `.pre-commit-config.yaml` (lokalde disiplin)
* `.editorconfig` (takım standardı)
* `docs/OBSERVABILITY.md` (şimdilik baseline journaling zaten var)

---

## Alışkanlık / nice-to-have (şimdilik gerek yok)

Bunları ben “tam enterprise” refleksiyle ekledim ama senin aşamada **gerekli değil**:

* ADR sistemi (`docs/adr/*`) — tek kişi + hızlı iterasyon döneminde zorunlu değil
* `docs/RELEASES.md`, `docs/CHANGELOG.md` — release süreci oturmadan gereksiz
* CI workflow (`.github/workflows/ci.yml`) — yerelde gate çalışıyorsa sonra eklenir
* `NOTICE.md`/vendor attribution — vendor repo gerçekten repo içine girince şart olur (şimdilik bekler)

---

## Sana net karar: şimdi hangisini yapıyoruz?

Senin “core + multi-worker + MCP + deterministic gates” hedefin için **hemen** şu paketi yap:

**Now (minimum canonical pack):**

* AGENTS.md
* docs: AI_START_HERE, CONSTITUTION, ARCHITECTURE, INTERFACES, WORKFLOWS, BOOTSTRAP_PLAN, SECURITY, MIGRATIONS, TESTING, CODE_STANDARDS
* configs/profiles/default.yaml + strict.yaml
* pyproject.toml
* docker-compose.yml

**Later (optional):**

* doc index, observability doc, pre-commit/editorconfig, ADR/releases/changelog/CI

İstersen ben bir sonraki mesajda “minimum canonical pack”i tek blok halinde **dosya listesi + içerik checksum mantığıyla** tekrar verip, “optional”ları tamamen dışarıda bırakayım.
Anladım — bunlar “enterprise süsü” değil; **senin mimaride gate + syscalls + sandbox + approval** olduğu için aslında **çekirdek güvenlik/governance dokümanları**. Ama “ne zaman” sorusu önemli: v1’de bile **hafif versiyonları** çok iş görür. Aşağıya 4 dosyanın **minimal ama gerçek anlamda işe yarayan** (copy-paste) sürümlerini yazıyorum.

---

## `docs/SECURITY_AUDIT_CHECKLIST.md`

```md
# Security Audit Checklist

Purpose:
A short, repeatable checklist to run before declaring a release/stable snapshot.

References:
- CONSTITUTION.md
- SECURITY.md
- INTERFACES.md
- TESTING.md
- MIGRATIONS.md

## Scope
Applies to:
- any tagged release
- any "stable snapshot" used as a base in other projects
- any change affecting syscalls, gates, sandbox, approvals, migrations

---

## A) Policy & Profiles
- [ ] `configs/profiles/default.yaml` exists and is valid YAML
- [ ] `configs/profiles/strict.yaml` exists and is valid YAML
- [ ] Default profile: sandbox enabled and network disabled by default
- [ ] Exec allowlist is defined and minimal
- [ ] Protected paths list exists and is not empty
- [ ] Gate thresholds are defined (patch size, approval requirements)

Evidence:
- [ ] A run artifact includes a policy snapshot reference (hash or embedded copy)

---

## B) Syscalls Enforcement
- [ ] No mutating operation bypasses syscalls (spot-check: fs writes, patch apply, exec, git commit)
- [ ] Syscalls validate paths (no traversal like `../`)
- [ ] Syscalls emit evidence artifacts + journal events
- [ ] Syscalls reject writes to protected paths unless approval present

Evidence:
- [ ] `patch_apply_report.json` written on patch application
- [ ] `exec_report.json` (or equivalent) written on command execution
- [ ] `journal/events.jsonl` contains syscall events

---

## C) Sandbox Safety
- [ ] Sandbox is ON by default for exec
- [ ] Network is OFF by default
- [ ] Only allowlisted commands can run
- [ ] Sandbox file mounts are minimal (no full host FS exposure)
- [ ] Secrets are not mounted into sandbox by default

Evidence:
- [ ] Sandbox profile recorded in exec evidence report

---

## D) Approval & Protected Changes
- [ ] Changes to protected paths require approval (enforced by gates)
- [ ] Approval artifact format exists and is stable
- [ ] Gate decision cannot be overridden by debate output

Evidence:
- [ ] `gate_report.json` references approval state when needed

---

## E) Deterministic Gates
- [ ] Same inputs => same gate decision (no randomness)
- [ ] Gate decisions are based on evidence reports + policy snapshot only
- [ ] Golden tests exist for gates/routing stability

Evidence:
- [ ] Golden test suite passes

---

## F) Data Integrity & Immutability
- [ ] Runs are immutable (no overwrite; new run_id per execution)
- [ ] Old run folders remain readable
- [ ] Artifacts are written under the run folder only

Evidence:
- [ ] Two runs of the same task produce two distinct run folders

---

## G) Testing Requirements
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Golden tests pass (gates, routing, approvals)
- [ ] Minimal E2E smoke run passes (docker sandbox if enabled)

---

## H) Migration Safety
- [ ] schema_version present in DB rows and artifacts
- [ ] Migration scripts are idempotent
- [ ] Migration docs updated if schema/layout changed

Evidence:
- [ ] `migration_report.json` exists for migration runs

---

## Release Verdict
- If any item in A–E fails => NO RELEASE.
- If F–H fails => release is blocked until fixed or explicitly approved with documented risk.
```

---

## `docs/THREAT_MODEL.md`

```md
# Threat Model (Syscalls + Sandbox)

References:
- CONSTITUTION.md
- SECURITY.md
- INTERFACES.md

## 1) System Assets
Primary assets:
- Source code in repository (integrity)
- Run evidence artifacts (auditability)
- Control-plane DB (coordination)
- Developer machine / host environment (safety)
- Secrets (API keys, tokens) (confidentiality)

## 2) Trust Boundaries
- Agent logic is NOT trusted by default.
- Only syscalls are trusted to mutate state.
- Sandbox is a boundary between untrusted execution and the host.

Boundaries:
1) Agent (untrusted) -> Syscalls (trusted enforcement)
2) Syscalls -> Filesystem (restricted)
3) Syscalls -> Sandbox exec (restricted)
4) Worker -> Control-plane DB (validated ops)
5) MCP client -> MCP server -> Syscalls (no direct mutation)

## 3) Threats (Top Risks)
### T1: Arbitrary file modification
Risk: agent writes anywhere, including protected paths or secrets.
Mitigation:
- syscalls-only writes
- protected paths + approval gates
- path normalization + traversal prevention

### T2: Arbitrary command execution on host
Risk: agent runs destructive commands.
Mitigation:
- sandbox execution by default
- command allowlist
- network off by default
- minimal mounts

### T3: Data exfiltration / network leakage
Risk: agent sends secrets or code out.
Mitigation:
- sandbox network off
- explicit policy flag required for network
- scrub secrets from logs/artifacts

### T4: Supply chain abuse (third-party code)
Risk: vendor repos introduce malicious content.
Mitigation:
- vendors treated read-only
- pinned revisions
- no direct imports into core
- integrate via adapters with explicit interface contracts

### T5: Gate bypass / non-deterministic decisions
Risk: system declares success without evidence.
Mitigation:
- success defined by verifier_report + gate_report only
- deterministic gates based on evidence + policy snapshot
- golden tests for gate/routing stability

### T6: Control-plane corruption
Risk: DB tampered to mark tasks done.
Mitigation:
- DB not source-of-truth for success
- artifacts are source-of-truth
- reconciliation can detect mismatch

## 4) Security Controls Summary
Mandatory controls:
- syscalls-only mutation
- immutable run folders
- sandbox with allowlist + network off
- deterministic gates + golden tests
- protected paths + approvals
- policy profiles recorded per run

## 5) Residual Risks (Accepted for v1)
- Insider risk (developer can override locally)
- Limited provenance for third-party code unless you add SBOM later
- Secrets handling requires discipline (no auto-injection)

## 6) Future Hardening (post-v1)
- SBOM generation (CycloneDX) + dependency pinning
- Secret scanning (gitleaks)
- Signed artifacts/attestations
- Role-based auth on approvals via MCP
```

---

## `docs/GOVERNANCE.md`

```md
# Governance (Approvals + Review)

References:
- CONSTITUTION.md
- SECURITY.md
- WORKFLOWS.md
- INTERFACES.md

## 1) Purpose
Governance exists to prevent:
- unsafe self-modification
- drift in core contracts
- silent regressions in gates/sandbox
- "it worked once" non-reproducible changes

## 2) Roles (minimal)
### Maintainer (you)
- can approve protected/high-risk changes
- can change policy profiles
- owns releases/stable snapshots

### Worker (automation)
- executes tasks under policy
- cannot self-approve protected changes

### Reviewer (optional future)
- second human reviewer for high-risk changes

## 3) Approval Triggers (must approve)
Approval required if any is true:
- protected paths touched (see SECURITY.md)
- risk_score >= threshold
- patch size exceeds threshold
- migrations changed
- syscall or gate logic changed
- sandbox profile changes
- policy profile changes

## 4) Approval Artifact
Approvals must be explicit and recorded:
- stored under run folder (or via approvals syscall)
- referenced by gate_report.json
- includes: run_id, decision, reason, timestamp, approver identity

Decisions:
- APPROVE
- REJECT
- REQUEST_CHANGES

## 5) Debate Output
Debate is advisory only:
- debate_report.json can inform decisions
- it cannot override gate logic

## 6) Change Control Rules
- Any change to contracts/syscalls/gates requires:
  - golden tests updated or added
  - evidence reports updated if schema changes
  - migrations updated if needed

## 7) Stable Snapshot Definition
A "stable snapshot" is valid only if:
- passes full test suite (unit/integration/golden)
- security audit checklist passes
- migration docs updated (if needed)
- policy profiles validated

## 8) Exceptions
If an exception is needed:
- must be documented in approval artifact
- must include explicit risk statement
- must include a follow-up task to remove exception
```

---

## `docs/STYLE_GUIDE.md`

```md
# Documentation Style Guide

Purpose:
Keep docs consistent, skimmable, and cross-linkable for agents and humans.

## 1) File Naming
- UPPER_SNAKE_CASE for top-level canonical docs: CONSTITUTION.md, BOOTSTRAP_PLAN.md
- lower_snake_case is allowed for long optional docs, but be consistent.
- Avoid metaphors in filenames.

## 2) Headings
- Use `#` for title, then `##`, `###` progressively.
- Avoid deep nesting beyond `###` unless needed.

## 3) Cross-links
- Prefer relative links: `CONSTITUTION.md`, `../AGENTS.md`
- Every doc must include a `References:` section near the top linking to relevant canonical docs.

## 4) Definitions
- When introducing a term (e.g., "syscall", "gate", "lease"), define it once in:
  - INTERFACES.md or ARCHITECTURE.md
- Other docs should link back rather than re-defining differently.

## 5) Normative Language
Use strict language consistently:
- MUST / MUST NOT = non-negotiable
- SHOULD / SHOULD NOT = strong recommendation
- MAY = optional

## 6) Checklists
- Use checkboxes for audits and release steps.
- Ensure checklists have clear pass/fail criteria.

## 7) Examples
- Keep examples minimal and accurate.
- Prefer filesystem paths and artifact names that match ARCHITECTURE.md.

## 8) Compatibility Notes
If a doc changes a contract or artifact:
- update MIGRATIONS.md
- add a short "Compatibility" section describing impact

## 9) Agent Friendliness
- Put critical rules near top.
- Keep sections short (5–12 lines each).
- Avoid huge prose blocks.
```

---

## Bunlar “alışkanlık mı” sorusuna net cevap

Bu 4’ü:

* **THREAT_MODEL**: syscalls+sandbox tasarımını “neden böyle” diye sabitler (drift önler)
* **GOVERNANCE**: approval mekanizmasını netleştirir (gate ile uyum şart)
* **SECURITY_AUDIT_CHECKLIST**: stable snapshot çıkarmanın ölçütü (senin “stable version” hedefin için direkt gerekli)
* **STYLE_GUIDE**: agentin doküman üretirken formatı bozmaması için pratik

Yani bunlar “süs” değil; ama **minimal** tuttum ki bloat olmasın.

İstersen bir sonraki adım olarak (hala kod yazmadan) şunları da ekleyebilirim:

* `docs/GLOSSARY.md` (syscall, gate, lease, run, task, evidence vs tek yerde)
* `docs/POLICY_REFERENCE.md` (profiles alanlarının resmi şeması)
Evet—**tam olarak bu amaçla** yazıldı: agent bu dokümanları “spec” gibi okuyup, **BOOTSTRAP_PLAN sırasıyla** inşa edebilir. Ama bunun çalışması için iki şart var:

1. Dokümanlar **tek otorite** olmalı (CONSTITUTION + INTERFACES çakışma bırakmamalı)
2. Agentin “ne üreteceği” net olmalı: **repo tree + minimum artifact set + DoD** (hepsi var)

Aşağıya, agentin gerçekten “baka baka” build edebilmesini garantileyen iki eksik parçayı da (söz verdiğim gibi) **tam metin** yazıyorum: `GLOSSARY.md` ve `POLICY_REFERENCE.md`. Bunlar “okuyup uygulama”yı kolaylaştırır.

---

## `docs/GLOSSARY.md`

```md
# Glossary

References:
- INTERFACES.md
- ARCHITECTURE.md
- WORKFLOWS.md
- SECURITY.md

This glossary defines canonical terms. If a term is used differently elsewhere, this file wins.

## Agent
An automation that proposes plans, generates patches, runs verifications, and writes artifacts. Agents are untrusted by default.

## Approval
A human decision recorded as an artifact (or via approvals syscall) that allows protected/high-risk changes.

## Artifact
A file produced under `workspaces/<task_id>/runs/<run_id>/artifacts/` that serves as evidence:
- executor_report.json
- patch_apply_report.json
- verifier_report.json
- gate_report.json
Artifacts determine success.

## Candidate (Evolution)
A proposed patch generated by an evolution workflow. Candidates are evaluated but not auto-merged if high risk or protected paths are touched.

## Control-plane
The coordination layer stored in DB (SQLite by default). Contains tasks, runs, leases, workers. Not the source of truth for success.

## Data-plane
The filesystem evidence layer: immutable runs, artifacts, journals, approvals.

## Deterministic Gate
A routing/decision function that outputs PASS/BLOCK/REQUIRE_APPROVAL based only on:
- policy snapshot
- evidence artifacts

## Evidence
The collection of artifacts + journal events that proves what happened during a run.

## Gate Report
`gate_report.json` produced by gates/risk scoring. It references verifier results, policy snapshot, and approval state.

## Lease
A time-bound lock for multi-worker scheduling. A worker must hold a lease to execute a task.

## MCP (Model Context Protocol)
A server interface that exposes stable tools (task/run/lease/artifact/approve/migrate). MCP must call the same syscalls as CLI.

## Policy Profile
A YAML config in `configs/profiles/` that defines sandbox behavior, allowlists, protected paths, and gate thresholds.

## Protected Paths
High-sensitivity paths that require approval to modify, defined by policy.

## Run
A single execution attempt for a task, identified by run_id, with its own immutable run folder.

## Sandbox
A restricted execution environment (Docker by default) used by exec syscall.

## Syscall
A guarded operation API that is the only allowed way to mutate state (files, exec, git, approvals, migrations). Syscalls emit evidence + journal events.

## Task
A unit of work tracked by the control-plane DB and implemented via one or more runs.

## Verifier
A tool (ruff + pytest baseline) that produces `verifier_report.json` and determines pass/fail of lint/tests.
```

---

## `docs/POLICY_REFERENCE.md`

```md
# Policy Reference (Profiles Schema)

References:
- SECURITY.md
- CONSTITUTION.md
- INTERFACES.md

This document defines the canonical schema for `configs/profiles/*.yaml`.

## 1) Top-level fields
### profile (string)
Human-readable profile name. Example: "default", "strict".

### sandbox (object)
Controls execution isolation.
Fields:
- enabled (bool): must be true by default
- network (bool): must be false by default

Example:
sandbox:
  enabled: true
  network: false

### exec (object)
Controls command execution restrictions.
Fields:
- allowlist (list[string]): allowed executables/commands

Example:
exec:
  allowlist:
    - "python"
    - "pytest"
    - "ruff"
    - "git"

### paths (object)
Controls path security.
Fields:
- protected (list[string]): path prefixes that require approval

Example:
paths:
  protected:
    - "src/platform/syscalls/"
    - "src/platform/orchestrator/gates.py"

### gates (object)
Controls deterministic gate thresholds.
Fields (minimum):
- require_approval_on_protected_paths (bool)
- max_patch_lines_without_approval (int)
- require_verifier_pass (bool)

Example:
gates:
  require_approval_on_protected_paths: true
  max_patch_lines_without_approval: 400
  require_verifier_pass: true

## 2) Recording policy in runs
At run start, the active profile must be recorded as:
- a policy snapshot hash (preferred), or
- an embedded copy under artifacts/policy_snapshot.yaml

Gate decisions must reference this snapshot.

## 3) Default guarantees
Any valid profile MUST guarantee:
- sandbox enabled by default
- network disabled by default
- allowlist exists and is non-empty
- protected paths exists and is non-empty
- verifier pass required for success

## 4) Compatibility & migrations
If profile schema changes:
- increment schema_version in relevant artifacts
- document in MIGRATIONS.md
- add golden tests for gate behavior under the new schema
```

---

## Agent “baka baka” gerçekten inşa edebilsin diye son bir kilit nokta

Dokümanlar yeterli, ama agentin “nereden başlayacağını” otomatik anlaması için **BOOTSTRAP_PLAN zaten bunu söylüyor**. Pratikte agent şu şekilde çalışır:

* `AGENTS.md` → read order
* `docs/BOOTSTRAP_PLAN.md` → Task 01’den başlar
* Her task sonunda DoD’yi kanıtlayan artifact/test üretir
* `SECURITY_AUDIT_CHECKLIST.md` → stable snapshot kriteri

Bu, senin “stable sürüm üret, sonra diğer projeye naklet” planıyla birebir uyumlu.

İstersen bir sonraki adımda (hala kod yazmadan) **tek bir “Minimum Repo Tree”** dokümanı da ekleyeyim:

* `docs/REPO_TREE.md` (hangi klasör hangi aşamada oluşacak, boş placeholder dosyalar dahil)
  Bu, agentin scaffold aşamasında hiç düşünmeden doğru tree’yi yaratmasını sağlar.
Süper. O zaman “doküman paketi” tarafı kapanmış sayılabilir.

Senin yapacağın pratik adım (agent’a verince sıfır sürtünme olsun diye):

1. Repo kökünde şu dosyaları **kesin** koy:

* `AGENTS.md`
* `docs/AI_START_HERE.md`
* `docs/CONSTITUTION.md`
* `docs/BOOTSTRAP_PLAN.md`
* `docs/ARCHITECTURE.md`
* `docs/INTERFACES.md`
* `docs/WORKFLOWS.md`
* `docs/SECURITY.md`
* `docs/MIGRATIONS.md`
* `docs/TESTING.md`
* `docs/REPO_TREE.md`
* `docs/GLOSSARY.md`
* `docs/POLICY_REFERENCE.md`
* `docs/THREAT_MODEL.md`
* `docs/GOVERNANCE.md`
* `docs/SECURITY_AUDIT_CHECKLIST.md`
* `docs/STYLE_GUIDE.md`

2. Agent’a “tek cümle” görev:

> Read `AGENTS.md`, then execute `docs/BOOTSTRAP_PLAN.md` tasks in order. Do not write outside syscalls. Produce full evidence artifacts.

3. İlk stable snapshot kriteri:

* `SECURITY_AUDIT_CHECKLIST.md` full PASS
* Golden test PASS
* Policy snapshot recording PASS

Ne zaman istersen, bir sonraki aşamada **koda geçmeden önce** “BOOTSTRAP_PLAN içindeki Task 01–12 için Definition of Done’ları daha da mekanik” hale getirip (her task için *exact* artifact listesi + exact test adı + expected tree delta) agent’ın hata yapma ihtimalini daha da sıfıra yaklaştırırız.
Kısa cevap: **hayır, her framework’ü direkt vendora kurmuyoruz**.
Uzun ve net cevap aşağıda—**hangi framework, nereye, ne zaman** sorusunu kapatıyorum.

---

## 🔴 Kritik İlke (bunu sabitleyelim)

**Core = framework-free.**
Framework’ler **vendor** ya da **adapter/MCP** olarak yaşar.

> “Direkt çalışsınlar” isteği anlaşılır ama bu **ilk günden teknik borç** demek.

---

# 1) Şimdi (V0 / Bootstrap) – Kurulacak ÇEKİRDEK stack

Bunlar **framework değil**, altyapı bağımlılığı. Core’a girebilir.

### Zorunlu

* **Python 3.11+**
* **LangGraph** → orchestrator state machine
* **Pydantic v2** → contracts
* **Typer** → CLI
* **Ruff + Pytest + MyPy** → verifier
* **Docker** → sandbox
* **SQLite** → control-plane DB
* **MCP SDK** → external tool interface

👉 Bunlar **pip dependency** (pyproject.toml) olur. Vendor değil.

---

# 2) “Çalışmaya başlasın” dediğin araçlar (Aider, OpenHands, vb.)

Burada **en sık yapılan hatayı** özellikle düzeltiyorum.

## ❌ Yanlış yaklaşım

* Aider’i core’a embed etmek
* Kodunu kopyalayıp modify etmek
* “agent zaten kullanır” deyip doğrudan import etmek

## ✅ Doğru yaklaşım (senin mimariyle %100 uyumlu)

### A) Aider

* **Vendor:** `vendors/aider/` (ya da pip install)
* **Kullanım:**

  * ya **CLI tool** olarak (`exec.run(["aider", ...])`)
  * ya **MCP tool** (aider server varsa)
* **Core’da:** sadece `AiderAdapter`

> Core Aider’in *ne yaptığıyla* değil,
> **ne ürettiği artifact’lerle** ilgilenir.

### B) OpenHands / OpenDevin

* **Vendor**
* **Çalışma şekli:** ayrı process / worker
* **İletişim:** MCP veya file-based protocol
* **Core:** “task → run → verify → gate”

---

# 3) Vendor’a KUR ama AKTİF ETME (şimdilik)

Bunlar **hemen entegre edilmez**, ama repo’da durması mantıklı.

### Code / Dev Agents

* Aider
* OpenHands
* OpenDevin
* GPT-Pilot

📍 **Nereye:** `vendors/`
📍 **Ne zaman:** V2/V3’te adapter yazınca

---

# 4) Asla Core’a girmemesi gerekenler

Bunlar **kesin vendor + adapter** olmalı:

* CrewAI
* AutoGen
* MetaGPT
* Langroid
* SuperAGI
* BabyAGI

Sebep:

> Bunlar **kendi orchestrator’larını dayatır**.
> Senin sistemde **tek orchestrator var**: LangGraph.

---

# 5) RAG / Memory tarafı (kritik karar)

### Şimdi (V1)

* **Yok**. Bilerek yok.
* Dosya + artifact + run history = yeterli

### Sonra (V2)

* **LlamaIndex** veya **LangChain**
  → sadece adapter olarak
* Vector DB (Chroma/FAISS)
  → core dışı servis

---

# 6) Observability

### Şimdi

* JSONL logs
* run artifacts

### Sonra

* Langfuse (adapter)
* OpenTelemetry (adapter)

---

# 7) Önerilen NET framework matrisi

| Amaç          | Şimdi       | Vendor’da | Core’da |
| ------------- | ----------- | --------- | ------- |
| Orchestration | LangGraph   | ❌         | ✅       |
| Contracts     | Pydantic    | ❌         | ✅       |
| CLI           | Typer       | ❌         | ✅       |
| Verifier      | Ruff/Pytest | ❌         | ✅       |
| Sandbox       | Docker      | ❌         | ✅       |
| Aider         | ❌           | ✅         | Adapter |
| OpenHands     | ❌           | ✅         | Adapter |
| CrewAI        | ❌           | ✅         | Adapter |
| AutoGen       | ❌           | ✅         | Adapter |
| RAG           | ❌           | ❌         | ❌       |

---

# 8) Senin “direkt çalışsınlar” isteğine dürüst eleştiri

> “Frameworkleri kuralım, çalışmaya başlasınlar”

Bu refleks **agent-first** ama **OS-first değil**.
Sen OS yazıyorsun.

Eğer şimdi:

* Aider’i core’a sokarsan
* CrewAI’yi workflow’a bağlarsan

👉 3 ay sonra:

* migration kabusu
* gate’ler bypass edilir
* “stable snapshot” hayal olur

---

## 🔒 Son karar (benim net önerim)

1. **V0–V1:**

   * Sadece LangGraph + verifier + sandbox + syscalls
   * Vendor klasörü var ama **pasif**
2. **V2:**

   * AiderAdapter
   * OpenHandsAdapter
3. **V3:**

   * Multi-agent (CrewAI/AutoGen) ama **dıştan**
4. **V4:**

   * Self-evolution (candidate-only)

İstersen bir sonraki adımda:

* **AiderAdapter nasıl görünür?** (interface + artifact contract)
* **“Bir framework adapter yazma checklist’i”** (10 maddelik net kural)

Hangisini istersin?
Aynen: “aşırı temel” olan core’a, geri kalan vendor/adapters. Ama bunu sezgiyle değil **mekanik bir kural setiyle** ayırmak lazım ki agent da hata yapamasın. Aşağıdaki karar sistemiyle %95 netleşir.

---

## Core vs Vendor: Mekanik Ayrım Kuralları

### 1) Core’da ne olur?

Core’da sadece şu 5 şey olur (başka hiçbir şey değil):

1. **Contracts (data model)**

   * Task, Run, Evidence reports, Approval format, Policy snapshot format
2. **Syscalls (enforcement boundary)**

   * fs/apply_patch, exec.run, git.commit (kısıtlı), approvals, migrate
3. **Control-plane (coordination)**

   * task/run/lease/worker DB + state transitions
4. **Workflow orchestration (routing + gates)**

   * LangGraph nodes/edges, deterministic gates, risk scoring
5. **Evidence + journaling (source of truth)**

   * artifacts + jsonl logs üretimi, run folder layout

**Core = “otorite + koordinasyon + kanıt”**.

> Eğer bir şey çıkarıldığında sistem “hala güvenli ve deterministik” kalıyorsa, o şey core değildir.

---

### 2) Vendor’da ne olur?

Core dışındaki her “kabiliyet sağlayıcı” vendor/adapters tarafına gider:

* Codegen/coding agents: Aider, OpenHands, OpenDevin
* Multi-agent frameworks: CrewAI, AutoGen, MetaGPT…
* RAG/memory: LlamaIndex, LangChain, MemGPT…
* Observability: Langfuse, OTel exporters
* Workflow UI: Flowise, dashboard frameworkleri
* Her türlü “model provider” SDK’sı (OpenAI/Anthropic vs) bile tercihen adapter

**Vendor = “capability providers”**.

---

## “Aşırı temel” = Core’a girer mi? Evet ama şartlı

“Aşırı temel” olan bir şey core’a girer **ancak** şu 3 şart sağlanıyorsa:

1. **Interface-only**: core içinde sadece arayüz/kontrat var (implementasyon yok)
2. **Replaceable**: aynı interface’e uyan başka implementasyonla değişebilir
3. **Determinism-safe**: değişse bile gate/evidence mantığını bozmaz

Örnek:

* `Verifier` core’da **interface** olur; Ruff/Pytest implementasyonu adapter’dır (tercihen).
* Ama V1’de pratik olsun diye Ruff/Pytest’i core’a koymak istiyorsan: OK, fakat **Adapter pattern** ile yaz; core ruff’a bağlanmış kalmasın.

---

## Karar Ağacı (Agent’ın bile uygulayabileceği)

Bir bileşen için sırayla sor:

1. **Bu bileşen olmadan core hala task/run/evidence üretebiliyor mu?**

   * Evet → Vendor/Adapter
   * Hayır → 2’ye geç

2. **Bu bileşen “enforcement boundary” mi? (syscall/gate/policy/approval)**

   * Evet → Core
   * Hayır → 3’e geç

3. **Bu bileşen “coordination” mı? (DB leases/workers/task states)**

   * Evet → Core
   * Hayır → 4’e geç

4. **Bu bileşen üçüncü parti ve büyük mü?**

   * Evet → Vendor (core import etmez)
   * Hayır → 5’e geç

5. **Bu bileşen bir “capability provider” mı? (codegen, rag, research, ui)**

   * Evet → Adapter/Vendor
   * Hayır → Core (ama interface-first)

Bu kadar.

---

## Core İçin “Allowed Dependencies” Kuralı

Core’da dependency sayısını sınırlamazsan vendorlar içeri sızar.

**Core allowed deps (öneri):**

* pydantic (+settings)
* langgraph
* anyio/asyncio
* aiosqlite (control-plane)
* rich/typer (cli)
* stdlib

**Core NOT allowed:**

* crewai/autogen/metagpt/langroid
* llamaindex/langchain/memgpt
* langfuse/opentelemetry exporters
* devin-like systems

Bunlar adapter.

---

## Somut örnek: Aider nereye?

* **Aider core değil** çünkü:

  * enforcement boundary değil
  * coordination değil
  * capability provider
  * büyük ve değişebilir
    ✅ Vendor + `AiderAdapter` (core adapter interface’i çağırır)

---

## Somut örnek: Docker sandbox nereye?

* Docker “capability” gibi görünür ama senin sistemde **security boundary**.
* Boundary enforcement syscalls ile olur.
  ✅ Core’da: `exec.run` kuralı + policy
  ✅ Adapter/infra’da: docker runner implementasyonu (ister core altında `syscalls/exec_impls/` olarak, ister adapters altında)

---

## Repo’da nasıl görünür? (net yerleşim)

* Core:

  * `src/platform/contracts/`
  * `src/platform/syscalls/`
  * `src/platform/control_plane/`
  * `src/platform/orchestrator/`
  * `src/platform/data_plane/`
* Vendor:

  * `vendors/<tool>/` (read-only snapshot)
* Adapter:

  * `src/platform/adapters/<tool_adapter>/`

**Rule:** core hiçbir zaman `vendors/` içinden import etmez.

---

İstersen ben bunu dokümana da çivileyeyim:

* `docs/ARCHITECTURE.md` içine “Core vs Vendor Decision Policy” bölümü,
* `docs/INTERFACES.md` içine “Adapter contract template” bölümü.

Tek seferde yapıp “canonical” hale getirebilirim.
Evet—**doküman paketi “tamam”** sayılır. Şu an elinde agent’ın **baka baka repo’yu inşa edebileceği** minimum+gerekli set var.

“Tamam” derken kastım şu:

* **Ne yapacağız / neden / hangi sırayla** → var
* **Core sınırı + vendor/adapters kuralı** → var
* **Syscalls/gates/approvals/sandbox mantığı** → var
* **Repo tree + workspace/run layout** → var
* **Migration prensibi** → var
* **Security/Governance/Threat model** → var
* **Docs yazım standardı** → var

Eksik kalabilecek tek şey (istersen sonra ekleriz) “çok mekanik bootstrap görev listesi”:

* `BOOTSTRAP_PLAN.md` içindeki her adımın DoD’sini **tek tek** “hangi dosyalar değişecek + hangi test koşacak + hangi artifact oluşacak” şeklinde aşırı deterministik hale getirmek.

Ama doküman tarafında “grand spec set” artık hazır. Bundan sonra iş:

1. Bu dosyaları repo’ya koymak
2. Agent’a `AGENTS.md` üzerinden yürütmek
3. BOOTSTRAP task’larını gerçek kodla doldurmak

İstersen sıradaki adım olarak ben **BOOTSTRAP_PLAN.md için Task 00–12** şeklinde (scaffold → syscalls skeleton → gates skeleton → verifier skeleton → docker sandbox skeleton → CLI skeleton → MCP skeleton → migration skeleton) net bir görev listesi yazayım; bu artık “kod üretmeye” doğrudan başlatır.
