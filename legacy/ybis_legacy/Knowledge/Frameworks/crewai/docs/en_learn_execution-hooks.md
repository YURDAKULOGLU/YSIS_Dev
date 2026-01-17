Execution Hooks Overview - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Learn

Execution Hooks Overview

[Home](/)[Documentation](/en/introduction)[AOP](/en/enterprise/introduction)[API Reference](/en/api-reference/introduction)[Examples](/en/examples/example)[Changelog](/en/changelog)

* [Website](https://crewai.com)
* [Forum](https://community.crewai.com)
* [Blog](https://blog.crewai.com)
* [CrewGPT](https://chatgpt.com/g/g-qqTuUWsBY-crewai-assistant)

##### Get Started

* [Introduction](/en/introduction)
* [Installation](/en/installation)
* [Quickstart](/en/quickstart)

##### Guides

* Strategy
* Agents
* Crews
* Flows
* Advanced

##### Core Concepts

* [Agents](/en/concepts/agents)
* [Tasks](/en/concepts/tasks)
* [Crews](/en/concepts/crews)
* [Flows](/en/concepts/flows)
* [Production Architecture](/en/concepts/production-architecture)
* [Knowledge](/en/concepts/knowledge)
* [LLMs](/en/concepts/llms)
* [Processes](/en/concepts/processes)
* [Collaboration](/en/concepts/collaboration)
* [Training](/en/concepts/training)
* [Memory](/en/concepts/memory)
* [Reasoning](/en/concepts/reasoning)
* [Planning](/en/concepts/planning)
* [Testing](/en/concepts/testing)
* [CLI](/en/concepts/cli)
* [Tools](/en/concepts/tools)
* [Event Listeners](/en/concepts/event-listener)

##### MCP Integration

* [MCP Servers as Tools in CrewAI](/en/mcp/overview)
* [MCP DSL Integration](/en/mcp/dsl-integration)
* [Stdio Transport](/en/mcp/stdio)
* [SSE Transport](/en/mcp/sse)
* [Streamable HTTP Transport](/en/mcp/streamable-http)
* [Connecting to Multiple MCP Servers](/en/mcp/multiple-servers)
* [MCP Security Considerations](/en/mcp/security)

##### Tools

* [Tools Overview](/en/tools/overview)
* File & Document
* Web Scraping & Browsing
* Search & Research
* Database & Data
* AI & Machine Learning
* Cloud & Storage
* Integrations
* Automation

##### Observability

* [CrewAI Tracing](/en/observability/tracing)
* [Overview](/en/observability/overview)
* [Arize Phoenix](/en/observability/arize-phoenix)
* [Braintrust](/en/observability/braintrust)
* [Datadog Integration](/en/observability/datadog)
* [LangDB Integration](/en/observability/langdb)
* [Langfuse Integration](/en/observability/langfuse)
* [Langtrace Integration](/en/observability/langtrace)
* [Maxim Integration](/en/observability/maxim)
* [MLflow Integration](/en/observability/mlflow)
* [Neatlogs Integration](/en/observability/neatlogs)
* [OpenLIT Integration](/en/observability/openlit)
* [Opik Integration](/en/observability/opik)
* [Patronus AI Evaluation](/en/observability/patronus-evaluation)
* [Portkey Integration](/en/observability/portkey)
* [Weave Integration](/en/observability/weave)
* [TrueFoundry Integration](/en/observability/truefoundry)

##### Learn

* [Overview](/en/learn/overview)
* [Strategic LLM Selection Guide](/en/learn/llm-selection-guide)
* [Conditional Tasks](/en/learn/conditional-tasks)
* [Coding Agents](/en/learn/coding-agents)
* [Create Custom Tools](/en/learn/create-custom-tools)
* [Custom LLM Implementation](/en/learn/custom-llm)
* [Custom Manager Agent](/en/learn/custom-manager-agent)
* [Customize Agents](/en/learn/customizing-agents)
* [Image Generation with DALL-E](/en/learn/dalle-image-generation)
* [Force Tool Output as Result](/en/learn/force-tool-output-as-result)
* [Hierarchical Process](/en/learn/hierarchical-process)
* [Human Input on Execution](/en/learn/human-input-on-execution)
* [Human-in-the-Loop (HITL) Workflows](/en/learn/human-in-the-loop)
* [Human Feedback in Flows](/en/learn/human-feedback-in-flows)
* [Kickoff Crew Asynchronously](/en/learn/kickoff-async)
* [Kickoff Crew for Each](/en/learn/kickoff-for-each)
* [Connect to any LLM](/en/learn/llm-connections)
* [Using Multimodal Agents](/en/learn/multimodal-agents)
* [Replay Tasks from Latest Crew Kickoff](/en/learn/replay-tasks-from-latest-crew-kickoff)
* [Sequential Processes](/en/learn/sequential-process)
* [Using Annotations in crew.py](/en/learn/using-annotations)
* [Execution Hooks Overview](/en/learn/execution-hooks)
* [LLM Call Hooks](/en/learn/llm-hooks)
* [Tool Call Hooks](/en/learn/tool-hooks)

##### Telemetry

* [Telemetry](/en/telemetry)

Execution Hooks provide fine-grained control over the runtime behavior of your CrewAI agents. Unlike kickoff hooks that run before and after crew execution, execution hooks intercept specific operations during agent execution, allowing you to modify behavior, implement safety checks, and add comprehensive monitoring.

## [​](#types-of-execution-hooks) Types of Execution Hooks

CrewAI provides two main categories of execution hooks:

### [​](#1-llm-call-hooks) 1. [LLM Call Hooks](/learn/llm-hooks)

Control and monitor language model interactions:

* **Before LLM Call**: Modify prompts, validate inputs, implement approval gates
* **After LLM Call**: Transform responses, sanitize outputs, update conversation history

**Use Cases:**

* Iteration limiting
* Cost tracking and token usage monitoring
* Response sanitization and content filtering
* Human-in-the-loop approval for LLM calls
* Adding safety guidelines or context
* Debug logging and request/response inspection

[View LLM Hooks Documentation →](/learn/llm-hooks)

### [​](#2-tool-call-hooks) 2. [Tool Call Hooks](/learn/tool-hooks)

Control and monitor tool execution:

* **Before Tool Call**: Modify inputs, validate parameters, block dangerous operations
* **After Tool Call**: Transform results, sanitize outputs, log execution details

**Use Cases:**

* Safety guardrails for destructive operations
* Human approval for sensitive actions
* Input validation and sanitization
* Result caching and rate limiting
* Tool usage analytics
* Debug logging and monitoring

[View Tool Hooks Documentation →](/learn/tool-hooks)

## [​](#hook-registration-methods) Hook Registration Methods

### [​](#1-decorator-based-hooks-recommended) 1. Decorator-Based Hooks (Recommended)

The cleanest and most Pythonic way to register hooks:

Copy

Ask AI

```
from crewai.hooks import before_llm_call, after_llm_call, before_tool_call, after_tool_call

@before_llm_call
def limit_iterations(context):
    """Prevent infinite loops by limiting iterations."""
    if context.iterations > 10:
        return False  # Block execution
    return None

@after_llm_call
def sanitize_response(context):
    """Remove sensitive data from LLM responses."""
    if "API_KEY" in context.response:
        return context.response.replace("API_KEY", "[REDACTED]")
    return None

@before_tool_call
def block_dangerous_tools(context):
    """Block destructive operations."""
    if context.tool_name == "delete_database":
        return False  # Block execution
    return None

@after_tool_call
def log_tool_result(context):
    """Log tool execution."""
    print(f"Tool {context.tool_name} completed")
    return None
```

### [​](#2-crew-scoped-hooks) 2. Crew-Scoped Hooks

Apply hooks only to specific crew instances:

Copy

Ask AI

```
from crewai import CrewBase
from crewai.project import crew
from crewai.hooks import before_llm_call_crew, after_tool_call_crew

@CrewBase
class MyProjCrew:
    @before_llm_call_crew
    def validate_inputs(self, context):
        # Only applies to this crew
        print(f"LLM call in {self.__class__.__name__}")
        return None

    @after_tool_call_crew
    def log_results(self, context):
        # Crew-specific logging
        print(f"Tool result: {context.tool_result[:50]}...")
        return None

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential
        )
```

## [​](#hook-execution-flow) Hook Execution Flow

### [​](#llm-call-flow) LLM Call Flow

Copy

Ask AI

```
Agent needs to call LLM
    ↓
[Before LLM Call Hooks Execute]
    ├→ Hook 1: Validate iteration count
    ├→ Hook 2: Add safety context
    └→ Hook 3: Log request
    ↓
If any hook returns False:
    ├→ Block LLM call
    └→ Raise ValueError
    ↓
If all hooks return True/None:
    ├→ LLM call proceeds
    └→ Response generated
    ↓
[After LLM Call Hooks Execute]
    ├→ Hook 1: Sanitize response
    ├→ Hook 2: Log response
    └→ Hook 3: Update metrics
    ↓
Final response returned
```

### [​](#tool-call-flow) Tool Call Flow

Copy

Ask AI

```
Agent needs to execute tool
    ↓
[Before Tool Call Hooks Execute]
    ├→ Hook 1: Check if tool is allowed
    ├→ Hook 2: Validate inputs
    └→ Hook 3: Request approval if needed
    ↓
If any hook returns False:
    ├→ Block tool execution
    └→ Return error message
    ↓
If all hooks return True/None:
    ├→ Tool execution proceeds
    └→ Result generated
    ↓
[After Tool Call Hooks Execute]
    ├→ Hook 1: Sanitize result
    ├→ Hook 2: Cache result
    └→ Hook 3: Log metrics
    ↓
Final result returned
```

## [​](#hook-context-objects) Hook Context Objects

### [​](#llmcallhookcontext) LLMCallHookContext

Provides access to LLM execution state:

Copy

Ask AI

```
class LLMCallHookContext:
    executor: CrewAgentExecutor  # Full executor access
    messages: list               # Mutable message list
    agent: Agent                 # Current agent
    task: Task                   # Current task
    crew: Crew                   # Crew instance
    llm: BaseLLM                 # LLM instance
    iterations: int              # Current iteration
    response: str | None         # LLM response (after hooks)
```

### [​](#toolcallhookcontext) ToolCallHookContext

Provides access to tool execution state:

Copy

Ask AI

```
class ToolCallHookContext:
    tool_name: str               # Tool being called
    tool_input: dict             # Mutable input parameters
    tool: CrewStructuredTool     # Tool instance
    agent: Agent | None          # Agent executing
    task: Task | None            # Current task
    crew: Crew | None            # Crew instance
    tool_result: str | None      # Tool result (after hooks)
```

## [​](#common-patterns) Common Patterns

### [​](#safety-and-validation) Safety and Validation

Copy

Ask AI

```
@before_tool_call
def safety_check(context):
    """Block destructive operations."""
    dangerous = ['delete_file', 'drop_table', 'system_shutdown']
    if context.tool_name in dangerous:
        print(f"🛑 Blocked: {context.tool_name}")
        return False
    return None

@before_llm_call
def iteration_limit(context):
    """Prevent infinite loops."""
    if context.iterations > 15:
        print("⛔ Maximum iterations exceeded")
        return False
    return None
```

### [​](#human-in-the-loop) Human-in-the-Loop

Copy

Ask AI

```
@before_tool_call
def require_approval(context):
    """Require approval for sensitive operations."""
    sensitive = ['send_email', 'make_payment', 'post_message']

    if context.tool_name in sensitive:
        response = context.request_human_input(
            prompt=f"Approve {context.tool_name}?",
            default_message="Type 'yes' to approve:"
        )

        if response.lower() != 'yes':
            return False

    return None
```

### [​](#monitoring-and-analytics) Monitoring and Analytics

Copy

Ask AI

```
from collections import defaultdict
import time

metrics = defaultdict(lambda: {'count': 0, 'total_time': 0})

@before_tool_call
def start_timer(context):
    context.tool_input['_start'] = time.time()
    return None

@after_tool_call
def track_metrics(context):
    start = context.tool_input.get('_start', time.time())
    duration = time.time() - start

    metrics[context.tool_name]['count'] += 1
    metrics[context.tool_name]['total_time'] += duration

    return None

# View metrics
def print_metrics():
    for tool, data in metrics.items():
        avg = data['total_time'] / data['count']
        print(f"{tool}: {data['count']} calls, {avg:.2f}s avg")
```

### [​](#response-sanitization) Response Sanitization

Copy

Ask AI

```
import re

@after_llm_call
def sanitize_llm_response(context):
    """Remove sensitive data from LLM responses."""
    if not context.response:
        return None

    result = context.response
    result = re.sub(r'(api[_-]?key)["\']?\s*[:=]\s*["\']?[\w-]+',
                   r'\1: [REDACTED]', result, flags=re.IGNORECASE)
    return result

@after_tool_call
def sanitize_tool_result(context):
    """Remove sensitive data from tool results."""
    if not context.tool_result:
        return None

    result = context.tool_result
    result = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                   '[EMAIL-REDACTED]', result)
    return result
```

## [​](#hook-management) Hook Management

### [​](#clearing-all-hooks) Clearing All Hooks

Copy

Ask AI

```
from crewai.hooks import clear_all_global_hooks

# Clear all hooks at once
result = clear_all_global_hooks()
print(f"Cleared {result['total']} hooks")
# Output: {'llm_hooks': (2, 1), 'tool_hooks': (1, 2), 'total': (3, 3)}
```

### [​](#clearing-specific-hook-types) Clearing Specific Hook Types

Copy

Ask AI

```
from crewai.hooks import (
    clear_before_llm_call_hooks,
    clear_after_llm_call_hooks,
    clear_before_tool_call_hooks,
    clear_after_tool_call_hooks
)

# Clear specific types
llm_before_count = clear_before_llm_call_hooks()
tool_after_count = clear_after_tool_call_hooks()
```

### [​](#unregistering-individual-hooks) Unregistering Individual Hooks

Copy

Ask AI

```
from crewai.hooks import (
    unregister_before_llm_call_hook,
    unregister_after_tool_call_hook
)

def my_hook(context):
    ...

# Register
register_before_llm_call_hook(my_hook)

# Later, unregister
success = unregister_before_llm_call_hook(my_hook)
print(f"Unregistered: {success}")
```

## [​](#best-practices) Best Practices

### [​](#1-keep-hooks-focused) 1. Keep Hooks Focused

Each hook should have a single, clear responsibility:

Copy

Ask AI

```
# ✅ Good - focused responsibility
@before_tool_call
def validate_file_path(context):
    if context.tool_name == 'read_file':
        if '..' in context.tool_input.get('path', ''):
            return False
    return None

# ❌ Bad - too many responsibilities
@before_tool_call
def do_everything(context):
    # Validation + logging + metrics + approval...
    ...
```

### [​](#2-handle-errors-gracefully) 2. Handle Errors Gracefully

Copy

Ask AI

```
@before_llm_call
def safe_hook(context):
    try:
        # Your logic
        if some_condition:
            return False
    except Exception as e:
        print(f"Hook error: {e}")
        return None  # Allow execution despite error
```

### [​](#3-modify-context-in-place) 3. Modify Context In-Place

Copy

Ask AI

```
# ✅ Correct - modify in-place
@before_llm_call
def add_context(context):
    context.messages.append({"role": "system", "content": "Be concise"})

# ❌ Wrong - replaces reference
@before_llm_call
def wrong_approach(context):
    context.messages = [{"role": "system", "content": "Be concise"}]
```

### [​](#4-use-type-hints) 4. Use Type Hints

Copy

Ask AI

```
from crewai.hooks import LLMCallHookContext, ToolCallHookContext

def my_llm_hook(context: LLMCallHookContext) -> bool | None:
    # IDE autocomplete and type checking
    return None

def my_tool_hook(context: ToolCallHookContext) -> str | None:
    return None
```

### [​](#5-clean-up-in-tests) 5. Clean Up in Tests

Copy

Ask AI

```
import pytest
from crewai.hooks import clear_all_global_hooks

@pytest.fixture(autouse=True)
def clean_hooks():
    """Reset hooks before each test."""
    yield
    clear_all_global_hooks()
```

## [​](#when-to-use-which-hook) When to Use Which Hook

### [​](#use-llm-hooks-when:) Use LLM Hooks When:

* Implementing iteration limits
* Adding context or safety guidelines to prompts
* Tracking token usage and costs
* Sanitizing or transforming responses
* Implementing approval gates for LLM calls
* Debugging prompt/response interactions

### [​](#use-tool-hooks-when:) Use Tool Hooks When:

* Blocking dangerous or destructive operations
* Validating tool inputs before execution
* Implementing approval gates for sensitive actions
* Caching tool results
* Tracking tool usage and performance
* Sanitizing tool outputs
* Rate limiting tool calls

### [​](#use-both-when:) Use Both When:

Building comprehensive observability, safety, or approval systems that need to monitor all agent operations.

## [​](#alternative-registration-methods) Alternative Registration Methods

### [​](#programmatic-registration-advanced) Programmatic Registration (Advanced)

For dynamic hook registration or when you need to register hooks programmatically:

Copy

Ask AI

```
from crewai.hooks import (
    register_before_llm_call_hook,
    register_after_tool_call_hook
)

def my_hook(context):
    return None

# Register programmatically
register_before_llm_call_hook(my_hook)

# Useful for:
# - Loading hooks from configuration
# - Conditional hook registration
# - Plugin systems
```

**Note:** For most use cases, decorators are cleaner and more maintainable.

## [​](#performance-considerations) Performance Considerations

1. **Keep Hooks Fast**: Hooks execute on every call - avoid heavy computation
2. **Cache When Possible**: Store expensive validations or lookups
3. **Be Selective**: Use crew-scoped hooks when global hooks aren’t needed
4. **Monitor Hook Overhead**: Profile hook execution time in production
5. **Lazy Import**: Import heavy dependencies only when needed

## [​](#debugging-hooks) Debugging Hooks

### [​](#enable-debug-logging) Enable Debug Logging

Copy

Ask AI

```
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@before_llm_call
def debug_hook(context):
    logger.debug(f"LLM call: {context.agent.role}, iteration {context.iterations}")
    return None
```

### [​](#hook-execution-order) Hook Execution Order

Hooks execute in registration order. If a before hook returns `False`, subsequent hooks don’t execute:

Copy

Ask AI

```
# Register order matters!
register_before_tool_call_hook(hook1)  # Executes first
register_before_tool_call_hook(hook2)  # Executes second
register_before_tool_call_hook(hook3)  # Executes third

# If hook2 returns False:
# - hook1 executed
# - hook2 executed and returned False
# - hook3 NOT executed
# - Tool call blocked
```

## [​](#related-documentation) Related Documentation

* [LLM Call Hooks →](/learn/llm-hooks) - Detailed LLM hook documentation
* [Tool Call Hooks →](/learn/tool-hooks) - Detailed tool hook documentation
* [Before and After Kickoff Hooks →](/learn/before-and-after-kickoff-hooks) - Crew lifecycle hooks
* [Human-in-the-Loop →](/learn/human-in-the-loop) - Human input patterns

## [​](#conclusion) Conclusion

Execution hooks provide powerful control over agent runtime behavior. Use them to implement safety guardrails, approval workflows, comprehensive monitoring, and custom business logic. Combined with proper error handling, type safety, and performance considerations, hooks enable production-ready, secure, and observable agent systems.

Was this page helpful?

YesNo

[Using Annotations in crew.py

Previous](/en/learn/using-annotations)[LLM Call Hooks

Next](/en/learn/llm-hooks)

⌘I