# E2B Sandbox Adapter

**Type:** Sandbox  
**Maturity:** Stable  
**Default Enabled:** No (requires E2B API key)

## Overview

E2B Sandbox provides isolated cloud execution environments for code. It offers network access, persistent file systems, and secure isolation. Ideal for tasks requiring external API access or when local execution is not desired.

## Features

- ✅ Cloud-based isolation
- ✅ Network access (when enabled)
- ✅ Persistent file system
- ✅ Secure execution environment
- ✅ Automatic cleanup

## Installation

### Prerequisites

1. **E2B Account:** Sign up at https://e2b.dev
2. **API Key:** Get your API key from E2B dashboard
3. **Python Package:** Already included in dependencies (`e2b>=1.0.0`)

### Setup

```bash
# Set E2B API key
export E2B_API_KEY="your-api-key-here"
```

Or add to your environment configuration:
```yaml
# configs/profiles/default.yaml
# E2B API key should be set via environment variable
```

## Configuration

### Policy Configuration

```yaml
# configs/profiles/default.yaml
sandbox:
  enabled: true
  type: "e2b"  # Use E2B sandbox
  network: true  # Enable network access (optional)

adapters:
  e2b_sandbox:
    enabled: true  # Enable E2B adapter
```

### Environment Variables

```bash
export E2B_API_KEY="your-api-key"
export E2B_SANDBOX_TIMEOUT="300"  # Optional: timeout in seconds
```

## Usage

### Via Syscalls

E2B sandbox is used automatically by `exec()` syscall when:
- `sandbox.type` is set to `"e2b"` in policy
- `E2B_API_KEY` is set
- Network is allowed (if `sandbox.network: true`)

```python
from src.ybis.syscalls import exec as exec_syscall
from src.ybis.contracts import RunContext

ctx = RunContext(...)
result = exec_syscall(
    ["python", "script.py"],
    ctx,
    use_sandbox=True,  # Will use E2B if configured
)
```

### Direct Usage

```python
from src.ybis.adapters.e2b_sandbox import E2BSandboxAdapter
from src.ybis.contracts import RunContext

ctx = RunContext(...)

with E2BSandboxAdapter(ctx) as sandbox:
    result = sandbox.execute_command(
        "python script.py",
        cwd="/workspace"
    )
```

## Capabilities

- **Isolated Execution:** Code runs in cloud sandbox
- **Network Access:** Can make HTTP requests (if enabled)
- **File System:** Persistent storage during sandbox lifetime
- **Security:** Automatic cleanup and isolation

## Limitations

- Requires E2B API key (paid service)
- Network access must be explicitly enabled
- Sandbox creation has latency (~2-5 seconds)
- Cost per sandbox hour (check E2B pricing)

## Cost Considerations

- E2B charges per sandbox hour
- Sandboxes are automatically closed after task completion
- Consider using local execution for simple tasks

## Troubleshooting

### API Key Not Set

**Error:** `E2B_API_KEY not set`

**Solution:**
```bash
export E2B_API_KEY="your-api-key"
```

### Network Disabled

**Error:** Commands fail with network errors

**Solution:**
```yaml
# configs/profiles/default.yaml
sandbox:
  network: true  # Enable network access
```

### Sandbox Creation Failed

**Error:** `Failed to create sandbox`

**Solution:**
- Check E2B API key validity
- Verify E2B service status
- Check network connectivity
- Review E2B account limits

## Fallback Behavior

If E2B sandbox is unavailable or disabled, the system automatically falls back to local subprocess execution. This ensures tasks can always execute, even without E2B.

## See Also

- [Adapter Catalog](../../configs/adapters.yaml)
- [Sandbox Configuration](../../configs/profiles/default.yaml)
- [E2B Documentation](https://docs.e2b.dev)


