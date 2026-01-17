Agent Repositories - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Build

Agent Repositories

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

Agent Repositories allow enterprise users to store, share, and reuse agent definitions across teams and projects. This feature enables organizations to maintain a centralized library of standardized agents, promoting consistency and reducing duplication of effort.

![Agent Repositories](https://mintcdn.com/crewai/Grq_Qb7_m8o-TQ5O/images/enterprise/agent-repositories.png?fit=max&auto=format&n=Grq_Qb7_m8o-TQ5O&q=85&s=c2064b8fc57a99dfb8124909b64e0f9d)

## [​](#benefits-of-agent-repositories) Benefits of Agent Repositories

* **Standardization**: Maintain consistent agent definitions across your organization
* **Reusability**: Create an agent once and use it in multiple crews and projects
* **Governance**: Implement organization-wide policies for agent configurations
* **Collaboration**: Enable teams to share and build upon each other’s work

## [​](#creating-and-use-agent-repositories) Creating and Use Agent Repositories

1. You must have an account at CrewAI, try the [free plan](https://app.crewai.com).
2. Create agents with specific roles and goals for your workflows.
3. Configure tools and capabilities for each specialized assistant.
4. Deploy agents across projects via visual interface or API integration.

![Agent Repositories](https://mintcdn.com/crewai/Grq_Qb7_m8o-TQ5O/images/enterprise/create-agent-repository.png?fit=max&auto=format&n=Grq_Qb7_m8o-TQ5O&q=85&s=837a5d30ad32f8cd5e0bda08638c4c4d)

### [​](#loading-agents-from-repositories) Loading Agents from Repositories

You can load agents from repositories in your code using the `from_repository` parameter to run locally:

Copy

Ask AI

```
from crewai import Agent

# Create an agent by loading it from a repository
# The agent is loaded with all its predefined configurations
researcher = Agent(
    from_repository="market-research-agent"
)
```

### [​](#overriding-repository-settings) Overriding Repository Settings

You can override specific settings from the repository by providing them in the configuration:

Copy

Ask AI

```
researcher = Agent(
    from_repository="market-research-agent",
    goal="Research the latest trends in AI development",  # Override the repository goal
    verbose=True  # Add a setting not in the repository
)
```

### [​](#example:-creating-a-crew-with-repository-agents) Example: Creating a Crew with Repository Agents

Copy

Ask AI

```
from crewai import Crew, Agent, Task

# Load agents from repositories
researcher = Agent(
    from_repository="market-research-agent"
)

writer = Agent(
    from_repository="content-writer-agent"
)

# Create tasks
research_task = Task(
    description="Research the latest trends in AI",
    agent=researcher
)

writing_task = Task(
    description="Write a comprehensive report based on the research",
    agent=writer
)

# Create the crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

# Run the crew
result = crew.kickoff()
```

### [​](#example:-using-kickoff-with-repository-agents) Example: Using `kickoff()` with Repository Agents

You can also use repository agents directly with the `kickoff()` method for simpler interactions:

Copy

Ask AI

```
from crewai import Agent
from pydantic import BaseModel
from typing import List

# Define a structured output format
class MarketAnalysis(BaseModel):
    key_trends: List[str]
    opportunities: List[str]
    recommendation: str

# Load an agent from repository
analyst = Agent(
    from_repository="market-analyst-agent",
    verbose=True
)

# Get a free-form response
result = analyst.kickoff("Analyze the AI market in 2025")
print(result.raw)  # Access the raw response

# Get structured output
structured_result = analyst.kickoff(
    "Provide a structured analysis of the AI market in 2025",
    response_format=MarketAnalysis
)

# Access structured data
print(f"Key Trends: {structured_result.pydantic.key_trends}")
print(f"Recommendation: {structured_result.pydantic.recommendation}")
```

## [​](#best-practices) Best Practices

1. **Naming Convention**: Use clear, descriptive names for your repository agents
2. **Documentation**: Include comprehensive descriptions for each agent
3. **Tool Management**: Ensure that tools referenced by repository agents are available in your environment
4. **Access Control**: Manage permissions to ensure only authorized team members can modify repository agents

## [​](#organization-management) Organization Management

To switch between organizations or see your current organization, use the CrewAI CLI:

Copy

Ask AI

```
# View current organization
crewai org current

# Switch to a different organization
crewai org switch <org_id>

# List all available organizations
crewai org list
```

When loading agents from repositories, you must be authenticated and switched to the correct organization. If you receive errors, check your authentication status and organization settings using the CLI commands above.

Was this page helpful?

YesNo

[Marketplace

Previous](/en/enterprise/features/marketplace)[Tools & Integrations

Next](/en/enterprise/features/tools-and-integrations)

⌘I