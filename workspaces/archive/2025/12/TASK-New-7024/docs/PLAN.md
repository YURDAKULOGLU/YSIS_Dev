---
id: TASK-New-7024
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T00:20:00
target_files:
  - src/snake_game.py
  - src/snake_game_test.py
---

# Task: PROJECT-SNAKE-001 (Validation Test)

## Objective
Build a fully functional, terminal-based Snake game. This task serves as an end-to-end validation of the YBIS V5 architecture (LiteLLM, Langfuse, Code Graph).

## Approach
We will use the `UniversalLLMProvider` (via manual call in a script, mimicking an agent) to generate the game code.

## Steps
1.  **Generate Code:** Use `litellm_provider` to generate `src/snake_game.py`.
2.  **Generate Tests:** Use `litellm_provider` to generate `src/snake_game_test.py`.
3.  **Verify:** Run tests.
4.  **Execute:** Run the game (briefly) to confirm it works.

## Success Criteria
- [ ] `src/snake_game.py` exists and is playable.
- [ ] `src/snake_game_test.py` passes.
- [ ] Langfuse traces appear (if keys present).