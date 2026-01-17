How to apply global concurrency and rate limits - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

How to apply global concurrency and rate limits

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

* [Manage global concurrency and rate limits](#manage-global-concurrency-and-rate-limits)
* [Using the UI](#using-the-ui)
* [Using the CLI](#using-the-cli)
* [Using Terraform](#using-terraform)
* [Using the API](#using-the-api)
* [Use the concurrency context manager](#use-the-concurrency-context-manager)
* [Synchronous usage](#synchronous-usage)
* [Asynchronous usage](#asynchronous-usage)
* [Using strict mode](#using-strict-mode)
* [Use rate\_limit](#use-rate-limit)
* [Synchronous usage](#synchronous-usage-2)
* [Asynchronous usage](#asynchronous-usage-2)
* [Use outside of flows](#use-outside-of-flows)
* [Common patterns](#common-patterns)
* [Throttle task submission](#throttle-task-submission)
* [Limit database connections](#limit-database-connections)
* [Control parallel processing](#control-parallel-processing)
* [Next steps](#next-steps)

Use global concurrency limits to control how many operations run simultaneously, and rate limits to control how frequently operations can start. This guide shows you how to create, manage, and use these limits in your workflows.
For a deeper understanding of how global concurrency limits work and when to use them, see the [global concurrency limits concept page](/v3/concepts/global-concurrency-limits).

## [​](#manage-global-concurrency-and-rate-limits) Manage global concurrency and rate limits

You can create, read, edit, and delete concurrency limits through the Prefect UI, CLI, Python SDK, Terraform, or API.
When creating a concurrency limit, you can specify:

* **Name**: How you’ll reference the limit in your code (no special characters like `/`, `%`, `&`, `>`, `<`)
* **Concurrency Limit**: Maximum number of slots available
* **Slot Decay Per Second**: Rate at which slots are released (required for rate limiting)
* **Active**: Whether the limit is enforced (`true`) or disabled (`false`)

### [​](#using-the-ui) Using the UI

Navigate to the **Concurrency** section in the Prefect UI to create, update, and delete concurrency limits.
![Concurrency limits in the UI](https://mintcdn.com/prefect-bd373955/61rCXJ5a7pFAZAcb/images/gcl-1.png?fit=max&auto=format&n=61rCXJ5a7pFAZAcb&q=85&s=2730ce50c5061894115a300fe25c53d1)

### [​](#using-the-cli) Using the CLI

You can manage global concurrency with the [Prefect CLI](https://docs.prefect.io/v3/api-ref/cli/global-concurrency-limit).
Create a new concurrency limit with the `prefect gcl create` command:

Copy

```
prefect gcl create my-concurrency-limit --limit 5 --slot-decay-per-second 1.0
```

Inspect a concurrency limit:

Copy

```
prefect gcl inspect my-concurrency-limit
```

Update a concurrency limit:

Copy

```
prefect gcl update my-concurrency-limit --limit 10
prefect gcl update my-concurrency-limit --disable
```

Delete a concurrency limit:

Copy

```
prefect gcl delete my-concurrency-limit
Are you sure you want to delete global concurrency limit 'my-concurrency-limit'? [y/N]: y
Deleted global concurrency limit with name 'my-concurrency-limit'.
```

See all available commands and options with `prefect gcl --help`.

### [​](#using-terraform) Using Terraform

You can manage global concurrency with the [Terraform provider for Prefect](https://registry.terraform.io/providers/PrefectHQ/prefect/latest/docs/resources/global_concurrency_limit).

### [​](#using-the-api) Using the API

You can manage global concurrency with the [Prefect API](https://app.prefect.cloud/api/docs#tag/Concurrency-Limits-V2).

## [​](#use-the-concurrency-context-manager) Use the `concurrency` context manager

Control concurrent operations using the `concurrency` context manager. Choose the synchronous or asynchronous version based on your code.

By default, if a concurrency limit doesn’t exist or lease renewal fails, a warning is logged but execution continues.Use `strict=True` to raise an error instead. This ensures concurrency enforcement is guaranteed, useful for preventing resource exhaustion like database connection pool limits.

### [​](#synchronous-usage) Synchronous usage

Copy

```
from prefect import flow, task
from prefect.concurrency.sync import concurrency
from prefect.futures import wait


@task
def process_data(x, y):
    with concurrency("database", occupy=1):
        return x + y


@flow
def my_flow():
    futures = []
    for x, y in [(1, 2), (2, 3), (3, 4), (4, 5)]:
        futures.append(process_data.submit(x, y))

    wait(futures)


if __name__ == "__main__":
    my_flow()
```

### [​](#asynchronous-usage) Asynchronous usage

Copy

```
import asyncio
from prefect import flow, task
from prefect.concurrency.asyncio import concurrency
from prefect.futures import wait


@task
async def process_data(x, y):
    async with concurrency("database", occupy=1):
        return x + y


@flow
def my_flow():
    futures = []
    for x, y in [(1, 2), (2, 3), (3, 4), (4, 5)]:
        futures.append(process_data.submit(x, y))

    wait(futures)


if __name__ == "__main__":
    asyncio.run(my_flow())
```

In both examples, the `concurrency` context manager occupies one slot on the `database` concurrency limit. If no slots are available, execution blocks until a slot becomes available.

### [​](#using-strict-mode) Using strict mode

Enable strict mode to ensure errors are raised if the limit doesn’t exist or if lease renewal fails:

Copy

```
from prefect import flow, task
from prefect.concurrency.sync import concurrency

@task
def process_critical_data(x, y):
    # strict=True ensures this task fails fast if concurrency can't be enforced
    with concurrency("database", occupy=1, strict=True):
        return x + y

@flow
def critical_flow():
    process_critical_data(1, 2)
```

## [​](#use-rate-limit) Use `rate_limit`

Control the frequency of operations using the `rate_limit` function.

The concurrency limit must have `slot_decay_per_second` configured. Without it, `rate_limit` will fail.

### [​](#synchronous-usage-2) Synchronous usage

Copy

```
from prefect import flow, task
from prefect.concurrency.sync import rate_limit


@task
def make_http_request():
    rate_limit("rate-limited-api")
    print("Making an HTTP request...")


@flow
def my_flow():
    for _ in range(10):
        make_http_request.submit()


if __name__ == "__main__":
    my_flow()
```

### [​](#asynchronous-usage-2) Asynchronous usage

Copy

```
import asyncio

from prefect import flow, task
from prefect.concurrency.asyncio import rate_limit


@task
async def make_http_request():
    await rate_limit("rate-limited-api")
    print("Making an HTTP request...")


@flow
def my_flow():
    for _ in range(10):
        make_http_request.submit()


if __name__ == "__main__":
    asyncio.run(my_flow())
```

The `rate_limit` function ensures requests are made at a controlled pace based on the concurrency limit’s `slot_decay_per_second` setting.

## [​](#use-outside-of-flows) Use outside of flows

You can use `concurrency` and `rate_limit` in any Python code, not just within flows.

Copy

```
import asyncio

from prefect.concurrency.asyncio import rate_limit


async def main():
    for _ in range(10):
        await rate_limit("rate-limited-api")
        print("Making an HTTP request...")



if __name__ == "__main__":
    asyncio.run(main())
```

## [​](#common-patterns) Common patterns

### [​](#throttle-task-submission) Throttle task submission

Prevent overwhelming downstream systems by controlling how quickly tasks are submitted:

Copy

```
from prefect import flow, task
from prefect.concurrency.sync import rate_limit


@task
def my_task(i):
    return i


@flow
def my_flow():
    for _ in range(100):
        rate_limit("slow-my-flow", occupy=1)
        my_task.submit(1)


if __name__ == "__main__":
    my_flow()
```

### [​](#limit-database-connections) Limit database connections

Prevent exhausting your database connection pool by limiting concurrent queries:

Copy

```
from prefect import flow, task, concurrency
from myproject import db

@task
def database_query(query):
    # Here we request a single slot on the 'database' concurrency limit. This
    # will block in the case that all of the database connections are in use
    # ensuring that we never exceed the maximum number of database connections.
    with concurrency("database", occupy=1):
        result = db.execute(query)
        return result

@flow
def my_flow():
    queries = ["SELECT * FROM table1", "SELECT * FROM table2", "SELECT * FROM table3"]

    for query in queries:
        database_query.submit(query)

if __name__ == "__main__":
    my_flow()
```

### [​](#control-parallel-processing) Control parallel processing

Process data in controlled batches to avoid resource exhaustion:

Copy

```
import asyncio
from prefect.concurrency.sync import concurrency


async def process_data(data):
    print(f"Processing: {data}")
    await asyncio.sleep(1)
    return f"Processed: {data}"


async def main():
    data_items = list(range(100))
    processed_data = []

    while data_items:
        with concurrency("data-processing", occupy=5):
            chunk = [data_items.pop() for _ in range(5)]
            processed_data += await asyncio.gather(
                *[process_data(item) for item in chunk]
            )

    print(processed_data)


if __name__ == "__main__":
    asyncio.run(main())
```

## [​](#next-steps) Next steps

For more information about how global concurrency limits work and when to use them versus other concurrency controls, see the [global concurrency limits concept page](/v3/concepts/global-concurrency-limits).

Was this page helpful?

YesNo

[Test workflows](/v3/how-to-guides/workflows/test-workflows)[Limit concurrent task runs with tags](/v3/how-to-guides/workflows/tag-based-concurrency-limits)

⌘I