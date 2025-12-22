# Postmortem — <TASK_ID / INCIDENT_ID>

Date: <YYYY-MM-DD>
Owner: <agent/human>
Status: Draft / Final

## 1) Summary
* What happened (1–3 sentences):
* Impact:
* Severity: Low / Medium / High / Critical
* Affected components:
* First detected at:
* Resolved at:

## 2) Failure Signature(s)
List all:
* `<SIGNATURE_1>`
* `<SIGNATURE_2>`

## 3) Context

### 3.1 Task Spec (original intent)
* Goal:
* Scope:
* Success criteria:

### 3.2 Environment
* OS:
* Python/Node versions:
* Provider/model used (from META.json):
* Sandbox/container digest (if any):
* Lockfile hash:

## 4) Timeline (UTC+03 or repo standard)
* T0: task started
* T1: plan produced
* T2: execution applied changes
* T3: sentinel failed
* T4: retry attempts
* T5: final outcome

## 5) What failed exactly?

### 5.1 Symptom
* Logs excerpt references (artifact paths, not raw dumps):
* Tests failing:
* Drift checks failing:

### 5.2 Root cause (single best explanation)
Choose one primary label:
* ROOT_CAUSE:TRUTH_DRIFT
* ROOT_CAUSE:PATH_DRIFT
* ROOT_CAUSE:SCOPE_DRIFT
* ROOT_CAUSE:DEPENDENCY_DRIFT
* ROOT_CAUSE:BEHAVIOR_DRIFT
* ROOT_CAUSE:EVIDENCE_DRIFT
* ROOT_CAUSE:TOOL_POLICY
* ROOT_CAUSE:MODEL_ROUTING
* ROOT_CAUSE:SANDBOX

Root cause explanation (clear + concrete):

## 6) Why was it not prevented earlier?
* Missing gate? (which one)
* Gate existed but misconfigured? (how)
* Signal existed but ignored? (why)

## 7) Resolution (what fixed it)
* Immediate fix:
* Verification that fix worked (test command + result):
* Evidence references (artifact paths):

## 8) Permanent Prevention Plan (the important part)
For each item, write: **Change → Where → How verified**

### 8.1 Policy changes
* Change:
* File/location:
* Verification (golden task / sentinel rule):

### 8.2 Sentinel / drift gate changes
* New check:
* Pattern/signature:
* Verification:

### 8.3 Golden tasks to add/update
* New/updated task:
* Expected signature:
* Why it prevents recurrence:

### 8.4 Prompt / workflow changes
* Prompt area (planner/executor/verifier/router):
* Change:
* Verification:

### 8.5 Repo hygiene / layout changes
* Move/delete/ignore:
* Why:
* Verification:

## 9) Follow-ups (action list)
| ID | Action | Owner | Priority | Due | Status |
| -- | ------ | ----- | -------- | --- | ------ |
| 1  |        |       | P0/P1/P2 |     |        |

## 10) Lessons learned (short)
* Lesson 1:
* Lesson 2:
* Lesson 3:

## 11) Links
* Artifact folder:
* Related ADR:
* Related PRs:
