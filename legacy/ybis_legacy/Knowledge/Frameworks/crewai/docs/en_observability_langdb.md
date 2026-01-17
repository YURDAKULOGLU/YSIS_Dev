LangDB Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

LangDB Integration

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

# [​](#introduction) Introduction

[LangDB AI Gateway](https://langdb.ai) provides OpenAI-compatible APIs to connect with multiple Large Language Models and serves as an observability platform that makes it effortless to trace CrewAI workflows end-to-end while providing access to 350+ language models. With a single `init()` call, all agent interactions, task executions, and LLM calls are captured, providing comprehensive observability and production-ready AI infrastructure for your applications.

![LangDB CrewAI trace example](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/langdb-1.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=6303d15055c19a7a6ec9d0c664f15c9f)

LangDB CrewAI Trace Example

**Checkout:** [View the live trace example](https://app.langdb.ai/sharing/threads/3becbfed-a1be-ae84-ea3c-4942867a3e22)

## [​](#features) Features

### [​](#ai-gateway-capabilities) AI Gateway Capabilities

* **Access to 350+ LLMs**: Connect to all major language models through a single integration
* **Virtual Models**: Create custom model configurations with specific parameters and routing rules
* **Virtual MCP**: Enable compatibility and integration with MCP (Model Context Protocol) systems for enhanced agent communication
* **Guardrails**: Implement safety measures and compliance controls for agent behavior

### [​](#observability-&-tracing) Observability & Tracing

* **Automatic Tracing**: Single `init()` call captures all CrewAI interactions
* **End-to-End Visibility**: Monitor agent workflows from start to finish
* **Tool Usage Tracking**: Track which tools agents use and their outcomes
* **Model Call Monitoring**: Detailed insights into LLM interactions
* **Performance Analytics**: Monitor latency, token usage, and costs
* **Debugging Support**: Step-through execution for troubleshooting
* **Real-time Monitoring**: Live traces and metrics dashboard

## [​](#setup-instructions) Setup Instructions

1

Install LangDB

Install the LangDB client with CrewAI feature flag:

Copy

Ask AI

```
pip install 'pylangdb[crewai]'
```

2

Set Environment Variables

Configure your LangDB credentials:

Copy

Ask AI

```
export LANGDB_API_KEY="<your_langdb_api_key>"
export LANGDB_PROJECT_ID="<your_langdb_project_id>"
export LANGDB_API_BASE_URL='https://api.us-east-1.langdb.ai'
```

3

Initialize Tracing

Import and initialize LangDB before configuring your CrewAI code:

Copy

Ask AI

```
from pylangdb.crewai import init
# Initialize LangDB
init()
```

4

Configure CrewAI with LangDB

Set up your LLM with LangDB headers:

Copy

Ask AI

```
from crewai import Agent, Task, Crew, LLM
import os

# Configure LLM with LangDB headers
llm = LLM(
    model="openai/gpt-4o", # Replace with the model you want to use
    api_key=os.getenv("LANGDB_API_KEY"),
    base_url=os.getenv("LANGDB_API_BASE_URL"),
    extra_headers={"x-project-id": os.getenv("LANGDB_PROJECT_ID")}
)
```

## [​](#quick-start-example) Quick Start Example

Here’s a simple example to get you started with LangDB and CrewAI:

Copy

Ask AI

```
import os
from pylangdb.crewai import init
from crewai import Agent, Task, Crew, LLM

# Initialize LangDB before any CrewAI imports
init()

def create_llm(model):
    return LLM(
        model=model,
        api_key=os.environ.get("LANGDB_API_KEY"),
        base_url=os.environ.get("LANGDB_API_BASE_URL"),
        extra_headers={"x-project-id": os.environ.get("LANGDB_PROJECT_ID")}
    )

# Define your agent
researcher = Agent(
    role="Research Specialist",
    goal="Research topics thoroughly",
    backstory="Expert researcher with skills in finding information",
    llm=create_llm("openai/gpt-4o"), # Replace with the model you want to use
    verbose=True
)

# Create a task
task = Task(
    description="Research the given topic and provide a comprehensive summary",
    agent=researcher,
    expected_output="Detailed research summary with key findings"
)

# Create and run the crew
crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
print(result)
```

## [​](#complete-example:-research-and-planning-agent) Complete Example: Research and Planning Agent

This comprehensive example demonstrates a multi-agent workflow with research and planning capabilities.

### [​](#prerequisites) Prerequisites

Copy

Ask AI

```
pip install crewai 'pylangdb[crewai]' crewai_tools setuptools python-dotenv
```

### [​](#environment-setup) Environment Setup

Copy

Ask AI

```
# LangDB credentials
export LANGDB_API_KEY="<your_langdb_api_key>"
export LANGDB_PROJECT_ID="<your_langdb_project_id>"
export LANGDB_API_BASE_URL='https://api.us-east-1.langdb.ai'

# Additional API keys (optional)
export SERPER_API_KEY="<your_serper_api_key>"  # For web search capabilities
```

### [​](#complete-implementation) Complete Implementation

Copy

Ask AI

```
#!/usr/bin/env python3

import os
import sys
from pylangdb.crewai import init
init()  # Initialize LangDB before any CrewAI imports
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

load_dotenv()

def create_llm(model):
    return LLM(
        model=model,
        api_key=os.environ.get("LANGDB_API_KEY"),
        base_url=os.environ.get("LANGDB_API_BASE_URL"),
        extra_headers={"x-project-id": os.environ.get("LANGDB_PROJECT_ID")}
    )

class ResearchPlanningCrew:
    def researcher(self) -> Agent:
        return Agent(
            role="Research Specialist",
            goal="Research topics thoroughly and compile comprehensive information",
            backstory="Expert researcher with skills in finding and analyzing information from various sources",
            tools=[SerperDevTool()],
            llm=create_llm("openai/gpt-4o"),
            verbose=True
        )
    
    def planner(self) -> Agent:
        return Agent(
            role="Strategic Planner",
            goal="Create actionable plans based on research findings",
            backstory="Strategic planner who breaks down complex challenges into executable plans",
            reasoning=True,
            max_reasoning_attempts=3,
            llm=create_llm("openai/anthropic/claude-3.7-sonnet"),
            verbose=True
        )
    
    def research_task(self) -> Task:
        return Task(
            description="Research the topic thoroughly and compile comprehensive information",
            agent=self.researcher(),
            expected_output="Comprehensive research report with key findings and insights"
        )
    
    def planning_task(self) -> Task:
        return Task(
            description="Create a strategic plan based on the research findings",
            agent=self.planner(),
            expected_output="Strategic execution plan with phases, goals, and actionable steps",
            context=[self.research_task()]
        )
    
    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher(), self.planner()],
            tasks=[self.research_task(), self.planning_task()],
            verbose=True,
            process=Process.sequential
        )

def main():
        topic = sys.argv[1] if len(sys.argv) > 1 else "Artificial Intelligence in Healthcare"
        
        crew_instance = ResearchPlanningCrew()
        
        # Update task descriptions with the specific topic
        crew_instance.research_task().description = f"Research {topic} thoroughly and compile comprehensive information"
    crew_instance.planning_task().description = f"Create a strategic plan for {topic} based on the research findings"
    
    result = crew_instance.crew().kickoff()
    print(result)

if __name__ == "__main__":
    main()
```

### [​](#running-the-example) Running the Example

Copy

Ask AI

```
python main.py "Sustainable Energy Solutions"
```

## [​](#viewing-traces-in-langdb) Viewing Traces in LangDB

After running your CrewAI application, you can view detailed traces in the LangDB dashboard:

![LangDB trace dashboard showing CrewAI workflow](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/langdb-2.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=74a88afefce3f84fb6f9482a1790b413)

LangDB Trace Dashboard

### [​](#what-you’ll-see) What You’ll See

* **Agent Interactions**: Complete flow of agent conversations and task handoffs
* **Tool Usage**: Which tools were called, their inputs, and outputs
* **Model Calls**: Detailed LLM interactions with prompts image.pngand responses
* **Performance Metrics**: Latency, token usage, and cost tracking
* **Execution Timeline**: Step-by-step view of the entire workflow

## [​](#troubleshooting) Troubleshooting

### [​](#common-issues) Common Issues

* **No traces appearing**: Ensure `init()` is called before any CrewAI imports
* **Authentication errors**: Verify your LangDB API key and project ID

## [​](#resources) Resources

[## LangDB Documentation

Official LangDB documentation and guides](https://docs.langdb.ai)[## LangDB Guides

Step-by-step tutorials for building AI agents](https://docs.langdb.ai/guides)[## GitHub Examples

Complete CrewAI integration examples](https://github.com/langdb/langdb-samples/tree/main/examples/crewai)[## LangDB Dashboard

Access your traces and analytics](https://app.langdb.ai)[## Model Catalog

Browse 350+ available language models](https://app.langdb.ai/models)[## Enterprise Features

Self-hosted options and enterprise capabilities](https://docs.langdb.ai/enterprise)

## [​](#next-steps) Next Steps

This guide covered the basics of integrating LangDB AI Gateway with CrewAI. To further enhance your AI workflows, explore:

* **Virtual Models**: Create custom model configurations with routing strategies
* **Guardrails & Safety**: Implement content filtering and compliance controls
* **Production Deployment**: Configure fallbacks, retries, and load balancing

For more advanced features and use cases, visit the [LangDB Documentation](https://docs.langdb.ai) or explore the [Model Catalog](https://app.langdb.ai/models) to discover all available models.

Was this page helpful?

YesNo

[Datadog Integration

Previous](/en/observability/datadog)[Langfuse Integration

Next](/en/observability/langfuse)

⌘I