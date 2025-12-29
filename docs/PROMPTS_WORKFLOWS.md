# PROMPTS AND WORKFLOWS

## Purpose
Define standard planner/executor/verifier/router expectations and how workflows are selected.

## Workflow Registry
- Source of truth: workflow-registry.yaml
- Default workflow: orchestrator_spine_v1
 - MCP 2025-11-25 async ops should be implemented in mcp_server as follow-up.

## Planner Standard
- Inputs: task description + context
- Output: Plan schema (objective, steps, files_to_modify, risks, success_criteria)
- Must return valid JSON matching Plan model.

## Executor Standard
- Inputs: Plan + sandbox/workspace path
- Output: CodeResult with files_modified and commands_run
- Must only touch allowed directories.

## Verifier Standard
- Inputs: CodeResult + workspace
- Output: VerificationResult with lint/tests/coverage
- Failures must include actionable errors.

## Router Standard
- Selects models by capability (planning/coding/verify)
- Avoids single-provider lock-in

## Required Artifacts
- PLAN.md, RUNBOOK.md, EVIDENCE/*, CHANGES/*, META.json
