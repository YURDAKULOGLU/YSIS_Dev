Weave Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

Weave Integration

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

# [​](#weave-overview) Weave Overview

[Weights & Biases (W&B) Weave](https://weave-docs.wandb.ai/) is a framework for tracking, experimenting with, evaluating, deploying, and improving LLM-based applications.
![Overview of W&B Weave CrewAI tracing usage](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/weave-tracing.gif?s=4a933830e3e3cf146c4c87cb44d46475)
Weave provides comprehensive support for every stage of your CrewAI application development:

* **Tracing & Monitoring**: Automatically track LLM calls and application logic to debug and analyze production systems
* **Systematic Iteration**: Refine and iterate on prompts, datasets, and models
* **Evaluation**: Use custom or pre-built scorers to systematically assess and enhance agent performance
* **Guardrails**: Protect your agents with pre- and post-safeguards for content moderation and prompt safety

Weave automatically captures traces for your CrewAI applications, enabling you to monitor and analyze your agents’ performance, interactions, and execution flow. This helps you build better evaluation datasets and optimize your agent workflows.

## [​](#setup-instructions) Setup Instructions

1

Install required packages

Copy

Ask AI

```
pip install crewai weave
```

2

Set up W&B Account

Sign up for a [Weights & Biases account](https://wandb.ai) if you haven’t already. You’ll need this to view your traces and metrics.

3

Initialize Weave in Your Application

Add the following code to your application:

Copy

Ask AI

```
import weave

# Initialize Weave with your project name
weave.init(project_name="crewai_demo")
```

After initialization, Weave will provide a URL where you can view your traces and metrics.

4

Create your Crews/Flows

Copy

Ask AI

```
from crewai import Agent, Task, Crew, LLM, Process

# Create an LLM with a temperature of 0 to ensure deterministic outputs
llm = LLM(model="gpt-4o", temperature=0)

# Create agents
researcher = Agent(
    role='Research Analyst',
    goal='Find and analyze the best investment opportunities',
    backstory='Expert in financial analysis and market research',
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

writer = Agent(
    role='Report Writer',
    goal='Write clear and concise investment reports',
    backstory='Experienced in creating detailed financial reports',
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Create tasks
research_task = Task(
    description='Deep research on the {topic}',
    expected_output='Comprehensive market data including key players, market size, and growth trends.',
    agent=researcher
)

writing_task = Task(
    description='Write a detailed report based on the research',
    expected_output='The report should be easy to read and understand. Use bullet points where applicable.',
    agent=writer
)

# Create a crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True,
    process=Process.sequential,
)

# Run the crew
result = crew.kickoff(inputs={"topic": "AI in material science"})
print(result)
```

5

View Traces in Weave

After running your CrewAI application, visit the Weave URL provided during initialization to view:

* LLM calls and their metadata
* Agent interactions and task execution flow
* Performance metrics like latency and token usage
* Any errors or issues that occurred during execution

![Weave tracing example with CrewAI](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/weave-tracing.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=f59e556fcc0ac8fcca8eaeef4c0551ae)

Weave Tracing Dashboard

## [​](#features) Features

* Weave automatically captures all CrewAI operations: agent interactions and task executions; LLM calls with metadata and token usage; tool usage and results.
* The integration supports all CrewAI execution methods: `kickoff()`, `kickoff_for_each()`, `kickoff_async()`, and `kickoff_for_each_async()`.
* Automatic tracing of all [crewAI-tools](https://github.com/crewAIInc/crewAI-tools).
* Flow feature support with decorator patching (`@start`, `@listen`, `@router`, `@or_`, `@and_`).
* Track custom guardrails passed to CrewAI `Task` with `@weave.op()`.

For detailed information on what’s supported, visit the [Weave CrewAI documentation](https://weave-docs.wandb.ai/guides/integrations/crewai/#getting-started-with-flow).

## [​](#resources) Resources

* [📘 Weave Documentation](https://weave-docs.wandb.ai)
* [📊 Example Weave x CrewAI dashboard](https://wandb.ai/ayut/crewai_demo/weave/traces?cols=%7B%22wb_run_id%22%3Afalse%2C%22attributes.weave.client_version%22%3Afalse%2C%22attributes.weave.os_name%22%3Afalse%2C%22attributes.weave.os_release%22%3Afalse%2C%22attributes.weave.os_version%22%3Afalse%2C%22attributes.weave.source%22%3Afalse%2C%22attributes.weave.sys_version%22%3Afalse%7D&peekPath=%2Fayut%2Fcrewai_demo%2Fcalls%2F0195c838-38cb-71a2-8a15-651ecddf9d89)
* [🐦 X](https://x.com/weave_wb)

Was this page helpful?

YesNo

[Portkey Integration

Previous](/en/observability/portkey)[TrueFoundry Integration

Next](/en/observability/truefoundry)

⌘I