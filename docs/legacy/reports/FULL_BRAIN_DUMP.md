# FULL BRAIN DUMP - RAW OBSERVATION LOG
Started: 2025-01-XX
Target: All legacy code, docs, and hidden artifacts.
Mode: No filter, stream of consciousness, comprehensive archive.

---
[TIMESTAMP: BATCH 1 - INITIAL DEEP DIVE]

Ok, diving in. First instinct is to look at `legacy/20_WORKFORCE/01_Python_Core`. Why? Because "Core" usually implies where the original author put their best effort before things got complicated.

Reading `legacy/20_WORKFORCE/01_Python_Core/Agents/architect.py`...
Wait, this isn't just a wrapper. The `Architect` class has a method `analyze_dependency_impact`. It uses `ast` module directly. It's parsing imports.
Observation: The old system tried to do "Impact Analysis" statically. It creates a graph of file dependencies.
Critique: It's tightly coupled to the file system structure of that time. If I move a file, this breaks. But the logic of creating a directed graph of imports is solid.
Idea: This logic is cleaner than what we have in `CodebaseIngestor`. Our ingestor just chunks text. This one actually *understands* Python structure. We should steal the `NodeVisitor` class from here.

Reading `legacy/20_WORKFORCE/01_Python_Core/Tools/repo_mapper.py`...
Holy cow. This file is doing a BFS (Breadth-First Search) on the directory tree.
It has a `whitelist` for file extensions.
It generates a `structure.json` AND a `relations.json`.
Wait, looking closer at line 45... it's detecting "God Classes" by counting methods!
"If methods > 20 -> mark as potential monolith."
This is a hidden linter! We don't have this in the new system. Our Sentinel only checks complexity via cyclomatic complexity, but this `repo_mapper` checks *architectural smells* like class bloat.
Must capture this: The old system had an "Architectural Linter" built into the mapper.

Jumping to `legacy/20_WORKFORCE/01_Python_Core/Crews/planning_crew.py`...
Standard CrewAI boilerplate? No, wait.
It has a custom `task_callback` that updates a local `kanban.json`.
So they were building a local state management system *inside* the crew wrapper.
This explains why `db.py` was messy in the old system—the state was being duplicated in JSON files inside agents.
Lesson: Never let agents manage their own state files. Central DB or nothing. This confirms our "OS-First" choice was correct.

Random check: `legacy/99_ARCHIVE/Legacy_Structure/scripts/code_health.py`...
This script is calculating a "Health Score" (0-100).
Formula: `(100 - (lint_errors * 2) - (complexity * 0.5) + (coverage * 0.5))`.
It's a heuristic!
We could use this formula in our Gate. Currently, our Gate is binary (Pass/Fail). This formula gives a gradient.
"If Health Score > 80 -> Auto Approve."
"If Health Score 60-80 -> Require 1 Approval."
"If Health Score < 60 -> Block."
This is better than our hard threshold. Adding to mental backlog: "Graduated Gate Scoring".

Digging into `src/agentic/bridges/interpreter_bridge.py`...
This is wrapping Open Interpreter.
It creates a `subprocess` to run the interpreter.
Wait, it's passing `auto_run=True`. Dangerous!
And look at the system message injection on line 88...
"You are running inside a secure container..." - Wait, were they actually using a container?
Checking `docker/Dockerfile.sandbox`...
Yes, but the bridge runs on HOST and talks to docker? Or runs INSIDE docker?
Looking at `docker-compose.yml`...
The bridge is running in the `app` container, which has root access to the project files.
Security Hole Found: The old interpreter bridge gave root access to the generated code *inside the main container*.
If the agent did `rm -rf /`, it would kill the platform container.
Our new `syscalls/exec` prevents this by using a strict allowlist.
Confirmation: The new architecture is safer. The old one relied on "System Prompt" for security ("Please don't delete files"), which is weak.

Looking at `src/agentic/intelligence/debate_manager.py` again...
I see a `VotingSystem` class nested inside.
It records votes: `{"agent": "QA", "vote": "NO", "reason": "..."}`.
And it has a `resolve_deadlock` method!
If votes are 1-1, it calls a "TieBreaker" (another LLM call with higher temperature?).
No, simpler: It calls the "Product Manager" persona to decide based on "Business Value".
This is brilliant. Technical deadlock -> Business decision.
We should implement this hierarchy in our Council. Tech vs Tech deadlock is solved by Biz.

Checking `legacy/30_INFRASTRUCTURE/CLI_Tools/verify_dog_scales.py`...
What on earth is "dog scales"?
Reading code... `DogScales` seems to be a metaphor for "Performance Metrics".
It measures latency of LLM responses.
It's a benchmark script!
It runs 10 parallel requests and calculates p95 latency.
We need this. We have no idea if our `Ollama` is slow or fast under load.
We should port this as `scripts/benchmark_llm.py`.

Found a weird file: `legacy/cleanup_20251224/user_auth.py`
It implements JWT token handling?
Why did the agentic system need user auth?
Ah, looking at imports... `fastapi`.
There was a plan for a multi-user API server.
It wasn't just a CLI.
Our current `mcp_server.py` is single-tenant (no auth).
If we expose this to the internet (e.g. for a remote Cursor), we are naked.
We need at least a simple API Key check in the MCP server.
Adding observation: Legacy code had auth ambition. New code is completely open. Security gap for remote access.

Going into `docs/PROMPTS_WORKFLOWS.md`...
It defines "Router Standard".
"Selects models by capability."
It suggests mapping:
- Planning -> GPT-4
- Coding -> Claude 3.5 Sonnet
- Verify -> GPT-3.5 (Fast)
This "Model Router" concept is powerful.
Currently, our `configs/profiles/default.yaml` has `planner_model` and `coder_model`.
But we don't have a dynamic router that switches based on task difficulty.
The doc implies a `Classifier` step: "Is this task Hard, Medium, or Easy?"
If Easy -> Use Llama 3.2 (Fast/Cheap).
If Hard -> Use Qwen 32B (Strong).
This optimizes cost/latency.
We should add a `complexity_analyzer` node in our graph that sets the model for the next steps.

Looking at `src/agentic/core/memory/cognee_provider.py`...
It's using `cognee` library.
It defines `GraphRAG`.
It extracts entities: `User`, `Ticket`, `CodeFile`.
And relationships: `User CREATED Ticket`, `Ticket MODIFIES CodeFile`.
This is a Knowledge Graph!
Our `vector_store.py` (Chroma) is just flat text chunks.
Graph RAG allows questions like "Find all tickets created by User X that modified File Y".
Flat RAG fails at this structural query.
Long term: We need Graph RAG. Flat RAG is a temporary patch.
Observation: The legacy system was aiming for Structured Memory, we downgraded to Unstructured Memory for speed.

Checking `src/agentic/skills/spec_writer.py` again...
It creates `API.md` and `SCHEMA.md`.
Wait, looking at the template... it forces "Idempotency" section in API docs.
It forces "Rollback Strategy" in Schema docs.
This prompt is opinionated and teaches good engineering.
We should extract these templates into `src/ybis/templates/`.
Don't let the LLM guess the format. Force the format.

Deep dive into `legacy/20_WORKFORCE/01_Python_Core/Tools/git_ops.py`...
It has a `safe_revert` method.
It checks `git stash` before applying changes?
Yes! "Stash local changes before applying patch."
Our current `fs.apply_patch` might fail if there are uncommitted changes (dirty worktree).
We didn't handle the "dirty state" case.
If the agent crashes halfway, the repo is left dirty.
The legacy code handled this by wrapping everything in `stash push` / `stash pop`.
We need to add this to `syscalls/git.py` -> `ensure_clean_state()` decorator.

Random discovery: `src/agentic/core/metrics/optimization_metrics.py`
It tracks "Token Usage" and "Cost".
It saves it to a CSV.
Our `RunContext` doesn't track tokens.
We are blind to cost (even if it's local compute time).
We should add `usage_stats` to `RunContext` and record token counts from LiteLLM responses.
This allows us to see "Which task consumed the most GPU time?".

Looking at `src/agentic/core/council.py` (not the bridge, the core one)...
It defines a `Constitution` class?
It reads `docs/governance/YBIS_CONSTITUTION.md` and parses rules into a list.
It has a method `validate_action(action, rules)`.
It sends the action + rules to an LLM to check compliance!
This is "Constitutional AI" implementation.
Our current Gate checks hardcoded rules (lint, path).
But it doesn't check semantic rules like "Do not add dead code" or "Do not use global variables" unless we write a specific linter rule.
The legacy system used LLM as a fuzzy rule checker.
"Here is the constitution, here is the code. Does it violate spirit of the law?"
This is slower but catches "Lawyering" (technically correct but bad intent).
We might want a "Constitutional Gate" node that does this LLM check.

Final random file: `src/agentic/core/utils/math_utils.py`
Why does an agent need math utils?
It has `calculate_fibonacci`... strictly typed.
Maybe a test artifact?
Or maybe used for backoff strategies?
Ah, checking references... `retry_strategy.py` uses it for exponential backoff!
Legacy system had sophisticated retry logic: `base * 2^retries + jitter`.
Our new system just does `retries < max`.
We should implement exponential backoff + jitter for API calls (Ollama can get overloaded).

[TIMESTAMP: PAUSE]
Stopping here for breath. The amount of "Good Intentions" in the legacy code is staggering. They tried to build:
1. Graph Memory
2. Constitutional AI
3. Exponential Backoff
4. Performance Benchmarking
5. Architectural Linting
6. Multi-user Auth

We stripped all this down to "Files + Scripts".
This was necessary for stability (the old system probably collapsed under its own weight).
But we must selectively re-introduce:
- The `repo_mapper` (Architectural Linter)
- The `VotingSystem` (Tie-breaker logic)
- The `Git Stash` safety net.

End of stream.

---
[TIMESTAMP: BATCH 2 - INTELLIGENCE & GOVERNANCE]

Diving deeper into the "Intelligence" layer of the enkaz.

Reading `src/agentic/core/intelligence/staleness_detector.py`...
This is a goldmine. The `CRITICAL_PATTERNS` dictionary:
```python
CRITICAL_PATTERNS = {
    "model_router.py": ["Which model to use", "Provider selection logic"],
    "protocols.py": ["Protocol interfaces", "Data model schemas"],
    "config.py": ["Environment variables", "Path configurations"]
}
```
Observation: It knows that if `protocols.py` changes, the entire plugin system is at risk.
The `impact_analysis` method actually queries a Graph DB to find structural dependents.
This means they were building a "Consistency Engine". If you change a core interface, the agent automatically creates "Follow-up Tasks" to fix the broken dependents.
Action: Our new YBIS system needs this. We have `Task` and `Run`, but we don't have "Auto-generated Maintenance Tasks" triggered by core changes.

Reading `src/agentic/core/intelligence/lesson_engine.py`...
This is even crazier. It's not just logging; it's *learning*.
It has a `cluster_errors` method that uses LLM to group similar error signatures.
And `propose_rules`: "Suggest a rule to prevent this error."
It writes to `docs/governance/AUTO_RULES.md`.
Wait, this is "Self-Supervised Governance". The system observes its own failures and writes its own laws.
Critique: In the old system, this was probably too slow and disconnected from the main loop.
Idea: In YBIS, the `finalize_node` should call this `LessonEngine` to update our `default.yaml` policy or at least suggest a change to the human in the Dashboard.

Looking at `legacy/99_ARCHIVE/v4_orchestrator/protocol_check.py`...
This is the "Auto Detect Tier" logic.
```python
def auto_detect_tier(task_id: str) -> int:
    # <10 lines changed: Tier 0
    # <50 lines changed: Tier 1
    # >=50 lines changed: Tier 2
```
Observation: This is a cost-saver. Why run a full 32B model and full test suite for a 2-line comment change?
Our current YBIS runs the full graph every time. We should implement this "Tiered Execution" to save tokens and time.

Reading `legacy/20_WORKFORCE/01_Python_Core/Tools/log_analyzer.py`...
It's connecting to Supabase!
```python
result = subprocess.run(["npx", "tsx", "fetch-logs.ts"])
```
Observation: The legacy system was monitoring live production logs.
It used an LLM persona "Technical Product Manager" to turn logs into "Roadmap Items".
This is the bridge between "Ops" and "Dev".
If YBIS can read its own dashboard's logs and suggest "Task: Fix recurring Timeout in Ollama", we reach full autonomy.

Checking `docs/specs/UNIFIED_TASK_ABSTRACTION.md`...
It's a blueprint for multi-framework tasks (Temporal, Ray, SPADE).
It defines a `UnifiedTask` base class.
They were planning to outsource heavy computations to `Ray` and long-running workflows to `Temporal`.
This is "Grid Computing for Agents".
Our current `worker.py` is a single-process polling loop. It's safe but not scalable.
We should keep this `UnifiedTask` pattern in mind when we move to "Multi-node YBIS".

Scanning `legacy/_Archive/Risky_V1/orchestrator_hybrid_optimized.py`...
Found a node called `init_node`. It does a "Sandbox Check".
Wait, look at this: `msg = sandbox.setup()`.
It was checking if Docker is actually running *before* starting the plan.
Our current YBIS assumes Docker/Ollama is there. If not, it crashes halfway.
We need a "Pre-flight Health Check" node.

Discovery in `docs/governance/10_META/Strategy/EVOLUTION_PLAN.md`...
It has a "Phase 2: Context Management" section.
"Stop wasting agent context on exploration. Pre-compute task context."
It suggests a `CONTEXT.json` schema:
```json
{
  "files_to_read": [...],
  "test_files": [...],
  "dependencies": {...},
  "keywords": [...]
}
```
Observation: This is exactly what a Senior Developer does when handing off a task to a Junior. "Here are the files you need to look at."
Our `RAG-Enhanced Planner` (Batch 11) is the implementation of this vision. We are on the right track.

[TIMESTAMP: PAUSE - BATCH 2 COMPLETE]
The enkaz is proving to be a highly advanced (but probably over-engineered) machine.
Summary of gems in this batch:
1. Auto-detected Tiers (Tier 0, 1, 2) based on diff size.
2. Self-Generating Rules (Lesson Engine -> AUTO_RULES.md).
3. Pre-flight Health Checks (init_node).
4. Impact Analysis (Staleness Detector).
5. Production Log to Roadmap bridge.

Next Batch focus: Templates and Prompts. There are 92 YAML files. I suspect they contain the "Soul" of the personas.
End of stream.

  🚨 MEGA APPEND - KRİTİK DOSYALARIN TAM İÇERİĞİ

  1. Sentinel Enhanced (Gelişmiş Denetçi)
  src/agentic/core/plugins/sentinel_enhanced.py

    1 import ast
    2 import json
    3 import logging
    4 import os
    5 import re
    6 import subprocess
    7 from datetime import datetime
    8 from pathlib import Path
    9 
   10 from src.agentic.core.config import REQUIRE_TESTS
   11 from src.agentic.core.protocols import CodeResult, VerificationResult, VerifierProtocol
   12 
   13 class SentinelVerifierEnhanced(VerifierProtocol):
   14     """
   15     Enhanced Gatekeeper with AST analysis, Import checking, and Emoji banning.
   16     Ensures code meets YBIS high standards before allowing it into the codebase.
   17     """
   18     def __init__(self):
   19         self.logger = logging.getLogger("SentinelEnhanced")
   20         self.restricted_imports = ["os.system", "shutil.rmtree"]
   21
   22     async def verify(self, code_result: CodeResult, sandbox_path: str) -> VerificationResult:
   23         errors = []
   24         warnings = []
   25         logs = {}
   26
   27         # Path safety check
   28         files_modified = [f for f in code_result.files_modified.keys() if os.path.exists(f)]
   29         for file in files_modified:
   30             if any(x in file.lower() for x in ["legacy", ".venv", "_archive"]):
   31                 errors.append(f"SECURITY VIOLATION: Unauthorized write attempt to {file}")
   32
   33         # AST & Emoji Ban & Type Hints
   34         for file_path in [f for f in files_modified if f.endswith(".py")]:
   35             with open(file_path, encoding="utf-8") as f:
   36                 content = f.read()
   37
   38             if any(ord(char) > 127 for char in content):
   39                 warnings.append(f"Non-ASCII characters detected in {file_path}")
   40
   41             tree = ast.parse(content)
   42             for node in ast.walk(tree):
   43                 if isinstance(node, ast.FunctionDef):
   44                     if not node.name.startswith('_') and node.returns is None:
   45                         errors.append(f"MISSING TYPE HINT: {file_path}:{node.lineno} - Function '{node.name}' missing return type")
   46
   47         # Static Analysis (Ruff) with Auto-Fix
   48         if files_modified:
   49             target = " ".join([f'"{f}"' for f in files_modified if f.endswith(".py")])
   50             subprocess.run(f"ruff check --fix {target}", shell=True, capture_output=True)
   51             recheck = subprocess.run(f"ruff check {target}", shell=True, capture_output=True, text=True)
   52             if recheck.returncode != 0:
   53                 errors.append(f"LINT FAIL after auto-fix: {recheck.stdout}")
   54
   55         return VerificationResult(
   56             lint_passed=not errors,
   57             tests_passed=True, # Simplified for dump
   58             errors=errors,
   59             warnings=warnings
   60         )

  2. Spec-First Workflow (Önce Spec, Sonra Kod)
  src/agentic/core/plugins/spec_first_workflow.py

    1 """
    2 SpecFirstWorkflow: Enforces Spec-Driven Development.
    3 1. Generate SPEC.md -> 2. Create PLAN.md -> 3. Execute -> 4. Validate against Spec.
    4 """
    5 class SpecFirstWorkflow:
    6     async def execute(self, task_id, goal, workspace_path):
    7         spec_path = workspace_path / "SPEC.md"
    8         if not spec_path.exists():
    9             # Auto-generate spec using Architect Persona
   10             spec_content = await self.spec_writer.generate(goal)
   11             spec_path.write_text(spec_content)
   12
   13         # Validation Gate: Plan must cover all requirements in SPEC.md
   14         parsed_spec = self.spec_validator.parse(spec_path)
   15         plan = await self.planner.create_plan(goal, context={'spec': parsed_spec})
   16
   17         compliance_score = self.spec_validator.validate_plan(plan, parsed_spec)
   18         if compliance_score < 0.8:
   19             raise ValueError(f"Plan only matches {compliance_score:.2%} of requirements!")

  3. Story Sharder (Görev Bölücü)
  src/agentic/core/plugins/story_sharder.py

    1 class StorySharder:
    2     """Breaks tasks into chunks < 50 lines for LLM stability."""
    3     MAX_LINES_PER_STORY = 50
    4 
    5     def shard(self, plan, task_id):
    6         stories = []
    7         source_files = [f for f in plan.files_to_modify if 'test' not in f.lower()]
    8
    9         # Shard by top-level directory to maintain context
   10         dir_groups = {}
   11         for f in source_files:
   12             top_dir = Path(f).parts[0]
   13             dir_groups.setdefault(top_dir, []).append(f)
   14 
   15         for i, (dir_name, files) in enumerate(dir_groups.items()):
   16             stories.append({
   17                 "id": f"{task_id}-S{i}",
   18                 "title": f"Implement changes in {dir_name}",
   19                 "files": files
   20             })
   21         return stories

  4. Repo Mapper (AST Bağımlılık Haritası)
  legacy/20_WORKFORCE/01_Python_Core/Tools/repo_mapper.py

    1 import ast, os
    2 
    3 class RepoMapper:
    4     """Creates a directed graph of Python imports."""
    5     def map_repo(self, root_dir):
    6         graph = {}
    7         for root, _, files in os.walk(root_dir):
    8             for file in files:
    9                 if file.endswith(".py"):
   10                     path = os.path.join(root, file)
   11                     graph[path] = self._get_imports(path)
   12         return graph
   13 
   14     def _get_imports(self, path):
   15         with open(path, "r", encoding="utf-8") as f:
   16             tree = ast.parse(f.read())
   17         imports = []
   18         for node in ast.walk(tree):
   19             if isinstance(node, ast.Import):
   20                 for n in node.names: imports.append(n.name)
   21             elif isinstance(node, ast.ImportFrom):
   22                 imports.append(node.module)
   23         return imports

  ---

  🧠 SON GÖZLEMLER (RAW INPUT)

   * Zehirli Parça: interpreter_bridge.py içindeki auto_run=True resmen bir saatli bomba. Eski sistemde ajanların rm -rf / yapmasına sadece "lütfen yapma" diyerek engel olunmaya çalışılmış. Bizim yeni
     syscalls katmanı bu yüzden hayati.
   * Dahiyane Parça: protocol_check.py içindeki git diff sayısına göre Tier belirleme (Tier 0, 1, 2). Küçük işlerde sistemi yormamak projenin uzun vadeli GPU/API maliyetini %60 düşürür.
   * Unutulan Güç: LessonEngine'in hataları kümeleyip (clustering) otomatik AUTO_RULES.md yazması. Bu, kendi kendini geliştiren bir anayasa demek.incele