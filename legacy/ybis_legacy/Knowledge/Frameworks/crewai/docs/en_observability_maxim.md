Maxim Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

Maxim Integration

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

# [​](#maxim-overview) Maxim Overview

Maxim AI provides comprehensive agent monitoring, evaluation, and observability for your CrewAI applications. With Maxim’s one-line integration, you can easily trace and analyse agent interactions, performance metrics, and more.

## [​](#features) Features

### [​](#prompt-management) Prompt Management

Maxim’s Prompt Management capabilities enable you to create, organize, and optimize prompts for your CrewAI agents. Rather than hardcoding instructions, leverage Maxim’s SDK to dynamically retrieve and apply version-controlled prompts.

* Prompt Playground
* Prompt Versions
* Prompt Comparisons

Create, refine, experiment and deploy your prompts via the playground. Organize of your prompts using folders and versions, experimenting with the real world cases by linking tools and context, and deploying based on custom logic.Easily experiment across models by [**configuring models**](https://www.getmaxim.ai/docs/introduction/quickstart/setting-up-workspace#add-model-api-keys) and selecting the relevant model from the dropdown at the top of the prompt playground.![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_playground.png)

As teams build their AI applications, a big part of experimentation is iterating on the prompt structure. In order to collaborate effectively and organize your changes clearly, Maxim allows prompt versioning and comparison runs across versions.![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_versions.png)

Iterating on Prompts as you evolve your AI application would need experiments across models, prompt structures, etc. In order to compare versions and make informed decisions about changes, the comparison playground allows a side by side view of results.

## [​](#why-use-prompt-comparison) **Why use Prompt comparison?**

Prompt comparison combines multiple single Prompts into one view, enabling a streamlined approach for various workflows:

1. **Model comparison**: Evaluate the performance of different models on the same Prompt.
2. **Prompt optimization**: Compare different versions of a Prompt to identify the most effective formulation.
3. **Cross-Model consistency**: Ensure consistent outputs across various models for the same Prompt.
4. **Performance benchmarking**: Analyze metrics like latency, cost, and token count across different models and Prompts.

### [​](#observability-&-evals) Observability & Evals

Maxim AI provides comprehensive observability & evaluation for your CrewAI agents, helping you understand exactly what’s happening during each execution.

* Agent Tracing
* Analytics + Evals
* Alerting
* Dashboards

Track your agent’s complete lifecycle, including tool calls, agent trajectories, and decision flows effortlessly.![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_agent_tracking.png)

Run detailed evaluations on full traces or individual nodes with support for:

* Multi-step interactions and granular trace analysis
* Session Level Evaluations
* Simulations for real-world testing

![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_trace_eval.png)

[## Auto Evals on Logs

Evaluate captured logs automatically from the UI based on filters and sampling](https://www.getmaxim.ai/docs/observe/how-to/evaluate-logs/auto-evaluation)[## Human Evals on Logs

Use human evaluation or rating to assess the quality of your logs and evaluate them.](https://www.getmaxim.ai/docs/observe/how-to/evaluate-logs/human-evaluation)[## Node Level Evals

Evaluate any component of your trace or log to gain insights into your agent’s behavior.](https://www.getmaxim.ai/docs/observe/how-to/evaluate-logs/node-level-evaluation)

---

Set thresholds on **error**, **cost, token usage, user feedback, latency** and get real-time alerts via Slack or PagerDuty.![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_alerts_1.png)

Visualize Traces over time, usage metrics, latency & error rates with ease.![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/maxim_dashboard_1.png)

## [​](#getting-started) Getting Started

### [​](#prerequisites) Prerequisites

* Python version >=3.10
* A Maxim account ([sign up here](https://getmaxim.ai/))
* Generate Maxim API Key
* A CrewAI project

### [​](#installation) Installation

Install the Maxim SDK via pip:

Copy

Ask AI

```
pip install maxim-py
```

Or add it to your `requirements.txt`:

Copy

Ask AI

```
maxim-py
```

### [​](#basic-setup) Basic Setup

### [​](#1-set-up-environment-variables) 1. Set up environment variables

Copy

Ask AI

```
### Environment Variables Setup

# Create a `.env` file in your project root:

# Maxim API Configuration
MAXIM_API_KEY=your_api_key_here
MAXIM_LOG_REPO_ID=your_repo_id_here
```

### [​](#2-import-the-required-packages) 2. Import the required packages

Copy

Ask AI

```
from crewai import Agent, Task, Crew, Process
from maxim import Maxim
from maxim.logger.crewai import instrument_crewai
```

### [​](#3-initialise-maxim-with-your-api-key) 3. Initialise Maxim with your API key

Copy

Ask AI

```
# Instrument CrewAI with just one line
instrument_crewai(Maxim().logger())
```

### [​](#4-create-and-run-your-crewai-application-as-usual) 4. Create and run your CrewAI application as usual

Copy

Ask AI

```
# Create your agent
researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover cutting-edge developments in AI',
    backstory="You are an expert researcher at a tech think tank...",
    verbose=True,
    llm=llm
)

# Define the task
research_task = Task(
    description="Research the latest AI advancements...",
    expected_output="",
    agent=researcher
)

# Configure and run the crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True
)

try:
    result = crew.kickoff()
finally:
    maxim.cleanup()  # Ensure cleanup happens even if errors occur
```

That’s it! All your CrewAI agent interactions will now be logged and available in your Maxim dashboard.
Check this Google Colab Notebook for a quick reference - [Notebook](https://colab.research.google.com/drive/1ZKIZWsmgQQ46n8TH9zLsT1negKkJA6K8?usp=sharing)

## [​](#viewing-your-traces) Viewing Your Traces

After running your CrewAI application:

1. Log in to your [Maxim Dashboard](https://app.getmaxim.ai/login)
2. Navigate to your repository
3. View detailed agent traces, including:
   * Agent conversations
   * Tool usage patterns
   * Performance metrics
   * Cost analytics![](https://raw.githubusercontent.com/akmadan/crewAI/docs_maxim_observability/docs/images/crewai_traces.gif)

## [​](#troubleshooting) Troubleshooting

### [​](#common-issues) Common Issues

* **No traces appearing**: Ensure your API key and repository ID are correct
* Ensure you’ve **`called instrument_crewai()`** ***before*** running your crew. This initializes logging hooks correctly.
* Set `debug=True` in your `instrument_crewai()` call to surface any internal errors:

  Copy

  Ask AI

  ```
  instrument_crewai(logger, debug=True)
  ```
* Configure your agents with `verbose=True` to capture detailed logs:

  Copy

  Ask AI

  ```
  agent = CrewAgent(..., verbose=True)
  ```
* Double-check that `instrument_crewai()` is called **before** creating or executing agents. This might be obvious, but it’s a common oversight.

## [​](#resources) Resources

[## CrewAI Docs

Official CrewAI documentation](https://docs.crewai.com/)[## Maxim Docs

Official Maxim documentation](https://getmaxim.ai/docs)[## Maxim Github

Maxim Github](https://github.com/maximhq)

Was this page helpful?

YesNo

[Langtrace Integration

Previous](/en/observability/langtrace)[MLflow Integration

Next](/en/observability/mlflow)

⌘I