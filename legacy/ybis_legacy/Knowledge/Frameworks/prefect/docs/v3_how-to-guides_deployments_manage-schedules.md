Manage Deployment schedules - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Deployments

Manage Deployment schedules

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

* [Prerequisites](#prerequisites)
* [Manage specific schedules](#manage-specific-schedules)
* [List schedules for a deployment](#list-schedules-for-a-deployment)
* [Pause a specific schedule](#pause-a-specific-schedule)
* [Resume a specific schedule](#resume-a-specific-schedule)
* [Manage schedules in bulk](#manage-schedules-in-bulk)
* [Pause all schedules](#pause-all-schedules)
* [Resume all schedules](#resume-all-schedules)
* [Skip confirmation prompt](#skip-confirmation-prompt)
* [Use cases](#use-cases)
* [Maintenance windows](#maintenance-windows)
* [Development environment management](#development-environment-management)
* [Important notes](#important-notes)
* [See also](#see-also)

You can pause and resume deployment schedules individually or in bulk.
This can be useful for maintenance windows, migration scenarios, or organizational changes.

## [​](#prerequisites) Prerequisites

To manage deployment schedules, you need:

* A Prefect server or [Prefect Cloud](/v3/get-started/quickstart) workspace
* One or more [deployments](/v3/how-to-guides/deployments/create-deployments) with [schedules](/v3/how-to-guides/deployments/create-schedules)
* [Prefect installed](/v3/get-started/install)

## [​](#manage-specific-schedules) Manage specific schedules

To pause or resume individual deployment schedules, you need the deployment name and schedule ID.

### [​](#list-schedules-for-a-deployment) List schedules for a deployment

First, list the schedules to get the schedule ID:

Copy

```
prefect deployment schedule ls my-flow/my-deployment
```

### [​](#pause-a-specific-schedule) Pause a specific schedule

Copy

```
prefect deployment schedule pause my-flow/my-deployment <schedule-id>
```

### [​](#resume-a-specific-schedule) Resume a specific schedule

Copy

```
prefect deployment schedule resume my-flow/my-deployment <schedule-id>
```

## [​](#manage-schedules-in-bulk) Manage schedules in bulk

When you have many deployments with active schedules, you can pause or resume all of them at once using the `--all` flag.

### [​](#pause-all-schedules) Pause all schedules

Use the `--all` flag with the `pause` command to pause all active schedules across all deployments:

Copy

```
prefect deployment schedule pause --all
```

This command pauses all active schedules across deployments in the current workspace. In interactive mode, you’ll be asked to confirm.
Example output:

Copy

```
Paused schedule for deployment my-flow/daily-sync
Paused schedule for deployment data-pipeline/hourly-update
Paused schedule for deployment ml-model/weekly-training
Paused 3 deployment schedule(s).
```

### [​](#resume-all-schedules) Resume all schedules

Similarly, use the `--all` flag with the `resume` command to resume all paused schedules:

Copy

```
prefect deployment schedule resume --all
```

This command resumes all paused schedules across deployments in the current workspace. In interactive mode, you’ll be asked to confirm.
Example output:

Copy

```
Resumed schedule for deployment my-flow/daily-sync
Resumed schedule for deployment data-pipeline/hourly-update
Resumed schedule for deployment ml-model/weekly-training
Resumed 3 deployment schedule(s).
```

### [​](#skip-confirmation-prompt) Skip confirmation prompt

To skip the interactive confirmation (useful for CI/CD pipelines or scripts), use the `--no-prompt` flag:

Copy

```
prefect --no-prompt deployment schedule pause --all
prefect --no-prompt deployment schedule resume --all
```

## [​](#use-cases) Use cases

### [​](#maintenance-windows) Maintenance windows

Pause all schedules during system maintenance:

Copy

```
# Before maintenance
prefect deployment schedule pause --all

# Perform maintenance tasks...

# After maintenance
prefect deployment schedule resume --all
```

### [​](#development-environment-management) Development environment management

Quickly pause all schedules in a development environment:

Copy

```
# Pause all dev schedules
prefect --profile dev deployment schedule pause --all

# Resume when ready
prefect --profile dev deployment schedule resume --all
```

## [​](#important-notes) Important notes

**Use caution with bulk operations**The `--all` flag affects all deployment schedules in your workspace.
In interactive mode, you’ll be prompted to confirm the operation showing the exact number of schedules that will be affected.
Always verify you’re in the correct workspace/profile before running bulk operations.

## [​](#see-also) See also

* [Create schedules](/v3/how-to-guides/deployments/create-schedules) - Learn how to create schedules for your deployments
* [Run deployments](/v3/how-to-guides/deployments/run-deployments) - Learn how to trigger deployment runs manually
* [Deployment concepts](/v3/concepts/deployments) - Understand deployments and their schedules

Was this page helpful?

YesNo

[Create Deployment Schedules](/v3/how-to-guides/deployments/create-schedules)[Deploy via Python](/v3/how-to-guides/deployments/deploy-via-python)

⌘I