# YBIS Knowledge Bridge

This document serves as a bridge between the current YBIS architecture and the
massive historical knowledge base stored in `legacy/ybis_legacy/Knowledge`.

## 📚 Repository Overview

The legacy knowledge base contains 2400+ documents across several critical
domains:

- **Frameworks**: Deep dives into LiteLLM, AutoGen, LangChain, and custom YBIS
  plugins.
- **Architectures**: Historical design decisions for the Workforce and
  Infrastructure layers.
- **Protocols**: Original 'Adamakıllı' operational standards.

## 🔍 How to use this Knowledge (for AI Agents)

When faced with complex architectural questions or tool integrations, do not
guess. Consult the legacy knowledge using these steps:

1. **Identify Domain**: Determine if your task relates to `Workforce`
   (multi-agent), `Infrastructure` (Docker/MCP), or `Intelligence`
   (RAG/Prompting).
2. **Search Pattern**: Use `grep_search` or `find_by_name` within
   `legacy/ybis_legacy/Knowledge` using keywords from your task.
3. **Cross-Reference**: Compare legacy patterns with current implementations in
   `src/ybis`.
4. **Synthesize**: Adopt the _logic_ (the "why") from legacy while respecting
   the _cleaner structure_ (the "how") of the new system.

## ⚠️ Forbidden Zones

- **DO NOT** import code directly from `legacy/` into `src/ybis`.
- **DO NOT** modify anything within `legacy/`. It is a read-only archive for
  reference only.
- Violations will be caught by the **Sentinel Gate**.

---

_Reference this bridge whenever you need 'Industrial-Grade' context._
