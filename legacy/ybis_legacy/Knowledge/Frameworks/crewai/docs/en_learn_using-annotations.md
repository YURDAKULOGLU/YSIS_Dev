Using Annotations in crew.py - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Learn

Using Annotations in crew.py

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

This guide explains how to use annotations to properly reference **agents**, **tasks**, and other components in the `crew.py` file.

## [​](#introduction) Introduction

Annotations in the CrewAI framework are used to decorate classes and methods, providing metadata and functionality to various components of your crew. These annotations help in organizing and structuring your code, making it more readable and maintainable.

## [​](#available-annotations) Available Annotations

The CrewAI framework provides the following annotations:

* `@CrewBase`: Used to decorate the main crew class.
* `@agent`: Decorates methods that define and return Agent objects.
* `@task`: Decorates methods that define and return Task objects.
* `@crew`: Decorates the method that creates and returns the Crew object.
* `@llm`: Decorates methods that initialize and return Language Model objects.
* `@tool`: Decorates methods that initialize and return Tool objects.
* `@callback`: Used for defining callback methods.
* `@output_json`: Used for methods that output JSON data.
* `@output_pydantic`: Used for methods that output Pydantic models.
* `@cache_handler`: Used for defining cache handling methods.

## [​](#usage-examples) Usage Examples

Let’s go through examples of how to use these annotations:

### [​](#1-crew-base-class) 1. Crew Base Class

Copy

Ask AI

```
@CrewBase
class LinkedinProfileCrew():
    """LinkedinProfile crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
```

The `@CrewBase` annotation is used to decorate the main crew class. This class typically contains configurations and methods for creating agents, tasks, and the crew itself.

`@CrewBase` does more than register the class:

* **Configuration bootstrapping:** looks for `agents_config` and `tasks_config` (defaulting to `config/agents.yaml` and `config/tasks.yaml`) beside the class file, loads them at instantiation, and safely falls back to empty dicts if files are missing.
* **Decorator orchestration:** keeps memoized references to every method marked with `@agent`, `@task`, `@before_kickoff`, or `@after_kickoff` so they are instantiated once per crew and executed in declaration order.
* **Hook wiring:** automatically attaches the preserved kickoff hooks to the `Crew` object returned by the `@crew` method, making them run before and after `.kickoff()`.
* **MCP integration:** when the class defines `mcp_server_params`, `get_mcp_tools()` lazily starts an MCP server adapter, hydrates the declared tools, and an internal after-kickoff hook stops the adapter. See [MCP overview](/en/mcp/overview) for adapter configuration details.

### [​](#2-tool-definition) 2. Tool Definition

Copy

Ask AI

```
@tool
def myLinkedInProfileTool(self):
    return LinkedInProfileTool()
```

The `@tool` annotation is used to decorate methods that return tool objects. These tools can be used by agents to perform specific tasks.

### [​](#3-llm-definition) 3. LLM Definition

Copy

Ask AI

```
@llm
def groq_llm(self):
    api_key = os.getenv('api_key')
    return ChatGroq(api_key=api_key, temperature=0, model_name="mixtral-8x7b-32768")
```

The `@llm` annotation is used to decorate methods that initialize and return Language Model objects. These LLMs are used by agents for natural language processing tasks.

### [​](#4-agent-definition) 4. Agent Definition

Copy

Ask AI

```
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher']
    )
```

The `@agent` annotation is used to decorate methods that define and return Agent objects.

### [​](#5-task-definition) 5. Task Definition

Copy

Ask AI

```
@task
def research_task(self) -> Task:
    return Task(
        config=self.tasks_config['research_linkedin_task'],
        agent=self.researcher()
    )
```

The `@task` annotation is used to decorate methods that define and return Task objects. These methods specify the task configuration and the agent responsible for the task.

### [​](#6-crew-creation) 6. Crew Creation

Copy

Ask AI

```
@crew
def crew(self) -> Crew:
    """Creates the LinkedinProfile crew"""
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.sequential,
        verbose=True
    )
```

The `@crew` annotation is used to decorate the method that creates and returns the `Crew` object. This method assembles all the components (agents and tasks) into a functional crew.

## [​](#yaml-configuration) YAML Configuration

The agent configurations are typically stored in a YAML file. Here’s an example of how the `agents.yaml` file might look for the researcher agent:

Copy

Ask AI

```
researcher:
    role: >
        LinkedIn Profile Senior Data Researcher
    goal: >
        Uncover detailed LinkedIn profiles based on provided name {name} and domain {domain}
        Generate a Dall-E image based on domain {domain}
    backstory: >
        You're a seasoned researcher with a knack for uncovering the most relevant LinkedIn profiles.
        Known for your ability to navigate LinkedIn efficiently, you excel at gathering and presenting
        professional information clearly and concisely.
    allow_delegation: False
    verbose: True
    llm: groq_llm
    tools:
        - myLinkedInProfileTool
        - mySerperDevTool
        - myDallETool
```

This YAML configuration corresponds to the researcher agent defined in the `LinkedinProfileCrew` class. The configuration specifies the agent’s role, goal, backstory, and other properties such as the LLM and tools it uses.
Note how the `llm` and `tools` in the YAML file correspond to the methods decorated with `@llm` and `@tool` in the Python class.

## [​](#best-practices) Best Practices

* **Consistent Naming**: Use clear and consistent naming conventions for your methods. For example, agent methods could be named after their roles (e.g., researcher, reporting\_analyst).
* **Environment Variables**: Use environment variables for sensitive information like API keys.
* **Flexibility**: Design your crew to be flexible by allowing easy addition or removal of agents and tasks.
* **YAML-Code Correspondence**: Ensure that the names and structures in your YAML files correspond correctly to the decorated methods in your Python code.

By following these guidelines and properly using annotations, you can create well-structured and maintainable crews using the CrewAI framework.

Was this page helpful?

YesNo

[Sequential Processes

Previous](/en/learn/sequential-process)[Execution Hooks Overview

Next](/en/learn/execution-hooks)

⌘I