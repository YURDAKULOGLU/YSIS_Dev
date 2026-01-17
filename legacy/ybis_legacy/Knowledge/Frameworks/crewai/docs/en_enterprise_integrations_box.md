Box Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Integration Docs

Box Integration

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

Enable your agents to manage files, folders, and documents through Box. Upload files, organize folder structures, search content, and streamline your team’s document management with AI-powered automation.

## [​](#prerequisites) Prerequisites

Before using the Box integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Box account with appropriate permissions
* Connected your Box account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## [​](#setting-up-box-integration) Setting Up Box Integration

### [​](#1-connect-your-box-account) 1. Connect Your Box Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Box** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for file and folder management
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

box/save\_file

**Description:** Save a file from URL in Box.**Parameters:**

* `fileAttributes` (object, required): Attributes - File metadata including name, parent folder, and timestamps.

  Copy

  Ask AI

  ```
  {
    "content_created_at": "2012-12-12T10:53:43-08:00",
    "content_modified_at": "2012-12-12T10:53:43-08:00",
    "name": "qwerty.png",
    "parent": { "id": "1234567" }
  }
  ```
* `file` (string, required): File URL - Files must be smaller than 50MB in size. (example: “<https://picsum.photos/200/300>”).

box/save\_file\_from\_object

**Description:** Save a file in Box.**Parameters:**

* `file` (string, required): File - Accepts a File Object containing file data. Files must be smaller than 50MB in size.
* `fileName` (string, required): File Name (example: “qwerty.png”).
* `folder` (string, optional): Folder - Use Connect Portal Workflow Settings to allow users to select the File’s Folder destination. Defaults to the user’s root folder if left blank.

box/get\_file\_by\_id

**Description:** Get a file by ID in Box.**Parameters:**

* `fileId` (string, required): File ID - The unique identifier that represents a file. (example: “12345”).

box/list\_files

**Description:** List files in Box.**Parameters:**

* `folderId` (string, required): Folder ID - The unique identifier that represents a folder. (example: “0”).
* `filterFormula` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.

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
            "field": "direction",
            "operator": "$stringExactlyMatches",
            "value": "ASC"
          }
        ]
      }
    ]
  }
  ```

box/create\_folder

**Description:** Create a folder in Box.**Parameters:**

* `folderName` (string, required): Name - The name for the new folder. (example: “New Folder”).
* `folderParent` (object, required): Parent Folder - The parent folder where the new folder will be created.

  Copy

  Ask AI

  ```
  {
    "id": "123456"
  }
  ```

box/move\_folder

**Description:** Move a folder in Box.**Parameters:**

* `folderId` (string, required): Folder ID - The unique identifier that represents a folder. (example: “0”).
* `folderName` (string, required): Name - The name for the folder. (example: “New Folder”).
* `folderParent` (object, required): Parent Folder - The new parent folder destination.

  Copy

  Ask AI

  ```
  {
    "id": "123456"
  }
  ```

box/get\_folder\_by\_id

**Description:** Get a folder by ID in Box.**Parameters:**

* `folderId` (string, required): Folder ID - The unique identifier that represents a folder. (example: “0”).

box/search\_folders

**Description:** Search folders in Box.**Parameters:**

* `folderId` (string, required): Folder ID - The folder to search within.
* `filterFormula` (object, optional): A filter in disjunctive normal form - OR of AND groups of single conditions.

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
            "field": "sort",
            "operator": "$stringExactlyMatches",
            "value": "name"
          }
        ]
      }
    ]
  }
  ```

box/delete\_folder

**Description:** Delete a folder in Box.**Parameters:**

* `folderId` (string, required): Folder ID - The unique identifier that represents a folder. (example: “0”).
* `recursive` (boolean, optional): Recursive - Delete a folder that is not empty by recursively deleting the folder and all of its content.

## [​](#usage-examples) Usage Examples

### [​](#basic-box-agent-setup) Basic Box Agent Setup

Copy

Ask AI

```
from crewai import Agent, Task, Crew
from crewai import Agent, Task, Crew

# Create an agent with Box capabilities
box_agent = Agent(
    role="Document Manager",
    goal="Manage files and folders in Box efficiently",
    backstory="An AI assistant specialized in document management and file organization.",
    apps=['box']  # All Box actions will be available
)

# Task to create a folder structure
create_structure_task = Task(
    description="Create a folder called 'Project Files' in the root directory and upload a document from URL",
    agent=box_agent,
    expected_output="Folder created and file uploaded successfully"
)

# Run the task
crew = Crew(
    agents=[box_agent],
    tasks=[create_structure_task]
)

crew.kickoff()
```

### [​](#filtering-specific-box-tools) Filtering Specific Box Tools

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create agent with specific Box actions only
file_organizer_agent = Agent(
    role="File Organizer",
    goal="Organize and manage file storage efficiently",
    backstory="An AI assistant that focuses on file organization and storage management.",
    apps=['box/create_folder', 'box/save_file', 'box/list_files']  # Specific Box actions
)

# Task to organize files
organization_task = Task(
    description="Create a folder structure for the marketing team and organize existing files",
    agent=file_organizer_agent,
    expected_output="Folder structure created and files organized"
)

crew = Crew(
    agents=[file_organizer_agent],
    tasks=[organization_task]
)

crew.kickoff()
```

### [​](#advanced-file-management) Advanced File Management

Copy

Ask AI

```
from crewai import Agent, Task, Crew

file_manager = Agent(
    role="File Manager",
    goal="Maintain organized file structure and manage document lifecycle",
    backstory="An experienced file manager who ensures documents are properly organized and accessible.",
    apps=['box']
)

# Complex task involving multiple Box operations
management_task = Task(
    description="""
    1. List all files in the root folder
    2. Create monthly archive folders for the current year
    3. Move old files to appropriate archive folders
    4. Generate a summary report of the file organization
    """,
    agent=file_manager,
    expected_output="Files organized into archive structure with summary report"
)

crew = Crew(
    agents=[file_manager],
    tasks=[management_task]
)

crew.kickoff()
```

Was this page helpful?

YesNo

[Asana Integration

Previous](/en/enterprise/integrations/asana)[ClickUp Integration

Next](/en/enterprise/integrations/clickup)

⌘I