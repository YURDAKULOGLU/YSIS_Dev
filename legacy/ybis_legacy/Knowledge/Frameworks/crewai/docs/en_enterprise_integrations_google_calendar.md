Google Calendar Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Integration Docs

Google Calendar Integration

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

Enable your agents to manage calendar events, schedules, and availability through Google Calendar. Create and update events, manage attendees, check availability, and streamline your scheduling workflows with AI-powered automation.

## [​](#prerequisites) Prerequisites

Before using the Google Calendar integration, ensure you have:

* A [CrewAI AOP](https://app.crewai.com) account with an active subscription
* A Google account with Google Calendar access
* Connected your Google account through the [Integrations page](https://app.crewai.com/crewai_plus/connectors)

## [​](#setting-up-google-calendar-integration) Setting Up Google Calendar Integration

### [​](#1-connect-your-google-account) 1. Connect Your Google Account

1. Navigate to [CrewAI AOP Integrations](https://app.crewai.com/crewai_plus/connectors)
2. Find **Google Calendar** in the Authentication Integrations section
3. Click **Connect** and complete the OAuth flow
4. Grant the necessary permissions for calendar access
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

google\_calendar/get\_availability

**Description:** Get calendar availability (free/busy information).**Parameters:**

* `timeMin` (string, required): Start time (RFC3339 format)
* `timeMax` (string, required): End time (RFC3339 format)
* `items` (array, required): Calendar IDs to check

  Copy

  Ask AI

  ```
  [
    {
      "id": "calendar_id"
    }
  ]
  ```
* `timeZone` (string, optional): Time zone used in the response. The default is UTC.
* `groupExpansionMax` (integer, optional): Maximal number of calendar identifiers to be provided for a single group. Maximum: 100
* `calendarExpansionMax` (integer, optional): Maximal number of calendars for which FreeBusy information is to be provided. Maximum: 50

google\_calendar/create\_event

**Description:** Create a new event in the specified calendar.**Parameters:**

* `calendarId` (string, required): Calendar ID (use ‘primary’ for main calendar)
* `summary` (string, required): Event title/summary
* `start_dateTime` (string, required): Start time in RFC3339 format (e.g., 2024-01-20T10:00:00-07:00)
* `end_dateTime` (string, required): End time in RFC3339 format
* `description` (string, optional): Event description
* `timeZone` (string, optional): Time zone (e.g., America/Los\_Angeles)
* `location` (string, optional): Geographic location of the event as free-form text.
* `attendees` (array, optional): List of attendees for the event.

  Copy

  Ask AI

  ```
  [
    {
      "email": "[email protected]",
      "displayName": "Attendee Name",
      "optional": false
    }
  ]
  ```
* `reminders` (object, optional): Information about the event’s reminders.

  Copy

  Ask AI

  ```
  {
    "useDefault": true,
    "overrides": [
      {
        "method": "email",
        "minutes": 15
      }
    ]
  }
  ```
* `conferenceData` (object, optional): The conference-related information, such as details of a Google Meet conference.

  Copy

  Ask AI

  ```
  {
    "createRequest": {
      "requestId": "unique-request-id",
      "conferenceSolutionKey": {
        "type": "hangoutsMeet"
      }
    }
  }
  ```
* `visibility` (string, optional): Visibility of the event. Options: default, public, private, confidential. Default: default
* `transparency` (string, optional): Whether the event blocks time on the calendar. Options: opaque, transparent. Default: opaque

google\_calendar/view\_events

**Description:** Retrieve events for the specified calendar.**Parameters:**

* `calendarId` (string, required): Calendar ID (use ‘primary’ for main calendar)
* `timeMin` (string, optional): Lower bound for events (RFC3339)
* `timeMax` (string, optional): Upper bound for events (RFC3339)
* `maxResults` (integer, optional): Maximum number of events (default 10). Minimum: 1, Maximum: 2500
* `orderBy` (string, optional): The order of the events returned in the result. Options: startTime, updated. Default: startTime
* `singleEvents` (boolean, optional): Whether to expand recurring events into instances and only return single one-off events and instances of recurring events. Default: true
* `showDeleted` (boolean, optional): Whether to include deleted events (with status equals cancelled) in the result. Default: false
* `showHiddenInvitations` (boolean, optional): Whether to include hidden invitations in the result. Default: false
* `q` (string, optional): Free text search terms to find events that match these terms in any field.
* `pageToken` (string, optional): Token specifying which result page to return.
* `timeZone` (string, optional): Time zone used in the response.
* `updatedMin` (string, optional): Lower bound for an event’s last modification time (RFC3339) to filter by.
* `iCalUID` (string, optional): Specifies an event ID in the iCalendar format to be provided in the response.

google\_calendar/update\_event

**Description:** Update an existing event.**Parameters:**

* `calendarId` (string, required): Calendar ID
* `eventId` (string, required): Event ID to update
* `summary` (string, optional): Updated event title
* `description` (string, optional): Updated event description
* `start_dateTime` (string, optional): Updated start time
* `end_dateTime` (string, optional): Updated end time

google\_calendar/delete\_event

**Description:** Delete a specified event.**Parameters:**

* `calendarId` (string, required): Calendar ID
* `eventId` (string, required): Event ID to delete

google\_calendar/view\_calendar\_list

**Description:** Retrieve user’s calendar list.**Parameters:**

* `maxResults` (integer, optional): Maximum number of entries returned on one result page. Minimum: 1
* `pageToken` (string, optional): Token specifying which result page to return.
* `showDeleted` (boolean, optional): Whether to include deleted calendar list entries in the result. Default: false
* `showHidden` (boolean, optional): Whether to show hidden entries. Default: false
* `minAccessRole` (string, optional): The minimum access role for the user in the returned entries. Options: freeBusyReader, owner, reader, writer

## [​](#usage-examples) Usage Examples

### [​](#basic-calendar-agent-setup) Basic Calendar Agent Setup

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create an agent with Google Calendar capabilities
calendar_agent = Agent(
    role="Schedule Manager",
    goal="Manage calendar events and scheduling efficiently",
    backstory="An AI assistant specialized in calendar management and scheduling coordination.",
    apps=['google_calendar']  # All Google Calendar actions will be available
)

# Task to create a meeting
create_meeting_task = Task(
    description="Create a team standup meeting for tomorrow at 9 AM with the development team",
    agent=calendar_agent,
    expected_output="Meeting created successfully with Google Meet link"
)

# Run the task
crew = Crew(
    agents=[calendar_agent],
    tasks=[create_meeting_task]
)

crew.kickoff()
```

### [​](#filtering-specific-calendar-tools) Filtering Specific Calendar Tools

Copy

Ask AI

```
meeting_coordinator = Agent(
    role="Meeting Coordinator",
    goal="Coordinate meetings and check availability",
    backstory="An AI assistant that focuses on meeting scheduling and availability management.",
    apps=['google_calendar/create_event', 'google_calendar/get_availability']
)

# Task to schedule a meeting with availability check
schedule_meeting = Task(
    description="Check availability for next week and schedule a project review meeting with stakeholders",
    agent=meeting_coordinator,
    expected_output="Meeting scheduled after checking availability of all participants"
)

crew = Crew(
    agents=[meeting_coordinator],
    tasks=[schedule_meeting]
)

crew.kickoff()
```

### [​](#event-management-and-updates) Event Management and Updates

Copy

Ask AI

```
from crewai import Agent, Task, Crew

event_manager = Agent(
    role="Event Manager",
    goal="Manage and update calendar events efficiently",
    backstory="An experienced event manager who handles event logistics and updates.",
    apps=['google_calendar']
)

# Task to manage event updates
event_management = Task(
    description="""
    1. List all events for this week
    2. Update any events that need location changes to include video conference links
    3. Check availability for upcoming meetings
    """,
    agent=event_manager,
    expected_output="Weekly events updated with proper locations and availability checked"
)

crew = Crew(
    agents=[event_manager],
    tasks=[event_management]
)

crew.kickoff()
```

### [​](#availability-and-calendar-management) Availability and Calendar Management

Copy

Ask AI

```
from crewai import Agent, Task, Crew

availability_coordinator = Agent(
    role="Availability Coordinator",
    goal="Coordinate availability and manage calendars for scheduling",
    backstory="An AI assistant that specializes in availability management and calendar coordination.",
    apps=['google_calendar']
)

# Task to coordinate availability
availability_task = Task(
    description="""
    1. Get the list of available calendars
    2. Check availability for all calendars next Friday afternoon
    3. Create a team meeting for the first available 2-hour slot
    4. Include Google Meet link and send invitations
    """,
    agent=availability_coordinator,
    expected_output="Team meeting scheduled based on availability with all team members invited"
)

crew = Crew(
    agents=[availability_coordinator],
    tasks=[availability_task]
)

crew.kickoff()
```

### [​](#automated-scheduling-workflows) Automated Scheduling Workflows

Copy

Ask AI

```
from crewai import Agent, Task, Crew

scheduling_automator = Agent(
    role="Scheduling Automator",
    goal="Automate scheduling workflows and calendar management",
    backstory="An AI assistant that automates complex scheduling scenarios and calendar workflows.",
    apps=['google_calendar']
)

# Complex scheduling automation task
automation_task = Task(
    description="""
    1. List all upcoming events for the next two weeks
    2. Identify any scheduling conflicts or back-to-back meetings
    3. Suggest optimal meeting times by checking availability
    4. Create buffer time between meetings where needed
    5. Update event descriptions with agenda items and meeting links
    """,
    agent=scheduling_automator,
    expected_output="Calendar optimized with resolved conflicts, buffer times, and updated meeting details"
)

crew = Crew(
    agents=[scheduling_automator],
    tasks=[automation_task]
)

crew.kickoff()
```

## [​](#troubleshooting) Troubleshooting

### [​](#common-issues) Common Issues

**Authentication Errors**

* Ensure your Google account has the necessary permissions for calendar access
* Verify that the OAuth connection includes all required scopes for Google Calendar API
* Check if calendar sharing settings allow the required access level

**Event Creation Issues**

* Verify that time formats are correct (RFC3339 format)
* Ensure attendee email addresses are properly formatted
* Check that the target calendar exists and is accessible
* Verify time zones are correctly specified

**Availability and Time Conflicts**

* Use proper RFC3339 format for time ranges when checking availability
* Ensure time zones are consistent across all operations
* Verify that calendar IDs are correct when checking multiple calendars

**Event Updates and Deletions**

* Verify that event IDs are correct and events exist
* Ensure you have edit permissions for the events
* Check that calendar ownership allows modifications

### [​](#getting-help) Getting Help

[## Need Help?

Contact our support team for assistance with Google Calendar integration setup or troubleshooting.](/cdn-cgi/l/email-protection#493a3c3939263b3d092a3b2c3e2820672a2624)

Was this page helpful?

YesNo

[Gmail Integration

Previous](/en/enterprise/integrations/gmail)[Google Contacts Integration

Next](/en/enterprise/integrations/google_contacts)

⌘I