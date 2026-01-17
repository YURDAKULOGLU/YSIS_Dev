How to connect to Prefect Cloud - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Prefect Cloud

How to connect to Prefect Cloud

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

* [Log into Prefect Cloud from a terminal](#log-into-prefect-cloud-from-a-terminal)
* [Steps](#steps)
* [Change workspaces](#change-workspaces)
* [Manually configure Prefect API settings](#manually-configure-prefect-api-settings)
* [Install requirements in execution environments](#install-requirements-in-execution-environments)

To create flow runs in a local or remote execution environment, first connect with Prefect Cloud or a
Prefect server as the backend API server.
This involves:

* Configuring the execution environment with the location of the API.
* Authenticating with the API, either by logging in or providing a valid API key (Prefect Cloud only).

## [​](#log-into-prefect-cloud-from-a-terminal) Log into Prefect Cloud from a terminal

Configure a local execution environment to use Prefect Cloud as the API server for flow runs.
You will log in a to Prefect Cloud account from the local environment where you want to run a flow.

### [​](#steps) Steps

1. Open a new terminal session.
2. [Install Prefect](/v3/get-started/install) in the environment where you want to execute flow runs.

Copy

```
pip install -U prefect
```

3. Use the `prefect cloud login` Prefect CLI command to log into Prefect Cloud from your environment.

Copy

```
prefect cloud login
```

The `prefect cloud login` command provides an interactive login experience.

Copy

```
prefect cloud login
```

Copy

```
? How would you like to authenticate? [Use arrows to move; enter to select]
> Log in with a web browser
    Paste an API key
Paste your authentication key:
? Which workspace would you like to use? [Use arrows to move; enter to select]
> prefect/terry-prefect-workspace
    g-gadflow/g-workspace
Authenticated with Prefect Cloud! Using workspace 'prefect/terry-prefect-workspace'.
```

You can authenticate by manually pasting an [API key](/v3/how-to-guides/cloud/manage-users/api-keys) or through a browser-based approval that auto-generates an API key with a 30-day expiration.

### [​](#change-workspaces) Change workspaces

To change which workspace to sync with, use the `prefect cloud workspace set`
Prefect CLI command while logged in, passing the account handle and workspace name:

Copy

```
prefect cloud workspace set --workspace "prefect/my-workspace"
```

If you don’t provide a workspace, you will need to select one.
**Workspace Settings** also shows you the `prefect cloud workspace set` Prefect CLI
command to sync a local execution environment with a given workspace.
You may also use the `prefect cloud login` command with the `--workspace` or `-w` option to set the current workspace.

Copy

```
prefect cloud login --workspace "prefect/my-workspace"
```

## [​](#manually-configure-prefect-api-settings) Manually configure Prefect API settings

You can manually configure the `PREFECT_API_URL` setting to specify the Prefect Cloud API.
For Prefect Cloud, configure the `PREFECT_API_URL` and `PREFECT_API_KEY` settings to authenticate
with Prefect Cloud by using an account ID, workspace ID, and API key.

Copy

```
prefect config set PREFECT_API_URL="https://api.prefect.cloud/api/accounts/[ACCOUNT-ID]/workspaces/[WORKSPACE-ID]"
prefect config set PREFECT_API_KEY="[API-KEY]"
```

**Find account ID and workspace ID in the browser**When authenticated to your Prefect Cloud workspace in the browser, you can get the account ID and workspace ID for the `PREFECT_API_URL` string from the page URL.For example, if you’re on the dashboard page, the URL looks like this:[https://app.prefect.cloud/account/[ACCOUNT-ID]/workspace/[WORKSPACE-ID]/dashboard](https://app.prefect.cloud/account/%5BACCOUNT-ID%5D/workspace/%5BWORKSPACE-ID%5D/dashboard)

The example above configures `PREFECT_API_URL` and `PREFECT_API_KEY` in the default profile.
You can use `prefect profile` CLI commands to create settings profiles for different configurations.
For example, you can configure a “cloud” profile to use the Prefect Cloud API URL and API key;
and another “local” profile for local development using a local Prefect API server started with `prefect server start`.
See [Settings](/v3/develop/settings-and-profiles) for details.

**Environment variables**You can set `PREFECT_API_URL` and `PREFECT_API_KEY` just like any other environment variable.
Setting these environment variables is a good way to connect to Prefect Cloud in a remote serverless environment.
See [Overriding defaults with environment variables](/v3/develop/settings-and-profiles) for more information.

## [​](#install-requirements-in-execution-environments) Install requirements in execution environments

In local and remote execution environments, such as VMs and containers, ensure that you’ve installed any flow
requirements or dependencies before creating a flow run.

Was this page helpful?

YesNo

[Run flows on Coiled](/v3/how-to-guides/deployment_infra/coiled)[Manage user accounts](/v3/how-to-guides/cloud/manage-users)

⌘I