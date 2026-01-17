How to limit concurrent task runs with tags - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

How to limit concurrent task runs with tags

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

* [Set concurrency limits on tags](#set-concurrency-limits-on-tags)
* [Apply multiple tags to a task](#apply-multiple-tags-to-a-task)
* [Configure concurrency limits](#configure-concurrency-limits)
* [CLI](#cli)
* [Python client](#python-client)
* [API](#api)
* [Terraform](#terraform)
* [Configure globally](#configure-globally)

Use task tags to limit how many tasks can run at the same time. This is useful when tasks interact with shared resources like databases or external APIs.

Copy

```
from prefect import flow, task

@task(tags=["database"])
def fetch_data():
    # This task will respect the "database" tag's concurrency limit
    return "data"

@flow
def my_workflow():
    fetch_data()
```

For more details on how tag-based concurrency limits work, see the [tag-based concurrency limits concept page](/v3/concepts/tag-based-concurrency-limits).

As of Prefect 3.4.19, tag-based concurrency limits are backed by [global concurrency limits](/v3/concepts/global-concurrency-limits). When you create a tag-based limit, you’ll see a corresponding global concurrency limit with the name `tag:{tag_name}`.

## [​](#set-concurrency-limits-on-tags) Set concurrency limits on tags

Tags without concurrency limits allow unlimited concurrent runs. Once you set a limit, only that many tasks with the tag can run simultaneously.

Copy

```
from prefect import flow, task

@task(tags=["database"])
def query_database(query: str):
    # Simulate database work
    return f"Results for {query}"

@flow
def data_pipeline():
    # These will respect the "database" tag limit
    query_database("SELECT * FROM users")
    query_database("SELECT * FROM orders")
    query_database("SELECT * FROM products")
```

## [​](#apply-multiple-tags-to-a-task) Apply multiple tags to a task

When a task has multiple tags, it must have available concurrency slots for **all** tags to run.

Copy

```
from prefect import task

@task(tags=["database", "analytics"])
def complex_query():
    # This task needs available slots in both "database" AND "analytics" limits
    return "complex results"
```

## [​](#configure-concurrency-limits) Configure concurrency limits

You can configure limits using the CLI, Python client, API, Terraform, or the Prefect UI.

### [​](#cli) CLI

Copy

```
# Set a limit of 10 for the "database" tag
prefect concurrency-limit create database 10

# View all concurrency limits
prefect concurrency-limit ls

# View details about a specific tag's limit
prefect concurrency-limit inspect database

# Delete a concurrency limit
prefect concurrency-limit delete database
```

### [​](#python-client) Python client

Copy

```
from prefect import get_client

async with get_client() as client:
    # Set a concurrency limit of 10 on the "database" tag
    await client.create_concurrency_limit(
        tag="database",
        concurrency_limit=10
    )

    # Read current limit for a tag
    limit = await client.read_concurrency_limit_by_tag(tag="database")

    # Delete a concurrency limit
    await client.delete_concurrency_limit_by_tag(tag="database")

    # View all concurrency limits
    limits = await client.read_concurrency_limits()
```

### [​](#api) API

Copy

```
# Create a concurrency limit
curl -X POST "http://localhost:4200/api/concurrency_limits/" \
  -H "Content-Type: application/json" \
  -d '{"tag": "database", "concurrency_limit": 10}'

# Get all concurrency limits
curl "http://localhost:4200/api/concurrency_limits/"
```

### [​](#terraform) Terraform

Copy

```
resource "prefect_concurrency_limit" "database_limit" {
  tag               = "database"
  concurrency_limit = 10
}
```

## [​](#configure-globally) Configure globally

When a task is delayed due to a concurrency limit, it will wait for a set wait time before retrying. You can set the wait time for when tasks are delayed due to concurrency limits:

Copy

```
prefect config set PREFECT_TASK_RUN_TAG_CONCURRENCY_SLOT_WAIT_SECONDS=60
```

Note: this setting needs to be set on the Prefect server, not the Prefect client.

Was this page helpful?

YesNo

[Apply global concurrency and rate limits](/v3/how-to-guides/workflows/global-concurrency-limits)[Create Deployments](/v3/how-to-guides/deployments/create-deployments)

⌘I