How to manage work pools - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflow Infrastructure

How to manage work pools

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

* [Using the CLI](#using-the-cli)
* [List available work pools](#list-available-work-pools)
* [Inspect a work pool](#inspect-a-work-pool)
* [Preview scheduled work](#preview-scheduled-work)
* [Pause a work pool](#pause-a-work-pool)
* [Resume a work pool](#resume-a-work-pool)
* [Delete a work pool](#delete-a-work-pool)
* [Manage concurrency for a work pool](#manage-concurrency-for-a-work-pool)
* [Base job template](#base-job-template)
* [Using Terraform](#using-terraform)
* [Using the REST API](#using-the-rest-api)
* [Further reading](#further-reading)

You can configure work pools by using the Prefect UI.
To manage work pools in the UI, click the **Work Pools** icon. This displays a list of currently configured work pools.
![The UI displays a list of configured work pools](https://mintcdn.com/prefect-bd373955/rT_XiX8cZI7Bzt5c/v3/img/ui/work-pool-list.png?fit=max&auto=format&n=rT_XiX8cZI7Bzt5c&q=85&s=16ad4508be0804e4a593a3091ce3182f)
Select the **+** button to create a new work pool. You can specify the details about infrastructure created for this work pool.

## [​](#using-the-cli) Using the CLI

You can manage work pools with the [Prefect CLI](https://docs.prefect.io/v3/api-ref/cli/work-pool).

Copy

```
prefect work-pool create [OPTIONS] NAME
```

`NAME` is a required, unique name for the work pool.
Optional configuration parameters to filter work on the pool include:

**Managing work pools in CI/CD**Version control your base job template by committing it as a JSON file to a git repository and control updates to your
work pools’ base job templates with the `prefect work-pool update` command in your CI/CD pipeline.For example, use the following command to update a work pool’s base job template to the contents of a file named `base-job-template.json`:

Copy

```
prefect work-pool update --base-job-template base-job-template.json my-work-pool
```

### [​](#list-available-work-pools) List available work pools

Copy

```
prefect work-pool ls
```

### [​](#inspect-a-work-pool) Inspect a work pool

Copy

```
prefect work-pool inspect 'test-pool'
```

### [​](#preview-scheduled-work) Preview scheduled work

Copy

```
prefect work-pool preview 'test-pool' --hours 12
```

### [​](#pause-a-work-pool) Pause a work pool

Copy

```
prefect work-pool pause 'test-pool'
```

### [​](#resume-a-work-pool) Resume a work pool

Copy

```
prefect work-pool resume 'test-pool'
```

### [​](#delete-a-work-pool) Delete a work pool

Copy

```
prefect work-pool delete 'test-pool'
```

**Pausing a work pool does not pause deployment schedules**

### [​](#manage-concurrency-for-a-work-pool) Manage concurrency for a work pool

Set concurrency:

Copy

```
prefect work-pool set-concurrency-limit [LIMIT] [POOL_NAME]
```

Clear concurrency:

Copy

```
prefect work-pool clear-concurrency-limit [POOL_NAME]
```

### [​](#base-job-template) Base job template

View default base job template:

Copy

```
prefect work-pool get-default-base-job-template --type process
```

Example `prefect.yaml`:

Copy

```
deployments:
- name: demo-deployment
  entrypoint: demo_project/demo_flow.py:some_work
  work_pool:
    name: above-ground  
    job_variables:
        stream_output: false
```

**Advanced customization of the base job template**For advanced use cases, create work pools with fully customizable job templates. This customization is available when
creating or editing a work pool on the ‘Advanced’ tab within the UI or when updating a work pool via the Prefect CLI.Advanced customization is useful anytime the underlying infrastructure supports a high degree of customization.
In these scenarios a work pool job template allows you to expose a minimal and easy-to-digest set of options to deployment authors.
Additionally, these options are the *only* customizable aspects for deployment infrastructure, which are useful for restricting
capabilities in secure environments. For example, the `kubernetes` worker type allows users to specify a custom job template  
to configure the manifest that workers use to create jobs for flow execution.See more information about [overriding a work pool’s job variables](/v3/deploy/infrastructure-concepts/customize).

## [​](#using-terraform) Using Terraform

You can manage work pools with the [Terraform provider for Prefect](https://registry.terraform.io/providers/PrefectHQ/prefect/latest/docs/resources/work_pool).

## [​](#using-the-rest-api) Using the REST API

You can manage work pools with the [Prefect API](https://app.prefect.cloud/api/docs#tag/Work-Pools).

## [​](#further-reading) Further reading

* [Work pools](/v3/concepts/work-pools) concept page
* [Customize job variables](/v3/deploy/infrastructure-concepts/customize) page

Was this page helpful?

YesNo

[Pass event payloads to flows](/v3/how-to-guides/automations/passing-event-payloads-to-flows)[Run Flows in Local Processes](/v3/how-to-guides/deployment_infra/run-flows-in-local-processes)

⌘I