Patronus AI Evaluation - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

Patronus AI Evaluation

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

# [​](#patronus-ai-evaluation) Patronus AI Evaluation

## [​](#overview) Overview

[Patronus AI](https://patronus.ai) provides comprehensive evaluation and monitoring capabilities for CrewAI agents, enabling you to assess model outputs, agent behaviors, and overall system performance. This integration allows you to implement continuous evaluation workflows that help maintain quality and reliability in production environments.

## [​](#key-features) Key Features

* **Automated Evaluation**: Real-time assessment of agent outputs and behaviors
* **Custom Criteria**: Define specific evaluation criteria tailored to your use cases
* **Performance Monitoring**: Track agent performance metrics over time
* **Quality Assurance**: Ensure consistent output quality across different scenarios
* **Safety & Compliance**: Monitor for potential issues and policy violations

## [​](#evaluation-tools) Evaluation Tools

Patronus provides three main evaluation tools for different use cases:

1. **PatronusEvalTool**: Allows agents to select the most appropriate evaluator and criteria for the evaluation task.
2. **PatronusPredefinedCriteriaEvalTool**: Uses predefined evaluator and criteria specified by the user.
3. **PatronusLocalEvaluatorTool**: Uses custom function evaluators defined by the user.

## [​](#installation) Installation

To use these tools, you need to install the Patronus package:

Copy

Ask AI

```
uv add patronus
```

You’ll also need to set up your Patronus API key as an environment variable:

Copy

Ask AI

```
export PATRONUS_API_KEY="your_patronus_api_key"
```

## [​](#steps-to-get-started) Steps to Get Started

To effectively use the Patronus evaluation tools, follow these steps:

1. **Install Patronus**: Install the Patronus package using the command above.
2. **Set Up API Key**: Set your Patronus API key as an environment variable.
3. **Choose the Right Tool**: Select the appropriate Patronus evaluation tool based on your needs.
4. **Configure the Tool**: Configure the tool with the necessary parameters.

## [​](#examples) Examples

### [​](#using-patronusevaltool) Using PatronusEvalTool

The following example demonstrates how to use the `PatronusEvalTool`, which allows agents to select the most appropriate evaluator and criteria:

Code

Copy

Ask AI

```
from crewai import Agent, Task, Crew
from crewai_tools import PatronusEvalTool

# Initialize the tool
patronus_eval_tool = PatronusEvalTool()

# Define an agent that uses the tool
coding_agent = Agent(
    role="Coding Agent",
    goal="Generate high quality code and verify that the output is code",
    backstory="An experienced coder who can generate high quality python code.",
    tools=[patronus_eval_tool],
    verbose=True,
)

# Example task to generate and evaluate code
generate_code_task = Task(
    description="Create a simple program to generate the first N numbers in the Fibonacci sequence. Select the most appropriate evaluator and criteria for evaluating your output.",
    expected_output="Program that generates the first N numbers in the Fibonacci sequence.",
    agent=coding_agent,
)

# Create and run the crew
crew = Crew(agents=[coding_agent], tasks=[generate_code_task])
result = crew.kickoff()
```

### [​](#using-patronuspredefinedcriteriaevaltool) Using PatronusPredefinedCriteriaEvalTool

The following example demonstrates how to use the `PatronusPredefinedCriteriaEvalTool`, which uses predefined evaluator and criteria:

Code

Copy

Ask AI

```
from crewai import Agent, Task, Crew
from crewai_tools import PatronusPredefinedCriteriaEvalTool

# Initialize the tool with predefined criteria
patronus_eval_tool = PatronusPredefinedCriteriaEvalTool(
    evaluators=[{"evaluator": "judge", "criteria": "contains-code"}]
)

# Define an agent that uses the tool
coding_agent = Agent(
    role="Coding Agent",
    goal="Generate high quality code",
    backstory="An experienced coder who can generate high quality python code.",
    tools=[patronus_eval_tool],
    verbose=True,
)

# Example task to generate code
generate_code_task = Task(
    description="Create a simple program to generate the first N numbers in the Fibonacci sequence.",
    expected_output="Program that generates the first N numbers in the Fibonacci sequence.",
    agent=coding_agent,
)

# Create and run the crew
crew = Crew(agents=[coding_agent], tasks=[generate_code_task])
result = crew.kickoff()
```

### [​](#using-patronuslocalevaluatortool) Using PatronusLocalEvaluatorTool

The following example demonstrates how to use the `PatronusLocalEvaluatorTool`, which uses custom function evaluators:

Code

Copy

Ask AI

```
from crewai import Agent, Task, Crew
from crewai_tools import PatronusLocalEvaluatorTool
from patronus import Client, EvaluationResult
import random

# Initialize the Patronus client
client = Client()

# Register a custom evaluator
@client.register_local_evaluator("random_evaluator")
def random_evaluator(**kwargs):
    score = random.random()
    return EvaluationResult(
        score_raw=score,
        pass_=score >= 0.5,
        explanation="example explanation",
    )

# Initialize the tool with the custom evaluator
patronus_eval_tool = PatronusLocalEvaluatorTool(
    patronus_client=client,
    evaluator="random_evaluator",
    evaluated_model_gold_answer="example label",
)

# Define an agent that uses the tool
coding_agent = Agent(
    role="Coding Agent",
    goal="Generate high quality code",
    backstory="An experienced coder who can generate high quality python code.",
    tools=[patronus_eval_tool],
    verbose=True,
)

# Example task to generate code
generate_code_task = Task(
    description="Create a simple program to generate the first N numbers in the Fibonacci sequence.",
    expected_output="Program that generates the first N numbers in the Fibonacci sequence.",
    agent=coding_agent,
)

# Create and run the crew
crew = Crew(agents=[coding_agent], tasks=[generate_code_task])
result = crew.kickoff()
```

## [​](#parameters) Parameters

### [​](#patronusevaltool) PatronusEvalTool

The `PatronusEvalTool` does not require any parameters during initialization. It automatically fetches available evaluators and criteria from the Patronus API.

### [​](#patronuspredefinedcriteriaevaltool) PatronusPredefinedCriteriaEvalTool

The `PatronusPredefinedCriteriaEvalTool` accepts the following parameters during initialization:

* **evaluators**: Required. A list of dictionaries containing the evaluator and criteria to use. For example: `[{"evaluator": "judge", "criteria": "contains-code"}]`.

### [​](#patronuslocalevaluatortool) PatronusLocalEvaluatorTool

The `PatronusLocalEvaluatorTool` accepts the following parameters during initialization:

* **patronus\_client**: Required. The Patronus client instance.
* **evaluator**: Optional. The name of the registered local evaluator to use. Default is an empty string.
* **evaluated\_model\_gold\_answer**: Optional. The gold answer to use for evaluation. Default is an empty string.

## [​](#usage) Usage

When using the Patronus evaluation tools, you provide the model input, output, and context, and the tool returns the evaluation results from the Patronus API.
For the `PatronusEvalTool` and `PatronusPredefinedCriteriaEvalTool`, the following parameters are required when calling the tool:

* **evaluated\_model\_input**: The agent’s task description in simple text.
* **evaluated\_model\_output**: The agent’s output of the task.
* **evaluated\_model\_retrieved\_context**: The agent’s context.

For the `PatronusLocalEvaluatorTool`, the same parameters are required, but the evaluator and gold answer are specified during initialization.

## [​](#conclusion) Conclusion

The Patronus evaluation tools provide a powerful way to evaluate and score model inputs and outputs using the Patronus AI platform. By enabling agents to evaluate their own outputs or the outputs of other agents, these tools can help improve the quality and reliability of CrewAI workflows.

Was this page helpful?

YesNo

[Opik Integration

Previous](/en/observability/opik)[Portkey Integration

Next](/en/observability/portkey)

⌘I