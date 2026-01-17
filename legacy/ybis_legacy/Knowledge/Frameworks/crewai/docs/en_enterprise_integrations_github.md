GitHub Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Integration Docs

GitHub Integration

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

Enable your agents to manage repositories, issues, and releases through GitHub. Create and update issues, manage releases, track project development, and streamline your software development workflow with AI-powered automation.

## [​](#prerequisites) Prerequisites

Before using the GitHub integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A GitHub account with appropriate repository permissions
* Connected your GitHub account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## [​](#setting-up-github-integration) Setting Up GitHub Integration

### [​](#1-connect-your-github-account) 1. Connect Your GitHub Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **GitHub** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for repository and issue management
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

github/create\_issue

**Description:** Create an issue in GitHub.**Parameters:**

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: “abc”).
* `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
* `title` (string, required): Issue Title - Specify the title of the issue to create.
* `body` (string, optional): Issue Body - Specify the body contents of the issue to create.
* `assignees` (string, optional): Assignees - Specify the assignee(s)’ GitHub login as an array of strings for this issue. (example: `["octocat"]`).

github/update\_issue

**Description:** Update an issue in GitHub.**Parameters:**

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: “abc”).
* `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
* `issue_number` (string, required): Issue Number - Specify the number of the issue to update.
* `title` (string, required): Issue Title - Specify the title of the issue to update.
* `body` (string, optional): Issue Body - Specify the body contents of the issue to update.
* `assignees` (string, optional): Assignees - Specify the assignee(s)’ GitHub login as an array of strings for this issue. (example: `["octocat"]`).
* `state` (string, optional): State - Specify the updated state of the issue.
  + Options: `open`, `closed`

github/get\_issue\_by\_number

**Description:** Get an issue by number in GitHub.**Parameters:**

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: “abc”).
* `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
* `issue_number` (string, required): Issue Number - Specify the number of the issue to fetch.

github/lock\_issue

**Description:** Lock an issue in GitHub.**Parameters:**

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: “abc”).
* `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
* `issue_number` (string, required): Issue Number - Specify the number of the issue to lock.
* `lock_reason` (string, required): Lock Reason - Specify a reason for locking the issue or pull request conversation.
  + Options: `off-topic`, `too heated`, `resolved`, `spam`

github/search\_issue

**Description:** Search for issues in GitHub.**Parameters:**

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Issue. (example: “abc”).
* `repo` (string, required): Repository - Specify the name of the associated repository for this Issue.
* `filter` (object, required): A filter in disjunctive normal form - OR of AND groups of single conditions.

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
            "field": "assignee",
            "operator": "$stringExactlyMatches",
            "value": "octocat"
          }
        ]
      }
    ]
  }
  ```

  Available fields: `assignee`, `creator`, `mentioned`, `labels`

github/create\_release

**Description:** Create a release in GitHub.**Parameters:**

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: “abc”).
* `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
* `tag_name` (string, required): Name - Specify the name of the release tag to be created. (example: “v1.0.0”).
* `target_commitish` (string, optional): Target - Specify the target of the release. This can either be a branch name or a commit SHA. Defaults to the main branch. (example: “master”).
* `body` (string, optional): Body - Specify a description for this release.
* `draft` (string, optional): Draft - Specify whether the created release should be a draft (unpublished) release.
  + Options: `true`, `false`
* `prerelease` (string, optional): Prerelease - Specify whether the created release should be a prerelease.
  + Options: `true`, `false`
* `discussion_category_name` (string, optional): Discussion Category Name - If specified, a discussion of the specified category is created and linked to the release. The value must be a category that already exists in the repository.
* `generate_release_notes` (string, optional): Release Notes - Specify whether the created release should automatically create release notes using the provided name and body specified.
  + Options: `true`, `false`

github/update\_release

**Description:** Update a release in GitHub.**Parameters:**

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: “abc”).
* `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
* `id` (string, required): Release ID - Specify the ID of the release to update.
* `tag_name` (string, optional): Name - Specify the name of the release tag to be updated. (example: “v1.0.0”).
* `target_commitish` (string, optional): Target - Specify the target of the release. This can either be a branch name or a commit SHA. Defaults to the main branch. (example: “master”).
* `body` (string, optional): Body - Specify a description for this release.
* `draft` (string, optional): Draft - Specify whether the created release should be a draft (unpublished) release.
  + Options: `true`, `false`
* `prerelease` (string, optional): Prerelease - Specify whether the created release should be a prerelease.
  + Options: `true`, `false`
* `discussion_category_name` (string, optional): Discussion Category Name - If specified, a discussion of the specified category is created and linked to the release. The value must be a category that already exists in the repository.
* `generate_release_notes` (string, optional): Release Notes - Specify whether the created release should automatically create release notes using the provided name and body specified.
  + Options: `true`, `false`

github/get\_release\_by\_id

**Description:** Get a release by ID in GitHub.**Parameters:**

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: “abc”).
* `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
* `id` (string, required): Release ID - Specify the release ID of the release to fetch.

github/get\_release\_by\_tag\_name

**Description:** Get a release by tag name in GitHub.**Parameters:**

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: “abc”).
* `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
* `tag_name` (string, required): Name - Specify the tag of the release to fetch. (example: “v1.0.0”).

github/delete\_release

**Description:** Delete a release in GitHub.**Parameters:**

* `owner` (string, required): Owner - Specify the name of the account owner of the associated repository for this Release. (example: “abc”).
* `repo` (string, required): Repository - Specify the name of the associated repository for this Release.
* `id` (string, required): Release ID - Specify the ID of the release to delete.

## [​](#usage-examples) Usage Examples

### [​](#basic-github-agent-setup) Basic GitHub Agent Setup

Copy

Ask AI

```
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

# Create an agent with Github capabilities
github_agent = Agent(
    role="Repository Manager",
    goal="Manage GitHub repositories, issues, and releases efficiently",
    backstory="An AI assistant specialized in repository management and issue tracking.",
    apps=['github']  # All Github actions will be available
)

# Task to create a new issue
create_issue_task = Task(
    description="Create a bug report issue for the login functionality in the main repository",
    agent=github_agent,
    expected_output="Issue created successfully with issue number"
)

# Run the task
crew = Crew(
    agents=[github_agent],
    tasks=[create_issue_task]
)

crew.kickoff()
```

### [​](#filtering-specific-github-tools) Filtering Specific GitHub Tools

Copy

Ask AI

```
issue_manager = Agent(
    role="Issue Manager",
    goal="Create and manage GitHub issues efficiently",
    backstory="An AI assistant that focuses on issue tracking and management.",
    apps=['github/create_issue']
)

# Task to manage issue workflow
issue_workflow = Task(
    description="Create a feature request issue and assign it to the development team",
    agent=issue_manager,
    expected_output="Feature request issue created and assigned successfully"
)

crew = Crew(
    agents=[issue_manager],
    tasks=[issue_workflow]
)

crew.kickoff()
```

### [​](#release-management) Release Management

Copy

Ask AI

```
from crewai import Agent, Task, Crew

release_manager = Agent(
    role="Release Manager",
    goal="Manage software releases and versioning",
    backstory="An experienced release manager who handles version control and release processes.",
    apps=['github']
)

# Task to create a new release
release_task = Task(
    description="""
    Create a new release v2.1.0 for the project with:
    - Auto-generated release notes
    - Target the main branch
    - Include a description of new features and bug fixes
    """,
    agent=release_manager,
    expected_output="Release v2.1.0 created successfully with release notes"
)

crew = Crew(
    agents=[release_manager],
    tasks=[release_task]
)

crew.kickoff()
```

### [​](#issue-tracking-and-management) Issue Tracking and Management

Copy

Ask AI

```
from crewai import Agent, Task, Crew

project_coordinator = Agent(
    role="Project Coordinator",
    goal="Track and coordinate project issues and development progress",
    backstory="An AI assistant that helps coordinate development work and track project progress.",
    apps=['github']
)

# Complex task involving multiple GitHub operations
coordination_task = Task(
    description="""
    1. Search for all open issues assigned to the current milestone
    2. Identify overdue issues and update their priority labels
    3. Create a weekly progress report issue
    4. Lock resolved issues that have been inactive for 30 days
    """,
    agent=project_coordinator,
    expected_output="Project coordination completed with progress report and issue management"
)

crew = Crew(
    agents=[project_coordinator],
    tasks=[coordination_task]
)

crew.kickoff()
```

### [​](#getting-help) Getting Help

[## Need Help?

Contact our support team for assistance with GitHub integration setup or troubleshooting.](/cdn-cgi/l/email-protection#32414742425d40467251405745535b1c515d5f)

Was this page helpful?

YesNo

[ClickUp Integration

Previous](/en/enterprise/integrations/clickup)[Gmail Integration

Next](/en/enterprise/integrations/gmail)

⌘I