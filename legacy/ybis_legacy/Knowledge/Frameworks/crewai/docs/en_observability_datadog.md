Datadog Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

Datadog Integration

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

# [​](#integrate-datadog-with-crewai) Integrate Datadog with CrewAI

This guide will demonstrate how to integrate **[Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/)** with **CrewAI** using [Datadog auto-instrumentation](https://docs.datadoghq.com/llm_observability/instrumentation/auto_instrumentation?tab=python). By the end of this guide, you will be able to submit LLM Observability traces to Datadog and view your CrewAI agent runs in Datadog LLM Observability’s [Agentic Execution View](https://docs.datadoghq.com/llm_observability/monitoring/agent_monitoring).

## [​](#what-is-datadog-llm-observability) What is Datadog LLM Observability?

[Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/) helps AI engineers, data scientists, and application developers quickly develop, evaluate, and monitor LLM applications. Confidently improve output quality, performance, costs, and overall risk with structured experiments, end-to-end tracing across AI agents, and evaluations.

## [​](#getting-started) Getting Started

### [​](#install-dependencies) Install Dependencies

Copy

Ask AI

```
pip install ddtrace crewai crewai-tools
```

### [​](#set-environment-variables) Set Environment Variables

If you do not have a Datadog API key, you can [create an account](https://www.datadoghq.com/) and [get your API key](https://docs.datadoghq.com/account_management/api-app-keys/#api-keys).
You will also need to specify an ML Application name in the following environment variables. An ML Application is a grouping of LLM Observability traces associated with a specific LLM-based application. See [ML Application Naming Guidelines](https://docs.datadoghq.com/llm_observability/instrumentation/sdk?tab=python#application-naming-guidelines) for more information on limitations with ML Application names.

Copy

Ask AI

```
export DD_API_KEY=<YOUR_DD_API_KEY>
export DD_SITE=<YOUR_DD_SITE>
export DD_LLMOBS_ENABLED=true
export DD_LLMOBS_ML_APP=<YOUR_ML_APP_NAME>
export DD_LLMOBS_AGENTLESS_ENABLED=true
export DD_APM_TRACING_ENABLED=false
```

Additionally, configure any LLM provider API keys

Copy

Ask AI

```
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
export ANTHROPIC_API_KEY=<YOUR_ANTHROPIC_API_KEY>
export GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
...
```

### [​](#create-a-crewai-agent-application) Create a CrewAI Agent Application

Copy

Ask AI

```
# crewai_agent.py
from crewai import Agent, Task, Crew

from crewai_tools import (
    WebsiteSearchTool
)

web_rag_tool = WebsiteSearchTool()

writer = Agent(
    role="Writer",
    goal="You make math engaging and understandable for young children through poetry",
    backstory="You're an expert in writing haikus but you know nothing of math.",
    tools=[web_rag_tool],
)

task = Task(
    description=("What is {multiplication}?"),
    expected_output=("Compose a haiku that includes the answer."),
    agent=writer
)

crew = Crew(
    agents=[writer],
    tasks=[task],
    share_crew=False
)

output = crew.kickoff(dict(multiplication="2 * 2"))
```

### [​](#run-the-application-with-datadog-auto-instrumentation) Run the Application with Datadog Auto-Instrumentation

With the [environment variables](#set-environment-variables) set, you can now run the application with Datadog auto-instrumentation.

Copy

Ask AI

```
ddtrace-run python crewai_agent.py
```

### [​](#view-the-traces-in-datadog) View the Traces in Datadog

After running the application, you can view the traces in [Datadog LLM Observability’s Traces View](https://app.datadoghq.com/llm/traces), selecting the ML Application name you chose from the top-left dropdown.
Clicking on a trace will show you the details of the trace, including total tokens used, number of LLM calls, models used, and estimated cost. Clicking into a specific span will narrow down these details, and show related input, output, and metadata.

![Datadog LLM Observability Trace View](https://mintcdn.com/crewai/YHPIyIjbLg-0Yd_V/images/datadog-llm-observability-1.png?fit=max&auto=format&n=YHPIyIjbLg-0Yd_V&q=85&s=12b76bf2631c8b24ed6828053b125074)

Additionally, you can view the execution graph view of the trace, which shows the control and data flow of the trace, which will scale with larger agents to show handoffs and relationships between LLM calls, tool calls, and agent interactions.

![Datadog LLM Observability Agent Execution Flow View](https://mintcdn.com/crewai/YHPIyIjbLg-0Yd_V/images/datadog-llm-observability-2.png?fit=max&auto=format&n=YHPIyIjbLg-0Yd_V&q=85&s=01a94c3f9f162ce0b918fa6039f6fa8e)

## [​](#references) References

* [Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/)
* [Datadog LLM Observability CrewAI Auto-Instrumentation](https://docs.datadoghq.com/llm_observability/instrumentation/auto_instrumentation?tab=python#crew-ai)

Was this page helpful?

YesNo

[Braintrust

Previous](/en/observability/braintrust)[LangDB Integration

Next](/en/observability/langdb)

⌘I