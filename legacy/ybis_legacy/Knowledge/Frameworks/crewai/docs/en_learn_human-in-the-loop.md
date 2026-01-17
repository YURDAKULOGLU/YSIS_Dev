Human-in-the-Loop (HITL) Workflows - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Learn

Human-in-the-Loop (HITL) Workflows

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

Human-in-the-Loop (HITL) is a powerful approach that combines artificial intelligence with human expertise to enhance decision-making and improve task outcomes. CrewAI provides multiple ways to implement HITL depending on your needs.

## [​](#choosing-your-hitl-approach) Choosing Your HITL Approach

CrewAI offers two main approaches for implementing human-in-the-loop workflows:

| Approach | Best For | Integration |
| --- | --- | --- |
| **Flow-based** (`@human_feedback` decorator) | Local development, console-based review, synchronous workflows | [Human Feedback in Flows](/en/learn/human-feedback-in-flows) |
| **Webhook-based** (Enterprise) | Production deployments, async workflows, external integrations (Slack, Teams, etc.) | This guide |

If you’re building flows and want to add human review steps with routing based on feedback, check out the [Human Feedback in Flows](/en/learn/human-feedback-in-flows) guide for the `@human_feedback` decorator.

## [​](#setting-up-webhook-based-hitl-workflows) Setting Up Webhook-Based HITL Workflows

1

Configure Your Task

Set up your task with human input enabled:

![Crew Human Input](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/crew-human-input.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=cb2e2bab131e9eff86b0c51dceb16e11)

2

Provide Webhook URL

When kicking off your crew, include a webhook URL for human input:

![Crew Webhook URL](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/crew-webhook-url.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=f2d298c0b4c7b3a62e1dee4e2e6f1bb3)

Example with Bearer authentication:

Copy

Ask AI

```
curl -X POST {BASE_URL}/kickoff \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
      "topic": "AI Research"
    },
    "humanInputWebhook": {
      "url": "https://your-webhook.com/hitl",
      "authentication": {
        "strategy": "bearer",
        "token": "your-webhook-secret-token"
      }
    }
  }'
```

Or with Basic authentication:

Copy

Ask AI

```
curl -X POST {BASE_URL}/kickoff \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
      "topic": "AI Research"
    },
    "humanInputWebhook": {
      "url": "https://your-webhook.com/hitl",
      "authentication": {
        "strategy": "basic",
        "username": "your-username",
        "password": "your-password"
      }
    }
  }'
```

3

Receive Webhook Notification

Once the crew completes the task requiring human input, you’ll receive a webhook notification containing:

* Execution ID
* Task ID
* Task output

4

Review Task Output

The system will pause in the `Pending Human Input` state. Review the task output carefully.

5

Submit Human Feedback

Call the resume endpoint of your crew with the following information:

![Crew Resume Endpoint](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/crew-resume-endpoint.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=1e1c2ca22a2d674426f8e663fed33eca)

**Critical: Webhook URLs Must Be Provided Again**:
You **must** provide the same webhook URLs (`taskWebhookUrl`, `stepWebhookUrl`, `crewWebhookUrl`) in the resume call that you used in the kickoff call. Webhook configurations are **NOT** automatically carried over from kickoff - they must be explicitly included in the resume request to continue receiving notifications for task completion, agent steps, and crew completion.

Example resume call with webhooks:

Copy

Ask AI

```
curl -X POST {BASE_URL}/resume \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "execution_id": "abcd1234-5678-90ef-ghij-klmnopqrstuv",
    "task_id": "research_task",
    "human_feedback": "Great work! Please add more details.",
    "is_approve": true,
    "taskWebhookUrl": "https://your-server.com/webhooks/task",
    "stepWebhookUrl": "https://your-server.com/webhooks/step",
    "crewWebhookUrl": "https://your-server.com/webhooks/crew"
  }'
```

**Feedback Impact on Task Execution**:
It’s crucial to exercise care when providing feedback, as the entire feedback content will be incorporated as additional context for further task executions.

This means:

* All information in your feedback becomes part of the task’s context.
* Irrelevant details may negatively influence it.
* Concise, relevant feedback helps maintain task focus and efficiency.
* Always review your feedback carefully before submission to ensure it contains only pertinent information that will positively guide the task’s execution.

6

Handle Negative Feedback

If you provide negative feedback:

* The crew will retry the task with added context from your feedback.
* You’ll receive another webhook notification for further review.
* Repeat steps 4-6 until satisfied.

7

Execution Continuation

When you submit positive feedback, the execution will proceed to the next steps.

## [​](#best-practices) Best Practices

* **Be Specific**: Provide clear, actionable feedback that directly addresses the task at hand
* **Stay Relevant**: Only include information that will help improve the task execution
* **Be Timely**: Respond to HITL prompts promptly to avoid workflow delays
* **Review Carefully**: Double-check your feedback before submitting to ensure accuracy

## [​](#common-use-cases) Common Use Cases

HITL workflows are particularly valuable for:

* Quality assurance and validation
* Complex decision-making scenarios
* Sensitive or high-stakes operations
* Creative tasks requiring human judgment
* Compliance and regulatory reviews

Was this page helpful?

YesNo

[Human Input on Execution

Previous](/en/learn/human-input-on-execution)[Human Feedback in Flows

Next](/en/learn/human-feedback-in-flows)

⌘I