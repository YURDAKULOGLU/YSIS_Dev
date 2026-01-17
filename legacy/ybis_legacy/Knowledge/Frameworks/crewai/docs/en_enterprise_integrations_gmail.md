Gmail Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Integration Docs

Gmail Integration

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

Enable your agents to manage emails, contacts, and drafts through Gmail. Send emails, search messages, manage contacts, create drafts, and streamline your email communications with AI-powered automation.

## [​](#prerequisites) Prerequisites

Before using the Gmail integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Gmail account with appropriate permissions
* Connected your Gmail account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## [​](#setting-up-gmail-integration) Setting Up Gmail Integration

### [​](#1-connect-your-gmail-account) 1. Connect Your Gmail Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Gmail** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for email and contact management
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

gmail/fetch\_emails

**Description:** Retrieve a list of messages.**Parameters:**

* `userId` (string, required): The user’s email address or ‘me’ for the authenticated user. (default: “me”)
* `q` (string, optional): Search query to filter messages (e.g., ‘from:[[email protected]](/cdn-cgi/l/email-protection#3d4e5250585253587d58455c504d5158135e5250) is:unread’).
* `maxResults` (integer, optional): Maximum number of messages to return (1-500). (default: 100)
* `pageToken` (string, optional): Page token to retrieve a specific page of results.
* `labelIds` (array, optional): Only return messages with labels that match all of the specified label IDs.
* `includeSpamTrash` (boolean, optional): Include messages from SPAM and TRASH in the results. (default: false)

gmail/send\_email

**Description:** Send an email.**Parameters:**

* `to` (string, required): Recipient email address.
* `subject` (string, required): Email subject line.
* `body` (string, required): Email message content.
* `userId` (string, optional): The user’s email address or ‘me’ for the authenticated user. (default: “me”)
* `cc` (string, optional): CC email addresses (comma-separated).
* `bcc` (string, optional): BCC email addresses (comma-separated).
* `from` (string, optional): Sender email address (if different from authenticated user).
* `replyTo` (string, optional): Reply-to email address.
* `threadId` (string, optional): Thread ID if replying to an existing conversation.

gmail/delete\_email

**Description:** Delete an email by ID.**Parameters:**

* `userId` (string, required): The user’s email address or ‘me’ for the authenticated user.
* `id` (string, required): The ID of the message to delete.

gmail/create\_draft

**Description:** Create a new draft email.**Parameters:**

* `userId` (string, required): The user’s email address or ‘me’ for the authenticated user.
* `message` (object, required): Message object containing the draft content.
  + `raw` (string, required): Base64url encoded email message.

gmail/get\_message

**Description:** Retrieve a specific message by ID.**Parameters:**

* `userId` (string, required): The user’s email address or ‘me’ for the authenticated user. (default: “me”)
* `id` (string, required): The ID of the message to retrieve.
* `format` (string, optional): The format to return the message in. Options: “full”, “metadata”, “minimal”, “raw”. (default: “full”)
* `metadataHeaders` (array, optional): When given and format is METADATA, only include headers specified.

gmail/get\_attachment

**Description:** Retrieve a message attachment.**Parameters:**

* `userId` (string, required): The user’s email address or ‘me’ for the authenticated user. (default: “me”)
* `messageId` (string, required): The ID of the message containing the attachment.
* `id` (string, required): The ID of the attachment to retrieve.

gmail/fetch\_thread

**Description:** Retrieve a specific email thread by ID.**Parameters:**

* `userId` (string, required): The user’s email address or ‘me’ for the authenticated user. (default: “me”)
* `id` (string, required): The ID of the thread to retrieve.
* `format` (string, optional): The format to return the messages in. Options: “full”, “metadata”, “minimal”. (default: “full”)
* `metadataHeaders` (array, optional): When given and format is METADATA, only include headers specified.

gmail/modify\_thread

**Description:** Modify the labels applied to a thread.**Parameters:**

* `userId` (string, required): The user’s email address or ‘me’ for the authenticated user. (default: “me”)
* `id` (string, required): The ID of the thread to modify.
* `addLabelIds` (array, optional): A list of IDs of labels to add to this thread.
* `removeLabelIds` (array, optional): A list of IDs of labels to remove from this thread.

gmail/trash\_thread

**Description:** Move a thread to the trash.**Parameters:**

* `userId` (string, required): The user’s email address or ‘me’ for the authenticated user. (default: “me”)
* `id` (string, required): The ID of the thread to trash.

gmail/untrash\_thread

**Description:** Remove a thread from the trash.**Parameters:**

* `userId` (string, required): The user’s email address or ‘me’ for the authenticated user. (default: “me”)
* `id` (string, required): The ID of the thread to untrash.

## [​](#usage-examples) Usage Examples

### [​](#basic-gmail-agent-setup) Basic Gmail Agent Setup

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create an agent with Gmail capabilities
gmail_agent = Agent(
    role="Email Manager",
    goal="Manage email communications and messages efficiently",
    backstory="An AI assistant specialized in email management and communication.",
    apps=['gmail']  # All Gmail actions will be available
)

# Task to send a follow-up email
send_email_task = Task(
    description="Send a follow-up email to [email protected] about the project update meeting",
    agent=gmail_agent,
    expected_output="Email sent successfully with confirmation"
)

# Run the task
crew = Crew(
    agents=[gmail_agent],
    tasks=[send_email_task]
)

crew.kickoff()
```

### [​](#filtering-specific-gmail-tools) Filtering Specific Gmail Tools

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create agent with specific Gmail actions only
email_coordinator = Agent(
    role="Email Coordinator",
    goal="Coordinate email communications and manage drafts",
    backstory="An AI assistant that focuses on email coordination and draft management.",
    apps=[
        'gmail/send_email',
        'gmail/fetch_emails',
        'gmail/create_draft'
    ]
)

# Task to prepare and send emails
email_coordination = Task(
    description="Search for emails from the marketing team, create a summary draft, and send it to stakeholders",
    agent=email_coordinator,
    expected_output="Summary email sent to stakeholders"
)

crew = Crew(
    agents=[email_coordinator],
    tasks=[email_coordination]
)

crew.kickoff()
```

### [​](#email-search-and-analysis) Email Search and Analysis

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create agent with Gmail search and analysis capabilities
email_analyst = Agent(
    role="Email Analyst",
    goal="Analyze email patterns and provide insights",
    backstory="An AI assistant that analyzes email data to provide actionable insights.",
    apps=['gmail/fetch_emails', 'gmail/get_message']  # Specific actions for email analysis
)

# Task to analyze email patterns
analysis_task = Task(
    description="""
    Search for all unread emails from the last 7 days,
    categorize them by sender domain,
    and create a summary report of communication patterns
    """,
    agent=email_analyst,
    expected_output="Email analysis report with communication patterns and recommendations"
)

crew = Crew(
    agents=[email_analyst],
    tasks=[analysis_task]
)

crew.kickoff()
```

### [​](#thread-management) Thread Management

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create agent with Gmail thread management capabilities
thread_manager = Agent(
    role="Thread Manager",
    goal="Organize and manage email threads efficiently",
    backstory="An AI assistant that specializes in email thread organization and management.",
    apps=[
        'gmail/fetch_thread',
        'gmail/modify_thread',
        'gmail/trash_thread'
    ]
)

# Task to organize email threads
thread_task = Task(
    description="""
    1. Fetch all threads from the last month
    2. Apply appropriate labels to organize threads by project
    3. Archive or trash threads that are no longer relevant
    """,
    agent=thread_manager,
    expected_output="Email threads organized with appropriate labels and cleanup completed"
)

crew = Crew(
    agents=[thread_manager],
    tasks=[thread_task]
)

crew.kickoff()
```

### [​](#getting-help) Getting Help

[## Need Help?

Contact our support team for assistance with Gmail integration setup or troubleshooting.](/cdn-cgi/l/email-protection#83f0f6f3f3ecf1f7c3e0f1e6f4e2eaade0ecee)

Was this page helpful?

YesNo

[GitHub Integration

Previous](/en/enterprise/integrations/github)[Google Calendar Integration

Next](/en/enterprise/integrations/google_calendar)

⌘I