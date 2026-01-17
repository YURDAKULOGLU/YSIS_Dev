Sequential Processes - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Learn

Sequential Processes

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

## [​](#introduction) Introduction

CrewAI offers a flexible framework for executing tasks in a structured manner, supporting both sequential and hierarchical processes.
This guide outlines how to effectively implement these processes to ensure efficient task execution and project completion.

## [​](#sequential-process-overview) Sequential Process Overview

The sequential process ensures tasks are executed one after the other, following a linear progression.
This approach is ideal for projects requiring tasks to be completed in a specific order.

### [​](#key-features) Key Features

* **Linear Task Flow**: Ensures orderly progression by handling tasks in a predetermined sequence.
* **Simplicity**: Best suited for projects with clear, step-by-step tasks.
* **Easy Monitoring**: Facilitates easy tracking of task completion and project progress.

## [​](#implementing-the-sequential-process) Implementing the Sequential Process

To use the sequential process, assemble your crew and define tasks in the order they need to be executed.

Code

Copy

Ask AI

```
from crewai import Crew, Process, Agent, Task, TaskOutput, CrewOutput

# Define your agents
researcher = Agent(
  role='Researcher',
  goal='Conduct foundational research',
  backstory='An experienced researcher with a passion for uncovering insights'
)
analyst = Agent(
  role='Data Analyst',
  goal='Analyze research findings',
  backstory='A meticulous analyst with a knack for uncovering patterns'
)
writer = Agent(
  role='Writer',
  goal='Draft the final report',
  backstory='A skilled writer with a talent for crafting compelling narratives'
)

# Define your tasks
research_task = Task(
  description='Gather relevant data...', 
  agent=researcher, 
  expected_output='Raw Data'
)
analysis_task = Task(
  description='Analyze the data...', 
  agent=analyst, 
  expected_output='Data Insights'
)
writing_task = Task(
  description='Compose the report...', 
  agent=writer, 
  expected_output='Final Report'
)

# Form the crew with a sequential process
report_crew = Crew(
  agents=[researcher, analyst, writer],
  tasks=[research_task, analysis_task, writing_task],
  process=Process.sequential
)

# Execute the crew
result = report_crew.kickoff()

# Accessing the type-safe output
task_output: TaskOutput = result.tasks[0].output
crew_output: CrewOutput = result.output
```

### [​](#note:) Note:

Each task in a sequential process **must** have an agent assigned. Ensure that every `Task` includes an `agent` parameter.

### [​](#workflow-in-action) Workflow in Action

1. **Initial Task**: In a sequential process, the first agent completes their task and signals completion.
2. **Subsequent Tasks**: Agents pick up their tasks based on the process type, with outcomes of preceding tasks or directives guiding their execution.
3. **Completion**: The process concludes once the final task is executed, leading to project completion.

## [​](#advanced-features) Advanced Features

### [​](#task-delegation) Task Delegation

In sequential processes, if an agent has `allow_delegation` set to `True`, they can delegate tasks to other agents in the crew.
This feature is automatically set up when there are multiple agents in the crew.

### [​](#asynchronous-execution) Asynchronous Execution

Tasks can be executed asynchronously, allowing for parallel processing when appropriate.
To create an asynchronous task, set `async_execution=True` when defining the task.

### [​](#memory-and-caching) Memory and Caching

CrewAI supports both memory and caching features:

* **Memory**: Enable by setting `memory=True` when creating the Crew. This allows agents to retain information across tasks.
* **Caching**: By default, caching is enabled. Set `cache=False` to disable it.

### [​](#callbacks) Callbacks

You can set callbacks at both the task and step level:

* `task_callback`: Executed after each task completion.
* `step_callback`: Executed after each step in an agent’s execution.

### [​](#usage-metrics) Usage Metrics

CrewAI tracks token usage across all tasks and agents. You can access these metrics after execution.

## [​](#best-practices-for-sequential-processes) Best Practices for Sequential Processes

1. **Order Matters**: Arrange tasks in a logical sequence where each task builds upon the previous one.
2. **Clear Task Descriptions**: Provide detailed descriptions for each task to guide the agents effectively.
3. **Appropriate Agent Selection**: Match agents’ skills and roles to the requirements of each task.
4. **Use Context**: Leverage the context from previous tasks to inform subsequent ones.

This updated documentation ensures that details accurately reflect the latest changes in the codebase and clearly describes how to leverage new features and configurations.
The content is kept simple and direct to ensure easy understanding.

Was this page helpful?

YesNo

[Replay Tasks from Latest Crew Kickoff

Previous](/en/learn/replay-tasks-from-latest-crew-kickoff)[Using Annotations in crew.py

Next](/en/learn/using-annotations)

⌘I