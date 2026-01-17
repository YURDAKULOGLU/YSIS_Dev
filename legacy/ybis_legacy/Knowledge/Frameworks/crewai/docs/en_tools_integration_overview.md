Overview - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘K

Search...

Navigation

Integrations

Overview

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

  + [Overview](/en/tools/integration/overview)
  + [Bedrock Invoke Agent Tool](/en/tools/integration/bedrockinvokeagenttool)
  + [CrewAI Run Automation Tool](/en/tools/integration/crewaiautomationtool)
  + [Merge Agent Handler Tool](/en/tools/integration/mergeagenthandlertool)
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

Integration tools let your agents hand off work to other automation platforms and managed AI services. Use them when a workflow needs to invoke an existing CrewAI deployment or delegate specialised tasks to providers such as Amazon Bedrock.

## [​](#available-tools) **Available Tools**

[## Merge Agent Handler Tool

Securely access hundreds of third-party tools like Linear, GitHub, Slack, and more through Merge’s unified API.](/en/tools/integration/mergeagenthandlertool)[## CrewAI Run Automation Tool

Invoke live CrewAI Platform automations, pass custom inputs, and poll for results directly from your agent.](/en/tools/integration/crewaiautomationtool)[## Bedrock Invoke Agent Tool

Call Amazon Bedrock Agents from your crews, reuse AWS guardrails, and stream responses back into the workflow.](/en/tools/integration/bedrockinvokeagenttool)

## [​](#common-use-cases) **Common Use Cases**

* **Chain automations**: Kick off an existing CrewAI deployment from within another crew or flow
* **Enterprise hand-off**: Route tasks to Bedrock Agents that already encapsulate company logic and guardrails
* **Hybrid workflows**: Combine CrewAI reasoning with downstream systems that expose their own agent APIs
* **Long-running jobs**: Poll external automations and merge the final results back into the current run

## [​](#quick-start-example) **Quick Start Example**

Copy

Ask AI

```
from crewai import Agent, Task, Crew
from crewai_tools import InvokeCrewAIAutomationTool
from crewai_tools.aws.bedrock.agents.invoke_agent_tool import BedrockInvokeAgentTool

# External automation
analysis_automation = InvokeCrewAIAutomationTool(
    crew_api_url="https://analysis-crew.acme.crewai.com",
    crew_bearer_token="YOUR_BEARER_TOKEN",
    crew_name="Analysis Automation",
    crew_description="Runs the production-grade analysis pipeline",
)

# Managed agent on Bedrock
knowledge_router = BedrockInvokeAgentTool(
    agent_id="bedrock-agent-id",
    agent_alias_id="prod",
)

automation_strategist = Agent(
    role="Automation Strategist",
    goal="Orchestrate external automations and summarise their output",
    backstory="You coordinate enterprise workflows and know when to delegate tasks to specialised services.",
    tools=[analysis_automation, knowledge_router],
    verbose=True,
)

execute_playbook = Task(
    description="Run the analysis automation and ask the Bedrock agent for executive talking points.",
    agent=automation_strategist,
)

Crew(agents=[automation_strategist], tasks=[execute_playbook]).kickoff()
```

## [​](#best-practices) **Best Practices**

* **Secure credentials**: Store API keys and bearer tokens in environment variables or a secrets manager
* **Plan for latency**: External automations may take longer—set appropriate polling intervals and timeouts
* **Reuse sessions**: Bedrock Agents support session IDs so you can maintain context across multiple tool calls
* **Validate responses**: Normalise remote output (JSON, text, status codes) before forwarding it to downstream tasks
* **Monitor usage**: Track audit logs in CrewAI Platform or AWS CloudWatch to stay ahead of quota limits and failures

Was this page helpful?

YesNo

[Bedrock Knowledge Base Retriever

Previous](/en/tools/cloud-storage/bedrockkbretriever)[Bedrock Invoke Agent Tool

Next](/en/tools/integration/bedrockinvokeagenttool)

⌘I