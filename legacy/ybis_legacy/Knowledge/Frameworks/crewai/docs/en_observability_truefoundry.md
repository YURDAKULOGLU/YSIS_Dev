TrueFoundry Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

TrueFoundry Integration

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

TrueFoundry provides an enterprise-ready [AI Gateway](https://www.truefoundry.com/ai-gateway) which can integrate with agentic frameworks like CrewAI and provides governance and observability for your AI Applications. TrueFoundry AI Gateway serves as a unified interface for LLM access, providing:

* **Unified API Access**: Connect to 250+ LLMs (OpenAI, Claude, Gemini, Groq, Mistral) through one API
* **Low Latency**: Sub-3ms internal latency with intelligent routing and load balancing
* **Enterprise Security**: SOC 2, HIPAA, GDPR compliance with RBAC and audit logging
* **Quota and cost management**: Token-based quotas, rate limiting, and comprehensive usage tracking
* **Observability**: Full request/response logging, metrics, and traces with customizable retention

## [​](#how-truefoundry-integrates-with-crewai) How TrueFoundry Integrates with CrewAI

### [​](#installation-&-setup) Installation & Setup

1

Install CrewAI

Copy

Ask AI

```
pip install crewai
```

2

Get TrueFoundry Access Token

1. Sign up for a [TrueFoundry account](https://www.truefoundry.com/register)
2. Follow the steps here in [Quick start](https://docs.truefoundry.com/gateway/quick-start)

3

Configure CrewAI with TrueFoundry

![TrueFoundry Code Configuration](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/new-code-snippet.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=746c0bd23a77535f35b0b2bcf3320bf5)

Copy

Ask AI

```
from crewai import LLM

# Create an LLM instance with TrueFoundry AI Gateway
truefoundry_llm = LLM(
    model="openai-main/gpt-4o",  # Similarly, you can call any model from any provider
    base_url="your_truefoundry_gateway_base_url",
    api_key="your_truefoundry_api_key"
)

# Use in your CrewAI agents
from crewai import Agent

@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        llm=truefoundry_llm,
        verbose=True
    )
```

### [​](#complete-crewai-example) Complete CrewAI Example

Copy

Ask AI

```
from crewai import Agent, Task, Crew, LLM

# Configure LLM with TrueFoundry
llm = LLM(
    model="openai-main/gpt-4o",
    base_url="your_truefoundry_gateway_base_url", 
    api_key="your_truefoundry_api_key"
)

# Create agents
researcher = Agent(
    role='Research Analyst',
    goal='Conduct detailed market research',
    backstory='Expert market analyst with attention to detail',
    llm=llm,
    verbose=True
)

writer = Agent(
    role='Content Writer', 
    goal='Create comprehensive reports',
    backstory='Experienced technical writer',
    llm=llm,
    verbose=True
)

# Create tasks
research_task = Task(
    description='Research AI market trends for 2024',
    agent=researcher,
    expected_output='Comprehensive research summary'
)

writing_task = Task(
    description='Create a market research report',
    agent=writer,
    expected_output='Well-structured report with insights',
    context=[research_task]
)

# Create and execute crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

result = crew.kickoff()
```

### [​](#observability-and-governance) Observability and Governance

Monitor your CrewAI agents through TrueFoundry’s metrics tab:
![TrueFoundry metrics](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/gateway-metrics.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=33755ff848cb457e162e806c20c98216)
With Truefoundry’s AI gateway, you can monitor and analyze:

* **Performance Metrics**: Track key latency metrics like Request Latency, Time to First Token (TTFS), and Inter-Token Latency (ITL) with P99, P90, and P50 percentiles
* **Cost and Token Usage**: Gain visibility into your application’s costs with detailed breakdowns of input/output tokens and the associated expenses for each model
* **Usage Patterns**: Understand how your application is being used with detailed analytics on user activity, model distribution, and team-based usage
* **Rate limit and Load balancing**: You can set up rate limiting, load balancing and fallback for your models

## [​](#tracing) Tracing

For a more detailed understanding on tracing, please see [getting-started-tracing](https://docs.truefoundry.com/docs/tracing/tracing-getting-started).For tracing, you can add the Traceloop SDK:
For tracing, you can add the Traceloop SDK:

Copy

Ask AI

```
pip install traceloop-sdk
```

Copy

Ask AI

```
from traceloop.sdk import Traceloop

# Initialize enhanced tracing
Traceloop.init(
    api_endpoint="https://your-truefoundry-endpoint/api/tracing",
    headers={
        "Authorization": f"Bearer {your_truefoundry_pat_token}",
        "TFY-Tracing-Project": "your_project_name",
    },
)
```

This provides additional trace correlation across your entire CrewAI workflow.
![TrueFoundry CrewAI Tracing](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/tracing_crewai.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=90623834e0ba9f4ccb09890f6824912d)

Was this page helpful?

YesNo

[Weave Integration

Previous](/en/observability/weave)[Overview

Next](/en/learn/overview)

⌘I