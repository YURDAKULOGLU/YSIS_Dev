Stdio Transport - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

MCP Integration

Stdio Transport

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

The Stdio (Standard Input/Output) transport is designed for connecting `MCPServerAdapter` to local MCP servers that communicate over their standard input and output streams. This is typically used when the MCP server is a script or executable running on the same machine as your CrewAI application.

## [​](#key-concepts) Key Concepts

* **Local Execution**: Stdio transport manages a locally running process for the MCP server.
* **`StdioServerParameters`**: This class from the `mcp` library is used to configure the command, arguments, and environment variables for launching the Stdio server.

## [​](#connecting-via-stdio) Connecting via Stdio

You can connect to an Stdio-based MCP server using two main approaches for managing the connection lifecycle:

### [​](#1-fully-managed-connection-recommended) 1. Fully Managed Connection (Recommended)

Using a Python context manager (`with` statement) is the recommended approach. It automatically handles starting the MCP server process and stopping it when the context is exited.

Copy

Ask AI

```
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
import os

# Create a StdioServerParameters object
server_params=StdioServerParameters(
    command="python3", 
    args=["servers/your_stdio_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

with MCPServerAdapter(server_params) as tools:
    print(f"Available tools from Stdio MCP server: {[tool.name for tool in tools]}")

    # Example: Using the tools from the Stdio MCP server in a CrewAI Agent
    research_agent = Agent(
        role="Local Data Processor",
        goal="Process data using a local Stdio-based tool.",
        backstory="An AI that leverages local scripts via MCP for specialized tasks.",
        tools=tools,
        reasoning=True,
        verbose=True,
    )
    
    processing_task = Task(
        description="Process the input data file 'data.txt' and summarize its contents.",
        expected_output="A summary of the processed data.",
        agent=research_agent,
        markdown=True
    )
    
    data_crew = Crew(
        agents=[research_agent],
        tasks=[processing_task],
        verbose=True,
        process=Process.sequential 
    )
   
    result = data_crew.kickoff()
    print("\nCrew Task Result (Stdio - Managed):\n", result)
```

### [​](#2-manual-connection-lifecycle) 2. Manual Connection Lifecycle

If you need finer-grained control over when the Stdio MCP server process is started and stopped, you can manage the `MCPServerAdapter` lifecycle manually.

You **MUST** call `mcp_server_adapter.stop()` to ensure the server process is terminated and resources are released. Using a `try...finally` block is highly recommended.

Copy

Ask AI

```
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
import os

# Create a StdioServerParameters object
stdio_params=StdioServerParameters(
    command="python3", 
    args=["servers/your_stdio_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

mcp_server_adapter = MCPServerAdapter(server_params=stdio_params)
try:
    mcp_server_adapter.start()  # Manually start the connection and server process
    tools = mcp_server_adapter.tools
    print(f"Available tools (manual Stdio): {[tool.name for tool in tools]}")

    # Example: Using the tools with your Agent, Task, Crew setup
    manual_agent = Agent(
        role="Local Task Executor",
        goal="Execute a specific local task using a manually managed Stdio tool.",
        backstory="An AI proficient in controlling local processes via MCP.",
        tools=tools,
        verbose=True
    )
    
    manual_task = Task(
        description="Execute the 'perform_analysis' command via the Stdio tool.",
        expected_output="Results of the analysis.",
        agent=manual_agent
    )
    
    manual_crew = Crew(
        agents=[manual_agent],
        tasks=[manual_task],
        verbose=True,
        process=Process.sequential
    )
        
       
    result = manual_crew.kickoff() # Actual inputs depend on your tool
    print("\nCrew Task Result (Stdio - Manual):\n", result)
            
except Exception as e:
    print(f"An error occurred during manual Stdio MCP integration: {e}")
finally:
    if mcp_server_adapter and mcp_server_adapter.is_connected: # Check if connected before stopping
        print("Stopping Stdio MCP server connection (manual)...")
        mcp_server_adapter.stop()  # **Crucial: Ensure stop is called**
    elif mcp_server_adapter: # If adapter exists but not connected (e.g. start failed)
        print("Stdio MCP server adapter was not connected. No stop needed or start failed.")
```

Remember to replace placeholder paths and commands with your actual Stdio server details. The `env` parameter in `StdioServerParameters` can
be used to set environment variables for the server process, which can be useful for configuring its behavior or providing necessary paths (like `PYTHONPATH`).

Was this page helpful?

YesNo

[MCP DSL Integration

Previous](/en/mcp/dsl-integration)[SSE Transport

Next](/en/mcp/sse)

⌘I