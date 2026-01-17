# Aider Executor Adapter

References:
- ../adapters/README.md
- ../../configs/adapters.yaml

**Type:** Executor Adapter  
**Maturity:** Experimental  
**Default Enabled:** No

## Overview
Aider provides LLM-assisted coding workflows as an executor.

## Installation
```bash
pip install -e ".[adapters-aider]"
```

## Configuration
```yaml
adapters:
  aider:
    enabled: true
executor:
  default: "aider"
```

## Notes
- Enable only when you want Aider-based execution.
- Requires model access configured via LLM settings.
