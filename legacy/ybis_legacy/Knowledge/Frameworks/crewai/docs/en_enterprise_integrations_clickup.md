ClickUp Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Integration Docs

ClickUp Integration

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

Enable your agents to manage tasks, projects, and productivity workflows through ClickUp. Create and update tasks, organize projects, manage team assignments, and streamline your productivity management with AI-powered automation.

## [​](#prerequisites) Prerequisites

Before using the ClickUp integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A ClickUp account with appropriate permissions
* Connected your ClickUp account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## [​](#setting-up-clickup-integration) Setting Up ClickUp Integration

### [​](#1-connect-your-clickup-account) 1. Connect Your ClickUp Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **ClickUp** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for task and project management
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

clickup/search\_tasks

**Description:** Search for tasks in ClickUp using advanced filters.**Parameters:**

* `taskFilterFormula` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.

  Copy

  Ask AI

  ```
  {
    "operator": "OR",
    "conditions": [
      {
        "operator": "AND",
        "conditions": [
          {
            "field": "statuses%5B%5D",
            "operator": "$stringExactlyMatches",
            "value": "open"
          }
        ]
      }
    ]
  }
  ```

  Available fields: `space_ids%5B%5D`, `project_ids%5B%5D`, `list_ids%5B%5D`, `statuses%5B%5D`, `include_closed`, `assignees%5B%5D`, `tags%5B%5D`, `due_date_gt`, `due_date_lt`, `date_created_gt`, `date_created_lt`, `date_updated_gt`, `date_updated_lt`

clickup/get\_task\_in\_list

**Description:** Get tasks in a specific list in ClickUp.**Parameters:**

* `listId` (string, required): List - Select a List to get tasks from. Use Connect Portal User Settings to allow users to select a ClickUp List.
* `taskFilterFormula` (string, optional): Search for tasks that match specified filters. For example: name=task1.

clickup/create\_task

**Description:** Create a task in ClickUp.**Parameters:**

* `listId` (string, required): List - Select a List to create this task in. Use Connect Portal User Settings to allow users to select a ClickUp List.
* `name` (string, required): Name - The task name.
* `description` (string, optional): Description - Task description.
* `status` (string, optional): Status - Select a Status for this task. Use Connect Portal User Settings to allow users to select a ClickUp Status.
* `assignees` (string, optional): Assignees - Select a Member (or an array of member IDs) to be assigned to this task. Use Connect Portal User Settings to allow users to select a ClickUp Member.
* `dueDate` (string, optional): Due Date - Specify a date for this task to be due on.
* `additionalFields` (string, optional): Additional Fields - Specify additional fields to include on this task as JSON.

clickup/update\_task

**Description:** Update a task in ClickUp.**Parameters:**

* `taskId` (string, required): Task ID - The ID of the task to update.
* `listId` (string, required): List - Select a List to create this task in. Use Connect Portal User Settings to allow users to select a ClickUp List.
* `name` (string, optional): Name - The task name.
* `description` (string, optional): Description - Task description.
* `status` (string, optional): Status - Select a Status for this task. Use Connect Portal User Settings to allow users to select a ClickUp Status.
* `assignees` (string, optional): Assignees - Select a Member (or an array of member IDs) to be assigned to this task. Use Connect Portal User Settings to allow users to select a ClickUp Member.
* `dueDate` (string, optional): Due Date - Specify a date for this task to be due on.
* `additionalFields` (string, optional): Additional Fields - Specify additional fields to include on this task as JSON.

clickup/delete\_task

**Description:** Delete a task in ClickUp.**Parameters:**

* `taskId` (string, required): Task ID - The ID of the task to delete.

clickup/get\_list

**Description:** Get List information in ClickUp.**Parameters:**

* `spaceId` (string, required): Space ID - The ID of the space containing the lists.

clickup/get\_custom\_fields\_in\_list

**Description:** Get Custom Fields in a List in ClickUp.**Parameters:**

* `listId` (string, required): List ID - The ID of the list to get custom fields from.

clickup/get\_all\_fields\_in\_list

**Description:** Get All Fields in a List in ClickUp.**Parameters:**

* `listId` (string, required): List ID - The ID of the list to get all fields from.

clickup/get\_space

**Description:** Get Space information in ClickUp.**Parameters:**

* `spaceId` (string, optional): Space ID - The ID of the space to retrieve.

clickup/get\_folders

**Description:** Get Folders in ClickUp.**Parameters:**

* `spaceId` (string, required): Space ID - The ID of the space containing the folders.

clickup/get\_member

**Description:** Get Member information in ClickUp.**Parameters:** None required.

## [​](#usage-examples) Usage Examples

### [​](#basic-clickup-agent-setup) Basic ClickUp Agent Setup

Copy

Ask AI

```
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

# Create an agent with Clickup capabilities
clickup_agent = Agent(
    role="Task Manager",
    goal="Manage tasks and projects in ClickUp efficiently",
    backstory="An AI assistant specialized in task management and productivity coordination.",
    apps=['clickup']  # All Clickup actions will be available
)

# Task to create a new task
create_task = Task(
    description="Create a task called 'Review Q1 Reports' in the Marketing list with high priority",
    agent=clickup_agent,
    expected_output="Task created successfully with task ID"
)

# Run the task
crew = Crew(
    agents=[clickup_agent],
    tasks=[create_task]
)

crew.kickoff()
```

### [​](#filtering-specific-clickup-tools) Filtering Specific ClickUp Tools

Copy

Ask AI

```
task_coordinator = Agent(
    role="Task Coordinator",
    goal="Create and manage tasks efficiently",
    backstory="An AI assistant that focuses on task creation and status management.",
    apps=['clickup/create_task']
)

# Task to manage task workflow
task_workflow = Task(
    description="Create a task for project planning and assign it to the development team",
    agent=task_coordinator,
    expected_output="Task created and assigned successfully"
)

crew = Crew(
    agents=[task_coordinator],
    tasks=[task_workflow]
)

crew.kickoff()
```

### [​](#advanced-project-management) Advanced Project Management

Copy

Ask AI

```
from crewai import Agent, Task, Crew

project_manager = Agent(
    role="Project Manager",
    goal="Coordinate project activities and track team productivity",
    backstory="An experienced project manager who ensures projects are delivered on time.",
    apps=['clickup']
)

# Complex task involving multiple ClickUp operations
project_coordination = Task(
    description="""
    1. Get all open tasks in the current space
    2. Identify overdue tasks and update their status
    3. Create a weekly report task summarizing project progress
    4. Assign the report task to the team lead
    """,
    agent=project_manager,
    expected_output="Project status updated and weekly report task created and assigned"
)

crew = Crew(
    agents=[project_manager],
    tasks=[project_coordination]
)

crew.kickoff()
```

### [​](#task-search-and-management) Task Search and Management

Copy

Ask AI

```
from crewai import Agent, Task, Crew

task_analyst = Agent(
    role="Task Analyst",
    goal="Analyze task patterns and optimize team productivity",
    backstory="An AI assistant that analyzes task data to improve team efficiency.",
    apps=['clickup']
)

# Task to analyze and optimize task distribution
task_analysis = Task(
    description="""
    Search for all tasks assigned to team members in the last 30 days,
    analyze completion patterns, and create optimization recommendations
    """,
    agent=task_analyst,
    expected_output="Task analysis report with optimization recommendations"
)

crew = Crew(
    agents=[task_analyst],
    tasks=[task_analysis]
)

crew.kickoff()
```

### [​](#getting-help) Getting Help

[## Need Help?

Contact our support team for assistance with ClickUp integration setup or troubleshooting.](/cdn-cgi/l/email-protection#b2c1c7c2c2ddc0c6f2d1c0d7c5d3db9cd1dddf)

Was this page helpful?

YesNo

[Box Integration

Previous](/en/enterprise/integrations/box)[GitHub Integration

Next](/en/enterprise/integrations/github)

⌘I