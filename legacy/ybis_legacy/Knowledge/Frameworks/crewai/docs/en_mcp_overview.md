MCP Servers as Tools in CrewAI - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

MCP Integration

MCP Servers as Tools in CrewAI

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

## [​](#overview) Overview

The [Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) provides a standardized way for AI agents to provide context to LLMs by communicating with external services, known as MCP Servers.
CrewAI offers **two approaches** for MCP integration:

### [​](#🚀-simple-dsl-integration-recommended) 🚀 **Simple DSL Integration** (Recommended)

Use the `mcps` field directly on agents for seamless MCP tool integration. The DSL supports both **string references** (for quick setup) and **structured configurations** (for full control).

#### [​](#string-based-references-quick-setup) String-Based References (Quick Setup)

Perfect for remote HTTPS servers and CrewAI AOP marketplace:

Copy

Ask AI

```
from crewai import Agent

agent = Agent(
    role="Research Analyst",
    goal="Research and analyze information",
    backstory="Expert researcher with access to external tools",
    mcps=[
        "https://mcp.exa.ai/mcp?api_key=your_key",           # External MCP server
        "https://api.weather.com/mcp#get_forecast",          # Specific tool from server
        "crewai-amp:financial-data",                         # CrewAI AOP marketplace
        "crewai-amp:research-tools#pubmed_search"            # Specific AMP tool
    ]
)
# MCP tools are now automatically available to your agent!
```

#### [​](#structured-configurations-full-control) Structured Configurations (Full Control)

For complete control over connection settings, tool filtering, and all transport types:

Copy

Ask AI

```
from crewai import Agent
from crewai.mcp import MCPServerStdio, MCPServerHTTP, MCPServerSSE
from crewai.mcp.filters import create_static_tool_filter

agent = Agent(
    role="Advanced Research Analyst",
    goal="Research with full control over MCP connections",
    backstory="Expert researcher with advanced tool access",
    mcps=[
        # Stdio transport for local servers
        MCPServerStdio(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem"],
            env={"API_KEY": "your_key"},
            tool_filter=create_static_tool_filter(
                allowed_tool_names=["read_file", "list_directory"]
            ),
            cache_tools_list=True,
        ),
        # HTTP/Streamable HTTP transport for remote servers
        MCPServerHTTP(
            url="https://api.example.com/mcp",
            headers={"Authorization": "Bearer your_token"},
            streamable=True,
            cache_tools_list=True,
        ),
        # SSE transport for real-time streaming
        MCPServerSSE(
            url="https://stream.example.com/mcp/sse",
            headers={"Authorization": "Bearer your_token"},
        ),
    ]
)
```

### [​](#🔧-advanced:-mcpserveradapter-for-complex-scenarios) 🔧 **Advanced: MCPServerAdapter** (For Complex Scenarios)

For advanced use cases requiring manual connection management, the `crewai-tools` library provides the `MCPServerAdapter` class.
We currently support the following transport mechanisms:

* **Stdio**: for local servers (communication via standard input/output between processes on the same machine)
* **Server-Sent Events (SSE)**: for remote servers (unidirectional, real-time data streaming from server to client over HTTP)
* **Streamable HTTPS**: for remote servers (flexible, potentially bi-directional communication over HTTPS, often utilizing SSE for server-to-client streams)

## [​](#video-tutorial) Video Tutorial

Watch this video tutorial for a comprehensive guide on MCP integration with CrewAI:

## [​](#installation) Installation

CrewAI MCP integration requires the `mcp` library:

Copy

Ask AI

```
# For Simple DSL Integration (Recommended)
uv add mcp

# For Advanced MCPServerAdapter usage
uv pip install 'crewai-tools[mcp]'
```

## [​](#quick-start:-simple-dsl-integration) Quick Start: Simple DSL Integration

The easiest way to integrate MCP servers is using the `mcps` field on your agents. You can use either string references or structured configurations.

### [​](#quick-start-with-string-references) Quick Start with String References

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create agent with MCP tools using string references
research_agent = Agent(
    role="Research Analyst",
    goal="Find and analyze information using advanced search tools",
    backstory="Expert researcher with access to multiple data sources",
    mcps=[
        "https://mcp.exa.ai/mcp?api_key=your_key&profile=your_profile",
        "crewai-amp:weather-service#current_conditions"
    ]
)

# Create task
research_task = Task(
    description="Research the latest developments in AI agent frameworks",
    expected_output="Comprehensive research report with citations",
    agent=research_agent
)

# Create and run crew
crew = Crew(agents=[research_agent], tasks=[research_task])
result = crew.kickoff()
```

### [​](#quick-start-with-structured-configurations) Quick Start with Structured Configurations

Copy

Ask AI

```
from crewai import Agent, Task, Crew
from crewai.mcp import MCPServerStdio, MCPServerHTTP, MCPServerSSE

# Create agent with structured MCP configurations
research_agent = Agent(
    role="Research Analyst",
    goal="Find and analyze information using advanced search tools",
    backstory="Expert researcher with access to multiple data sources",
    mcps=[
        # Local stdio server
        MCPServerStdio(
            command="python",
            args=["local_server.py"],
            env={"API_KEY": "your_key"},
        ),
        # Remote HTTP server
        MCPServerHTTP(
            url="https://api.research.com/mcp",
            headers={"Authorization": "Bearer your_token"},
        ),
    ]
)

# Create task
research_task = Task(
    description="Research the latest developments in AI agent frameworks",
    expected_output="Comprehensive research report with citations",
    agent=research_agent
)

# Create and run crew
crew = Crew(agents=[research_agent], tasks=[research_task])
result = crew.kickoff()
```

That’s it! The MCP tools are automatically discovered and available to your agent.

## [​](#mcp-reference-formats) MCP Reference Formats

The `mcps` field supports both **string references** (for quick setup) and **structured configurations** (for full control). You can mix both formats in the same list.

### [​](#string-based-references) String-Based References

#### [​](#external-mcp-servers) External MCP Servers

Copy

Ask AI

```
mcps=[
    # Full server - get all available tools
    "https://mcp.example.com/api",

    # Specific tool from server using # syntax
    "https://api.weather.com/mcp#get_current_weather",

    # Server with authentication parameters
    "https://mcp.exa.ai/mcp?api_key=your_key&profile=your_profile"
]
```

#### [​](#crewai-aop-marketplace) CrewAI AOP Marketplace

Copy

Ask AI

```
mcps=[
    # Full AMP MCP service - get all available tools
    "crewai-amp:financial-data",

    # Specific tool from AMP service using # syntax
    "crewai-amp:research-tools#pubmed_search",

    # Multiple AMP services
    "crewai-amp:weather-service",
    "crewai-amp:market-analysis"
]
```

### [​](#structured-configurations) Structured Configurations

#### [​](#stdio-transport-local-servers) Stdio Transport (Local Servers)

Perfect for local MCP servers that run as processes:

Copy

Ask AI

```
from crewai.mcp import MCPServerStdio
from crewai.mcp.filters import create_static_tool_filter

mcps=[
    MCPServerStdio(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
        env={"API_KEY": "your_key"},
        tool_filter=create_static_tool_filter(
            allowed_tool_names=["read_file", "write_file"]
        ),
        cache_tools_list=True,
    ),
    # Python-based server
    MCPServerStdio(
        command="python",
        args=["path/to/server.py"],
        env={"UV_PYTHON": "3.12", "API_KEY": "your_key"},
    ),
]
```

#### [​](#http/streamable-http-transport-remote-servers) HTTP/Streamable HTTP Transport (Remote Servers)

For remote MCP servers over HTTP/HTTPS:

Copy

Ask AI

```
from crewai.mcp import MCPServerHTTP

mcps=[
    # Streamable HTTP (default)
    MCPServerHTTP(
        url="https://api.example.com/mcp",
        headers={"Authorization": "Bearer your_token"},
        streamable=True,
        cache_tools_list=True,
    ),
    # Standard HTTP
    MCPServerHTTP(
        url="https://api.example.com/mcp",
        headers={"Authorization": "Bearer your_token"},
        streamable=False,
    ),
]
```

#### [​](#sse-transport-real-time-streaming) SSE Transport (Real-Time Streaming)

For remote servers using Server-Sent Events:

Copy

Ask AI

```
from crewai.mcp import MCPServerSSE

mcps=[
    MCPServerSSE(
        url="https://stream.example.com/mcp/sse",
        headers={"Authorization": "Bearer your_token"},
        cache_tools_list=True,
    ),
]
```

### [​](#mixed-references) Mixed References

You can combine string references and structured configurations:

Copy

Ask AI

```
from crewai.mcp import MCPServerStdio, MCPServerHTTP

mcps=[
    # String references
    "https://external-api.com/mcp",              # External server
    "crewai-amp:financial-insights",             # AMP service

    # Structured configurations
    MCPServerStdio(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
    ),
    MCPServerHTTP(
        url="https://api.example.com/mcp",
        headers={"Authorization": "Bearer token"},
    ),
]
```

### [​](#tool-filtering) Tool Filtering

Structured configurations support advanced tool filtering:

Copy

Ask AI

```
from crewai.mcp import MCPServerStdio
from crewai.mcp.filters import create_static_tool_filter, create_dynamic_tool_filter, ToolFilterContext

# Static filtering (allow/block lists)
static_filter = create_static_tool_filter(
    allowed_tool_names=["read_file", "write_file"],
    blocked_tool_names=["delete_file"],
)

# Dynamic filtering (context-aware)
def dynamic_filter(context: ToolFilterContext, tool: dict) -> bool:
    # Block dangerous tools for certain agent roles
    if context.agent.role == "Code Reviewer":
        if "delete" in tool.get("name", "").lower():
            return False
    return True

mcps=[
    MCPServerStdio(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
        tool_filter=static_filter,  # or dynamic_filter
    ),
]
```

## [​](#configuration-parameters) Configuration Parameters

Each transport type supports specific configuration options:

### [​](#mcpserverstdio-parameters) MCPServerStdio Parameters

* **`command`** (required): Command to execute (e.g., `"python"`, `"node"`, `"npx"`, `"uvx"`)
* **`args`** (optional): List of command arguments (e.g., `["server.py"]` or `["-y", "@mcp/server"]`)
* **`env`** (optional): Dictionary of environment variables to pass to the process
* **`tool_filter`** (optional): Tool filter function for filtering available tools
* **`cache_tools_list`** (optional): Whether to cache the tool list for faster subsequent access (default: `False`)

### [​](#mcpserverhttp-parameters) MCPServerHTTP Parameters

* **`url`** (required): Server URL (e.g., `"https://api.example.com/mcp"`)
* **`headers`** (optional): Dictionary of HTTP headers for authentication or other purposes
* **`streamable`** (optional): Whether to use streamable HTTP transport (default: `True`)
* **`tool_filter`** (optional): Tool filter function for filtering available tools
* **`cache_tools_list`** (optional): Whether to cache the tool list for faster subsequent access (default: `False`)

### [​](#mcpserversse-parameters) MCPServerSSE Parameters

* **`url`** (required): Server URL (e.g., `"https://api.example.com/mcp/sse"`)
* **`headers`** (optional): Dictionary of HTTP headers for authentication or other purposes
* **`tool_filter`** (optional): Tool filter function for filtering available tools
* **`cache_tools_list`** (optional): Whether to cache the tool list for faster subsequent access (default: `False`)

### [​](#common-parameters) Common Parameters

All transport types support:

* **`tool_filter`**: Filter function to control which tools are available. Can be:
  + `None` (default): All tools are available
  + Static filter: Created with `create_static_tool_filter()` for allow/block lists
  + Dynamic filter: Created with `create_dynamic_tool_filter()` for context-aware filtering
* **`cache_tools_list`**: When `True`, caches the tool list after first discovery to improve performance on subsequent connections

## [​](#key-features) Key Features

* 🔄 **Automatic Tool Discovery**: Tools are automatically discovered and integrated
* 🏷️ **Name Collision Prevention**: Server names are prefixed to tool names
* ⚡ **Performance Optimized**: On-demand connections with schema caching
* 🛡️ **Error Resilience**: Graceful handling of unavailable servers
* ⏱️ **Timeout Protection**: Built-in timeouts prevent hanging connections
* 📊 **Transparent Integration**: Works seamlessly with existing CrewAI features
* 🔧 **Full Transport Support**: Stdio, HTTP/Streamable HTTP, and SSE transports
* 🎯 **Advanced Filtering**: Static and dynamic tool filtering capabilities
* 🔐 **Flexible Authentication**: Support for headers, environment variables, and query parameters

## [​](#error-handling) Error Handling

The MCP DSL integration is designed to be resilient and handles failures gracefully:

Copy

Ask AI

```
from crewai import Agent
from crewai.mcp import MCPServerStdio, MCPServerHTTP

agent = Agent(
    role="Resilient Agent",
    goal="Continue working despite server issues",
    backstory="Agent that handles failures gracefully",
    mcps=[
        # String references
        "https://reliable-server.com/mcp",        # Will work
        "https://unreachable-server.com/mcp",     # Will be skipped gracefully
        "crewai-amp:working-service",             # Will work

        # Structured configs
        MCPServerStdio(
            command="python",
            args=["reliable_server.py"],          # Will work
        ),
        MCPServerHTTP(
            url="https://slow-server.com/mcp",     # Will timeout gracefully
        ),
    ]
)
# Agent will use tools from working servers and log warnings for failing ones
```

All connection errors are handled gracefully:

* **Connection failures**: Logged as warnings, agent continues with available tools
* **Timeout errors**: Connections timeout after 30 seconds (configurable)
* **Authentication errors**: Logged clearly for debugging
* **Invalid configurations**: Validation errors are raised at agent creation time

## [​](#advanced:-mcpserveradapter) Advanced: MCPServerAdapter

For complex scenarios requiring manual connection management, use the `MCPServerAdapter` class from `crewai-tools`. Using a Python context manager (`with` statement) is the recommended approach as it automatically handles starting and stopping the connection to the MCP server.

## [​](#connection-configuration) Connection Configuration

The `MCPServerAdapter` supports several configuration options to customize the connection behavior:

* **`connect_timeout`** (optional): Maximum time in seconds to wait for establishing a connection to the MCP server. Defaults to 30 seconds if not specified. This is particularly useful for remote servers that may have variable response times.

Copy

Ask AI

```
# Example with custom connection timeout
with MCPServerAdapter(server_params, connect_timeout=60) as tools:
    # Connection will timeout after 60 seconds if not established
    pass
```

Copy

Ask AI

```
from crewai import Agent
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters # For Stdio Server

# Example server_params (choose one based on your server type):
# 1. Stdio Server:
server_params=StdioServerParameters(
    command="python3",
    args=["servers/your_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

# 2. SSE Server:
server_params = {
    "url": "http://localhost:8000/sse",
    "transport": "sse"
}

# 3. Streamable HTTP Server:
server_params = {
    "url": "http://localhost:8001/mcp",
    "transport": "streamable-http"
}

# Example usage (uncomment and adapt once server_params is set):
with MCPServerAdapter(server_params, connect_timeout=60) as mcp_tools:
    print(f"Available tools: {[tool.name for tool in mcp_tools]}")

    my_agent = Agent(
        role="MCP Tool User",
        goal="Utilize tools from an MCP server.",
        backstory="I can connect to MCP servers and use their tools.",
        tools=mcp_tools, # Pass the loaded tools to your agent
        reasoning=True,
        verbose=True
    )
    # ... rest of your crew setup ...
```

This general pattern shows how to integrate tools. For specific examples tailored to each transport, refer to the detailed guides below.

## [​](#filtering-tools) Filtering Tools

There are two ways to filter tools:

1. Accessing a specific tool using dictionary-style indexing.
2. Pass a list of tool names to the `MCPServerAdapter` constructor.

### [​](#accessing-a-specific-tool-using-dictionary-style-indexing) Accessing a specific tool using dictionary-style indexing.

Copy

Ask AI

```
with MCPServerAdapter(server_params, connect_timeout=60) as mcp_tools:
    print(f"Available tools: {[tool.name for tool in mcp_tools]}")

    my_agent = Agent(
        role="MCP Tool User",
        goal="Utilize tools from an MCP server.",
        backstory="I can connect to MCP servers and use their tools.",
        tools=[mcp_tools["tool_name"]], # Pass the loaded tools to your agent
        reasoning=True,
        verbose=True
    )
    # ... rest of your crew setup ...
```

### [​](#pass-a-list-of-tool-names-to-the-mcpserveradapter-constructor) Pass a list of tool names to the `MCPServerAdapter` constructor.

Copy

Ask AI

```
with MCPServerAdapter(server_params, "tool_name", connect_timeout=60) as mcp_tools:
    print(f"Available tools: {[tool.name for tool in mcp_tools]}")

    my_agent = Agent(
        role="MCP Tool User",
        goal="Utilize tools from an MCP server.",
        backstory="I can connect to MCP servers and use their tools.",
        tools=mcp_tools, # Pass the loaded tools to your agent
        reasoning=True,
        verbose=True
    )
    # ... rest of your crew setup ...
```

## [​](#using-with-crewbase) Using with CrewBase

To use MCPServer tools within a CrewBase class, use the `get_mcp_tools` method. Server configurations should be provided via the `mcp_server_params` attribute. You can pass either a single configuration or a list of multiple server configurations.

Copy

Ask AI

```
@CrewBase
class CrewWithMCP:
  # ... define your agents and tasks config file ...

  mcp_server_params = [
    # Streamable HTTP Server
    {
        "url": "http://localhost:8001/mcp",
        "transport": "streamable-http"
    },
    # SSE Server
    {
        "url": "http://localhost:8000/sse",
        "transport": "sse"
    },
    # StdIO Server
    StdioServerParameters(
        command="python3",
        args=["servers/your_stdio_server.py"],
        env={"UV_PYTHON": "3.12", **os.environ},
    )
  ]

  @agent
  def your_agent(self):
      return Agent(config=self.agents_config["your_agent"], tools=self.get_mcp_tools()) # get all available tools

    # ... rest of your crew setup ...
```

When a crew class is decorated with `@CrewBase`, the adapter lifecycle is managed for you:

* The first call to `get_mcp_tools()` lazily creates a shared `MCPServerAdapter` that is reused by every agent in the crew.
* The adapter automatically shuts down after `.kickoff()` completes thanks to an implicit after-kickoff hook injected by `@CrewBase`, so no manual cleanup is required.
* If `mcp_server_params` is not defined, `get_mcp_tools()` simply returns an empty list, allowing the same code paths to run with or without MCP configured.

This makes it safe to call `get_mcp_tools()` from multiple agent methods or selectively enable MCP per environment.

### [​](#connection-timeout-configuration) Connection Timeout Configuration

You can configure the connection timeout for MCP servers by setting the `mcp_connect_timeout` class attribute. If no timeout is specified, it defaults to 30 seconds.

Copy

Ask AI

```
@CrewBase
class CrewWithMCP:
  mcp_server_params = [...]
  mcp_connect_timeout = 60  # 60 seconds timeout for all MCP connections

  @agent
  def your_agent(self):
      return Agent(config=self.agents_config["your_agent"], tools=self.get_mcp_tools())
```

Copy

Ask AI

```
@CrewBase
class CrewWithDefaultTimeout:
  mcp_server_params = [...]
  # No mcp_connect_timeout specified - uses default 30 seconds

  @agent
  def your_agent(self):
      return Agent(config=self.agents_config["your_agent"], tools=self.get_mcp_tools())
```

### [​](#filtering-tools-2) Filtering Tools

You can filter which tools are available to your agent by passing a list of tool names to the `get_mcp_tools` method.

Copy

Ask AI

```
@agent
def another_agent(self):
    return Agent(
      config=self.agents_config["your_agent"],
      tools=self.get_mcp_tools("tool_1", "tool_2") # get specific tools
    )
```

The timeout configuration applies to all MCP tool calls within the crew:

Copy

Ask AI

```
@CrewBase
class CrewWithCustomTimeout:
  mcp_server_params = [...]
  mcp_connect_timeout = 90  # 90 seconds timeout for all MCP connections

  @agent
  def filtered_agent(self):
      return Agent(
        config=self.agents_config["your_agent"],
        tools=self.get_mcp_tools("tool_1", "tool_2") # specific tools with custom timeout
      )
```

## [​](#explore-mcp-integrations) Explore MCP Integrations

[## Simple DSL Integration

**Recommended**: Use the simple `mcps=[]` field syntax for effortless MCP integration.](/en/mcp/dsl-integration)[## Stdio Transport

Connect to local MCP servers via standard input/output. Ideal for scripts and local executables.](/en/mcp/stdio)[## SSE Transport

Integrate with remote MCP servers using Server-Sent Events for real-time data streaming.](/en/mcp/sse)[## Streamable HTTP Transport

Utilize flexible Streamable HTTP for robust communication with remote MCP servers.](/en/mcp/streamable-http)[## Connecting to Multiple Servers

Aggregate tools from several MCP servers simultaneously using a single adapter.](/en/mcp/multiple-servers)[## Security Considerations

Review important security best practices for MCP integration to keep your agents safe.](/en/mcp/security)

Checkout this repository for full demos and examples of MCP integration with CrewAI! 👇
[## GitHub Repository

CrewAI MCP Demo](https://github.com/tonykipkemboi/crewai-mcp-demo)

## [​](#staying-safe-with-mcp) Staying Safe with MCP

Always ensure that you trust an MCP Server before using it.

#### [​](#security-warning:-dns-rebinding-attacks) Security Warning: DNS Rebinding Attacks

SSE transports can be vulnerable to DNS rebinding attacks if not properly secured.
To prevent this:

1. **Always validate Origin headers** on incoming SSE connections to ensure they come from expected sources
2. **Avoid binding servers to all network interfaces** (0.0.0.0) when running locally - bind only to localhost (127.0.0.1) instead
3. **Implement proper authentication** for all SSE connections

Without these protections, attackers could use DNS rebinding to interact with local MCP servers from remote websites.
For more details, see the [Anthropic’s MCP Transport Security docs](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations).

### [​](#limitations) Limitations

* **Supported Primitives**: Currently, `MCPServerAdapter` primarily supports adapting MCP `tools`.
  Other MCP primitives like `prompts` or `resources` are not directly integrated as CrewAI components through this adapter at this time.
* **Output Handling**: The adapter typically processes the primary text output from an MCP tool (e.g., `.content[0].text`). Complex or multi-modal outputs might require custom handling if not fitting this pattern.

Was this page helpful?

YesNo

[Event Listeners

Previous](/en/concepts/event-listener)[MCP DSL Integration

Next](/en/mcp/dsl-integration)

⌘I