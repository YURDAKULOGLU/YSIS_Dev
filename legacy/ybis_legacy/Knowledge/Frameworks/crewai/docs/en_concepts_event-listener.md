Event Listeners - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Core Concepts

Event Listeners

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

CrewAI provides a powerful event system that allows you to listen for and react to various events that occur during the execution of your Crew. This feature enables you to build custom integrations, monitoring solutions, logging systems, or any other functionality that needs to be triggered based on CrewAI’s internal events.

## [​](#how-it-works) How It Works

CrewAI uses an event bus architecture to emit events throughout the execution lifecycle. The event system is built on the following components:

1. **CrewAIEventsBus**: A singleton event bus that manages event registration and emission
2. **BaseEvent**: Base class for all events in the system
3. **BaseEventListener**: Abstract base class for creating custom event listeners

When specific actions occur in CrewAI (like a Crew starting execution, an Agent completing a task, or a tool being used), the system emits corresponding events. You can register handlers for these events to execute custom code when they occur.

CrewAI AOP provides a built-in Prompt Tracing feature that leverages the event system to track, store, and visualize all prompts, completions, and associated metadata. This provides powerful debugging capabilities and transparency into your agent operations.![Prompt Tracing Dashboard](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/traces-overview.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=9c02d5b7306bf7adaeadd77a018f8fea)With Prompt Tracing you can:

* View the complete history of all prompts sent to your LLM
* Track token usage and costs
* Debug agent reasoning failures
* Share prompt sequences with your team
* Compare different prompt strategies
* Export traces for compliance and auditing

## [​](#creating-a-custom-event-listener) Creating a Custom Event Listener

To create a custom event listener, you need to:

1. Create a class that inherits from `BaseEventListener`
2. Implement the `setup_listeners` method
3. Register handlers for the events you’re interested in
4. Create an instance of your listener in the appropriate file

Here’s a simple example of a custom event listener class:

Copy

Ask AI

```
from crewai.events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    AgentExecutionCompletedEvent,
)
from crewai.events import BaseEventListener

class MyCustomListener(BaseEventListener):
    def __init__(self):
        super().__init__()

    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event):
            print(f"Crew '{event.crew_name}' has started execution!")

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_completed(source, event):
            print(f"Crew '{event.crew_name}' has completed execution!")
            print(f"Output: {event.output}")

        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source, event):
            print(f"Agent '{event.agent.role}' completed task")
            print(f"Output: {event.output}")
```

## [​](#properly-registering-your-listener) Properly Registering Your Listener

Simply defining your listener class isn’t enough. You need to create an instance of it and ensure it’s imported in your application. This ensures that:

1. The event handlers are registered with the event bus
2. The listener instance remains in memory (not garbage collected)
3. The listener is active when events are emitted

### [​](#option-1:-import-and-instantiate-in-your-crew-or-flow-implementation) Option 1: Import and Instantiate in Your Crew or Flow Implementation

The most important thing is to create an instance of your listener in the file where your Crew or Flow is defined and executed:

#### [​](#for-crew-based-applications) For Crew-based Applications

Create and import your listener at the top of your Crew implementation file:

Copy

Ask AI

```
# In your crew.py file
from crewai import Agent, Crew, Task
from my_listeners import MyCustomListener

# Create an instance of your listener
my_listener = MyCustomListener()

class MyCustomCrew:
    # Your crew implementation...

    def crew(self):
        return Crew(
            agents=[...],
            tasks=[...],
            # ...
        )
```

#### [​](#for-flow-based-applications) For Flow-based Applications

Create and import your listener at the top of your Flow implementation file:

Copy

Ask AI

```
# In your main.py or flow.py file
from crewai.flow import Flow, listen, start
from my_listeners import MyCustomListener

# Create an instance of your listener
my_listener = MyCustomListener()

class MyCustomFlow(Flow):
    # Your flow implementation...

    @start()
    def first_step(self):
        # ...
```

This ensures that your listener is loaded and active when your Crew or Flow is executed.

### [​](#option-2:-create-a-package-for-your-listeners) Option 2: Create a Package for Your Listeners

For a more structured approach, especially if you have multiple listeners:

1. Create a package for your listeners:

Copy

Ask AI

```
my_project/
  ├── listeners/
  │   ├── __init__.py
  │   ├── my_custom_listener.py
  │   └── another_listener.py
```

2. In `my_custom_listener.py`, define your listener class and create an instance:

Copy

Ask AI

```
# my_custom_listener.py
from crewai.events import BaseEventListener
# ... import events ...

class MyCustomListener(BaseEventListener):
    # ... implementation ...

# Create an instance of your listener
my_custom_listener = MyCustomListener()
```

3. In `__init__.py`, import the listener instances to ensure they’re loaded:

Copy

Ask AI

```
# __init__.py
from .my_custom_listener import my_custom_listener
from .another_listener import another_listener

# Optionally export them if you need to access them elsewhere
__all__ = ['my_custom_listener', 'another_listener']
```

4. Import your listeners package in your Crew or Flow file:

Copy

Ask AI

```
# In your crew.py or flow.py file
import my_project.listeners  # This loads all your listeners

class MyCustomCrew:
    # Your crew implementation...
```

This is how third-party event listeners are registered in the CrewAI codebase.

## [​](#available-event-types) Available Event Types

CrewAI provides a wide range of events that you can listen for:

### [​](#crew-events) Crew Events

* **CrewKickoffStartedEvent**: Emitted when a Crew starts execution
* **CrewKickoffCompletedEvent**: Emitted when a Crew completes execution
* **CrewKickoffFailedEvent**: Emitted when a Crew fails to complete execution
* **CrewTestStartedEvent**: Emitted when a Crew starts testing
* **CrewTestCompletedEvent**: Emitted when a Crew completes testing
* **CrewTestFailedEvent**: Emitted when a Crew fails to complete testing
* **CrewTrainStartedEvent**: Emitted when a Crew starts training
* **CrewTrainCompletedEvent**: Emitted when a Crew completes training
* **CrewTrainFailedEvent**: Emitted when a Crew fails to complete training

### [​](#agent-events) Agent Events

* **AgentExecutionStartedEvent**: Emitted when an Agent starts executing a task
* **AgentExecutionCompletedEvent**: Emitted when an Agent completes executing a task
* **AgentExecutionErrorEvent**: Emitted when an Agent encounters an error during execution

### [​](#task-events) Task Events

* **TaskStartedEvent**: Emitted when a Task starts execution
* **TaskCompletedEvent**: Emitted when a Task completes execution
* **TaskFailedEvent**: Emitted when a Task fails to complete execution
* **TaskEvaluationEvent**: Emitted when a Task is evaluated

### [​](#tool-usage-events) Tool Usage Events

* **ToolUsageStartedEvent**: Emitted when a tool execution is started
* **ToolUsageFinishedEvent**: Emitted when a tool execution is completed
* **ToolUsageErrorEvent**: Emitted when a tool execution encounters an error
* **ToolValidateInputErrorEvent**: Emitted when a tool input validation encounters an error
* **ToolExecutionErrorEvent**: Emitted when a tool execution encounters an error
* **ToolSelectionErrorEvent**: Emitted when there’s an error selecting a tool

### [​](#knowledge-events) Knowledge Events

* **KnowledgeRetrievalStartedEvent**: Emitted when a knowledge retrieval is started
* **KnowledgeRetrievalCompletedEvent**: Emitted when a knowledge retrieval is completed
* **KnowledgeQueryStartedEvent**: Emitted when a knowledge query is started
* **KnowledgeQueryCompletedEvent**: Emitted when a knowledge query is completed
* **KnowledgeQueryFailedEvent**: Emitted when a knowledge query fails
* **KnowledgeSearchQueryFailedEvent**: Emitted when a knowledge search query fails

### [​](#llm-guardrail-events) LLM Guardrail Events

* **LLMGuardrailStartedEvent**: Emitted when a guardrail validation starts. Contains details about the guardrail being applied and retry count.
* **LLMGuardrailCompletedEvent**: Emitted when a guardrail validation completes. Contains details about validation success/failure, results, and error messages if any.

### [​](#flow-events) Flow Events

* **FlowCreatedEvent**: Emitted when a Flow is created
* **FlowStartedEvent**: Emitted when a Flow starts execution
* **FlowFinishedEvent**: Emitted when a Flow completes execution
* **FlowPlotEvent**: Emitted when a Flow is plotted
* **MethodExecutionStartedEvent**: Emitted when a Flow method starts execution
* **MethodExecutionFinishedEvent**: Emitted when a Flow method completes execution
* **MethodExecutionFailedEvent**: Emitted when a Flow method fails to complete execution

### [​](#llm-events) LLM Events

* **LLMCallStartedEvent**: Emitted when an LLM call starts
* **LLMCallCompletedEvent**: Emitted when an LLM call completes
* **LLMCallFailedEvent**: Emitted when an LLM call fails
* **LLMStreamChunkEvent**: Emitted for each chunk received during streaming LLM responses

### [​](#memory-events) Memory Events

* **MemoryQueryStartedEvent**: Emitted when a memory query is started. Contains the query, limit, and optional score threshold.
* **MemoryQueryCompletedEvent**: Emitted when a memory query is completed successfully. Contains the query, results, limit, score threshold, and query execution time.
* **MemoryQueryFailedEvent**: Emitted when a memory query fails. Contains the query, limit, score threshold, and error message.
* **MemorySaveStartedEvent**: Emitted when a memory save operation is started. Contains the value to be saved, metadata, and optional agent role.
* **MemorySaveCompletedEvent**: Emitted when a memory save operation is completed successfully. Contains the saved value, metadata, agent role, and save execution time.
* **MemorySaveFailedEvent**: Emitted when a memory save operation fails. Contains the value, metadata, agent role, and error message.
* **MemoryRetrievalStartedEvent**: Emitted when memory retrieval for a task prompt starts. Contains the optional task ID.
* **MemoryRetrievalCompletedEvent**: Emitted when memory retrieval for a task prompt completes successfully. Contains the task ID, memory content, and retrieval execution time.

## [​](#event-handler-structure) Event Handler Structure

Each event handler receives two parameters:

1. **source**: The object that emitted the event
2. **event**: The event instance, containing event-specific data

The structure of the event object depends on the event type, but all events inherit from `BaseEvent` and include:

* **timestamp**: The time when the event was emitted
* **type**: A string identifier for the event type

Additional fields vary by event type. For example, `CrewKickoffCompletedEvent` includes `crew_name` and `output` fields.

## [​](#advanced-usage:-scoped-handlers) Advanced Usage: Scoped Handlers

For temporary event handling (useful for testing or specific operations), you can use the `scoped_handlers` context manager:

Copy

Ask AI

```
from crewai.events import crewai_event_bus, CrewKickoffStartedEvent

with crewai_event_bus.scoped_handlers():
    @crewai_event_bus.on(CrewKickoffStartedEvent)
    def temp_handler(source, event):
        print("This handler only exists within this context")

    # Do something that emits events

# Outside the context, the temporary handler is removed
```

## [​](#use-cases) Use Cases

Event listeners can be used for a variety of purposes:

1. **Logging and Monitoring**: Track the execution of your Crew and log important events
2. **Analytics**: Collect data about your Crew’s performance and behavior
3. **Debugging**: Set up temporary listeners to debug specific issues
4. **Integration**: Connect CrewAI with external systems like monitoring platforms, databases, or notification services
5. **Custom Behavior**: Trigger custom actions based on specific events

## [​](#best-practices) Best Practices

1. **Keep Handlers Light**: Event handlers should be lightweight and avoid blocking operations
2. **Error Handling**: Include proper error handling in your event handlers to prevent exceptions from affecting the main execution
3. **Cleanup**: If your listener allocates resources, ensure they’re properly cleaned up
4. **Selective Listening**: Only listen for events you actually need to handle
5. **Testing**: Test your event listeners in isolation to ensure they behave as expected

By leveraging CrewAI’s event system, you can extend its functionality and integrate it seamlessly with your existing infrastructure.

Was this page helpful?

YesNo

[Tools

Previous](/en/concepts/tools)[MCP Servers as Tools in CrewAI

Next](/en/mcp/overview)

⌘I