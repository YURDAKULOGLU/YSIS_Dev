CrewAI Tracing - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

CrewAI Tracing

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

# [​](#crewai-built-in-tracing) CrewAI Built-in Tracing

CrewAI provides built-in tracing capabilities that allow you to monitor and debug your Crews and Flows in real-time. This guide demonstrates how to enable tracing for both **Crews** and **Flows** using CrewAI’s integrated observability platform.
> **What is CrewAI Tracing?** CrewAI’s built-in tracing provides comprehensive observability for your AI agents, including agent decisions, task execution timelines, tool usage, and LLM calls - all accessible through the [CrewAI AOP platform](https://app.crewai.com).

![CrewAI Tracing Interface](https://mintcdn.com/crewai/xsUWvx-8zGU3Skk0/images/crewai-tracing.png?fit=max&auto=format&n=xsUWvx-8zGU3Skk0&q=85&s=b7e95a8f56ed3c459699acf641b4ae5a)

## [​](#prerequisites) Prerequisites

Before you can use CrewAI tracing, you need:

1. **CrewAI AOP Account**: Sign up for a free account at [app.crewai.com](https://app.crewai.com)
2. **CLI Authentication**: Use the CrewAI CLI to authenticate your local environment

Copy

Ask AI

```
crewai login
```

## [​](#setup-instructions) Setup Instructions

### [​](#step-1:-create-your-crewai-aop-account) Step 1: Create Your CrewAI AOP Account

Visit [app.crewai.com](https://app.crewai.com) and create your free account. This will give you access to the CrewAI AOP platform where you can view traces, metrics, and manage your crews.

### [​](#step-2:-install-crewai-cli-and-authenticate) Step 2: Install CrewAI CLI and Authenticate

If you haven’t already, install CrewAI with the CLI tools:

Copy

Ask AI

```
uv add crewai[tools]
```

Then authenticate your CLI with your CrewAI AOP account:

Copy

Ask AI

```
crewai login
```

This command will:

1. Open your browser to the authentication page
2. Prompt you to enter a device code
3. Authenticate your local environment with your CrewAI AOP account
4. Enable tracing capabilities for your local development

### [​](#step-3:-enable-tracing-in-your-crew) Step 3: Enable Tracing in Your Crew

You can enable tracing for your Crew by setting the `tracing` parameter to `True`:

Copy

Ask AI

```
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool

# Define your agents
researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI and data science",
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends.
    You have a knack for dissecting complex data and presenting actionable insights.""",
    verbose=True,
    tools=[SerperDevTool()],
)

writer = Agent(
    role="Tech Content Strategist",
    goal="Craft compelling content on tech advancements",
    backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.""",
    verbose=True,
)

# Create tasks for your agents
research_task = Task(
    description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
    Identify key trends, breakthrough technologies, and potential industry impacts.""",
    expected_output="Full analysis report in bullet points",
    agent=researcher,
)

writing_task = Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights the most significant AI advancements.
    Your post should be informative yet accessible, catering to a tech-savvy audience.""",
    expected_output="Full blog post of at least 4 paragraphs",
    agent=writer,
)

# Enable tracing in your crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    tracing=True,  # Enable built-in tracing
    verbose=True
)

# Execute your crew
result = crew.kickoff()
```

### [​](#step-4:-enable-tracing-in-your-flow) Step 4: Enable Tracing in Your Flow

Similarly, you can enable tracing for CrewAI Flows:

Copy

Ask AI

```
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class ExampleState(BaseModel):
    counter: int = 0
    message: str = ""

class ExampleFlow(Flow[ExampleState]):
    def __init__(self):
        super().__init__(tracing=True)  # Enable tracing for the flow

    @start()
    def first_method(self):
        print("Starting the flow")
        self.state.counter = 1
        self.state.message = "Flow started"
        return "continue"

    @listen("continue")
    def second_method(self):
        print("Continuing the flow")
        self.state.counter += 1
        self.state.message = "Flow continued"
        return "finish"

    @listen("finish")
    def final_method(self):
        print("Finishing the flow")
        self.state.counter += 1
        self.state.message = "Flow completed"

# Create and run the flow with tracing enabled
flow = ExampleFlow(tracing=True)
result = flow.kickoff()
```

### [​](#step-5:-view-traces-in-the-crewai-aop-dashboard) Step 5: View Traces in the CrewAI AOP Dashboard

After running the crew or flow, you can view the traces generated by your CrewAI application in the CrewAI AOP dashboard. You should see detailed steps of the agent interactions, tool usages, and LLM calls.
Just click on the link below to view the traces or head over to the traces tab in the dashboard [here](https://app.crewai.com/crewai_plus/trace_batches)
![CrewAI Tracing Interface](https://mintcdn.com/crewai/iG0g1htk7RWkFuad/images/view-traces.png?fit=max&auto=format&n=iG0g1htk7RWkFuad&q=85&s=72981ddafcda030270c059f08b98db03)

### [​](#alternative:-environment-variable-configuration) Alternative: Environment Variable Configuration

You can also enable tracing globally by setting an environment variable:

Copy

Ask AI

```
export CREWAI_TRACING_ENABLED=true
```

Or add it to your `.env` file:

Copy

Ask AI

```
CREWAI_TRACING_ENABLED=true
```

When this environment variable is set, all Crews and Flows will automatically have tracing enabled, even without explicitly setting `tracing=True`.

## [​](#viewing-your-traces) Viewing Your Traces

### [​](#access-the-crewai-aop-dashboard) Access the CrewAI AOP Dashboard

1. Visit [app.crewai.com](https://app.crewai.com) and log in to your account
2. Navigate to your project dashboard
3. Click on the **Traces** tab to view execution details

### [​](#what-you’ll-see-in-traces) What You’ll See in Traces

CrewAI tracing provides comprehensive visibility into:

* **Agent Decisions**: See how agents reason through tasks and make decisions
* **Task Execution Timeline**: Visual representation of task sequences and dependencies
* **Tool Usage**: Monitor which tools are called and their results
* **LLM Calls**: Track all language model interactions, including prompts and responses
* **Performance Metrics**: Execution times, token usage, and costs
* **Error Tracking**: Detailed error information and stack traces

### [​](#trace-features) Trace Features

* **Execution Timeline**: Click through different stages of execution
* **Detailed Logs**: Access comprehensive logs for debugging
* **Performance Analytics**: Analyze execution patterns and optimize performance
* **Export Capabilities**: Download traces for further analysis

### [​](#authentication-issues) Authentication Issues

If you encounter authentication problems:

1. Ensure you’re logged in: `crewai login`
2. Check your internet connection
3. Verify your account at [app.crewai.com](https://app.crewai.com)

### [​](#traces-not-appearing) Traces Not Appearing

If traces aren’t showing up in the dashboard:

1. Confirm `tracing=True` is set in your Crew/Flow
2. Check that `CREWAI_TRACING_ENABLED=true` if using environment variables
3. Ensure you’re authenticated with `crewai login`
4. Verify your crew/flow is actually executing

Was this page helpful?

YesNo

[Zapier Actions Tool

Previous](/en/tools/automation/zapieractionstool)[Overview

Next](/en/observability/overview)

⌘I