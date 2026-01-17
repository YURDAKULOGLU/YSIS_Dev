Asana Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Integration Docs

Asana Integration

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

Enable your agents to manage tasks, projects, and team coordination through Asana. Create tasks, update project status, manage assignments, and streamline your team’s workflow with AI-powered automation.

## [​](#prerequisites) Prerequisites

Before using the Asana integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* An Asana account with appropriate permissions
* Connected your Asana account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## [​](#setting-up-asana-integration) Setting Up Asana Integration

### [​](#1-connect-your-asana-account) 1. Connect Your Asana Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Asana** in the Authentication Integrations section
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

asana/create\_comment

**Description:** Create a comment in Asana.**Parameters:**

* `task` (string, required): Task ID - The ID of the Task the comment will be added to. The comment will be authored by the currently authenticated user.
* `text` (string, required): Text (example: “This is a comment.”).

asana/create\_project

**Description:** Create a project in Asana.**Parameters:**

* `name` (string, required): Name (example: “Stuff to buy”).
* `workspace` (string, required): Workspace - Use Connect Portal Workflow Settings to allow users to select which Workspace to create Projects in. Defaults to the user’s first Workspace if left blank.
* `team` (string, optional): Team - Use Connect Portal Workflow Settings to allow users to select which Team to share this Project with. Defaults to the user’s first Team if left blank.
* `notes` (string, optional): Notes (example: “These are things we need to purchase.”).

asana/get\_projects

**Description:** Get a list of projects in Asana.**Parameters:**

* `archived` (string, optional): Archived - Choose “true” to show archived projects, “false” to display only active projects, or “default” to show both archived and active projects.
  + Options: `default`, `true`, `false`

asana/get\_project\_by\_id

**Description:** Get a project by ID in Asana.**Parameters:**

* `projectFilterId` (string, required): Project ID.

asana/create\_task

**Description:** Create a task in Asana.**Parameters:**

* `name` (string, required): Name (example: “Task Name”).
* `workspace` (string, optional): Workspace - Use Connect Portal Workflow Settings to allow users to select which Workspace to create Tasks in. Defaults to the user’s first Workspace if left blank..
* `project` (string, optional): Project - Use Connect Portal Workflow Settings to allow users to select which Project to create this Task in.
* `notes` (string, optional): Notes.
* `dueOnDate` (string, optional): Due On - The date on which this task is due. Cannot be used together with Due At. (example: “YYYY-MM-DD”).
* `dueAtDate` (string, optional): Due At - The date and time (ISO timestamp) at which this task is due. Cannot be used together with Due On. (example: “2019-09-15T02:06:58.147Z”).
* `assignee` (string, optional): Assignee - The ID of the Asana user this task will be assigned to. Use Connect Portal Workflow Settings to allow users to select an Assignee.
* `gid` (string, optional): External ID - An ID from your application to associate this task with. You can use this ID to sync updates to this task later.

asana/update\_task

**Description:** Update a task in Asana.**Parameters:**

* `taskId` (string, required): Task ID - The ID of the Task that will be updated.
* `completeStatus` (string, optional): Completed Status.
  + Options: `true`, `false`
* `name` (string, optional): Name (example: “Task Name”).
* `notes` (string, optional): Notes.
* `dueOnDate` (string, optional): Due On - The date on which this task is due. Cannot be used together with Due At. (example: “YYYY-MM-DD”).
* `dueAtDate` (string, optional): Due At - The date and time (ISO timestamp) at which this task is due. Cannot be used together with Due On. (example: “2019-09-15T02:06:58.147Z”).
* `assignee` (string, optional): Assignee - The ID of the Asana user this task will be assigned to. Use Connect Portal Workflow Settings to allow users to select an Assignee.
* `gid` (string, optional): External ID - An ID from your application to associate this task with. You can use this ID to sync updates to this task later.

asana/get\_tasks

**Description:** Get a list of tasks in Asana.**Parameters:**

* `workspace` (string, optional): Workspace - The ID of the Workspace to filter tasks on. Use Connect Portal Workflow Settings to allow users to select a Workspace.
* `project` (string, optional): Project - The ID of the Project to filter tasks on. Use Connect Portal Workflow Settings to allow users to select a Project.
* `assignee` (string, optional): Assignee - The ID of the assignee to filter tasks on. Use Connect Portal Workflow Settings to allow users to select an Assignee.
* `completedSince` (string, optional): Completed since - Only return tasks that are either incomplete or that have been completed since this time (ISO or Unix timestamp). (example: “2014-04-25T16:15:47-04:00”).

asana/get\_tasks\_by\_id

**Description:** Get a list of tasks by ID in Asana.**Parameters:**

* `taskId` (string, required): Task ID.

asana/get\_task\_by\_external\_id

**Description:** Get a task by external ID in Asana.**Parameters:**

* `gid` (string, required): External ID - The ID that this task is associated or synced with, from your application.

asana/add\_task\_to\_section

**Description:** Add a task to a section in Asana.**Parameters:**

* `sectionId` (string, required): Section ID - The ID of the section to add this task to.
* `taskId` (string, required): Task ID - The ID of the task. (example: “1204619611402340”).
* `beforeTaskId` (string, optional): Before Task ID - The ID of a task in this section that this task will be inserted before. Cannot be used with After Task ID. (example: “1204619611402340”).
* `afterTaskId` (string, optional): After Task ID - The ID of a task in this section that this task will be inserted after. Cannot be used with Before Task ID. (example: “1204619611402340”).

asana/get\_teams

**Description:** Get a list of teams in Asana.**Parameters:**

* `workspace` (string, required): Workspace - Returns the teams in this workspace visible to the authorized user.

asana/get\_workspaces

**Description:** Get a list of workspaces in Asana.**Parameters:** None required.

## [​](#usage-examples) Usage Examples

### [​](#basic-asana-agent-setup) Basic Asana Agent Setup

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create an agent with Asana capabilities
asana_agent = Agent(
    role="Project Manager",
    goal="Manage tasks and projects in Asana efficiently",
    backstory="An AI assistant specialized in project management and task coordination.",
    apps=['asana']  # All Asana actions will be available
)

# Task to create a new project
create_project_task = Task(
    description="Create a new project called 'Q1 Marketing Campaign' in the Marketing workspace",
    agent=asana_agent,
    expected_output="Confirmation that the project was created successfully with project ID"
)

# Run the task
crew = Crew(
    agents=[asana_agent],
    tasks=[create_project_task]
)

crew.kickoff()
```

### [​](#filtering-specific-asana-tools) Filtering Specific Asana Tools

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create agent with specific Asana actions only
task_manager_agent = Agent(
    role="Task Manager",
    goal="Create and manage tasks efficiently",
    backstory="An AI assistant that focuses on task creation and management.",
    apps=[
        'asana/create_task',
        'asana/update_task',
        'asana/get_tasks'
    ]  # Specific Asana actions
)

# Task to create and assign a task
task_management = Task(
    description="Create a task called 'Review quarterly reports' and assign it to the appropriate team member",
    agent=task_manager_agent,
    expected_output="Task created and assigned successfully"
)

crew = Crew(
    agents=[task_manager_agent],
    tasks=[task_management]
)

crew.kickoff()
```

### [​](#advanced-project-management) Advanced Project Management

Copy

Ask AI

```
from crewai import Agent, Task, Crew

project_coordinator = Agent(
    role="Project Coordinator",
    goal="Coordinate project activities and track progress",
    backstory="An experienced project coordinator who ensures projects run smoothly.",
    apps=['asana']
)

# Complex task involving multiple Asana operations
coordination_task = Task(
    description="""
    1. Get all active projects in the workspace
    2. For each project, get the list of incomplete tasks
    3. Create a summary report task in the 'Management Reports' project
    4. Add comments to overdue tasks to request status updates
    """,
    agent=project_coordinator,
    expected_output="Summary report created and status update requests sent for overdue tasks"
)

crew = Crew(
    agents=[project_coordinator],
    tasks=[coordination_task]
)

crew.kickoff()
```

Was this page helpful?

YesNo

[Role-Based Access Control (RBAC)

Previous](/en/enterprise/features/rbac)[Box Integration

Next](/en/enterprise/integrations/box)

⌘I