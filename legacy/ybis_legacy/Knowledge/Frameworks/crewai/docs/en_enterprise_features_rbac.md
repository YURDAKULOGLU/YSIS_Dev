Role-Based Access Control (RBAC) - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Manage

Role-Based Access Control (RBAC)

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

RBAC in CrewAI AOP enables secure, scalable access management through a combination of organization‑level roles and automation‑level visibility controls.

![RBAC overview in CrewAI AOP](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/users_and_roles.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=31b2661025e9813f32938f9d583228b5)

## [​](#users-and-roles) Users and Roles

Each member in your CrewAI workspace is assigned a role, which determines their access across various features.
You can:

* Use predefined roles (Owner, Member)
* Create custom roles tailored to specific permissions
* Assign roles at any time through the settings panel

You can configure users and roles in Settings → Roles.

1

Open Roles settings

Go to **Settings → Roles** in CrewAI AOP.

2

Choose a role type

Use a predefined role (**Owner**, **Member**) or click **Create role** to define a custom one.

3

Assign to members

Select users and assign the role. You can change this anytime.

### [​](#configuration-summary) Configuration summary

| Area | Where to configure | Options |
| --- | --- | --- |
| Users & Roles | Settings → Roles | Predefined: Owner, Member; Custom roles |
| Automation visibility | Automation → Settings → Visibility | Private; Whitelist users/roles |

## [​](#automation‑level-access-control) Automation‑level Access Control

In addition to organization‑wide roles, CrewAI Automations support fine‑grained visibility settings that let you restrict access to specific automations by user or role.
This is useful for:

* Keeping sensitive or experimental automations private
* Managing visibility across large teams or external collaborators
* Testing automations in isolated contexts

Deployments can be configured as private, meaning only whitelisted users and roles will be able to:

* View the deployment
* Run it or interact with its API
* Access its logs, metrics, and settings

The organization owner always has access, regardless of visibility settings.
You can configure automation‑level access control in Automation → Settings → Visibility tab.

1

Open Visibility tab

Navigate to **Automation → Settings → Visibility**.

2

Set visibility

Choose **Private** to restrict access. The organization owner always retains access.

3

Whitelist access

Add specific users and roles allowed to view, run, and access logs/metrics/settings.

4

Save and verify

Save changes, then confirm that non‑whitelisted users cannot view or run the automation.

### [​](#private-visibility:-access-outcomes) Private visibility: access outcomes

| Action | Owner | Whitelisted user/role | Not whitelisted |
| --- | --- | --- | --- |
| View automation | ✓ | ✓ | ✗ |
| Run automation/API | ✓ | ✓ | ✗ |
| Access logs/metrics/settings | ✓ | ✓ | ✗ |

The organization owner always has access. In private mode, only whitelisted users and roles can view, run, and access logs/metrics/settings.

![Automation Visibility settings in CrewAI AOP](https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/visibility.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=48e3dd12b9d55da6f7adc82ea80be56d)

[## Need Help?

Contact our support team for assistance with RBAC questions.](/cdn-cgi/l/email-protection#b1c2c4c1c1dec3c5f1d2c3d4c6d0d89fd2dedc)

Was this page helpful?

YesNo

[Hallucination Guardrail

Previous](/en/enterprise/features/hallucination-guardrail)[Asana Integration

Next](/en/enterprise/integrations/asana)

⌘I