# T-102 (P0) Plugin Architecture Core + Infrastructure

**Context:** All tools (LangChain, MCP, Aider, CrewAI) are currently hard-coded. Need plugin architecture for flexibility.

**Constraint:** Free & open-source only (see ARCHITECTURE_PRINCIPLES.md)

**Goal:** Build minimal plugin core (<500 lines) and integrate observability/LLM proxy.

---

## Strategic Vision

**Current (hard-coded):**
```python
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.aider_executor import AiderExecutor

planner = SimplePlanner()
executor = AiderExecutor()
```

**Target (plugin-based):**
```python
from src.agentic.core.plugin_system import ToolRegistry

planner = ToolRegistry.get("@llm/planner")
executor = ToolRegistry.get("@tools/aider")
calculator = ToolRegistry.get("@math/calculator")
```

---

## Architecture

### Component 1: ToolProtocol (Interface)

**File:** `src/agentic/core/plugin_system/protocol.py`

```python
from typing import Protocol, Any, Dict
from dataclasses import dataclass

@dataclass
class ToolMetadata:
    name: str                    # e.g., "@math/calculator"
    description: str             # Human-readable
    deterministic: bool          # True if same input = same output
    cost_per_invocation: float  # 0.0 for local tools
    parameters_schema: Dict      # JSON Schema

class ToolProtocol(Protocol):
    """Universal tool interface - all plugins implement this"""

    @property
    def metadata(self) -> ToolMetadata:
        """Tool metadata"""
        ...

    async def invoke(self, **kwargs) -> Any:
        """Execute the tool"""
        ...

    async def validate_params(self, **kwargs) -> bool:
        """Check if parameters are valid"""
        ...
```

---

### Component 2: ToolRegistry (Central Hub)

**File:** `src/agentic/core/plugin_system/registry.py`

```python
from typing import Dict, Optional
from .protocol import ToolProtocol, ToolMetadata

class ToolRegistry:
    """Central registry for all tools"""

    _tools: Dict[str, ToolProtocol] = {}

    @classmethod
    def register(cls, tool: ToolProtocol):
        """Register a tool"""
        name = tool.metadata.name
        if name in cls._tools:
            raise ValueError(f"Tool {name} already registered")
        cls._tools[name] = tool
        print(f"[Registry] Registered: {name}")

    @classmethod
    def get(cls, name: str) -> Optional[ToolProtocol]:
        """Get tool by name"""
        return cls._tools.get(name)

    @classmethod
    def list_tools(cls, deterministic_only: bool = False) -> List[ToolMetadata]:
        """List all registered tools"""
        tools = cls._tools.values()
        if deterministic_only:
            tools = [t for t in tools if t.metadata.deterministic]
        return [t.metadata for t in tools]

    @classmethod
    async def invoke(cls, name: str, **kwargs) -> Any:
        """Invoke tool by name (with observability)"""
        tool = cls.get(name)
        if not tool:
            raise ValueError(f"Tool {name} not found")

        # Validate parameters
        if not await tool.validate_params(**kwargs):
            raise ValueError(f"Invalid parameters for {name}")

        # Execute (traced by decorator)
        return await tool.invoke(**kwargs)
```

---

### Component 3: PluginLoader (Auto-Discovery)

**File:** `src/agentic/core/plugin_system/loader.py`

```python
import importlib
import pkgutil
from pathlib import Path
from .protocol import ToolProtocol
from .registry import ToolRegistry

class PluginLoader:
    """Auto-discover and load plugins"""

    @staticmethod
    def discover_plugins(plugin_dir: Path):
        """Scan directory for plugins and register them"""
        for (_, module_name, _) in pkgutil.iter_modules([str(plugin_dir)]):
            # Import module
            module = importlib.import_module(f"plugins.{module_name}")

            # Find tool classes
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, ToolProtocol):
                    # Instantiate and register
                    tool = attr()
                    ToolRegistry.register(tool)

    @staticmethod
    def load_builtin_plugins():
        """Load built-in plugins (calculator, file ops, etc.)"""
        from plugins.builtin import (
            CalculatorTool,
            FileReadTool,
            GitStatusTool
        )

        ToolRegistry.register(CalculatorTool())
        ToolRegistry.register(FileReadTool())
        ToolRegistry.register(GitStatusTool())
```

---

### Component 4: Example Plugin (Calculator)

**File:** `src/agentic/core/plugins/builtin/calculator.py`

```python
from plugin_system.protocol import ToolProtocol, ToolMetadata

class CalculatorTool(ToolProtocol):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="@math/calculator",
            description="Perform mathematical operations",
            deterministic=True,
            cost_per_invocation=0.0,
            parameters_schema={
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["operation", "a", "b"]
            }
        )

    async def invoke(self, operation: str, a: float, b: float) -> float:
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                raise ValueError("Division by zero")
            return a / b
        else:
            raise ValueError(f"Unknown operation: {operation}")

    async def validate_params(self, **kwargs) -> bool:
        required = ["operation", "a", "b"]
        return all(k in kwargs for k in required)
```

---

## Infrastructure Integration

### Part 1: LangFuse (Observability)

**Setup:**
```bash
# Self-hosted via Docker
docker-compose up -d langfuse
```

**Integration:** `src/agentic/core/plugin_system/observability.py`

```python
from langfuse import Langfuse
from functools import wraps

# Initialize LangFuse (self-hosted)
langfuse = Langfuse(
    host="http://localhost:3000",
    public_key="local",
    secret_key="local"
)

def trace_tool(func):
    """Decorator to trace tool invocations"""
    @wraps(func)
    async def wrapper(name: str, **kwargs):
        # Start trace
        trace = langfuse.trace(name=name, metadata=kwargs)

        try:
            result = await func(name, **kwargs)
            trace.update(output=result, status_message="success")
            return result
        except Exception as e:
            trace.update(status_message="error", level="ERROR")
            raise
        finally:
            trace.flush()

    return wrapper

# Apply to ToolRegistry.invoke
ToolRegistry.invoke = trace_tool(ToolRegistry.invoke)
```

---

### Part 2: LiteLLM (LLM Proxy)

**Setup:**
```bash
pip install litellm
```

**Config:** `litellm_config.yaml`
```yaml
model_list:
  - model_name: main
    litellm_params:
      model: ollama/qwen2.5:32b
      api_base: http://localhost:11434

  - model_name: fast
    litellm_params:
      model: ollama/qwen2.5:14b
      api_base: http://localhost:11434

router_settings:
  fallbacks: [{"fast": ["main"]}]
  num_retries: 2
```

**Integration:** `src/agentic/core/plugin_system/llm_proxy.py`

```python
from litellm import completion

class LLMProxy:
    """Universal LLM interface via LiteLLM"""

    @staticmethod
    async def completion(messages: List[Dict], model: str = "main"):
        """Call LLM via proxy"""
        response = await completion(
            model=model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
```

---

## Implementation Plan

### Step 1: Core Infrastructure
1. Create `src/agentic/core/plugin_system/` directory
2. Implement `protocol.py` (ToolProtocol, ToolMetadata)
3. Implement `registry.py` (ToolRegistry)
4. Implement `loader.py` (PluginLoader)
5. Write tests for each component

### Step 2: Built-in Plugins
1. Implement `@math/calculator`
2. Implement `@file/read`
3. Implement `@git/status`
4. Test each plugin

### Step 3: LangFuse Integration
1. Setup LangFuse Docker container
2. Implement `observability.py`
3. Apply `@trace_tool` decorator
4. Test tracing

### Step 4: LiteLLM Integration
1. Install LiteLLM
2. Create `litellm_config.yaml`
3. Implement `llm_proxy.py`
4. Update SimplePlanner to use proxy

### Step 5: Integration Testing
1. Register all built-in plugins
2. Invoke each via ToolRegistry
3. Check LangFuse dashboard (traces appear)
4. Verify LiteLLM fallback works

---

## Acceptance Criteria

- [ ] ToolProtocol interface defined
- [ ] ToolRegistry can register/get/invoke tools
- [ ] PluginLoader auto-discovers plugins
- [ ] 3+ built-in plugins implemented (calculator, file, git)
- [ ] LangFuse traces all tool invocations
- [ ] LiteLLM proxy works for LLM calls
- [ ] All tests pass
- [ ] Zero proprietary dependencies

---

## Testing Strategy

### Unit Tests
```python
# test_calculator.py
async def test_calculator_add():
    calc = CalculatorTool()
    result = await calc.invoke(operation="add", a=2, b=3)
    assert result == 5

# test_registry.py
async def test_tool_registration():
    ToolRegistry.register(CalculatorTool())
    tool = ToolRegistry.get("@math/calculator")
    assert tool is not None
```

### Integration Tests
```python
# test_integration.py
async def test_full_flow():
    # Register plugin
    ToolRegistry.register(CalculatorTool())

    # Invoke via registry
    result = await ToolRegistry.invoke(
        "@math/calculator",
        operation="multiply",
        a=4,
        b=5
    )
    assert result == 20

    # Check trace in LangFuse
    traces = langfuse.get_traces(name="@math/calculator")
    assert len(traces) > 0
```

---

## Dogfooding Plan

**While building T-102:**
1. Use `@file/read` to read existing plugin code
2. Use LangFuse to track T-102 execution
3. Use LiteLLM proxy for any LLM-based code generation

**After T-102:**
- T-103 will use @langchain/file-ops (built on this core)
- T-104 will use @crewai/code-analysis (built on this core)

---

## Migration Path (Existing Code)

**Before:**
```python
from src.agentic.core.plugins.simple_planner import SimplePlanner
planner = SimplePlanner()
```

**After:**
```python
from src.agentic.core.plugin_system import ToolRegistry
planner = ToolRegistry.get("@llm/planner")
```

**SimplePlanner conversion:**
```python
class SimplePlannerPlugin(ToolProtocol):
    @property
    def metadata(self):
        return ToolMetadata(
            name="@llm/planner",
            description="Task planning via LLM",
            deterministic=False,
            cost_per_invocation=0.01  # Estimate
        )

    async def invoke(self, task: str, context: Dict) -> Plan:
        # Use existing SimplePlanner logic
        # But call LLM via LiteLLM proxy
        return await self._plan(task, context)
```

---

## Files to Create

```
src/agentic/core/plugin_system/
├── __init__.py
├── protocol.py          # ToolProtocol, ToolMetadata
├── registry.py          # ToolRegistry
├── loader.py            # PluginLoader
├── observability.py     # LangFuse integration
└── llm_proxy.py         # LiteLLM integration

src/agentic/core/plugins/builtin/
├── __init__.py
├── calculator.py        # @math/calculator
├── file_ops.py          # @file/read, @file/write
└── git_ops.py           # @git/status, @git/diff

tests/plugin_system/
├── test_protocol.py
├── test_registry.py
├── test_loader.py
├── test_calculator.py
└── test_integration.py

docker/
└── docker-compose.yml   # LangFuse setup

litellm_config.yaml      # LiteLLM configuration
```

---

## Estimated Complexity

- **Core plugin system:** ~300 lines
- **Built-in plugins:** ~200 lines
- **Observability:** ~100 lines
- **LLM proxy:** ~50 lines
- **Tests:** ~300 lines

**Total:** ~950 lines (within budget)

---

**Created:** 2025-12-20
**Priority:** P0 (Foundation for all future tools)
**Dependencies:** None (starts from scratch)
**Blocks:** T-103, T-104, T-105, T-106 (all depend on this)
