OpenLIT Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

OpenLIT Integration

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

# [​](#openlit-overview) OpenLIT Overview

[OpenLIT](https://github.com/openlit/openlit?src=crewai-docs) is an open-source tool that makes it simple to monitor the performance of AI agents, LLMs, VectorDBs, and GPUs with just **one** line of code.
It provides OpenTelemetry-native tracing and metrics to track important parameters like cost, latency, interactions and task sequences.
This setup enables you to track hyperparameters and monitor for performance issues, helping you find ways to enhance and fine-tune your agents over time.

![Overview Agent usage including cost and tokens](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/openlit1.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=2b7fe9d84e9ec2b33c5eae6fa5668bee)![Overview of agent otel traces and metrics](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/openlit2.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=74bb57f622b6eeb67fd33d93d682df26)![Overview of agent traces in details](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/openlit3.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=734cbc0c8fee538986d74b063c20cef6)

OpenLIT Dashboard

### [​](#features) Features

* **Analytics Dashboard**: Monitor your Agents health and performance with detailed dashboards that track metrics, costs, and user interactions.
* **OpenTelemetry-native Observability SDK**: Vendor-neutral SDKs to send traces and metrics to your existing observability tools like Grafana, DataDog and more.
* **Cost Tracking for Custom and Fine-Tuned Models**: Tailor cost estimations for specific models using custom pricing files for precise budgeting.
* **Exceptions Monitoring Dashboard**: Quickly spot and resolve issues by tracking common exceptions and errors with a monitoring dashboard.
* **Compliance and Security**: Detect potential threats such as profanity and PII leaks.
* **Prompt Injection Detection**: Identify potential code injection and secret leaks.
* **API Keys and Secrets Management**: Securely handle your LLM API keys and secrets centrally, avoiding insecure practices.
* **Prompt Management**: Manage and version Agent prompts using PromptHub for consistent and easy access across Agents.
* **Model Playground** Test and compare different models for your CrewAI agents before deployment.

## [​](#setup-instructions) Setup Instructions

1

Deploy OpenLIT

1

Git Clone OpenLIT Repository

Copy

Ask AI

```
git clone [email protected]:openlit/openlit.git
```

2

Start Docker Compose

From the root directory of the [OpenLIT Repo](https://github.com/openlit/openlit), Run the below command:

Copy

Ask AI

```
docker compose up -d
```

2

Install OpenLIT SDK

Copy

Ask AI

```
pip install openlit
```

3

Initialize OpenLIT in Your Application

Add the following two lines to your application code:

* Setup using function arguments
* Setup using Environment Variables

Copy

Ask AI

```
import openlit
openlit.init(otlp_endpoint="http://127.0.0.1:4318")
```

Example Usage for monitoring a CrewAI Agent:

Copy

Ask AI

```
from crewai import Agent, Task, Crew, Process
import openlit

openlit.init(disable_metrics=True)
# Define your agents
researcher = Agent(
    role="Researcher",
    goal="Conduct thorough research and analysis on AI and AI agents",
    backstory="You're an expert researcher, specialized in technology, software engineering, AI, and startups. You work as a freelancer and are currently researching for a new client.",
    allow_delegation=False,
    llm='command-r'
)


# Define your task
task = Task(
    description="Generate a list of 5 interesting ideas for an article, then write one captivating paragraph for each idea that showcases the potential of a full article on this topic. Return the list of ideas with their paragraphs and your notes.",
    expected_output="5 bullet points, each with a paragraph and accompanying notes.",
)

# Define the manager agent
manager = Agent(
    role="Project Manager",
    goal="Efficiently manage the crew and ensure high-quality task completion",
    backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard.",
    allow_delegation=True,
    llm='command-r'
)

# Instantiate your crew with a custom manager
crew = Crew(
    agents=[researcher],
    tasks=[task],
    manager_agent=manager,
    process=Process.hierarchical,
)

# Start the crew's work
result = crew.kickoff()

print(result)
```

Add the following two lines to your application code:

Copy

Ask AI

```
import openlit

openlit.init()
```

Run the following command to configure the OTEL export endpoint:

Copy

Ask AI

```
export OTEL_EXPORTER_OTLP_ENDPOINT = "http://127.0.0.1:4318"
```

Example Usage for monitoring a CrewAI Async Agent:

Copy

Ask AI

```
import asyncio
from crewai import Crew, Agent, Task
import openlit

openlit.init(otlp_endpoint="http://127.0.0.1:4318")

# Create an agent with code execution enabled
coding_agent = Agent(
  role="Python Data Analyst",
  goal="Analyze data and provide insights using Python",
  backstory="You are an experienced data analyst with strong Python skills.",
  allow_code_execution=True,
  llm="command-r"
)

# Create a task that requires code execution
data_analysis_task = Task(
  description="Analyze the given dataset and calculate the average age of participants. Ages: {ages}",
  agent=coding_agent,
  expected_output="5 bullet points, each with a paragraph and accompanying notes.",
)

# Create a crew and add the task
analysis_crew = Crew(
  agents=[coding_agent],
  tasks=[data_analysis_task]
)

# Async function to kickoff the crew asynchronously
async def async_crew_execution():
    result = await analysis_crew.kickoff_async(inputs={"ages": [25, 30, 35, 40, 45]})
    print("Crew Result:", result)

# Run the async function
asyncio.run(async_crew_execution())
```

Refer to OpenLIT [Python SDK repository](https://github.com/openlit/openlit/tree/main/sdk/python) for more advanced configurations and use cases.

4

Visualize and Analyze

With the Agent Observability data now being collected and sent to OpenLIT, the next step is to visualize and analyze this data to get insights into your Agent’s performance, behavior, and identify areas of improvement.Just head over to OpenLIT at `127.0.0.1:3000` on your browser to start exploring. You can login using the default credentials

* **Email**: `[email protected]`
* **Password**: `openlituser`

![Overview Agent usage including cost and tokens](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/openlit1.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=2b7fe9d84e9ec2b33c5eae6fa5668bee)![Overview of agent otel traces and metrics](https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/openlit2.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=74bb57f622b6eeb67fd33d93d682df26)

OpenLIT Dashboard

Was this page helpful?

YesNo

[Neatlogs Integration

Previous](/en/observability/neatlogs)[Opik Integration

Next](/en/observability/opik)

⌘I