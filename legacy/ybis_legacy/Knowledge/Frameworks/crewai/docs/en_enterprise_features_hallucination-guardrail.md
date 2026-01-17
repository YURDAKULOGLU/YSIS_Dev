Hallucination Guardrail - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Operate

Hallucination Guardrail

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

The Hallucination Guardrail is an enterprise feature that validates AI-generated content to ensure it’s grounded in facts and doesn’t contain hallucinations. It analyzes task outputs against reference context and provides detailed feedback when potentially hallucinated content is detected.

## [​](#what-are-hallucinations) What are Hallucinations?

AI hallucinations occur when language models generate content that appears plausible but is factually incorrect or not supported by the provided context. The Hallucination Guardrail helps prevent these issues by:

* Comparing outputs against reference context
* Evaluating faithfulness to source material
* Providing detailed feedback on problematic content
* Supporting custom thresholds for validation strictness

## [​](#basic-usage) Basic Usage

### [​](#setting-up-the-guardrail) Setting Up the Guardrail

Copy

Ask AI

```
from crewai.tasks.hallucination_guardrail import HallucinationGuardrail
from crewai import LLM

# Basic usage - will use task's expected_output as context
guardrail = HallucinationGuardrail(
    llm=LLM(model="gpt-4o-mini")
)

# With explicit reference context
context_guardrail = HallucinationGuardrail(
    context="AI helps with various tasks including analysis and generation.",
    llm=LLM(model="gpt-4o-mini")
)
```

### [​](#adding-to-tasks) Adding to Tasks

Copy

Ask AI

```
from crewai import Task

# Create your task with the guardrail
task = Task(
    description="Write a summary about AI capabilities",
    expected_output="A factual summary based on the provided context",
    agent=my_agent,
    guardrail=guardrail  # Add the guardrail to validate output
)
```

## [​](#advanced-configuration) Advanced Configuration

### [​](#custom-threshold-validation) Custom Threshold Validation

For stricter validation, you can set a custom faithfulness threshold (0-10 scale):

Copy

Ask AI

```
# Strict guardrail requiring high faithfulness score
strict_guardrail = HallucinationGuardrail(
    context="Quantum computing uses qubits that exist in superposition states.",
    llm=LLM(model="gpt-4o-mini"),
    threshold=8.0  # Requires score >= 8 to pass validation
)
```

### [​](#including-tool-response-context) Including Tool Response Context

When your task uses tools, you can include tool responses for more accurate validation:

Copy

Ask AI

```
# Guardrail with tool response context
weather_guardrail = HallucinationGuardrail(
    context="Current weather information for the requested location",
    llm=LLM(model="gpt-4o-mini"),
    tool_response="Weather API returned: Temperature 22°C, Humidity 65%, Clear skies"
)
```

## [​](#how-it-works) How It Works

### [​](#validation-process) Validation Process

1. **Context Analysis**: The guardrail compares task output against the provided reference context
2. **Faithfulness Scoring**: Uses an internal evaluator to assign a faithfulness score (0-10)
3. **Verdict Determination**: Determines if content is faithful or contains hallucinations
4. **Threshold Checking**: If a custom threshold is set, validates against that score
5. **Feedback Generation**: Provides detailed reasons when validation fails

### [​](#validation-logic) Validation Logic

* **Default Mode**: Uses verdict-based validation (FAITHFUL vs HALLUCINATED)
* **Threshold Mode**: Requires faithfulness score to meet or exceed the specified threshold
* **Error Handling**: Gracefully handles evaluation errors and provides informative feedback

## [​](#guardrail-results) Guardrail Results

The guardrail returns structured results indicating validation status:

Copy

Ask AI

```
# Example of guardrail result structure
{
    "valid": False,
    "feedback": "Content appears to be hallucinated (score: 4.2/10, verdict: HALLUCINATED). The output contains information not supported by the provided context."
}
```

### [​](#result-properties) Result Properties

* **valid**: Boolean indicating whether the output passed validation
* **feedback**: Detailed explanation when validation fails, including:
  + Faithfulness score
  + Verdict classification
  + Specific reasons for failure

## [​](#integration-with-task-system) Integration with Task System

### [​](#automatic-validation) Automatic Validation

When a guardrail is added to a task, it automatically validates the output before the task is marked as complete:

Copy

Ask AI

```
# Task output validation flow
task_output = agent.execute_task(task)
validation_result = guardrail(task_output)

if validation_result.valid:
    # Task completes successfully
    return task_output
else:
    # Task fails with validation feedback
    raise ValidationError(validation_result.feedback)
```

### [​](#event-tracking) Event Tracking

The guardrail integrates with CrewAI’s event system to provide observability:

* **Validation Started**: When guardrail evaluation begins
* **Validation Completed**: When evaluation finishes with results
* **Validation Failed**: When technical errors occur during evaluation

## [​](#best-practices) Best Practices

### [​](#context-guidelines) Context Guidelines

1

Provide Comprehensive Context

Include all relevant factual information that the AI should base its output on:

Copy

Ask AI

```
context = """
Company XYZ was founded in 2020 and specializes in renewable energy solutions.
They have 150 employees and generated $50M revenue in 2023.
Their main products include solar panels and wind turbines.
"""
```

2

Keep Context Relevant

Only include information directly related to the task to avoid confusion:

Copy

Ask AI

```
# Good: Focused context
context = "The current weather in New York is 18°C with light rain."

# Avoid: Unrelated information
context = "The weather is 18°C. The city has 8 million people. Traffic is heavy."
```

3

Update Context Regularly

Ensure your reference context reflects current, accurate information.

### [​](#threshold-selection) Threshold Selection

1

Start with Default Validation

Begin without custom thresholds to understand baseline performance.

2

Adjust Based on Requirements

* **High-stakes content**: Use threshold 8-10 for maximum accuracy
* **General content**: Use threshold 6-7 for balanced validation
* **Creative content**: Use threshold 4-5 or default verdict-based validation

3

Monitor and Iterate

Track validation results and adjust thresholds based on false positives/negatives.

## [​](#performance-considerations) Performance Considerations

### [​](#impact-on-execution-time) Impact on Execution Time

* **Validation Overhead**: Each guardrail adds ~1-3 seconds per task
* **LLM Efficiency**: Choose efficient models for evaluation (e.g., gpt-4o-mini)

### [​](#cost-optimization) Cost Optimization

* **Model Selection**: Use smaller, efficient models for guardrail evaluation
* **Context Size**: Keep reference context concise but comprehensive
* **Caching**: Consider caching validation results for repeated content

## [​](#troubleshooting) Troubleshooting

Validation Always Fails

**Possible Causes:**

* Context is too restrictive or unrelated to task output
* Threshold is set too high for the content type
* Reference context contains outdated information

**Solutions:**

* Review and update context to match task requirements
* Lower threshold or use default verdict-based validation
* Ensure context is current and accurate



False Positives (Valid Content Marked Invalid)

**Possible Causes:**

* Threshold too high for creative or interpretive tasks
* Context doesn’t cover all valid aspects of the output
* Evaluation model being overly conservative

**Solutions:**

* Lower threshold or use default validation
* Expand context to include broader acceptable content
* Test with different evaluation models



Evaluation Errors

**Possible Causes:**

* Network connectivity issues
* LLM model unavailable or rate limited
* Malformed task output or context

**Solutions:**

* Check network connectivity and LLM service status
* Implement retry logic for transient failures
* Validate task output format before guardrail evaluation

[## Need Help?

Contact our support team for assistance with hallucination guardrail configuration or troubleshooting.](/cdn-cgi/l/email-protection#681b1d1818071a1c280b1a0d1f0901460b0705)

Was this page helpful?

YesNo

[Webhook Streaming

Previous](/en/enterprise/features/webhook-streaming)[Role-Based Access Control (RBAC)

Next](/en/enterprise/features/rbac)

⌘I