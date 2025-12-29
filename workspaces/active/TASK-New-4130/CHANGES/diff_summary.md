# Diff Summary

- Added manual provider abstraction (BaseProvider + ProviderCapabilities).
- Implemented OllamaProvider with httpx.
- Added ProviderFactory with fallback chain and provider mode flags.
- Wired run_orchestrator planner selection via provider mode.
- Updated Stable vNext roadmap with provider mode flags.
