Production Architecture - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘K

Search...

Navigation

Core Concepts

Production Architecture

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

# [​](#the-flow-first-mindset) The Flow-First Mindset

When building production AI applications with CrewAI, **we recommend starting with a Flow**.
While it’s possible to run individual Crews or Agents, wrapping them in a Flow provides the necessary structure for a robust, scalable application.

## [​](#why-flows) Why Flows?

1. **State Management**: Flows provide a built-in way to manage state across different steps of your application. This is crucial for passing data between Crews, maintaining context, and handling user inputs.
2. **Control**: Flows allow you to define precise execution paths, including loops, conditionals, and branching logic. This is essential for handling edge cases and ensuring your application behaves predictably.
3. **Observability**: Flows provide a clear structure that makes it easier to trace execution, debug issues, and monitor performance. We recommend using [CrewAI Tracing](/en/observability/tracing) for detailed insights. Simply run `crewai login` to enable free observability features.

## [​](#the-architecture) The Architecture

A typical production CrewAI application looks like this:


### [​](#1-the-flow-class) 1. The Flow Class

Your `Flow` class is the entry point. It defines the state schema and the methods that execute your logic.

Copy

Ask AI

```
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class AppState(BaseModel):
    user_input: str = ""
    research_results: str = ""
    final_report: str = ""

class ProductionFlow(Flow[AppState]):
    @start()
    def gather_input(self):
        # ... logic to get input ...
        pass

    @listen(gather_input)
    def run_research_crew(self):
        # ... trigger a Crew ...
        pass
```

### [​](#2-state-management) 2. State Management

Use Pydantic models to define your state. This ensures type safety and makes it clear what data is available at each step.

* **Keep it minimal**: Store only what you need to persist between steps.
* **Use structured data**: Avoid unstructured dictionaries when possible.

### [​](#3-crews-as-units-of-work) 3. Crews as Units of Work

Delegate complex tasks to Crews. A Crew should be focused on a specific goal (e.g., “Research a topic”, “Write a blog post”).

* **Don’t over-engineer Crews**: Keep them focused.
* **Pass state explicitly**: Pass the necessary data from the Flow state to the Crew inputs.

Copy

Ask AI

```
    @listen(gather_input)
    def run_research_crew(self):
        crew = ResearchCrew()
        result = crew.kickoff(inputs={"topic": self.state.user_input})
        self.state.research_results = result.raw
```

## [​](#control-primitives) Control Primitives

Leverage CrewAI’s control primitives to add robustness and control to your Crews.

### [​](#1-task-guardrails) 1. Task Guardrails

Use [Task Guardrails](/en/concepts/tasks#task-guardrails) to validate task outputs before they are accepted. This ensures that your agents produce high-quality results.

Copy

Ask AI

```
def validate_content(result: TaskOutput) -> Tuple[bool, Any]:
    if len(result.raw) < 100:
        return (False, "Content is too short. Please expand.")
    return (True, result.raw)

task = Task(
    ...,
    guardrail=validate_content
)
```

### [​](#2-structured-outputs) 2. Structured Outputs

Always use structured outputs (`output_pydantic` or `output_json`) when passing data between tasks or to your application. This prevents parsing errors and ensures type safety.

Copy

Ask AI

```
class ResearchResult(BaseModel):
    summary: str
    sources: List[str]

task = Task(
    ...,
    output_pydantic=ResearchResult
)
```

### [​](#3-llm-hooks) 3. LLM Hooks

Use [LLM Hooks](/en/learn/llm-hooks) to inspect or modify messages before they are sent to the LLM, or to sanitize responses.

Copy

Ask AI

```
@before_llm_call
def log_request(context):
    print(f"Agent {context.agent.role} is calling the LLM...")
```

## [​](#deployment-patterns) Deployment Patterns

When deploying your Flow, consider the following:

### [​](#crewai-enterprise) CrewAI Enterprise

The easiest way to deploy your Flow is using CrewAI Enterprise. It handles the infrastructure, authentication, and monitoring for you.
Check out the [Deployment Guide](/en/enterprise/guides/deploy-crew) to get started.

Copy

Ask AI

```
crewai deploy create
```

### [​](#async-execution) Async Execution

For long-running tasks, use `kickoff_async` to avoid blocking your API.

### [​](#persistence) Persistence

Use the `@persist` decorator to save the state of your Flow to a database. This allows you to resume execution if the process crashes or if you need to wait for human input.

Copy

Ask AI

```
@persist
class ProductionFlow(Flow[AppState]):
    # ...
```

## [​](#summary) Summary

* **Start with a Flow.**
* **Define a clear State.**
* **Use Crews for complex tasks.**
* **Deploy with an API and persistence.**

Was this page helpful?

YesNo

[Flows

Previous](/en/concepts/flows)[Knowledge

Next](/en/concepts/knowledge)

⌘I