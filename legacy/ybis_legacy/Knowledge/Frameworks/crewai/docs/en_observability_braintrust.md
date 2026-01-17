Braintrust - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

Braintrust

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

# [​](#braintrust-integration) Braintrust Integration

This guide demonstrates how to integrate **Braintrust** with **CrewAI** using OpenTelemetry for comprehensive tracing and evaluation. By the end of this guide, you will be able to trace your CrewAI agents, monitor their performance, and evaluate their outputs using Braintrust’s powerful observability platform.
> **What is Braintrust?** [Braintrust](https://www.braintrust.dev) is an AI evaluation and observability platform that provides comprehensive tracing, evaluation, and monitoring for AI applications with built-in experiment tracking and performance analytics.

## [​](#get-started) Get Started

We’ll walk through a simple example of using CrewAI and integrating it with Braintrust via OpenTelemetry for comprehensive observability and evaluation.

### [​](#step-1:-install-dependencies) Step 1: Install Dependencies

Copy

Ask AI

```
uv add braintrust[otel] crewai crewai-tools opentelemetry-instrumentation-openai opentelemetry-instrumentation-crewai python-dotenv
```

### [​](#step-2:-set-up-environment-variables) Step 2: Set Up Environment Variables

Setup Braintrust API keys and configure OpenTelemetry to send traces to Braintrust. You’ll need a Braintrust API key and your OpenAI API key.

Copy

Ask AI

```
import os
from getpass import getpass

# Get your Braintrust credentials
BRAINTRUST_API_KEY = getpass("🔑 Enter your Braintrust API Key: ")

# Get API keys for services
OPENAI_API_KEY = getpass("🔑 Enter your OpenAI API key: ")

# Set environment variables
os.environ["BRAINTRUST_API_KEY"] = BRAINTRUST_API_KEY
os.environ["BRAINTRUST_PARENT"] = "project_name:crewai-demo"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
```

### [​](#step-3:-initialize-opentelemetry-with-braintrust) Step 3: Initialize OpenTelemetry with Braintrust

Initialize the Braintrust OpenTelemetry instrumentation to start capturing traces and send them to Braintrust.

Copy

Ask AI

```
import os
from typing import Any, Dict

from braintrust.otel import BraintrustSpanProcessor
from crewai import Agent, Crew, Task
from crewai.llm import LLM
from opentelemetry import trace
from opentelemetry.instrumentation.crewai import CrewAIInstrumentor
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from opentelemetry.sdk.trace import TracerProvider

def setup_tracing() -> None:
    """Setup OpenTelemetry tracing with Braintrust."""
    current_provider = trace.get_tracer_provider()
    if isinstance(current_provider, TracerProvider):
        provider = current_provider
    else:
        provider = TracerProvider()
        trace.set_tracer_provider(provider)

    provider.add_span_processor(BraintrustSpanProcessor())
    CrewAIInstrumentor().instrument(tracer_provider=provider)
    OpenAIInstrumentor().instrument(tracer_provider=provider)


setup_tracing()
```

### [​](#step-4:-create-a-crewai-application) Step 4: Create a CrewAI Application

We’ll create a CrewAI application where two agents collaborate to research and write a blog post about AI advancements, with comprehensive tracing enabled.

Copy

Ask AI

```
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool

def create_crew() -> Crew:
    """Create a crew with multiple agents for comprehensive tracing."""
    llm = LLM(model="gpt-4o-mini")
    search_tool = SerperDevTool()

    # Define agents with specific roles
    researcher = Agent(
        role="Senior Research Analyst",
        goal="Uncover cutting-edge developments in AI and data science",
        backstory="""You work at a leading tech think tank.
        Your expertise lies in identifying emerging trends.
        You have a knack for dissecting complex data and presenting actionable insights.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[search_tool],
    )

    writer = Agent(
        role="Tech Content Strategist",
        goal="Craft compelling content on tech advancements",
        backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
        You transform complex concepts into compelling narratives.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
    )

    # Create tasks for your agents
    research_task = Task(
        description="""Conduct a comprehensive analysis of the latest advancements in {topic}.
        Identify key trends, breakthrough technologies, and potential industry impacts.""",
        expected_output="Full analysis report in bullet points",
        agent=researcher,
    )

    writing_task = Task(
        description="""Using the insights provided, develop an engaging blog
        post that highlights the most significant {topic} advancements.
        Your post should be informative yet accessible, catering to a tech-savvy audience.
        Make it sound cool, avoid complex words so it doesn't sound like AI.""",
        expected_output="Full blog post of at least 4 paragraphs",
        agent=writer,
        context=[research_task],
    )

    # Instantiate your crew with a sequential process
    crew = Crew(
        agents=[researcher, writer], 
        tasks=[research_task, writing_task], 
        verbose=True, 
        process=Process.sequential
    )

    return crew

def run_crew():
    """Run the crew and return results."""
    crew = create_crew()
    result = crew.kickoff(inputs={"topic": "AI developments"})
    return result

# Run your crew
if __name__ == "__main__":
    # Instrumentation is already initialized above in this module
    result = run_crew()
    print(result)
```

### [​](#step-5:-view-traces-in-braintrust) Step 5: View Traces in Braintrust

After running your crew, you can view comprehensive traces in Braintrust through different perspectives:

* Trace
* Timeline
* Thread

![Braintrust Trace View](https://mintcdn.com/crewai/sTI-JqU6hicMPzD1/images/braintrust-trace-view.png?fit=max&auto=format&n=sTI-JqU6hicMPzD1&q=85&s=311f727eeadf1c39380c08e992278dd0)

![Braintrust Timeline View](https://mintcdn.com/crewai/sTI-JqU6hicMPzD1/images/braintrust-timeline-view.png?fit=max&auto=format&n=sTI-JqU6hicMPzD1&q=85&s=03090206aecd3a7b2f21a24af2514b08)

![Braintrust Thread View](https://mintcdn.com/crewai/sTI-JqU6hicMPzD1/images/braintrust-thread-view.png?fit=max&auto=format&n=sTI-JqU6hicMPzD1&q=85&s=1bc0a6842a5dd9e6d7c2dd742417e79b)

### [​](#step-6:-evaluate-via-sdk-experiments) Step 6: Evaluate via SDK (Experiments)

You can also run evaluations using Braintrust’s Eval SDK. This is useful for comparing versions or scoring outputs offline. Below is a Python example using the `Eval` class with the crew we created above:

Copy

Ask AI

```
# eval_crew.py
from braintrust import Eval
from autoevals import Levenshtein

def evaluate_crew_task(input_data):
    """Task function that wraps our crew for evaluation."""
    crew = create_crew()
    result = crew.kickoff(inputs={"topic": input_data["topic"]})
    return str(result)

Eval(
    "AI Research Crew",  # Project name
    {
        "data": lambda: [
            {"topic": "artificial intelligence trends 2024"},
            {"topic": "machine learning breakthroughs"},
            {"topic": "AI ethics and governance"},
        ],
        "task": evaluate_crew_task,
        "scores": [Levenshtein],
    },
)
```

Setup your API key and run:

Copy

Ask AI

```
export BRAINTRUST_API_KEY="YOUR_API_KEY"
braintrust eval eval_crew.py
```

See the [Braintrust Eval SDK guide](https://www.braintrust.dev/docs/start/eval-sdk) for more details.

### [​](#key-features-of-braintrust-integration) Key Features of Braintrust Integration

* **Comprehensive Tracing**: Track all agent interactions, tool usage, and LLM calls
* **Performance Monitoring**: Monitor execution times, token usage, and success rates
* **Experiment Tracking**: Compare different crew configurations and models
* **Automated Evaluation**: Set up custom evaluation metrics for crew outputs
* **Error Tracking**: Monitor and debug failures across your crew executions
* **Cost Analysis**: Track token usage and associated costs

### [​](#version-compatibility-information) Version Compatibility Information

* Python 3.8+
* CrewAI >= 0.86.0
* Braintrust >= 0.1.0
* OpenTelemetry SDK >= 1.31.0

### [​](#references) References

* [Braintrust Documentation](https://www.braintrust.dev/docs) - Overview of the Braintrust platform
* [Braintrust CrewAI Integration](https://www.braintrust.dev/docs/integrations/crew-ai) - Official CrewAI integration guide
* [Braintrust Eval SDK](https://www.braintrust.dev/docs/start/eval-sdk) - Run experiments via the SDK
* [CrewAI Documentation](https://docs.crewai.com/) - Overview of the CrewAI framework
* [OpenTelemetry Docs](https://opentelemetry.io/docs/) - OpenTelemetry guide
* [Braintrust GitHub](https://github.com/braintrustdata/braintrust) - Source code for Braintrust SDK

Was this page helpful?

YesNo

[Arize Phoenix

Previous](/en/observability/arize-phoenix)[Datadog Integration

Next](/en/observability/datadog)

⌘I