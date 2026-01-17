How to manage workspaces - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Prefect Cloud

How to manage workspaces

[Getting Started](/v3/get-started)[Concepts](/v3/concepts)[How-to Guides](/v3/how-to-guides)[Advanced](/v3/advanced)[Examples](/v3/examples)[Integrations](/integrations/integrations)[API Reference](/v3/api-ref)[Contribute](/contribute)[Release Notes](/v3/release-notes)

* [Overview](/v3/how-to-guides)

##### Workflows

* [Write and run a workflow](/v3/how-to-guides/workflows/write-and-run)
* [Use assets to track workflow outputs](/v3/how-to-guides/workflows/assets)
* [Automatically rerun a workflow when it fails](/v3/how-to-guides/workflows/retries)
* [Manually retry a flow run](/v3/how-to-guides/workflows/retry-flow-runs)
* [Customize workflow metadata](/v3/how-to-guides/workflows/custom-metadata)
* [Pass inputs to a workflow](/v3/how-to-guides/workflows/pass-inputs)
* [Add logging](/v3/how-to-guides/workflows/add-logging)
* [Access runtime information](/v3/how-to-guides/workflows/access-runtime-info)
* [Run work concurrently](/v3/how-to-guides/workflows/run-work-concurrently)
* [Cache workflow step outputs](/v3/how-to-guides/workflows/cache-workflow-steps)
* [Run background tasks](/v3/how-to-guides/workflows/run-background-tasks)
* [Respond to state changes](/v3/how-to-guides/workflows/state-change-hooks)
* [Create Artifacts](/v3/how-to-guides/workflows/artifacts)
* [Test workflows](/v3/how-to-guides/workflows/test-workflows)
* [Apply global concurrency and rate limits](/v3/how-to-guides/workflows/global-concurrency-limits)
* [Limit concurrent task runs with tags](/v3/how-to-guides/workflows/tag-based-concurrency-limits)

##### Deployments

* [Create Deployments](/v3/how-to-guides/deployments/create-deployments)
* [Trigger ad-hoc deployment runs](/v3/how-to-guides/deployments/run-deployments)
* [Create Deployment Schedules](/v3/how-to-guides/deployments/create-schedules)
* [Manage Deployment schedules](/v3/how-to-guides/deployments/manage-schedules)
* [Deploy via Python](/v3/how-to-guides/deployments/deploy-via-python)
* [Define deployments with YAML](/v3/how-to-guides/deployments/prefect-yaml)
* [Retrieve code from storage](/v3/how-to-guides/deployments/store-flow-code)
* [Version Deployments](/v3/how-to-guides/deployments/versioning)
* [Override Job Configuration](/v3/how-to-guides/deployments/customize-job-variables)

##### Configuration

* [Store secrets](/v3/how-to-guides/configuration/store-secrets)
* [Share configuration between workflows](/v3/how-to-guides/configuration/variables)
* [Manage settings](/v3/how-to-guides/configuration/manage-settings)

##### Automations

* [Create Automations](/v3/how-to-guides/automations/creating-automations)
* [Create Deployment Triggers](/v3/how-to-guides/automations/creating-deployment-triggers)
* [Chain Deployments with Events](/v3/how-to-guides/automations/chaining-deployments-with-events)
* [Access parameters in templates](/v3/how-to-guides/automations/access-parameters-in-templates)
* [Pass event payloads to flows](/v3/how-to-guides/automations/passing-event-payloads-to-flows)

##### Workflow Infrastructure

* [Manage Work Pools](/v3/how-to-guides/deployment_infra/manage-work-pools)
* [Run Flows in Local Processes](/v3/how-to-guides/deployment_infra/run-flows-in-local-processes)
* [Run flows on Prefect Managed infrastructure](/v3/how-to-guides/deployment_infra/managed)
* [Run flows on serverless compute](/v3/how-to-guides/deployment_infra/serverless)
* [Run flows in Docker containers](/v3/how-to-guides/deployment_infra/docker)
* [Run flows in a static container](/v3/how-to-guides/deployment_infra/serve-flows-docker)
* [Run flows on Kubernetes](/v3/how-to-guides/deployment_infra/kubernetes)
* [Run flows on Modal](/v3/how-to-guides/deployment_infra/modal)
* [Run flows on Coiled](/v3/how-to-guides/deployment_infra/coiled)

##### Prefect Cloud

* [Connect to Prefect Cloud](/v3/how-to-guides/cloud/connect-to-cloud)
* Manage accounts
* [Manage Workspaces](/v3/how-to-guides/cloud/workspaces)
* [Create a Webhook](/v3/how-to-guides/cloud/create-a-webhook)
* [Troubleshoot Prefect Cloud](/v3/how-to-guides/cloud/troubleshoot-cloud)

##### Prefect Self-hosted

* [Run a local Prefect server](/v3/how-to-guides/self-hosted/server-cli)
* [Run the Prefect server in Docker](/v3/how-to-guides/self-hosted/server-docker)
* [Run Prefect on Windows](/v3/how-to-guides/self-hosted/server-windows)
* [Run the Prefect Server via Docker Compose](/v3/how-to-guides/self-hosted/docker-compose)

##### AI

* [Use the Prefect MCP server](/v3/how-to-guides/ai/use-prefect-mcp-server)

##### Migrate

* [Migrate from Airflow](/v3/how-to-guides/migrate/airflow)
* [Upgrade to Prefect 3.0](/v3/how-to-guides/migrate/upgrade-to-prefect-3)
* [Upgrade from agents to workers](/v3/how-to-guides/migrate/upgrade-agents-to-workers)
* [Transfer resources between environments](/v3/how-to-guides/migrate/transfer-resources)

On this page

* [Get started with workspaces](#get-started-with-workspaces)
* [Create a workspace](#create-a-workspace)
* [Control access](#control-access)
* [Transfer a workspace](#transfer-a-workspace)
* [Delete a workspace](#delete-a-workspace)

A workspace is a discrete environment within Prefect Cloud for your workflows and related information.
For example, you can use separate workspaces to isolate dev, staging, and prod environments, or to provide separation between different teams.

## [​](#get-started-with-workspaces) Get started with workspaces

When you first log into Prefect Cloud, you are prompted to create your own workspace.
To see all workspace workspaces you can access, click on your workspace name in the top of the navigation sidebar.
To see all workspace workspaces you can access, click on your workspace name in the top of the navigation sidebar.
Your list of available workspaces may include:

* Your own account’s workspace.
* Workspaces in an account you’re invited to with Admin or Member access.

Your user permissions within workspaces may vary. Account admins can assign roles and permissions at the workspace level.

## [​](#create-a-workspace) Create a workspace

On the Account settings dropdown, select the “Create a new workspace” button to create a new workspace.
Configure:

* The **Workspace Owner** from the dropdown account menu options.
* A unique **Workspace Name** must be unique within the account.
* An optional description for the workspace.

Select **Create** to create the new workspace. The number of available workspaces varies by [Prefect Cloud plan](https://www.prefect.io/pricing/).
See [Pricing](https://www.prefect.io/pricing/) if you need additional workspaces or users.

## [​](#control-access) Control access

Within a Prefect Cloud Pro or Enterprise tier account, workspace owners can invite other people as members, and provision [service accounts](https://docs.prefect.io/ui/service-accounts/) to a workspace.
A workspace owner assigns a [workspace role](https://docs.prefect.io/ui/roles/) to the user and specifies the user’s scope of permissions within the workspace.
As a workspace owner, select **Workspaces -> Members** to manage members and **Workspaces -> Service Accounts** and service accounts for the workspace.
Previously invited individuals or provisioned service accounts are listed here.
To invite someone to an account, select the **Members +** icon. You can select from a list of existing account members.
Select a role for the user. This is the initial role for the user within the workspace.
A workspace owner can change this role at any time.
To remove a workspace member, select **Remove** from the menu on the right side of the user information on this page.
To add a service account to a workspace, select the **Service Accounts +** icon.
Select a **Name**, **Account Role**, **Expiration Date**, and optionally, a **Workspace**.
To update, delete, or rotate the API key for a service account, select an option for an existing service account from the menu on the right side of the service account.

## [​](#transfer-a-workspace) Transfer a workspace

Workspace transfer enables you to move an existing workspace from one account to another.
Workspace transfer retains existing workspace configuration and flow run history, including blocks, deployments, automations, work pools, and logs.

**Workspace transfer permissions**You must have administrator privileges to initiate or approve a workspace transfer.To initiate a workspace transfer between personal accounts, contact [support@prefect.io](mailto:support@prefect.io).

Click on the name of your workspace in the sidebar navigation and select **Workspace settings**.
From the three dot menu in the upper right of the page, select **Transfer**.
The **Transfer Workspace** page shows the workspace to be transferred on the left.
Select the target account for the workspace on the right.

**Workspace transfer impact on accounts**Workspace transfer may impact resource usage and costs for source and target accounts.When you transfer a workspace, users, API keys, and service accounts may lose access to the workspace.
The audit log will no longer track activity on the workspace.
Flow runs ending outside of the destination account’s flow run retention period will be removed.
You may also need to update Prefect CLI profiles and execution environment settings to access the workspace’s new location.You may incur new charges in the target account to accommodate the transferred workspace.

## [​](#delete-a-workspace) Delete a workspace

Deleting a workspace deletes all of its data including deployments, flow run history, work pools, and automations.
Click on the name of your workspace in the sidebar navigation and select **Workspace settings**.
From the three dot menu in the upper right of the page, select **Delete**.

Was this page helpful?

YesNo

[Secure access over PrivateLink](/v3/how-to-guides/cloud/manage-users/secure-access-by-private-link)[Create a Webhook](/v3/how-to-guides/cloud/create-a-webhook)

⌘I