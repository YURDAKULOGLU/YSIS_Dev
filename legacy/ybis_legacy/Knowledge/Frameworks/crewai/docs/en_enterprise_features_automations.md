Automations - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘K

Search...

Navigation

Build

Automations

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

Automations is the live operations hub for your deployed crews. Use it to deploy from GitHub or a ZIP file, manage environment variables, re‑deploy when needed, and monitor the status of each automation.

![Automations Overview](https://mintcdn.com/crewai/Grq_Qb7_m8o-TQ5O/images/enterprise/automations-overview.png?fit=max&auto=format&n=Grq_Qb7_m8o-TQ5O&q=85&s=a7d0655da82c70b0ca152715cb8253f4)

## [​](#deployment-methods) Deployment Methods

### [​](#deploy-from-github) Deploy from GitHub

Use this for version‑controlled projects and continuous deployment.

1

Connect GitHub

Click **Configure GitHub** and authorize access.

2

Select Repository & Branch

Choose the **Repository** and **Branch** you want to deploy from.

3

Enable Auto‑deploy (optional)

Turn on **Automatically deploy new commits** to ship updates on every push.

4

Add Environment Variables

Add secrets individually or use **Bulk View** for multiple variables.

5

Deploy

Click **Deploy** to create your live automation.

![GitHub Deployment](https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/deploy-from-github.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=4fb72dc68799d5a0c35e2e74f1a7cc6c)

### [​](#deploy-from-zip) Deploy from ZIP

Ship quickly without Git—upload a compressed package of your project.

1

Choose File

Select the ZIP archive from your computer.

2

Add Environment Variables

Provide any required variables or keys.

3

Deploy

Click **Deploy** to create your live automation.

![ZIP Deployment](https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/deploy-from-zip.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=8cea74868a553d34b0aa182ad5489099)

## [​](#automations-dashboard) Automations Dashboard

The table lists all live automations with key details:

* **CREW**: Automation name
* **STATUS**: Online / Failed / In Progress
* **URL**: Endpoint for kickoff/status
* **TOKEN**: Automation token
* **ACTIONS**: Re‑deploy, delete, and more

Use the top‑right controls to filter and search:

* Search by name
* Filter by **Status**
* Filter by **Source** (GitHub / Studio / ZIP)

Once deployed, you can view the automation details and have the **Options** dropdown menu to `chat with this crew`, `Export React Component` and `Export as MCP`.

![Automations Table](https://mintcdn.com/crewai/Grq_Qb7_m8o-TQ5O/images/enterprise/automations-table.png?fit=max&auto=format&n=Grq_Qb7_m8o-TQ5O&q=85&s=f7fb571e8473f5cb7940c3e3bb34f95c)

## [​](#best-practices) Best Practices

* Prefer GitHub deployments for version control and CI/CD
* Use re‑deploy to roll forward after code or config updates or set it to auto-deploy on every push

## [​](#related) Related

[## Deploy a Crew

Deploy a Crew from GitHub or ZIP file.](/en/enterprise/guides/deploy-crew)[## Automation Triggers

Trigger automations via webhooks or API.](/en/enterprise/guides/automation-triggers)[## Webhook Automation

Stream real-time events and updates to your systems.](/en/enterprise/guides/webhook-automation)

Was this page helpful?

YesNo

[CrewAI AOP

Previous](/en/enterprise/introduction)[Crew Studio

Next](/en/enterprise/features/crew-studio)

⌘I