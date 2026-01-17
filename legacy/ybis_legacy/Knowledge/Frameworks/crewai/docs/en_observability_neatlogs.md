Neatlogs Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

Neatlogs Integration

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

# [​](#introduction) Introduction

Neatlogs helps you **see what your agent did**, **why**, and **share it**.
It captures every step: thoughts, tool calls, responses, evaluations. No raw logs. Just clear, structured traces. Great for debugging and collaboration.

## [​](#why-use-neatlogs) Why use Neatlogs?

CrewAI agents use multiple tools and reasoning steps. When something goes wrong, you need context — not just errors.
Neatlogs lets you:

* Follow the full decision path
* Add feedback directly on steps
* Chat with the trace using AI assistant
* Share runs publicly for feedback
* Turn insights into tasks

All in one place.
Manage your traces effortlessly
![Traces](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/neatlogs-1.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=d01a5ce64066c6c7387b238068e71369)
![Trace Response](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/neatlogs-2.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=5b737699468781be25098c33040d2125)
The best UX to view a CrewAI trace. Post comments anywhere you want. Use AI to debug.
![Trace Details](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/neatlogs-3.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=43cda9bcd83376dda4523ff0596b2043)
![Ai Chat Bot With A Trace](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/neatlogs-4.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=c9e7ad0653cae7bfaad2dd448d90eda0)
![Comments Drawer](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/neatlogs-5.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=a977655abb8cd26d9ed4cef5fdd7d859)

## [​](#core-features) Core Features

* **Trace Viewer**: Track thoughts, tools, and decisions in sequence
* **Inline Comments**: Tag teammates on any trace step
* **Feedback & Evaluation**: Mark outputs as correct or incorrect
* **Error Highlighting**: Automatic flagging of API/tool failures
* **Task Conversion**: Convert comments into assigned tasks
* **Ask the Trace (AI)**: Chat with your trace using Neatlogs AI bot
* **Public Sharing**: Publish trace links to your community

## [​](#quick-setup-with-crewai) Quick Setup with CrewAI

1

Sign Up & Get API Key

Visit [neatlogs.com](https://neatlogs.com/?utm_source=crewAI-docs), create a project, copy the API key.

2

Install SDK

Copy

Ask AI

```
pip install neatlogs
```

(Latest version 0.8.0, Python 3.8+; MIT license)

3

Initialize Neatlogs

Before starting Crew agents, add:

Copy

Ask AI

```
import neatlogs
neatlogs.init("YOUR_PROJECT_API_KEY")
```

Agents run as usual. Neatlogs captures everything automatically.

## [​](#under-the-hood) Under the Hood

According to GitHub, Neatlogs:

* Captures thoughts, tool calls, responses, errors, and token stats
* Supports AI-powered task generation and robust evaluation workflows

All with just two lines of code.

## [​](#watch-it-work) Watch It Work

### [​](#🔍-full-demo-4-min) 🔍 Full Demo (4 min)

### [​](#⚙️-crewai-integration-30s) ⚙️ CrewAI Integration (30 s)

## [​](#links-&-support) Links & Support

* 📘 [Neatlogs Docs](https://docs.neatlogs.com/)
* 🔐 [Dashboard & API Key](https://app.neatlogs.com/)
* 🐦 [Follow on Twitter](https://twitter.com/neatlogs)
* 📧 Contact: [[email protected]](/cdn-cgi/l/email-protection#ed8588818182ad83888c9981828a9ec38e8280)
* 🛠 [GitHub SDK](https://github.com/NeatLogs/neatlogs)

## [​](#tl;dr) TL;DR

With just:

Copy

Ask AI

```
pip install neatlogs

import neatlogs
neatlogs.init("YOUR_API_KEY")

You can now capture, understand, share, and act on your CrewAI agent runs in seconds.
No setup overhead. Full trace transparency. Full team collaboration.
```

Was this page helpful?

YesNo

[MLflow Integration

Previous](/en/observability/mlflow)[OpenLIT Integration

Next](/en/observability/openlit)

⌘I