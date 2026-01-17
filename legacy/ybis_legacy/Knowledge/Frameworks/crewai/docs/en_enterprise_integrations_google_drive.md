Google Drive Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Integration Docs

Google Drive Integration

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

Enable your agents to manage files and folders through Google Drive. Upload, download, organize, and share files, create folders, and streamline your document management workflows with AI-powered automation.

## [​](#prerequisites) Prerequisites

Before using the Google Drive integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Google account with Google Drive access
* Connected your Google account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## [​](#setting-up-google-drive-integration) Setting Up Google Drive Integration

### [​](#1-connect-your-google-account) 1. Connect Your Google Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Google Drive** in the Authentication Integrations section
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

google\_drive/get\_file

**Description:** Get a file by ID from Google Drive.**Parameters:**

* `file_id` (string, required): The ID of the file to retrieve.

google\_drive/list\_files

**Description:** List files in Google Drive.**Parameters:**

* `q` (string, optional): Query string to filter files (example: “name contains ‘report’”).
* `page_size` (integer, optional): Maximum number of files to return (default: 100, max: 1000).
* `page_token` (string, optional): Token for retrieving the next page of results.
* `order_by` (string, optional): Sort order (example: “name”, “createdTime desc”, “modifiedTime”).
* `spaces` (string, optional): Comma-separated list of spaces to query (drive, appDataFolder, photos).

google\_drive/upload\_file

**Description:** Upload a file to Google Drive.**Parameters:**

* `name` (string, required): Name of the file to create.
* `content` (string, required): Content of the file to upload.
* `mime_type` (string, optional): MIME type of the file (example: “text/plain”, “application/pdf”).
* `parent_folder_id` (string, optional): ID of the parent folder where the file should be created.
* `description` (string, optional): Description of the file.

google\_drive/download\_file

**Description:** Download a file from Google Drive.**Parameters:**

* `file_id` (string, required): The ID of the file to download.
* `mime_type` (string, optional): MIME type for export (required for Google Workspace documents).

google\_drive/create\_folder

**Description:** Create a new folder in Google Drive.**Parameters:**

* `name` (string, required): Name of the folder to create.
* `parent_folder_id` (string, optional): ID of the parent folder where the new folder should be created.
* `description` (string, optional): Description of the folder.

google\_drive/delete\_file

**Description:** Delete a file from Google Drive.**Parameters:**

* `file_id` (string, required): The ID of the file to delete.

google\_drive/share\_file

**Description:** Share a file in Google Drive with specific users or make it public.**Parameters:**

* `file_id` (string, required): The ID of the file to share.
* `role` (string, required): The role granted by this permission (reader, writer, commenter, owner).
* `type` (string, required): The type of the grantee (user, group, domain, anyone).
* `email_address` (string, optional): The email address of the user or group to share with (required for user/group types).
* `domain` (string, optional): The domain to share with (required for domain type).
* `send_notification_email` (boolean, optional): Whether to send a notification email (default: true).
* `email_message` (string, optional): A plain text custom message to include in the notification email.

google\_drive/update\_file

**Description:** Update an existing file in Google Drive.**Parameters:**

* `file_id` (string, required): The ID of the file to update.
* `name` (string, optional): New name for the file.
* `content` (string, optional): New content for the file.
* `mime_type` (string, optional): New MIME type for the file.
* `description` (string, optional): New description for the file.
* `add_parents` (string, optional): Comma-separated list of parent folder IDs to add.
* `remove_parents` (string, optional): Comma-separated list of parent folder IDs to remove.

## [​](#usage-examples) Usage Examples

### [​](#basic-google-drive-agent-setup) Basic Google Drive Agent Setup

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create an agent with Google Drive capabilities
drive_agent = Agent(
    role="File Manager",
    goal="Manage files and folders in Google Drive efficiently",
    backstory="An AI assistant specialized in document and file management.",
    apps=['google_drive']  # All Google Drive actions will be available
)

# Task to organize files
organize_files_task = Task(
    description="List all files in the root directory and organize them into appropriate folders",
    agent=drive_agent,
    expected_output="Summary of files organized with folder structure"
)

# Run the task
crew = Crew(
    agents=[drive_agent],
    tasks=[organize_files_task]
)

crew.kickoff()
```

### [​](#filtering-specific-google-drive-tools) Filtering Specific Google Drive Tools

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create agent with specific Google Drive actions only
file_manager_agent = Agent(
    role="Document Manager",
    goal="Upload and manage documents efficiently",
    backstory="An AI assistant that focuses on document upload and organization.",
    apps=[
        'google_drive/upload_file',
        'google_drive/create_folder',
        'google_drive/share_file'
    ]  # Specific Google Drive actions
)

# Task to upload and share documents
document_task = Task(
    description="Upload the quarterly report and share it with the finance team",
    agent=file_manager_agent,
    expected_output="Document uploaded and sharing permissions configured"
)

crew = Crew(
    agents=[file_manager_agent],
    tasks=[document_task]
)

crew.kickoff()
```

### [​](#advanced-file-management) Advanced File Management

Copy

Ask AI

```
from crewai import Agent, Task, Crew

file_organizer = Agent(
    role="File Organizer",
    goal="Maintain organized file structure and manage permissions",
    backstory="An experienced file manager who ensures proper organization and access control.",
    apps=['google_drive']
)

# Complex task involving multiple Google Drive operations
organization_task = Task(
    description="""
    1. List all files in the shared folder
    2. Create folders for different document types (Reports, Presentations, Spreadsheets)
    3. Move files to appropriate folders based on their type
    4. Set appropriate sharing permissions for each folder
    5. Create a summary document of the organization changes
    """,
    agent=file_organizer,
    expected_output="Files organized into categorized folders with proper permissions and summary report"
)

crew = Crew(
    agents=[file_organizer],
    tasks=[organization_task]
)

crew.kickoff()
```

Was this page helpful?

YesNo

[Google Docs Integration

Previous](/en/enterprise/integrations/google_docs)[Google Sheets Integration

Next](/en/enterprise/integrations/google_sheets)

⌘I