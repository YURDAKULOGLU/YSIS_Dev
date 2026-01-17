How to create deployments - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Deployments

How to create deployments

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

* [Create deployments with static infrastructure](#create-deployments-with-static-infrastructure)
* [Create a deployment with serve](#create-a-deployment-with-serve)
* [Create deployments with dynamic infrastructure](#create-deployments-with-dynamic-infrastructure)
* [Create a deployment with deploy](#create-a-deployment-with-deploy)
* [Create a deployment with a YAML file](#create-a-deployment-with-a-yaml-file)
* [Create a deployment with Terraform](#create-a-deployment-with-terraform)
* [Create a deployment with the API](#create-a-deployment-with-the-api)

There are several ways to create deployments, each catering to different organizational needs.

## [​](#create-deployments-with-static-infrastructure) Create deployments with static infrastructure

### [​](#create-a-deployment-with-serve) Create a deployment with `serve`

This is the simplest way to get started with deployments:

Copy

```
from prefect import flow


@flow
def my_flow():
    print("Hello, Prefect!")


if __name__ == "__main__":
    my_flow.serve(name="my-first-deployment", cron="* * * * *")
```

The `serve` method creates a deployment from your flow and immediately begins listening for scheduled runs to execute.
Providing `cron="* * * * *"` to `.serve` associates a schedule with your flow so it will run every minute of every day.

## [​](#create-deployments-with-dynamic-infrastructure) Create deployments with dynamic infrastructure

For more configuration, you can create a deployment that uses a work pool.
Reasons to create a work-pool based deployment include:

* Wanting to run your flow on dynamically provisioned infrastructure
* Needing more control over the execution environment on a per-flow run basis
* Creating an infrastructure template to use across deployments

Work pools are popular with data platform teams because they allow you to manage infrastructure configuration across an organization.
Prefect offers two options for creating deployments with [dynamic infrastructure](/v3/deploy/infrastructure-concepts/work-pools):

* [Deployments created with the Python SDK](/v3/deploy/infrastructure-concepts/deploy-via-python)
* [Deployments created with a YAML file](/v3/deploy/infrastructure-concepts/prefect-yaml)

### [​](#create-a-deployment-with-deploy) Create a deployment with `deploy`

To define a deployment with a Python script, use the `flow.deploy` method.
Here’s an example of a deployment that uses a work pool and bakes the code into a Docker image.

Copy

```
from prefect import flow


@flow
def my_flow():
    print("Hello, Prefect!")

if __name__ == "__main__":
    my_flow.deploy(
        name="my-second-deployment",
        work_pool_name="my-work-pool",
        image="my-image",
        push=False,
        cron="* * * * *",
    )
```

To learn more about the `deploy` method, see [Deploy flows with Python](/v3/deploy/infrastructure-concepts/deploy-via-python).

### [​](#create-a-deployment-with-a-yaml-file) Create a deployment with a YAML file

If you’d rather take a declarative approach to defining a deployment through a YAML file, use a [`prefect.yaml` file](/v3/deploy/infrastructure-concepts/prefect-yaml).
Prefect provides an interactive CLI that walks you through creating a `prefect.yaml` file:

Copy

```
prefect deploy
```

The result is a `prefect.yaml` file for deployment creation.
The file contains `build`, `push`, and `pull` steps for building a Docker image, pushing code to a Docker registry, and pulling code at runtime.
Learn more about creating deployments with a YAML file in [Define deployments with YAML](/v3/deploy/infrastructure-concepts/prefect-yaml).
Prefect also provides [CI/CD options](/v3/deploy/infrastructure-concepts/deploy-ci-cd) for automatically creating YAML-based deployments.

### [​](#create-a-deployment-with-terraform) Create a deployment with Terraform

You can manage deployments with the [Terraform provider for Prefect](https://registry.terraform.io/providers/PrefectHQ/prefect/latest/docs/resources/deployment).

### [​](#create-a-deployment-with-the-api) Create a deployment with the API

You can manage deployments with the [Prefect API](https://app.prefect.cloud/api/docs#tag/Deployments).

**Choosing between deployment methods**For many cases, `serve` is sufficient for scheduling and orchestration.
The work pool / worker paradigm via `.deploy()` or `prefect deploy` can be great for complex infrastructure requirements and isolated flow run environments.
You are not locked into one method and can combine approaches as needed.

Was this page helpful?

YesNo

[Limit concurrent task runs with tags](/v3/how-to-guides/workflows/tag-based-concurrency-limits)[Trigger ad-hoc deployment runs](/v3/how-to-guides/deployments/run-deployments)

⌘I