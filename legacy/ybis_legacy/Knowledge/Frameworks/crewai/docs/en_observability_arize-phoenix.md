Arize Phoenix - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

Arize Phoenix

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

# [​](#arize-phoenix-integration) Arize Phoenix Integration

This guide demonstrates how to integrate **Arize Phoenix** with **CrewAI** using OpenTelemetry via the [OpenInference](https://github.com/openinference/openinference) SDK. By the end of this guide, you will be able to trace your CrewAI agents and easily debug your agents.
> **What is Arize Phoenix?** [Arize Phoenix](https://phoenix.arize.com) is an LLM observability platform that provides tracing and evaluation for AI applications.

[![Watch a Video Demo of Our Integration with Phoenix](https://storage.googleapis.com/arize-assets/fixtures/setup_crewai.png)](https://www.youtube.com/watch?v=Yc5q3l6F7Ww)

## [​](#get-started) Get Started

We’ll walk through a simple example of using CrewAI and integrating it with Arize Phoenix via OpenTelemetry using OpenInference.
You can also access this guide on [Google Colab](https://colab.research.google.com/github/Arize-ai/phoenix/blob/main/tutorials/tracing/crewai_tracing_tutorial.ipynb).

### [​](#step-1:-install-dependencies) Step 1: Install Dependencies

Copy

Ask AI

```
pip install openinference-instrumentation-crewai crewai crewai-tools arize-phoenix-otel
```

### [​](#step-2:-set-up-environment-variables) Step 2: Set Up Environment Variables

Setup Phoenix Cloud API keys and configure OpenTelemetry to send traces to Phoenix. Phoenix Cloud is a hosted version of Arize Phoenix, but it is not required to use this integration.
You can get your free Serper API key [here](https://serper.dev/).

Copy

Ask AI

```
import os
from getpass import getpass

# Get your Phoenix Cloud credentials
PHOENIX_API_KEY = getpass("🔑 Enter your Phoenix Cloud API Key: ")

# Get API keys for services
OPENAI_API_KEY = getpass("🔑 Enter your OpenAI API key: ")
SERPER_API_KEY = getpass("🔑 Enter your Serper API key: ")

# Set environment variables
os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={PHOENIX_API_KEY}"
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com" # Phoenix Cloud, change this to your own endpoint if you are using a self-hosted instance
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["SERPER_API_KEY"] = SERPER_API_KEY
```

### [​](#step-3:-initialize-opentelemetry-with-phoenix) Step 3: Initialize OpenTelemetry with Phoenix

Initialize the OpenInference OpenTelemetry instrumentation SDK to start capturing traces and send them to Phoenix.

Copy

Ask AI

```
from phoenix.otel import register

tracer_provider = register(
    project_name="crewai-tracing-demo",
    auto_instrument=True,
)
```

### [​](#step-4:-create-a-crewai-application) Step 4: Create a CrewAI Application

We’ll create a CrewAI application where two agents collaborate to research and write a blog post about AI advancements.

Copy

Ask AI

```
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from openinference.instrumentation.crewai import CrewAIInstrumentor
from phoenix.otel import register

# setup monitoring for your crew
tracer_provider = register(
    endpoint="http://localhost:6006/v1/traces")
CrewAIInstrumentor().instrument(skip_dep_check=True, tracer_provider=tracer_provider)
search_tool = SerperDevTool()

# Define your agents with roles and goals
researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI and data science",
    backstory="""You work at a leading tech think tank.
    Your expertise lies in identifying emerging trends.
    You have a knack for dissecting complex data and presenting actionable insights.""",
    verbose=True,
    allow_delegation=False,
    # You can pass an optional llm attribute specifying what model you wanna use.
    # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7),
    tools=[search_tool],
)
writer = Agent(
    role="Tech Content Strategist",
    goal="Craft compelling content on tech advancements",
    backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.""",
    verbose=True,
    allow_delegation=True,
)

# Create tasks for your agents
task1 = Task(
    description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
    Identify key trends, breakthrough technologies, and potential industry impacts.""",
    expected_output="Full analysis report in bullet points",
    agent=researcher,
)

task2 = Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights the most significant AI advancements.
    Your post should be informative yet accessible, catering to a tech-savvy audience.
    Make it sound cool, avoid complex words so it doesn't sound like AI.""",
    expected_output="Full blog post of at least 4 paragraphs",
    agent=writer,
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, writer], tasks=[task1, task2], verbose=1, process=Process.sequential
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)
```

### [​](#step-5:-view-traces-in-phoenix) Step 5: View Traces in Phoenix

After running the agent, you can view the traces generated by your CrewAI application in Phoenix. You should see detailed steps of the agent interactions and LLM calls, which can help you debug and optimize your AI agents.
Log into your Phoenix Cloud account and navigate to the project you specified in the `project_name` parameter. You’ll see a timeline view of your trace with all the agent interactions, tool usages, and LLM calls.
![Example trace in Phoenix showing agent interactions](https://storage.googleapis.com/arize-assets/fixtures/crewai_traces.png)

### [​](#version-compatibility-information) Version Compatibility Information

* Python 3.8+
* CrewAI >= 0.86.0
* Arize Phoenix >= 7.0.1
* OpenTelemetry SDK >= 1.31.0

### [​](#references) References

* [Phoenix Documentation](https://docs.arize.com/phoenix/) - Overview of the Phoenix platform.
* [CrewAI Documentation](https://docs.crewai.com/) - Overview of the CrewAI framework.
* [OpenTelemetry Docs](https://opentelemetry.io/docs/) - OpenTelemetry guide
* [OpenInference GitHub](https://github.com/openinference/openinference) - Source code for OpenInference SDK.

Was this page helpful?

YesNo

[Overview

Previous](/en/observability/overview)[Braintrust

Next](/en/observability/braintrust)

⌘I