Streamable HTTP Transport - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

MCP Integration

Streamable HTTP Transport

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

Streamable HTTP transport provides a flexible way to connect to remote MCP servers. It’s often built upon HTTP and can support various communication patterns, including request-response and streaming, sometimes utilizing Server-Sent Events (SSE) for server-to-client streams within a broader HTTP interaction.

## [​](#key-concepts) Key Concepts

* **Remote Servers**: Designed for MCP servers hosted remotely.
* **Flexibility**: Can support more complex interaction patterns than plain SSE, potentially including bi-directional communication if the server implements it.
* **`MCPServerAdapter` Configuration**: You’ll need to provide the server’s base URL for MCP communication and specify `"streamable-http"` as the transport type.

## [​](#connecting-via-streamable-http) Connecting via Streamable HTTP

You have two primary methods for managing the connection lifecycle with a Streamable HTTP MCP server:

### [​](#1-fully-managed-connection-recommended) 1. Fully Managed Connection (Recommended)

The recommended approach is to use a Python context manager (`with` statement), which handles the connection’s setup and teardown automatically.

Copy

Ask AI

```
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8001/mcp", # Replace with your actual Streamable HTTP server URL
    "transport": "streamable-http"
}

try:
    with MCPServerAdapter(server_params) as tools:
        print(f"Available tools from Streamable HTTP MCP server: {[tool.name for tool in tools]}")

        http_agent = Agent(
            role="HTTP Service Integrator",
            goal="Utilize tools from a remote MCP server via Streamable HTTP.",
            backstory="An AI agent adept at interacting with complex web services.",
            tools=tools,
            verbose=True,
        )

        http_task = Task(
            description="Perform a complex data query using a tool from the Streamable HTTP server.",
            expected_output="The result of the complex data query.",
            agent=http_agent,
        )

        http_crew = Crew(
            agents=[http_agent],
            tasks=[http_task],
            verbose=True,
            process=Process.sequential
        )
        
        result = http_crew.kickoff() 
        print("\nCrew Task Result (Streamable HTTP - Managed):\n", result)

except Exception as e:
    print(f"Error connecting to or using Streamable HTTP MCP server (Managed): {e}")
    print("Ensure the Streamable HTTP MCP server is running and accessible at the specified URL.")
```

**Note:** Replace `"http://localhost:8001/mcp"` with the actual URL of your Streamable HTTP MCP server.

### [​](#2-manual-connection-lifecycle) 2. Manual Connection Lifecycle

For scenarios requiring more explicit control, you can manage the `MCPServerAdapter` connection manually.

It is **critical** to call `mcp_server_adapter.stop()` when you are done to close the connection and free up resources. A `try...finally` block is the safest way to ensure this.

Copy

Ask AI

```
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8001/mcp", # Replace with your actual Streamable HTTP server URL
    "transport": "streamable-http"
}

mcp_server_adapter = None 
try:
    mcp_server_adapter = MCPServerAdapter(server_params)
    mcp_server_adapter.start()
    tools = mcp_server_adapter.tools
    print(f"Available tools (manual Streamable HTTP): {[tool.name for tool in tools]}")

    manual_http_agent = Agent(
        role="Advanced Web Service User",
        goal="Interact with an MCP server using manually managed Streamable HTTP connections.",
        backstory="An AI specialist in fine-tuning HTTP-based service integrations.",
        tools=tools,
        verbose=True
    )
    
    data_processing_task = Task(
        description="Submit data for processing and retrieve results via Streamable HTTP.",
        expected_output="Processed data or confirmation.",
        agent=manual_http_agent
    )
    
    data_crew = Crew(
        agents=[manual_http_agent],
        tasks=[data_processing_task],
        verbose=True,
        process=Process.sequential
    )
    
    result = data_crew.kickoff()
    print("\nCrew Task Result (Streamable HTTP - Manual):\n", result)

except Exception as e:
    print(f"An error occurred during manual Streamable HTTP MCP integration: {e}")
    print("Ensure the Streamable HTTP MCP server is running and accessible.")
finally:
    if mcp_server_adapter and mcp_server_adapter.is_connected:
        print("Stopping Streamable HTTP MCP server connection (manual)...")
        mcp_server_adapter.stop()  # **Crucial: Ensure stop is called**
    elif mcp_server_adapter:
        print("Streamable HTTP MCP server adapter was not connected. No stop needed or start failed.")
```

## [​](#security-considerations) Security Considerations

When using Streamable HTTP transport, general web security best practices are paramount:

* **Use HTTPS**: Always prefer HTTPS (HTTP Secure) for your MCP server URLs to encrypt data in transit.
* **Authentication**: Implement robust authentication mechanisms if your MCP server exposes sensitive tools or data.
* **Input Validation**: Ensure your MCP server validates all incoming requests and parameters.

For a comprehensive guide on securing your MCP integrations, please refer to our [Security Considerations](./security.mdx) page and the official [MCP Transport Security documentation](https://modelcontextprotocol.io/docs/concepts/transports#security-considerations).

Was this page helpful?

YesNo

[SSE Transport

Previous](/en/mcp/sse)[Connecting to Multiple MCP Servers

Next](/en/mcp/multiple-servers)

⌘I