Introduction - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘K

Search...

Navigation

Get Started

Introduction

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

# [​](#what-is-crewai) What is CrewAI?

**CrewAI is the leading open-source framework for orchestrating autonomous AI agents and building complex workflows.**
It empowers developers to build production-ready multi-agent systems by combining the collaborative intelligence of **Crews** with the precise control of **Flows**.

* **[CrewAI Flows](/en/guides/flows/first-flow)**: The backbone of your AI application. Flows allow you to create structured, event-driven workflows that manage state and control execution. They provide the scaffolding for your AI agents to work within.
* **[CrewAI Crews](/en/guides/crews/first-crew)**: The units of work within your Flow. Crews are teams of autonomous agents that collaborate to solve specific tasks delegated to them by the Flow.

With over 100,000 developers certified through our community courses, CrewAI is the standard for enterprise-ready AI automation.

## [​](#the-crewai-architecture) The CrewAI Architecture

CrewAI’s architecture is designed to balance autonomy with control.

### [​](#1-flows:-the-backbone) 1. Flows: The Backbone

Think of a Flow as the “manager” or the “process definition” of your application. It defines the steps, the logic, and how data moves through your system.

![CrewAI Framework Overview](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/flows.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=82ea168de2f004553dcea21410cd7d8a)

CrewAI Framework Overview

Flows provide:

* **State Management**: Persist data across steps and executions.
* **Event-Driven Execution**: Trigger actions based on events or external inputs.
* **Control Flow**: Use conditional logic, loops, and branching.

### [​](#2-crews:-the-intelligence) 2. Crews: The Intelligence

Crews are the “teams” that do the heavy lifting. Within a Flow, you can trigger a Crew to tackle a complex problem requiring creativity and collaboration.

![CrewAI Framework Overview](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crews.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=514fd0b06e4128e62f10728d44601975)

CrewAI Framework Overview

Crews provide:

* **Role-Playing Agents**: Specialized agents with specific goals and tools.
* **Autonomous Collaboration**: Agents work together to solve tasks.
* **Task Delegation**: Tasks are assigned and executed based on agent capabilities.

## [​](#how-it-all-works-together) How It All Works Together

1. **The Flow** triggers an event or starts a process.
2. **The Flow** manages the state and decides what to do next.
3. **The Flow** delegates a complex task to a **Crew**.
4. **The Crew**’s agents collaborate to complete the task.
5. **The Crew** returns the result to the **Flow**.
6. **The Flow** continues execution based on the result.

## [​](#key-features) Key Features

## Production-Grade Flows

Build reliable, stateful workflows that can handle long-running processes and complex logic.

## Autonomous Crews

Deploy teams of agents that can plan, execute, and collaborate to achieve high-level goals.

## Flexible Tools

Connect your agents to any API, database, or local tool.

## Enterprise Security

Designed with security and compliance in mind for enterprise deployments.

## [​](#when-to-use-crews-vs-flows) When to Use Crews vs. Flows

**The short answer: Use both.**
For any production-ready application, **start with a Flow**.

* **Use a Flow** to define the overall structure, state, and logic of your application.
* **Use a Crew** within a Flow step when you need a team of agents to perform a specific, complex task that requires autonomy.

| Use Case | Architecture |
| --- | --- |
| **Simple Automation** | Single Flow with Python tasks |
| **Complex Research** | Flow managing state -> Crew performing research |
| **Application Backend** | Flow handling API requests -> Crew generating content -> Flow saving to DB |

## [​](#why-choose-crewai) Why Choose CrewAI?

* 🧠 **Autonomous Operation**: Agents make intelligent decisions based on their roles and available tools
* 📝 **Natural Interaction**: Agents communicate and collaborate like human team members
* 🛠️ **Extensible Design**: Easy to add new tools, roles, and capabilities
* 🚀 **Production Ready**: Built for reliability and scalability in real-world applications
* 🔒 **Security-Focused**: Designed with enterprise security requirements in mind
* 💰 **Cost-Efficient**: Optimized to minimize token usage and API calls

## [​](#ready-to-start-building) Ready to Start Building?

[## Build Your First Flow

Learn how to create structured, event-driven workflows with precise control over execution.](/en/guides/flows/first-flow)[## Build Your First Crew

Step-by-step tutorial to create a collaborative AI team that works together to solve complex problems.](/en/guides/crews/first-crew)

[## Install CrewAI

Get started with CrewAI in your development environment.](/en/installation)[## Quick Start

Follow our quickstart guide to create your first CrewAI agent and get hands-on experience.](en/quickstart)[## Join the Community

Connect with other developers, get help, and share your CrewAI experiences.](https://community.crewai.com)

Was this page helpful?

YesNo

[Installation

Next](/en/installation)

⌘I