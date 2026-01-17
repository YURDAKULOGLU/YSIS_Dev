Tool Call Hooks - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Learn

Tool Call Hooks

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

Tool Call Hooks provide fine-grained control over tool execution during agent operations. These hooks allow you to intercept tool calls, modify inputs, transform outputs, implement safety checks, and add comprehensive logging or monitoring.

## [​](#overview) Overview

Tool hooks are executed at two critical points:

* **Before Tool Call**: Modify inputs, validate parameters, or block execution
* **After Tool Call**: Transform results, sanitize outputs, or log execution details

## [​](#hook-types) Hook Types

### [​](#before-tool-call-hooks) Before Tool Call Hooks

Executed before every tool execution, these hooks can:

* Inspect and modify tool inputs
* Block tool execution based on conditions
* Implement approval gates for dangerous operations
* Validate parameters
* Log tool invocations

**Signature:**

Copy

Ask AI

```
def before_hook(context: ToolCallHookContext) -> bool | None:
    # Return False to block execution
    # Return True or None to allow execution
    ...
```

### [​](#after-tool-call-hooks) After Tool Call Hooks

Executed after every tool execution, these hooks can:

* Modify or sanitize tool results
* Add metadata or formatting
* Log execution results
* Implement result validation
* Transform output formats

**Signature:**

Copy

Ask AI

```
def after_hook(context: ToolCallHookContext) -> str | None:
    # Return modified result string
    # Return None to keep original result
    ...
```

## [​](#tool-hook-context) Tool Hook Context

The `ToolCallHookContext` object provides comprehensive access to tool execution state:

Copy

Ask AI

```
class ToolCallHookContext:
    tool_name: str                    # Name of the tool being called
    tool_input: dict[str, Any]        # Mutable tool input parameters
    tool: CrewStructuredTool          # Tool instance reference
    agent: Agent | BaseAgent | None   # Agent executing the tool
    task: Task | None                 # Current task
    crew: Crew | None                 # Crew instance
    tool_result: str | None           # Tool result (after hooks only)
```

### [​](#modifying-tool-inputs) Modifying Tool Inputs

**Important:** Always modify tool inputs in-place:

Copy

Ask AI

```
# ✅ Correct - modify in-place
def sanitize_input(context: ToolCallHookContext) -> None:
    context.tool_input['query'] = context.tool_input['query'].lower()

# ❌ Wrong - replaces dict reference
def wrong_approach(context: ToolCallHookContext) -> None:
    context.tool_input = {'query': 'new query'}
```

## [​](#registration-methods) Registration Methods

### [​](#1-global-hook-registration) 1. Global Hook Registration

Register hooks that apply to all tool calls across all crews:

Copy

Ask AI

```
from crewai.hooks import register_before_tool_call_hook, register_after_tool_call_hook

def log_tool_call(context):
    print(f"Tool: {context.tool_name}")
    print(f"Input: {context.tool_input}")
    return None  # Allow execution

register_before_tool_call_hook(log_tool_call)
```

### [​](#2-decorator-based-registration) 2. Decorator-Based Registration

Use decorators for cleaner syntax:

Copy

Ask AI

```
from crewai.hooks import before_tool_call, after_tool_call

@before_tool_call
def block_dangerous_tools(context):
    dangerous_tools = ['delete_database', 'drop_table', 'rm_rf']
    if context.tool_name in dangerous_tools:
        print(f"⛔ Blocked dangerous tool: {context.tool_name}")
        return False  # Block execution
    return None

@after_tool_call
def sanitize_results(context):
    if context.tool_result and "password" in context.tool_result.lower():
        return context.tool_result.replace("password", "[REDACTED]")
    return None
```

### [​](#3-crew-scoped-hooks) 3. Crew-Scoped Hooks

Register hooks for a specific crew instance:

Copy

Ask AI

```
@CrewBase
class MyProjCrew:
    @before_tool_call_crew
    def validate_tool_inputs(self, context):
        # Only applies to this crew
        if context.tool_name == "web_search":
            if not context.tool_input.get('query'):
                print("❌ Invalid search query")
                return False
        return None

    @after_tool_call_crew
    def log_tool_results(self, context):
        # Crew-specific tool logging
        print(f"✅ {context.tool_name} completed")
        return None

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
```

## [​](#common-use-cases) Common Use Cases

### [​](#1-safety-guardrails) 1. Safety Guardrails

Copy

Ask AI

```
@before_tool_call
def safety_check(context: ToolCallHookContext) -> bool | None:
    # Block tools that could cause harm
    destructive_tools = [
        'delete_file',
        'drop_table',
        'remove_user',
        'system_shutdown'
    ]

    if context.tool_name in destructive_tools:
        print(f"🛑 Blocked destructive tool: {context.tool_name}")
        return False

    # Warn on sensitive operations
    sensitive_tools = ['send_email', 'post_to_social_media', 'charge_payment']
    if context.tool_name in sensitive_tools:
        print(f"⚠️  Executing sensitive tool: {context.tool_name}")

    return None
```

### [​](#2-human-approval-gate) 2. Human Approval Gate

Copy

Ask AI

```
@before_tool_call
def require_approval_for_actions(context: ToolCallHookContext) -> bool | None:
    approval_required = [
        'send_email',
        'make_purchase',
        'delete_file',
        'post_message'
    ]

    if context.tool_name in approval_required:
        response = context.request_human_input(
            prompt=f"Approve {context.tool_name}?",
            default_message=f"Input: {context.tool_input}\nType 'yes' to approve:"
        )

        if response.lower() != 'yes':
            print(f"❌ Tool execution denied: {context.tool_name}")
            return False

    return None
```

### [​](#3-input-validation-and-sanitization) 3. Input Validation and Sanitization

Copy

Ask AI

```
@before_tool_call
def validate_and_sanitize_inputs(context: ToolCallHookContext) -> bool | None:
    # Validate search queries
    if context.tool_name == 'web_search':
        query = context.tool_input.get('query', '')
        if len(query) < 3:
            print("❌ Search query too short")
            return False

        # Sanitize query
        context.tool_input['query'] = query.strip().lower()

    # Validate file paths
    if context.tool_name == 'read_file':
        path = context.tool_input.get('path', '')
        if '..' in path or path.startswith('/'):
            print("❌ Invalid file path")
            return False

    return None
```

### [​](#4-result-sanitization) 4. Result Sanitization

Copy

Ask AI

```
@after_tool_call
def sanitize_sensitive_data(context: ToolCallHookContext) -> str | None:
    if not context.tool_result:
        return None

    import re
    result = context.tool_result

    # Remove API keys
    result = re.sub(
        r'(api[_-]?key|token)["\']?\s*[:=]\s*["\']?[\w-]+',
        r'\1: [REDACTED]',
        result,
        flags=re.IGNORECASE
    )

    # Remove email addresses
    result = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '[EMAIL-REDACTED]',
        result
    )

    # Remove credit card numbers
    result = re.sub(
        r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
        '[CARD-REDACTED]',
        result
    )

    return result
```

### [​](#5-tool-usage-analytics) 5. Tool Usage Analytics

Copy

Ask AI

```
import time
from collections import defaultdict

tool_stats = defaultdict(lambda: {'count': 0, 'total_time': 0, 'failures': 0})

@before_tool_call
def start_timer(context: ToolCallHookContext) -> None:
    context.tool_input['_start_time'] = time.time()
    return None

@after_tool_call
def track_tool_usage(context: ToolCallHookContext) -> None:
    start_time = context.tool_input.get('_start_time', time.time())
    duration = time.time() - start_time

    tool_stats[context.tool_name]['count'] += 1
    tool_stats[context.tool_name]['total_time'] += duration

    if not context.tool_result or 'error' in context.tool_result.lower():
        tool_stats[context.tool_name]['failures'] += 1

    print(f"""
    📊 Tool Stats for {context.tool_name}:
    - Executions: {tool_stats[context.tool_name]['count']}
    - Avg Time: {tool_stats[context.tool_name]['total_time'] / tool_stats[context.tool_name]['count']:.2f}s
    - Failures: {tool_stats[context.tool_name]['failures']}
    """)

    return None
```

### [​](#6-rate-limiting) 6. Rate Limiting

Copy

Ask AI

```
from collections import defaultdict
from datetime import datetime, timedelta

tool_call_history = defaultdict(list)

@before_tool_call
def rate_limit_tools(context: ToolCallHookContext) -> bool | None:
    tool_name = context.tool_name
    now = datetime.now()

    # Clean old entries (older than 1 minute)
    tool_call_history[tool_name] = [
        call_time for call_time in tool_call_history[tool_name]
        if now - call_time < timedelta(minutes=1)
    ]

    # Check rate limit (max 10 calls per minute)
    if len(tool_call_history[tool_name]) >= 10:
        print(f"🚫 Rate limit exceeded for {tool_name}")
        return False

    # Record this call
    tool_call_history[tool_name].append(now)
    return None
```

### [​](#7-caching-tool-results) 7. Caching Tool Results

Copy

Ask AI

```
import hashlib
import json

tool_cache = {}

def cache_key(tool_name: str, tool_input: dict) -> str:
    """Generate cache key from tool name and input."""
    input_str = json.dumps(tool_input, sort_keys=True)
    return hashlib.md5(f"{tool_name}:{input_str}".encode()).hexdigest()

@before_tool_call
def check_cache(context: ToolCallHookContext) -> bool | None:
    key = cache_key(context.tool_name, context.tool_input)
    if key in tool_cache:
        print(f"💾 Cache hit for {context.tool_name}")
        # Note: Can't return cached result from before hook
        # Would need to implement this differently
    return None

@after_tool_call
def cache_result(context: ToolCallHookContext) -> None:
    if context.tool_result:
        key = cache_key(context.tool_name, context.tool_input)
        tool_cache[key] = context.tool_result
        print(f"💾 Cached result for {context.tool_name}")
    return None
```

### [​](#8-debug-logging) 8. Debug Logging

Copy

Ask AI

```
@before_tool_call
def debug_tool_call(context: ToolCallHookContext) -> None:
    print(f"""
    🔍 Tool Call Debug:
    - Tool: {context.tool_name}
    - Agent: {context.agent.role if context.agent else 'Unknown'}
    - Task: {context.task.description[:50] if context.task else 'Unknown'}...
    - Input: {context.tool_input}
    """)
    return None

@after_tool_call
def debug_tool_result(context: ToolCallHookContext) -> None:
    if context.tool_result:
        result_preview = context.tool_result[:200]
        print(f"✅ Result Preview: {result_preview}...")
    else:
        print("⚠️  No result returned")
    return None
```

## [​](#hook-management) Hook Management

### [​](#unregistering-hooks) Unregistering Hooks

Copy

Ask AI

```
from crewai.hooks import (
    unregister_before_tool_call_hook,
    unregister_after_tool_call_hook
)

# Unregister specific hook
def my_hook(context):
    ...

register_before_tool_call_hook(my_hook)
# Later...
success = unregister_before_tool_call_hook(my_hook)
print(f"Unregistered: {success}")
```

### [​](#clearing-hooks) Clearing Hooks

Copy

Ask AI

```
from crewai.hooks import (
    clear_before_tool_call_hooks,
    clear_after_tool_call_hooks,
    clear_all_tool_call_hooks
)

# Clear specific hook type
count = clear_before_tool_call_hooks()
print(f"Cleared {count} before hooks")

# Clear all tool hooks
before_count, after_count = clear_all_tool_call_hooks()
print(f"Cleared {before_count} before and {after_count} after hooks")
```

### [​](#listing-registered-hooks) Listing Registered Hooks

Copy

Ask AI

```
from crewai.hooks import (
    get_before_tool_call_hooks,
    get_after_tool_call_hooks
)

# Get current hooks
before_hooks = get_before_tool_call_hooks()
after_hooks = get_after_tool_call_hooks()

print(f"Registered: {len(before_hooks)} before, {len(after_hooks)} after")
```

## [​](#advanced-patterns) Advanced Patterns

### [​](#conditional-hook-execution) Conditional Hook Execution

Copy

Ask AI

```
@before_tool_call
def conditional_blocking(context: ToolCallHookContext) -> bool | None:
    # Only block for specific agents
    if context.agent and context.agent.role == "junior_agent":
        if context.tool_name in ['delete_file', 'send_email']:
            print(f"❌ Junior agents cannot use {context.tool_name}")
            return False

    # Only block during specific tasks
    if context.task and "sensitive" in context.task.description.lower():
        if context.tool_name == 'web_search':
            print("❌ Web search blocked for sensitive tasks")
            return False

    return None
```

### [​](#context-aware-input-modification) Context-Aware Input Modification

Copy

Ask AI

```
@before_tool_call
def enhance_tool_inputs(context: ToolCallHookContext) -> None:
    # Add context based on agent role
    if context.agent and context.agent.role == "researcher":
        if context.tool_name == 'web_search':
            # Add domain restrictions for researchers
            context.tool_input['domains'] = ['edu', 'gov', 'org']

    # Add context based on task
    if context.task and "urgent" in context.task.description.lower():
        if context.tool_name == 'send_email':
            context.tool_input['priority'] = 'high'

    return None
```

### [​](#tool-chain-monitoring) Tool Chain Monitoring

Copy

Ask AI

```
tool_call_chain = []

@before_tool_call
def track_tool_chain(context: ToolCallHookContext) -> None:
    tool_call_chain.append({
        'tool': context.tool_name,
        'timestamp': time.time(),
        'agent': context.agent.role if context.agent else 'Unknown'
    })

    # Detect potential infinite loops
    recent_calls = tool_call_chain[-5:]
    if len(recent_calls) == 5 and all(c['tool'] == context.tool_name for c in recent_calls):
        print(f"⚠️  Warning: {context.tool_name} called 5 times in a row")

    return None
```

## [​](#best-practices) Best Practices

1. **Keep Hooks Focused**: Each hook should have a single responsibility
2. **Avoid Heavy Computation**: Hooks execute on every tool call
3. **Handle Errors Gracefully**: Use try-except to prevent hook failures
4. **Use Type Hints**: Leverage `ToolCallHookContext` for better IDE support
5. **Document Blocking Conditions**: Make it clear when/why tools are blocked
6. **Test Hooks Independently**: Unit test hooks before using in production
7. **Clear Hooks in Tests**: Use `clear_all_tool_call_hooks()` between test runs
8. **Modify In-Place**: Always modify `context.tool_input` in-place, never replace
9. **Log Important Decisions**: Especially when blocking tool execution
10. **Consider Performance**: Cache expensive validations when possible

## [​](#error-handling) Error Handling

Copy

Ask AI

```
@before_tool_call
def safe_validation(context: ToolCallHookContext) -> bool | None:
    try:
        # Your validation logic
        if not validate_input(context.tool_input):
            return False
    except Exception as e:
        print(f"⚠️ Hook error: {e}")
        # Decide: allow or block on error
        return None  # Allow execution despite error
```

## [​](#type-safety) Type Safety

Copy

Ask AI

```
from crewai.hooks import ToolCallHookContext, BeforeToolCallHookType, AfterToolCallHookType

# Explicit type annotations
def my_before_hook(context: ToolCallHookContext) -> bool | None:
    return None

def my_after_hook(context: ToolCallHookContext) -> str | None:
    return None

# Type-safe registration
register_before_tool_call_hook(my_before_hook)
register_after_tool_call_hook(my_after_hook)
```

## [​](#integration-with-existing-tools) Integration with Existing Tools

### [​](#wrapping-existing-validation) Wrapping Existing Validation

Copy

Ask AI

```
def existing_validator(tool_name: str, inputs: dict) -> bool:
    """Your existing validation function."""
    # Your validation logic
    return True

@before_tool_call
def integrate_validator(context: ToolCallHookContext) -> bool | None:
    if not existing_validator(context.tool_name, context.tool_input):
        print(f"❌ Validation failed for {context.tool_name}")
        return False
    return None
```

### [​](#logging-to-external-systems) Logging to External Systems

Copy

Ask AI

```
import logging

logger = logging.getLogger(__name__)

@before_tool_call
def log_to_external_system(context: ToolCallHookContext) -> None:
    logger.info(f"Tool call: {context.tool_name}", extra={
        'tool_name': context.tool_name,
        'tool_input': context.tool_input,
        'agent': context.agent.role if context.agent else None
    })
    return None
```

## [​](#troubleshooting) Troubleshooting

### [​](#hook-not-executing) Hook Not Executing

* Verify hook is registered before crew execution
* Check if previous hook returned `False` (blocks execution and subsequent hooks)
* Ensure hook signature matches expected type

### [​](#input-modifications-not-working) Input Modifications Not Working

* Use in-place modifications: `context.tool_input['key'] = value`
* Don’t replace the dict: `context.tool_input = {}`

### [​](#result-modifications-not-working) Result Modifications Not Working

* Return the modified string from after hooks
* Returning `None` keeps the original result
* Ensure the tool actually returned a result

### [​](#tool-blocked-unexpectedly) Tool Blocked Unexpectedly

* Check all before hooks for blocking conditions
* Verify hook execution order
* Add debug logging to identify which hook is blocking

## [​](#conclusion) Conclusion

Tool Call Hooks provide powerful capabilities for controlling and monitoring tool execution in CrewAI. Use them to implement safety guardrails, approval gates, input validation, result sanitization, logging, and analytics. Combined with proper error handling and type safety, hooks enable secure and production-ready agent systems with comprehensive observability.

Was this page helpful?

YesNo

[LLM Call Hooks

Previous](/en/learn/llm-hooks)[Telemetry

Next](/en/telemetry)

⌘I