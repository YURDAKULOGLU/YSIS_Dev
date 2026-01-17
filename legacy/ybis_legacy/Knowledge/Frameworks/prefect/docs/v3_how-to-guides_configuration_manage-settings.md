How to manage settings - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Configuration

How to manage settings

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

* [View current configuration](#view-current-configuration)
* [Configure settings for the active profile](#configure-settings-for-the-active-profile)
* [Create a new profile](#create-a-new-profile)
* [Configure settings for a project](#configure-settings-for-a-project)
* [Configure temporary settings for a process](#configure-temporary-settings-for-a-process)

### [​](#view-current-configuration) View current configuration

To view all available settings and their active values from the command line, run:

Copy

```
prefect config view --show-defaults
```

These settings are type-validated and you may verify your setup at any time with:

Copy

```
prefect config validate
```

### [​](#configure-settings-for-the-active-profile) Configure settings for the active profile

To update a setting for the active profile, run:

Copy

```
prefect config set <setting>=<value>
```

For example, to set the `PREFECT_API_URL` setting to `http://127.0.0.1:4200/api`, run:

Copy

```
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

To restore the default value for a setting, run:

Copy

```
prefect config unset <setting>
```

For example, to restore the default value for the `PREFECT_API_URL` setting, run:

Copy

```
prefect config unset PREFECT_API_URL
```

### [​](#create-a-new-profile) Create a new profile

To create a new profile, run:

Copy

```
prefect profile create <profile>
```

To switch to a new profile, run:

Copy

```
prefect profile use <profile>
```

### [​](#configure-settings-for-a-project) Configure settings for a project

To configure settings for a project, create a `prefect.toml` or `.env` file in the project directory and add the settings with the values you want to use.
For example, to configure the `PREFECT_API_URL` setting to `http://127.0.0.1:4200/api`, create a `.env` file with the following content:

Copy

```
PREFECT_API_URL=http://127.0.0.1:4200/api
```

To configure the `PREFECT_API_URL` setting to `http://127.0.0.1:4200/api` in a `prefect.toml` file, create a `prefect.toml` file with the following content:

Copy

```
api.url = "http://127.0.0.1:4200/api"
```

Refer to the [setting concept guide](/v3/concepts/settings-and-profiles) for more information on how to configure settings and the [settings reference guide](/v3/api-ref/settings-ref) for more information on the available settings.

### [​](#configure-temporary-settings-for-a-process) Configure temporary settings for a process

To configure temporary settings for a process, set an environment variable with the name matching the setting you want to configure.
For example, to configure the `PREFECT_API_URL` setting to `http://127.0.0.1:4200/api` for a process, set the `PREFECT_API_URL` environment variable to `http://127.0.0.1:4200/api`.

Copy

```
export PREFECT_API_URL=http://127.0.0.1:4200/api
```

You can use this to run a command with the temporary setting:

Copy

```
PREFECT_LOGGING_LEVEL=DEBUG python my_script.py
```

Was this page helpful?

YesNo

[Share configuration between workflows](/v3/how-to-guides/configuration/variables)[Create Automations](/v3/how-to-guides/automations/creating-automations)

⌘I