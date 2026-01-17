# YBIS Project Context & Capability Map

## 🧠 System Philosophy
"Steward OroYstein": A self-evolving organism that expands by assimilating external frameworks.
Do not reinvent the wheel. If an organ exists in `organs/`, use it.

## 🛠️ Available Organs (Frankenstein's Harvest)

### 1. Self-Evolution & Optimization
- **EvoAgentX** (`organs/EvoAgentX`)
  - *Purpose:* Autonomous agent evolution, feedback loops, and self-optimization.
  - *Docs:* `Knowledge/Frameworks/EvoAgentX`
- **Self-Improve-Swarms** (`organs/Self-Improve-Swarms`)
  - *Purpose:* Swarm intelligence for creating new tools and capabilities.
  - *Docs:* `Knowledge/Frameworks/Self-Improve-Swarms`
- **Poetiq ARC Solver** (`organs/poetiq-arc-agi-solver`)
  - *Purpose:* High-level reasoning and AGI-benchmark solving.
  - *Docs:* `Knowledge/Frameworks/Poetiq`

### 2. Execution & Coding
- **OpenHands** (`organs/OpenHands`)
  - *Purpose:* End-to-end software engineering agent. Docker-based execution.
  - *Docs:* `Knowledge/Frameworks/OpenHands`
- **DSPy** (`organs/dspy`)
  - *Purpose:* Programmable prompt optimization.
  - *Docs:* `Knowledge/Frameworks/DSPy`

### 3. Orchestration
- **LangGraph** (Integrated)
- **CrewAI** (Integrated via `src/agentic/crews`)

## 🔗 Bridge Locations
- **Poetiq:** `src/agentic/intelligence/poetiq_bridge.py`
- **OpenHands:** `src/agentic/core/executors/openhands_executor.py`
- **Orchestrator:** `src/orchestrator/runner.py`

## 🚨 Constitutional Rules for Expansion
1. **Docs First:** Before using an organ, read its documentation in `Knowledge/Frameworks`.
2. **Import, Don't Copy:** Import the organ's modules directly from `organs/`.
3. **Report Gaps:** If an organ is missing a feature, use `Self-Improve-Swarms` to build it.