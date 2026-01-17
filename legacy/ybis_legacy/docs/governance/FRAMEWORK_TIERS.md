# 🏗️ Framework Tiers & Governance

> **Standard v1.0**
> *Major organs require team consensus.*

---

## 1. TIER 1: INFRASTRUCTURE (The Organs)
*Requires Mandatory Debate + Council Vote.*
- **Definition:** Any library that changes the core execution flow, state management, or provider abstraction.
- **Examples:** LangGraph, LiteLLM, Cognee, Langfuse.
- **Protocol:**
  1. Start a Debate: `ybis.py debate start --topic "Add X"`.
  2. Council deliberation (minimum 24h).
  3. Consensus reached (Vote Score > 0).
  4. Implement with `FRAMEWORK_INTAKE.md`.

## 2. TIER 2: SKILLS & TOOLS (The Hands)
*Requires Architect Review (or silent approval if low risk).*
- **Definition:** Libraries added to `src/agentic/skills/` or `organs/` that don't affect the core loop.
- **Examples:** Tree-sitter, Pandas, Playwright, BeautifulSoup.
- **Protocol:**
  1. Fill `FRAMEWORK_INTAKE.md`.
  2. Architect approval.

## 3. TIER 3: UTILITIES (The Fingers)
*Auto-approved.*
- **Definition:** Pure utility libraries with zero external impact.
- **Examples:** Colorama, PyYAML, TQDM.

---

## ⚖️ Voting Rules
- **Council:** Multi-LLM consensus (Claude, Gemini, Codex).
- **Veto:** The Architect (User) has final veto power on any tier.
