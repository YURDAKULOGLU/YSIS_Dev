Reasoning - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Core Concepts

Reasoning

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

Agent reasoning is a feature that allows agents to reflect on a task and create a plan before execution. This helps agents approach tasks more methodically and ensures they’re ready to perform the assigned work.

## [​](#usage) Usage

To enable reasoning for an agent, simply set `reasoning=True` when creating the agent:

Copy

Ask AI

```
from crewai import Agent

agent = Agent(
    role="Data Analyst",
    goal="Analyze complex datasets and provide insights",
    backstory="You are an experienced data analyst with expertise in finding patterns in complex data.",
    reasoning=True,  # Enable reasoning
    max_reasoning_attempts=3  # Optional: Set a maximum number of reasoning attempts
)
```

## [​](#how-it-works) How It Works

When reasoning is enabled, before executing a task, the agent will:

1. Reflect on the task and create a detailed plan
2. Evaluate whether it’s ready to execute the task
3. Refine the plan as necessary until it’s ready or max\_reasoning\_attempts is reached
4. Inject the reasoning plan into the task description before execution

This process helps the agent break down complex tasks into manageable steps and identify potential challenges before starting.

## [​](#configuration-options) Configuration Options

[​](#param-reasoning)

reasoning

bool

default:"False"

Enable or disable reasoning

[​](#param-max-reasoning-attempts)

max\_reasoning\_attempts

int

default:"None"

Maximum number of attempts to refine the plan before proceeding with execution. If None (default), the agent will continue refining until it’s ready.

## [​](#example) Example

Here’s a complete example:

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create an agent with reasoning enabled
analyst = Agent(
    role="Data Analyst",
    goal="Analyze data and provide insights",
    backstory="You are an expert data analyst.",
    reasoning=True,
    max_reasoning_attempts=3  # Optional: Set a limit on reasoning attempts
)

# Create a task
analysis_task = Task(
    description="Analyze the provided sales data and identify key trends.",
    expected_output="A report highlighting the top 3 sales trends.",
    agent=analyst
)

# Create a crew and run the task
crew = Crew(agents=[analyst], tasks=[analysis_task])
result = crew.kickoff()

print(result)
```

## [​](#error-handling) Error Handling

The reasoning process is designed to be robust, with error handling built in. If an error occurs during reasoning, the agent will proceed with executing the task without the reasoning plan. This ensures that tasks can still be executed even if the reasoning process fails.
Here’s how to handle potential errors in your code:

Copy

Ask AI

```
from crewai import Agent, Task
import logging

# Set up logging to capture any reasoning errors
logging.basicConfig(level=logging.INFO)

# Create an agent with reasoning enabled
agent = Agent(
    role="Data Analyst",
    goal="Analyze data and provide insights",
    reasoning=True,
    max_reasoning_attempts=3
)

# Create a task
task = Task(
    description="Analyze the provided sales data and identify key trends.",
    expected_output="A report highlighting the top 3 sales trends.",
    agent=agent
)

# Execute the task
# If an error occurs during reasoning, it will be logged and execution will continue
result = agent.execute_task(task)
```

## [​](#example-reasoning-output) Example Reasoning Output

Here’s an example of what a reasoning plan might look like for a data analysis task:

Copy

Ask AI

```
Task: Analyze the provided sales data and identify key trends.

Reasoning Plan:
I'll analyze the sales data to identify the top 3 trends.

1. Understanding of the task:
   I need to analyze sales data to identify key trends that would be valuable for business decision-making.

2. Key steps I'll take:
   - First, I'll examine the data structure to understand what fields are available
   - Then I'll perform exploratory data analysis to identify patterns
   - Next, I'll analyze sales by time periods to identify temporal trends
   - I'll also analyze sales by product categories and customer segments
   - Finally, I'll identify the top 3 most significant trends

3. Approach to challenges:
   - If the data has missing values, I'll decide whether to fill or filter them
   - If the data has outliers, I'll investigate whether they're valid data points or errors
   - If trends aren't immediately obvious, I'll apply statistical methods to uncover patterns

4. Use of available tools:
   - I'll use data analysis tools to explore and visualize the data
   - I'll use statistical tools to identify significant patterns
   - I'll use knowledge retrieval to access relevant information about sales analysis

5. Expected outcome:
   A concise report highlighting the top 3 sales trends with supporting evidence from the data.

READY: I am ready to execute the task.
```

This reasoning plan helps the agent organize its approach to the task, consider potential challenges, and ensure it delivers the expected output.

Was this page helpful?

YesNo

[Memory

Previous](/en/concepts/memory)[Planning

Next](/en/concepts/planning)

⌘I