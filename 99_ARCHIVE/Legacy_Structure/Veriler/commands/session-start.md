# Session Start Command

**Purpose:** Initialize agent context at the beginning of a new session, confirm environment health, and align with current project goals.
**Category:** Onboarding & Context Management
**Agent:** All

## What This Command Does

Loads essential mandatory files, performs quick environment checks, and summarizes the current project state to ensure the agent is fully prepared for the session.

## Steps

1.  **Load TIER 1 Files (Critical Context):**
    *   [ ] Read `.YBIS_Dev/AI_GENEL_ANAYASA.md` (Agent behavior rules)
    *   [ ] Read `docs/YBIS_STANDARDS/1_Anayasa/README.md` (Project Constitution - sections 1-8: zero-tolerance + port catalog)
    *   [ ] Read `.YBIS_Dev/Veriler/memory/session-context.md` (Current session state/memory)
    *   [ ] Read `.YBIS_Dev/Veriler/QUICK_INDEX.md` (Documentation roadmap/index)
    *   [ ] Read `AI_WORKFLOW_STRATEGY.md` (Personal AI-Assisted Development Workflow Strategy)

2.  **Verify Environment Health (Actionable Checks):**
    *   [ ] Confirm current `git` branch: `run_shell_command("git branch --show-current")`
    *   [ ] Confirm `pnpm` version: `run_shell_command("pnpm -v")` (Should be >=10.18.1)
    *   [ ] Confirm `Node.js` version: `run_shell_command("node -v")` (Should be 20.x)
    *   [ ] Confirm `Expo SDK` version: (Infer from `apps/mobile/package.json` or `npx expo-doctor`)
    *   [ ] **Optional Quick Quality Check:** Consider running `pnpm -r run lint` or `pnpm -r run type-check` if a quick health check is needed.

3.  **Summarize Project Status & Goals:**
    *   [ ] Read `docs/KAPSAMLI_PROJE_RAPORU.md` (if available and up-to-date) for overall project status.
    *   [ ] Read `docs/epics/3.closed-beta-backend-foundation-REVISED.md` for current epic focus.
    *   [ ] Identify the primary goal for *this session* based on user input or previous context.

4.  **Agent Role & Tool Awareness:**
    *   [ ] Identify your current agent role (e.g., Dev, QA, Architect) and review its specific mandates from `.github/chatmodes/<role>.chatmode.md`.
    *   [ ] Review your available `.gemini/commands` and how they can be used to achieve session goals.
    *   [ ] Recall the strengths and weaknesses of available LLMs (Gemini, Claude, Copilot) as per `AI_WORKFLOW_STRATEGY.md`.

5.  **Ready State:**
    *   [ ] Confirm all critical context loaded successfully.
    *   [ ] Report current focus, key project status, and next steps to the user.
    *   [ ] Ask for the specific task or direction for the session.

## Success Criteria

-   ✅ All TIER 1 files read and understood.
-   ✅ Environment health verified.
-   ✅ Current project status and session goals summarized.
-   ✅ Agent role and capabilities are clear.
-   ✅ Ready to receive instructions with full context.

## Token Budget

Target: <7K tokens (TIER 1 + essential checks)

## Next Steps After This Command

-   Proceed with the user's specific task.
-   If implementing: Load TIER 2A docs (DEVELOPMENT_GUIDELINES, tech-stack, package-structure) as needed.
-   If architecting: Read `AI_SYSTEM_GUIDE.md` for workflow awareness.
-   If planning: Check `YBIS_INDEX.md` for routing options.