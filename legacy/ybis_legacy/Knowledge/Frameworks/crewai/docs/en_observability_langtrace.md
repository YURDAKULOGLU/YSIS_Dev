Langtrace Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

Langtrace Integration

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

# [​](#langtrace-overview) Langtrace Overview

Langtrace is an open-source, external tool that helps you set up observability and evaluations for Large Language Models (LLMs), LLM frameworks, and Vector Databases.
While not built directly into CrewAI, Langtrace can be used alongside CrewAI to gain deep visibility into the cost, latency, and performance of your CrewAI Agents.
This integration allows you to log hyperparameters, monitor performance regressions, and establish a process for continuous improvement of your Agents.
![Overview of a select series of agent session runs](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/langtrace1.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=85b67e42028ca9383087737279f8931f)
![Overview of agent traces](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/langtrace2.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=24f08e5c56b6200e386d305a7bee347c)
![Overview of llm traces in details](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/langtrace3.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=f1a8624e0c05d59deded640e4751a986)

## [​](#setup-instructions) Setup Instructions

1

Sign up for Langtrace

Sign up by visiting <https://langtrace.ai/signup>.

2

Create a project

Set the project type to `CrewAI` and generate an API key.

3

Install Langtrace in your CrewAI project

Use the following command:

Copy

Ask AI

```
pip install langtrace-python-sdk
```

4

Import Langtrace

Import and initialize Langtrace at the beginning of your script, before any CrewAI imports:

Copy

Ask AI

```
from langtrace_python_sdk import langtrace
langtrace.init(api_key='<LANGTRACE_API_KEY>')

# Now import CrewAI modules
from crewai import Agent, Task, Crew
```

### [​](#features-and-their-application-to-crewai) Features and Their Application to CrewAI

1. **LLM Token and Cost Tracking**
   * Monitor the token usage and associated costs for each CrewAI agent interaction.
2. **Trace Graph for Execution Steps**
   * Visualize the execution flow of your CrewAI tasks, including latency and logs.
   * Useful for identifying bottlenecks in your agent workflows.
3. **Dataset Curation with Manual Annotation**
   * Create datasets from your CrewAI task outputs for future training or evaluation.
4. **Prompt Versioning and Management**
   * Keep track of different versions of prompts used in your CrewAI agents.
   * Useful for A/B testing and optimizing agent performance.
5. **Prompt Playground with Model Comparisons**
   * Test and compare different prompts and models for your CrewAI agents before deployment.
6. **Testing and Evaluations**
   * Set up automated tests for your CrewAI agents and tasks.

Was this page helpful?

YesNo

[Langfuse Integration

Previous](/en/observability/langfuse)[Maxim Integration

Next](/en/observability/maxim)

⌘I