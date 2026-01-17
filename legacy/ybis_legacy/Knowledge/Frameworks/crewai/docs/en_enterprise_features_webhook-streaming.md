Webhook Streaming - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Operate

Webhook Streaming

[Home](/)[Documentation](/en/introduction)[AOP](/en/enterprise/introduction)[API Reference](/en/api-reference/introduction)[Examples](/en/examples/example)[Changelog](/en/changelog)

* [Website](https://crewai.com)
* [Forum](https://community.crewai.com)
* [Blog](https://blog.crewai.com)
* [CrewGPT](https://chatgpt.com/g/g-qqTuUWsBY-crewai-assistant)

##### Getting Started

* [CrewAI AOP](/en/enterprise/introduction)

##### Build

* [Automations](/en/enterprise/features/automations)
* [Crew Studio](/en/enterprise/features/crew-studio)
* [Marketplace](/en/enterprise/features/marketplace)
* [Agent Repositories](/en/enterprise/features/agent-repositories)
* [Tools & Integrations](/en/enterprise/features/tools-and-integrations)

##### Operate

* [Traces](/en/enterprise/features/traces)
* [Webhook Streaming](/en/enterprise/features/webhook-streaming)
* [Hallucination Guardrail](/en/enterprise/features/hallucination-guardrail)

##### Manage

* [Role-Based Access Control (RBAC)](/en/enterprise/features/rbac)

##### Integration Docs

* [Asana Integration](/en/enterprise/integrations/asana)
* [Box Integration](/en/enterprise/integrations/box)
* [ClickUp Integration](/en/enterprise/integrations/clickup)
* [GitHub Integration](/en/enterprise/integrations/github)
* [Gmail Integration](/en/enterprise/integrations/gmail)
* [Google Calendar Integration](/en/enterprise/integrations/google_calendar)
* [Google Contacts Integration](/en/enterprise/integrations/google_contacts)
* [Google Docs Integration](/en/enterprise/integrations/google_docs)
* [Google Drive Integration](/en/enterprise/integrations/google_drive)
* [Google Sheets Integration](/en/enterprise/integrations/google_sheets)
* [Google Slides Integration](/en/enterprise/integrations/google_slides)
* [HubSpot Integration](/en/enterprise/integrations/hubspot)
* [Jira Integration](/en/enterprise/integrations/jira)
* [Linear Integration](/en/enterprise/integrations/linear)
* [Microsoft Excel Integration](/en/enterprise/integrations/microsoft_excel)
* [Microsoft OneDrive Integration](/en/enterprise/integrations/microsoft_onedrive)
* [Microsoft Outlook Integration](/en/enterprise/integrations/microsoft_outlook)
* [Microsoft SharePoint Integration](/en/enterprise/integrations/microsoft_sharepoint)
* [Microsoft Teams Integration](/en/enterprise/integrations/microsoft_teams)
* [Microsoft Word Integration](/en/enterprise/integrations/microsoft_word)
* [Notion Integration](/en/enterprise/integrations/notion)
* [Salesforce Integration](/en/enterprise/integrations/salesforce)
* [Shopify Integration](/en/enterprise/integrations/shopify)
* [Slack Integration](/en/enterprise/integrations/slack)
* [Stripe Integration](/en/enterprise/integrations/stripe)
* [Zendesk Integration](/en/enterprise/integrations/zendesk)

##### Triggers

* [Triggers Overview](/en/enterprise/guides/automation-triggers)
* [Gmail Trigger](/en/enterprise/guides/gmail-trigger)
* [Google Calendar Trigger](/en/enterprise/guides/google-calendar-trigger)
* [Google Drive Trigger](/en/enterprise/guides/google-drive-trigger)
* [Outlook Trigger](/en/enterprise/guides/outlook-trigger)
* [OneDrive Trigger](/en/enterprise/guides/onedrive-trigger)
* [Microsoft Teams Trigger](/en/enterprise/guides/microsoft-teams-trigger)
* [Slack Trigger](/en/enterprise/guides/slack-trigger)
* [HubSpot Trigger](/en/enterprise/guides/hubspot-trigger)
* [Salesforce Trigger](/en/enterprise/guides/salesforce-trigger)
* [Zapier Trigger](/en/enterprise/guides/zapier-trigger)

##### How-To Guides

* [Build Crew](/en/enterprise/guides/build-crew)
* [Deploy Crew](/en/enterprise/guides/deploy-crew)
* [Kickoff Crew](/en/enterprise/guides/kickoff-crew)
* [Update Crew](/en/enterprise/guides/update-crew)
* [Enable Crew Studio](/en/enterprise/guides/enable-crew-studio)
* [Open Telemetry Logs](/en/enterprise/guides/capture_telemetry_logs)
* [Azure OpenAI Setup](/en/enterprise/guides/azure-openai-setup)
* [Tool Repository](/en/enterprise/guides/tool-repository)
* [React Component Export](/en/enterprise/guides/react-component-export)
* [Team Management](/en/enterprise/guides/team-management)
* [HITL Workflows](/en/enterprise/guides/human-in-the-loop)
* [Webhook Automation](/en/enterprise/guides/webhook-automation)

##### Resources

* [FAQs](/en/enterprise/resources/frequently-asked-questions)

## [​](#overview) Overview

Enterprise Event Streaming lets you receive real-time webhook updates about your crews and flows deployed to
CrewAI AOP, such as model calls, tool usage, and flow steps.

## [​](#usage) Usage

When using the Kickoff API, include a `webhooks` object to your request, for example:

Copy

Ask AI

```
{
  "inputs": {"foo": "bar"},
  "webhooks": {
    "events": ["crew_kickoff_started", "llm_call_started"],
    "url": "https://your.endpoint/webhook",
    "realtime": false,
    "authentication": {
      "strategy": "bearer",
      "token": "my-secret-token"
    }
  }
}
```

If `realtime` is set to `true`, each event is delivered individually and immediately, at the cost of crew/flow performance.

## [​](#webhook-format) Webhook Format

Each webhook sends a list of events:

Copy

Ask AI

```
{
  "events": [
    {
      "id": "event-id",
      "execution_id": "crew-run-id",
      "timestamp": "2025-02-16T10:58:44.965Z",
      "type": "llm_call_started",
      "data": {
        "model": "gpt-4",
        "messages": [
          {"role": "system", "content": "You are an assistant."},
          {"role": "user", "content": "Summarize this article."}
        ]
      }
    }
  ]
}
```

The `data` object structure varies by event type. Refer to the [event list](https://github.com/crewAIInc/crewAI/tree/main/src/crewai/utilities/events) on GitHub.
As requests are sent over HTTP, the order of events can’t be guaranteed. If you need ordering, use the `timestamp` field.

## [​](#supported-events) Supported Events

CrewAI supports both system events and custom events in Enterprise Event Streaming. These events are sent to your configured webhook endpoint during crew and flow execution.

### [​](#flow-events:) Flow Events:

* `flow_created`
* `flow_started`
* `flow_finished`
* `flow_plot`
* `method_execution_started`
* `method_execution_finished`
* `method_execution_failed`

### [​](#agent-events:) Agent Events:

* `agent_execution_started`
* `agent_execution_completed`
* `agent_execution_error`
* `lite_agent_execution_started`
* `lite_agent_execution_completed`
* `lite_agent_execution_error`
* `agent_logs_started`
* `agent_logs_execution`
* `agent_evaluation_started`
* `agent_evaluation_completed`
* `agent_evaluation_failed`

### [​](#crew-events:) Crew Events:

* `crew_kickoff_started`
* `crew_kickoff_completed`
* `crew_kickoff_failed`
* `crew_train_started`
* `crew_train_completed`
* `crew_train_failed`
* `crew_test_started`
* `crew_test_completed`
* `crew_test_failed`
* `crew_test_result`

### [​](#task-events:) Task Events:

* `task_started`
* `task_completed`
* `task_failed`
* `task_evaluation`

### [​](#tool-usage-events:) Tool Usage Events:

* `tool_usage_started`
* `tool_usage_finished`
* `tool_usage_error`
* `tool_validate_input_error`
* `tool_selection_error`
* `tool_execution_error`

### [​](#llm-events:) LLM Events:

* `llm_call_started`
* `llm_call_completed`
* `llm_call_failed`
* `llm_stream_chunk`

### [​](#llm-guardrail-events:) LLM Guardrail Events:

* `llm_guardrail_started`
* `llm_guardrail_completed`

### [​](#memory-events:) Memory Events:

* `memory_query_started`
* `memory_query_completed`
* `memory_query_failed`
* `memory_save_started`
* `memory_save_completed`
* `memory_save_failed`
* `memory_retrieval_started`
* `memory_retrieval_completed`

### [​](#knowledge-events:) Knowledge Events:

* `knowledge_search_query_started`
* `knowledge_search_query_completed`
* `knowledge_search_query_failed`
* `knowledge_query_started`
* `knowledge_query_completed`
* `knowledge_query_failed`

### [​](#reasoning-events:) Reasoning Events:

* `agent_reasoning_started`
* `agent_reasoning_completed`
* `agent_reasoning_failed`

Event names match the internal event bus. See GitHub for the full list of events.
You can emit your own custom events, and they will be delivered through the webhook stream alongside system events.

[## GitHub

Full list of events](https://github.com/crewAIInc/crewAI/tree/main/src/crewai/utilities/events)[## Need Help?

Contact our support team for assistance with webhook integration or troubleshooting.](/cdn-cgi/l/email-protection#71020401011e0305311203140610185f121e1c)

Was this page helpful?

YesNo

[Traces

Previous](/en/enterprise/features/traces)[Hallucination Guardrail

Next](/en/enterprise/features/hallucination-guardrail)

⌘I