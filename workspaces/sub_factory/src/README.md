# 🏗️ Source Code Map

> **Zone:** Production Code
> **Access:** Builders & Architects

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| **`agentic/`** | **The Backend.** Contains the Brain (Graph), Logic (Core), and Plugins. |
| **`dashboard/`** | **The Frontend.** Streamlit/Flask apps for monitoring the system. |
| **`utils/`** | **Shared Tools.** Common functions used by both backend and frontend. |

## Rules
- **No Circular Imports:** `agentic` should not import from `dashboard`.
- **Statelessness:** Code here should be mostly stateless. State lives in `Knowledge/LocalDB`.
