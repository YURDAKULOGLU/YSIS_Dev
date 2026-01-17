Hierarchical Process - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Learn

Hierarchical Process

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

The hierarchical process in CrewAI introduces a structured approach to task management, simulating traditional organizational hierarchies for efficient task delegation and execution.
This systematic workflow enhances project outcomes by ensuring tasks are handled with optimal efficiency and accuracy.

The hierarchical process is designed to leverage advanced models like GPT-4, optimizing token usage while handling complex tasks with greater efficiency.

## [​](#hierarchical-process-overview) Hierarchical Process Overview

By default, tasks in CrewAI are managed through a sequential process. However, adopting a hierarchical approach allows for a clear hierarchy in task management,
where a ‘manager’ agent coordinates the workflow, delegates tasks, and validates outcomes for streamlined and effective execution. This manager agent can now be either
automatically created by CrewAI or explicitly set by the user.

### [​](#key-features) Key Features

* **Task Delegation**: A manager agent allocates tasks among crew members based on their roles and capabilities.
* **Result Validation**: The manager evaluates outcomes to ensure they meet the required standards.
* **Efficient Workflow**: Emulates corporate structures, providing an organized approach to task management.
* **System Prompt Handling**: Optionally specify whether the system should use predefined prompts.
* **Stop Words Control**: Optionally specify whether stop words should be used, supporting various models including the o1 models.
* **Context Window Respect**: Prioritize important context by enabling respect of the context window, which is now the default behavior.
* **Delegation Control**: Delegation is now disabled by default to give users explicit control.
* **Max Requests Per Minute**: Configurable option to set the maximum number of requests per minute.
* **Max Iterations**: Limit the maximum number of iterations for obtaining a final answer.

## [​](#implementing-the-hierarchical-process) Implementing the Hierarchical Process

To utilize the hierarchical process, it’s essential to explicitly set the process attribute to `Process.hierarchical`, as the default behavior is `Process.sequential`.
Define a crew with a designated manager and establish a clear chain of command.

Assign tools at the agent level to facilitate task delegation and execution by the designated agents under the manager’s guidance.
Tools can also be specified at the task level for precise control over tool availability during task execution.

Configuring the `manager_llm` parameter is crucial for the hierarchical process.
The system requires a manager LLM to be set up for proper function, ensuring tailored decision-making.

Code

Copy

Ask AI

```
from crewai import Crew, Process, Agent

# Agents are defined with attributes for backstory, cache, and verbose mode
researcher = Agent(
    role='Researcher',
    goal='Conduct in-depth analysis',
    backstory='Experienced data analyst with a knack for uncovering hidden trends.',
)
writer = Agent(
    role='Writer',
    goal='Create engaging content',
    backstory='Creative writer passionate about storytelling in technical domains.',
)

# Establishing the crew with a hierarchical process and additional configurations
project_crew = Crew(
    tasks=[...],  # Tasks to be delegated and executed under the manager's supervision
    agents=[researcher, writer],
    manager_llm="gpt-4o",  # Specify which LLM the manager should use
    process=Process.hierarchical,  
    planning=True, 
)
```

### [​](#using-a-custom-manager-agent) Using a Custom Manager Agent

Alternatively, you can create a custom manager agent with specific attributes tailored to your project’s management needs. This gives you more control over the manager’s behavior and capabilities.

Copy

Ask AI

```
# Define a custom manager agent
manager = Agent(
    role="Project Manager",
    goal="Efficiently manage the crew and ensure high-quality task completion",
    backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success.",
    allow_delegation=True,
)

# Use the custom manager in your crew
project_crew = Crew(
    tasks=[...],
    agents=[researcher, writer],
    manager_agent=manager,  # Use your custom manager agent
    process=Process.hierarchical,
    planning=True,
)
```

For more details on creating and customizing a manager agent, check out the [Custom Manager Agent documentation](/en/learn/custom-manager-agent).

### [​](#workflow-in-action) Workflow in Action

1. **Task Assignment**: The manager assigns tasks strategically, considering each agent’s capabilities and available tools.
2. **Execution and Review**: Agents complete their tasks with the option for asynchronous execution and callback functions for streamlined workflows.
3. **Sequential Task Progression**: Despite being a hierarchical process, tasks follow a logical order for smooth progression, facilitated by the manager’s oversight.

## [​](#conclusion) Conclusion

Adopting the hierarchical process in CrewAI, with the correct configurations and understanding of the system’s capabilities, facilitates an organized and efficient approach to project management.
Utilize the advanced features and customizations to tailor the workflow to your specific needs, ensuring optimal task execution and project success.

Was this page helpful?

YesNo

[Force Tool Output as Result

Previous](/en/learn/force-tool-output-as-result)[Human Input on Execution

Next](/en/learn/human-input-on-execution)

⌘I