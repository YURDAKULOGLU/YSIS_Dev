Kickoff Crew Asynchronously - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Learn

Kickoff Crew Asynchronously

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

CrewAI provides the ability to kickoff a crew asynchronously, allowing you to start the crew execution in a non-blocking manner.
This feature is particularly useful when you want to run multiple crews concurrently or when you need to perform other tasks while the crew is executing.
CrewAI offers two approaches for async execution:

| Method | Type | Description |
| --- | --- | --- |
| `akickoff()` | Native async | True async/await throughout the entire execution chain |
| `kickoff_async()` | Thread-based | Wraps synchronous execution in `asyncio.to_thread` |

For high-concurrency workloads, `akickoff()` is recommended as it uses native async for task execution, memory operations, and knowledge retrieval.

## [​](#native-async-execution-with-akickoff) Native Async Execution with `akickoff()`

The `akickoff()` method provides true native async execution, using async/await throughout the entire execution chain including task execution, memory operations, and knowledge queries.

### [​](#method-signature) Method Signature

Code

Copy

Ask AI

```
async def akickoff(self, inputs: dict) -> CrewOutput:
```

### [​](#parameters) Parameters

* `inputs` (dict): A dictionary containing the input data required for the tasks.

### [​](#returns) Returns

* `CrewOutput`: An object representing the result of the crew execution.

### [​](#example:-native-async-crew-execution) Example: Native Async Crew Execution

Code

Copy

Ask AI

```
import asyncio
from crewai import Crew, Agent, Task

# Create an agent
coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

# Create a task
data_analysis_task = Task(
    description="Analyze the given dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

# Create a crew
analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task]
)

# Native async execution
async def main():
    result = await analysis_crew.akickoff(inputs={"ages": [25, 30, 35, 40, 45]})
    print("Crew Result:", result)

asyncio.run(main())
```

### [​](#example:-multiple-native-async-crews) Example: Multiple Native Async Crews

Run multiple crews concurrently using `asyncio.gather()` with native async:

Code

Copy

Ask AI

```
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

task_1 = Task(
    description="Analyze the first dataset and calculate the average age. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

task_2 = Task(
    description="Analyze the second dataset and calculate the average age. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

crew_1 = Crew(agents=[coding_agent], tasks=[task_1])
crew_2 = Crew(agents=[coding_agent], tasks=[task_2])

async def main():
    results = await asyncio.gather(
        crew_1.akickoff(inputs={"ages": [25, 30, 35, 40, 45]}),
        crew_2.akickoff(inputs={"ages": [20, 22, 24, 28, 30]})
    )

    for i, result in enumerate(results, 1):
        print(f"Crew {i} Result:", result)

asyncio.run(main())
```

### [​](#example:-native-async-for-multiple-inputs) Example: Native Async for Multiple Inputs

Use `akickoff_for_each()` to execute your crew against multiple inputs concurrently with native async:

Code

Copy

Ask AI

```
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

data_analysis_task = Task(
    description="Analyze the dataset and calculate the average age. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task]
)

async def main():
    datasets = [
        {"ages": [25, 30, 35, 40, 45]},
        {"ages": [20, 22, 24, 28, 30]},
        {"ages": [30, 35, 40, 45, 50]}
    ]

    results = await analysis_crew.akickoff_for_each(datasets)

    for i, result in enumerate(results, 1):
        print(f"Dataset {i} Result:", result)

asyncio.run(main())
```

## [​](#thread-based-async-with-kickoff-async) Thread-Based Async with `kickoff_async()`

The `kickoff_async()` method provides async execution by wrapping the synchronous `kickoff()` in a thread. This is useful for simpler async integration or backward compatibility.

### [​](#method-signature-2) Method Signature

Code

Copy

Ask AI

```
async def kickoff_async(self, inputs: dict) -> CrewOutput:
```

### [​](#parameters-2) Parameters

* `inputs` (dict): A dictionary containing the input data required for the tasks.

### [​](#returns-2) Returns

* `CrewOutput`: An object representing the result of the crew execution.

### [​](#example:-thread-based-async-execution) Example: Thread-Based Async Execution

Code

Copy

Ask AI

```
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

data_analysis_task = Task(
    description="Analyze the given dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

analysis_crew = Crew(
    agents=[coding_agent],
    tasks=[data_analysis_task]
)

async def async_crew_execution():
    result = await analysis_crew.kickoff_async(inputs={"ages": [25, 30, 35, 40, 45]})
    print("Crew Result:", result)

asyncio.run(async_crew_execution())
```

### [​](#example:-multiple-thread-based-async-crews) Example: Multiple Thread-Based Async Crews

Code

Copy

Ask AI

```
import asyncio
from crewai import Crew, Agent, Task

coding_agent = Agent(
    role="Python Data Analyst",
    goal="Analyze data and provide insights using Python",
    backstory="You are an experienced data analyst with strong Python skills.",
    allow_code_execution=True
)

task_1 = Task(
    description="Analyze the first dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

task_2 = Task(
    description="Analyze the second dataset and calculate the average age of participants. Ages: {ages}",
    agent=coding_agent,
    expected_output="The average age of the participants."
)

crew_1 = Crew(agents=[coding_agent], tasks=[task_1])
crew_2 = Crew(agents=[coding_agent], tasks=[task_2])

async def async_multiple_crews():
    result_1 = crew_1.kickoff_async(inputs={"ages": [25, 30, 35, 40, 45]})
    result_2 = crew_2.kickoff_async(inputs={"ages": [20, 22, 24, 28, 30]})

    results = await asyncio.gather(result_1, result_2)

    for i, result in enumerate(results, 1):
        print(f"Crew {i} Result:", result)

asyncio.run(async_multiple_crews())
```

## [​](#async-streaming) Async Streaming

Both async methods support streaming when `stream=True` is set on the crew:

Code

Copy

Ask AI

```
import asyncio
from crewai import Crew, Agent, Task

agent = Agent(
    role="Researcher",
    goal="Research and summarize topics",
    backstory="You are an expert researcher."
)

task = Task(
    description="Research the topic: {topic}",
    agent=agent,
    expected_output="A comprehensive summary of the topic."
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    stream=True  # Enable streaming
)

async def main():
    streaming_output = await crew.akickoff(inputs={"topic": "AI trends in 2024"})

    # Async iteration over streaming chunks
    async for chunk in streaming_output:
        print(f"Chunk: {chunk.content}")

    # Access final result after streaming completes
    result = streaming_output.result
    print(f"Final result: {result.raw}")

asyncio.run(main())
```

## [​](#potential-use-cases) Potential Use Cases

* **Parallel Content Generation**: Kickoff multiple independent crews asynchronously, each responsible for generating content on different topics. For example, one crew might research and draft an article on AI trends, while another crew generates social media posts about a new product launch.
* **Concurrent Market Research Tasks**: Launch multiple crews asynchronously to conduct market research in parallel. One crew might analyze industry trends, while another examines competitor strategies, and yet another evaluates consumer sentiment.
* **Independent Travel Planning Modules**: Execute separate crews to independently plan different aspects of a trip. One crew might handle flight options, another handles accommodation, and a third plans activities.

## [​](#choosing-between-akickoff-and-kickoff-async) Choosing Between `akickoff()` and `kickoff_async()`

| Feature | `akickoff()` | `kickoff_async()` |
| --- | --- | --- |
| Execution model | Native async/await | Thread-based wrapper |
| Task execution | Async with `aexecute_sync()` | Sync in thread pool |
| Memory operations | Async | Sync in thread pool |
| Knowledge retrieval | Async | Sync in thread pool |
| Best for | High-concurrency, I/O-bound workloads | Simple async integration |
| Streaming support | Yes | Yes |

Was this page helpful?

YesNo

[Human Feedback in Flows

Previous](/en/learn/human-feedback-in-flows)[Kickoff Crew for Each

Next](/en/learn/kickoff-for-each)

⌘I