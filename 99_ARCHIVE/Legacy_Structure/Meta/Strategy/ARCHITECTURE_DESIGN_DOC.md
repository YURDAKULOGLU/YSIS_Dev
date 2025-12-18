# YBIS Cloud-Native Architecture: "Dog Scales Dog"

**Version:** 0.1.0 (Draft)
**Status:** PROPOSED

## 1. Executive Summary
This document outlines the **Grand Unification** architecture for `.YBIS_Dev`. Instead of choosing one framework, we leverage the specific strengths of **LangGraph**, **CrewAI**, and **AutoGen** running on a **Dockerized** microservices foundation. The "Dog Scales Dog" pattern enables recursive self-scaling.

## 2. The Triad (Unified Frameworks)

### 2.1. The Spine: LangGraph (State & Control)
*   **Role:** The centralized State Machine and "Operating System" of the agent.
*   **Responsibility:**
    *   Maintains global `AgentState`.
    *   Defines execution cycles (Plan -> Execute -> Verify).
    *   Handles routing and error recovery (The "Safety Net").
    *   **Why:** Best-in-class for strict control flow and cycle management.

### 2.2. The Departments: CrewAI (Execution Teams)
*   **Role:** Specialized "Crews" for specific domains (Coding Crew, QA Crew, Strategy Crew).
*   **Responsibility:**
    *   Takes a clean objective from LangGraph.
    *   Executes multi-step processes using specific Roles (Worker -> Manager).
    *   **Why:** Best-in-class for defining Agent Personas and Hierarchical Tasks.

### 2.3. The Meeting Room: AutoGen (Dialogue & Negotiation)
*   **Role:** Dynamic problem-solving when requirements are ambiguous.
*   **Responsibility:**
    *   If CrewAI gets stuck, LangGraph routes to AutoGen.
    *   Simulates a conversation (e.g., "User" vs "Architect" vs "Developer").
    *   **Why:** Best-in-class for Conversational Patterns and self-correction through dialogue.

### 2.4. The Hands: Aider (Code Engineering)
*   **Role:** The "Surgeon" for file modifications.
*   **Responsibility:**
    *   Executed by CrewAI (Coding Agent) or LangGraph directly.
    *   Applies changes to the filesystem (Shadow or Real).
    *   Uses **git** for version control and undo capability.
    *   **Why:** Best-in-class for direct codebase manipulation and diff handling.

---

## 3. "Dog Scales Dog" (Recursive Architecture)

**The Concept:** A "Dog" (Parent Orchestrator) can spawn new "Scales" (Child Containers) to handle sub-tasks.

### 3.1. Infrastructure (Docker)
*   **`ybis-core`**: The main container running LangGraph (The "Dog").
*   **`ybis-worker-{id}`**: Ephemeral containers spawned for heavy lifting (The "Scales").
*   **Shared Memory**: `Redis` (Queue/Events) and `ChromaDB` (Vector Store).

### 3.2. Communications
*   **Inter-Container**: Redis Pub/Sub or HTTP (FastAPI).
*   **Human-in-the-Loop**: Aider Bridge (via CLI/Socket).

## 4. Implementation Stages

1.  **Stage 1: The Core (Docker)**
    *   Build `Dockerfile` for Python 3.12 + Frameworks.
    *   Setup `docker-compose.yml` with Redis/Chroma.

2.  **Stage 2: The Spine (LangGraph)**
    *   Migrate `state_unified.py` to LangGraph state.
    *   Port `orchestrator_unified.py` to `UnifedGraph` class.

3.  **Stage 3: The Integration**
    *   Wrap `Crew` execution as a LangGraph Node.
    *   Wrap `AutoGen` chat as a LangGraph Node.
