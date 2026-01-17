# Local Coder Adapter

**Type:** Executor  
**Maturity:** Stable  
**Default Enabled:** Yes

## Overview

Local Coder is the default code executor for YBIS. It uses native Ollama models for code generation, editing, and error correction. It's designed to work entirely offline and is the recommended executor for local-first deployments.

## Features

- ✅ Native Ollama integration (no external API required)
- ✅ Code generation and file editing
- ✅ Error correction and retry logic
- ✅ Context-aware planning
- ✅ Local-first (no network required)

## Installation

Local Coder is enabled by default and requires no additional installation. It uses `litellm` for Ollama communication, which is included in core dependencies.

**Required:**
- Ollama installed and running locally
- At least one code model pulled (e.g., `ollama pull qwen2.5-coder:32b`)

## Configuration

### Policy Configuration

```yaml
# configs/profiles/default.yaml
adapters:
  local_coder:
    enabled: true  # Always enabled by default
```

### LLM Configuration

```yaml
# configs/profiles/default.yaml
llm:
  planner_model: "ollama/llama3.2:3b"  # Fast for planning
  coder_model: "ollama/qwen2.5-coder:32b"  # Strong for coding
  api_base: "http://localhost:11434"  # Ollama API base
```

## Usage

### Via Executor Registry

```python
from src.ybis.executors.registry import get_executor_registry
from src.ybis.contracts import RunContext, Plan

registry = get_executor_registry()
executor = registry.get_executor("local_coder")

ctx = RunContext(
    task_id="TASK-123",
    run_id="RUN-456",
    run_path=Path("workspaces/TASK-123/runs/RUN-456"),
)

plan = Plan(
    objective="Add user authentication",
    files=["src/auth.py"],
    instructions="Implement login and registration",
)

report = executor.generate_code(ctx, plan)
```

### Via Orchestrator

Local Coder is used automatically by the orchestrator when no other executor is specified:

```python
# Policy selects local_coder as default executor
# No explicit configuration needed
```

## Capabilities

- **Code Generation:** Generate new code files from scratch
- **File Editing:** Modify existing files based on instructions
- **Error Correction:** Fix errors from previous attempts
- **Context Awareness:** Uses plan and spec for better code generation

## Limitations

- Requires local Ollama installation
- Model quality depends on local model size
- No advanced editing features (like Aider's search/replace)

## Troubleshooting

### Ollama Not Running

**Error:** `Connection refused` or `Ollama not available`

**Solution:**
```bash
# Start Ollama
ollama serve

# Or check if running
curl http://localhost:11434/api/tags
```

### Model Not Found

**Error:** `Model not found`

**Solution:**
```bash
# Pull required models
ollama pull llama3.2:3b
ollama pull qwen2.5-coder:32b
```

### Slow Performance

**Solution:**
- Use smaller models for planning (`llama3.2:3b`)
- Use larger models only for coding (`qwen2.5-coder:32b`)
- Ensure sufficient RAM/GPU for model size

## See Also

- [Adapter Catalog](../../configs/adapters.yaml)
- [Executor Registry Guide](../ADAPTER_REGISTRY_GUIDE.md)
- [Policy Configuration](../../configs/profiles/default.yaml)


