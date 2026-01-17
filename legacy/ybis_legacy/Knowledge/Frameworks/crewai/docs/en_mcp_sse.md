SSE Transport - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

MCP Integration

SSE Transport

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

Server-Sent Events (SSE) provide a standard way for a web server to send updates to a client over a single, long-lived HTTP connection. In the context of MCP, SSE is used for remote servers to stream data (like tool responses) to your CrewAI application in real-time.

## [​](#key-concepts) Key Concepts

* **Remote Servers**: SSE is suitable for MCP servers hosted remotely.
* **Unidirectional Stream**: Typically, SSE is a one-way communication channel from server to client.
* **`MCPServerAdapter` Configuration**: For SSE, you’ll provide the server’s URL and specify the transport type.

## [​](#connecting-via-sse) Connecting via SSE

You can connect to an SSE-based MCP server using two main approaches for managing the connection lifecycle:

### [​](#1-fully-managed-connection-recommended) 1. Fully Managed Connection (Recommended)

Using a Python context manager (`with` statement) is the recommended approach. It automatically handles establishing and closing the connection to the SSE MCP server.

Copy

Ask AI

```
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8000/sse", # Replace with your actual SSE server URL
    "transport": "sse" 
}

# Using MCPServerAdapter with a context manager
try:
    with MCPServerAdapter(server_params) as tools:
        print(f"Available tools from SSE MCP server: {[tool.name for tool in tools]}")

        # Example: Using a tool from the SSE MCP server
        sse_agent = Agent(
            role="Remote Service User",
            goal="Utilize a tool provided by a remote SSE MCP server.",
            backstory="An AI agent that connects to external services via SSE.",
            tools=tools,
            reasoning=True,
            verbose=True,
        )

        sse_task = Task(
            description="Fetch real-time stock updates for 'AAPL' using an SSE tool.",
            expected_output="The latest stock price for AAPL.",
            agent=sse_agent,
            markdown=True
        )

        sse_crew = Crew(
            agents=[sse_agent],
            tasks=[sse_task],
            verbose=True,
            process=Process.sequential
        )
        
        if tools: # Only kickoff if tools were loaded
            result = sse_crew.kickoff() # Add inputs={'stock_symbol': 'AAPL'} if tool requires it
            print("\nCrew Task Result (SSE - Managed):\n", result)
        else:
            print("Skipping crew kickoff as tools were not loaded (check server connection).")

except Exception as e:
    print(f"Error connecting to or using SSE MCP server (Managed): {e}")
    print("Ensure the SSE MCP server is running and accessible at the specified URL.")
```

Replace `"http://localhost:8000/sse"` with the actual URL of your SSE MCP server.

### [​](#2-manual-connection-lifecycle) 2. Manual Connection Lifecycle

If you need finer-grained control, you can manage the `MCPServerAdapter` connection lifecycle manually.

You **MUST** call `mcp_server_adapter.stop()` to ensure the connection is closed and resources are released. Using a `try...finally` block is highly recommended.

Copy

Ask AI

```
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8000/sse", # Replace with your actual SSE server URL
    "transport": "sse"
}

mcp_server_adapter = None 
try:
    mcp_server_adapter = MCPServerAdapter(server_params)
    mcp_server_adapter.start()
    tools = mcp_server_adapter.tools
    print(f"Available tools (manual SSE): {[tool.name for tool in tools]}")

    manual_sse_agent = Agent(
        role="Remote Data Analyst",
        goal="Analyze data fetched from a remote SSE MCP server using manual connection management.",
        backstory="An AI skilled in handling SSE connections explicitly.",
        tools=tools,
        verbose=True
    )
    
    analysis_task = Task(
        description="Fetch and analyze the latest user activity trends from the SSE server.",
        expected_output="A summary report of user activity trends.",
        agent=manual_sse_agent
    )
    
    analysis_crew = Crew(
        agents=[manual_sse_agent],
        tasks=[analysis_task],
        verbose=True,
        process=Process.sequential
    )
    
    result = analysis_crew.kickoff()
    print("\nCrew Task Result (SSE - Manual):\n", result)

except Exception as e:
    print(f"An error occurred during manual SSE MCP integration: {e}")
    print("Ensure the SSE MCP server is running and accessible.")
finally:
    if mcp_server_adapter and mcp_server_adapter.is_connected:
        print("Stopping SSE MCP server connection (manual)...")
        mcp_server_adapter.stop()  # **Crucial: Ensure stop is called**
    elif mcp_server_adapter:
        print("SSE MCP server adapter was not connected. No stop needed or start failed.")
```

## [​](#security-considerations-for-sse) Security Considerations for SSE

**DNS Rebinding Attacks**: SSE transports can be vulnerable to DNS rebinding attacks if the MCP server is not properly secured. This could allow malicious websites to interact with local or intranet-based MCP servers.

To mitigate this risk:

* MCP server implementations should **validate `Origin` headers** on incoming SSE connections.
* When running local SSE MCP servers for development, **bind only to `localhost` (`127.0.0.1`)** rather than all network interfaces (`0.0.0.0`).
* Implement **proper authentication** for all SSE connections if they expose sensitive tools or data.

For a comprehensive overview of security best practices, please refer to our [Security Considerations](./security.mdx) page and the official [MCP Transport Security documentation](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations).

Was this page helpful?

YesNo

[Stdio Transport

Previous](/en/mcp/stdio)[Streamable HTTP Transport

Next](/en/mcp/streamable-http)

⌘I