Google Docs Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Integration Docs

Google Docs Integration

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

Enable your agents to create, edit, and manage Google Docs documents with text manipulation and formatting. Automate document creation, insert and replace text, manage content ranges, and streamline your document workflows with AI-powered automation.

## [​](#prerequisites) Prerequisites

Before using the Google Docs integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Google account with Google Docs access
* Connected your Google account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## [​](#setting-up-google-docs-integration) Setting Up Google Docs Integration

### [​](#1-connect-your-google-account) 1. Connect Your Google Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Google Docs** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for document access
5. Copy your Enterprise Token from [Integration Settings](https://app.crewai.com/crewai_plus/settings/integrations)

### [​](#2-install-required-package) 2. Install Required Package

Copy

Ask AI

```
uv add crewai-tools
```

### [​](#3-environment-variable-setup) 3. Environment Variable Setup

To use integrations with `Agent(apps=[])`, you must set the `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise Token.

Copy

Ask AI

```
export CREWAI_PLATFORM_INTEGRATION_TOKEN="your_enterprise_token"
```

Or add it to your `.env` file:

Copy

Ask AI

```
CREWAI_PLATFORM_INTEGRATION_TOKEN=your_enterprise_token
```

## [​](#available-actions) Available Actions

google\_docs/create\_document

**Description:** Create a new Google Document.**Parameters:**

* `title` (string, optional): The title for the new document.

google\_docs/get\_document

**Description:** Get the contents and metadata of a Google Document.**Parameters:**

* `documentId` (string, required): The ID of the document to retrieve.
* `includeTabsContent` (boolean, optional): Whether to include tab content. Default is `false`.
* `suggestionsViewMode` (string, optional): The suggestions view mode to apply to the document. Enum: `DEFAULT_FOR_CURRENT_ACCESS`, `PREVIEW_SUGGESTIONS_ACCEPTED`, `PREVIEW_WITHOUT_SUGGESTIONS`. Default is `DEFAULT_FOR_CURRENT_ACCESS`.

google\_docs/batch\_update

**Description:** Apply one or more updates to a Google Document.**Parameters:**

* `documentId` (string, required): The ID of the document to update.
* `requests` (array, required): A list of updates to apply to the document. Each item is an object representing a request.
* `writeControl` (object, optional): Provides control over how write requests are executed. Contains `requiredRevisionId` (string) and `targetRevisionId` (string).

google\_docs/insert\_text

**Description:** Insert text into a Google Document at a specific location.**Parameters:**

* `documentId` (string, required): The ID of the document to update.
* `text` (string, required): The text to insert.
* `index` (integer, optional): The zero-based index where to insert the text. Default is `1`.

google\_docs/replace\_text

**Description:** Replace all instances of text in a Google Document.**Parameters:**

* `documentId` (string, required): The ID of the document to update.
* `containsText` (string, required): The text to find and replace.
* `replaceText` (string, required): The text to replace it with.
* `matchCase` (boolean, optional): Whether the search should respect case. Default is `false`.

google\_docs/delete\_content\_range

**Description:** Delete content from a specific range in a Google Document.**Parameters:**

* `documentId` (string, required): The ID of the document to update.
* `startIndex` (integer, required): The start index of the range to delete.
* `endIndex` (integer, required): The end index of the range to delete.

google\_docs/insert\_page\_break

**Description:** Insert a page break at a specific location in a Google Document.**Parameters:**

* `documentId` (string, required): The ID of the document to update.
* `index` (integer, optional): The zero-based index where to insert the page break. Default is `1`.

google\_docs/create\_named\_range

**Description:** Create a named range in a Google Document.**Parameters:**

* `documentId` (string, required): The ID of the document to update.
* `name` (string, required): The name for the named range.
* `startIndex` (integer, required): The start index of the range.
* `endIndex` (integer, required): The end index of the range.

## [​](#usage-examples) Usage Examples

### [​](#basic-google-docs-agent-setup) Basic Google Docs Agent Setup

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create an agent with Google Docs capabilities
docs_agent = Agent(
    role="Document Creator",
    goal="Create and manage Google Docs documents efficiently",
    backstory="An AI assistant specialized in Google Docs document creation and editing.",
    apps=['google_docs']  # All Google Docs actions will be available
)

# Task to create a new document
create_doc_task = Task(
    description="Create a new Google Document titled 'Project Status Report'",
    agent=docs_agent,
    expected_output="New Google Document 'Project Status Report' created successfully"
)

# Run the task
crew = Crew(
    agents=[docs_agent],
    tasks=[create_doc_task]
)

crew.kickoff()
```

### [​](#text-editing-and-content-management) Text Editing and Content Management

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create an agent focused on text editing
text_editor = Agent(
    role="Document Editor",
    goal="Edit and update content in Google Docs documents",
    backstory="An AI assistant skilled in precise text editing and content management.",
    apps=['google_docs/insert_text', 'google_docs/replace_text', 'google_docs/delete_content_range']
)

# Task to edit document content
edit_content_task = Task(
    description="In document 'your_document_id', insert the text 'Executive Summary: ' at the beginning, then replace all instances of 'TODO' with 'COMPLETED'.",
    agent=text_editor,
    expected_output="Document updated with new text inserted and TODO items replaced."
)

crew = Crew(
    agents=[text_editor],
    tasks=[edit_content_task]
)

crew.kickoff()
```

### [​](#advanced-document-operations) Advanced Document Operations

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create an agent for advanced document operations
document_formatter = Agent(
    role="Document Formatter",
    goal="Apply advanced formatting and structure to Google Docs",
    backstory="An AI assistant that handles complex document formatting and organization.",
    apps=['google_docs/batch_update', 'google_docs/insert_page_break', 'google_docs/create_named_range']
)

# Task to format document
format_doc_task = Task(
    description="In document 'your_document_id', insert a page break at position 100, create a named range called 'Introduction' for characters 1-50, and apply batch formatting updates.",
    agent=document_formatter,
    expected_output="Document formatted with page break, named range, and styling applied."
)

crew = Crew(
    agents=[document_formatter],
    tasks=[format_doc_task]
)

crew.kickoff()
```

## [​](#troubleshooting) Troubleshooting

### [​](#common-issues) Common Issues

**Authentication Errors**

* Ensure your Google account has the necessary permissions for Google Docs access.
* Verify that the OAuth connection includes all required scopes (`https://www.googleapis.com/auth/documents`).

**Document ID Issues**

* Double-check document IDs for correctness.
* Ensure the document exists and is accessible to your account.
* Document IDs can be found in the Google Docs URL.

**Text Insertion and Range Operations**

* When using `insert_text` or `delete_content_range`, ensure index positions are valid.
* Remember that Google Docs uses zero-based indexing.
* The document must have content at the specified index positions.

**Batch Update Request Formatting**

* When using `batch_update`, ensure the `requests` array is correctly formatted according to the Google Docs API documentation.
* Complex updates require specific JSON structures for each request type.

**Replace Text Operations**

* For `replace_text`, ensure the `containsText` parameter exactly matches the text you want to replace.
* Use `matchCase` parameter to control case sensitivity.

### [​](#getting-help) Getting Help

[## Need Help?

Contact our support team for assistance with Google Docs integration setup or troubleshooting.](/cdn-cgi/l/email-protection#582b2d2828372a2c183b2a3d2f3931763b3735)

Was this page helpful?

YesNo

[Google Contacts Integration

Previous](/en/enterprise/integrations/google_contacts)[Google Drive Integration

Next](/en/enterprise/integrations/google_drive)

⌘I