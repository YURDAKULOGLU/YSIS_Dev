How to automatically rerun your workflow when it fails - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

How to automatically rerun your workflow when it fails

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

* [Set the number of retries](#set-the-number-of-retries)
* [Wait between retries](#wait-between-retries)
* [Retry parts of a workflow](#retry-parts-of-a-workflow)
* [Retry with configurable delay](#retry-with-configurable-delay)
* [Retry with a custom condition](#retry-with-a-custom-condition)
* [Add jitter to retry delays](#add-jitter-to-retry-delays)
* [Configure task retry behavior globally](#configure-task-retry-behavior-globally)

### [​](#set-the-number-of-retries) Set the number of retries

To rerun your workflow when an exception is raised, set the `retries` parameter to an integer.

Copy

```
from prefect import flow


@flow(retries=3)
def troublesome_workflow():
    raise Exception("oopsie daisy")
```

### [​](#wait-between-retries) Wait between retries

To add a wait between retries, pass a value to the `retry_delay_seconds` parameter.

Copy

```
from prefect import flow


@flow(retries=3, retry_delay_seconds=2.7182)
def troublesome_workflow():
    raise Exception("oopsie daisy")
```

### [​](#retry-parts-of-a-workflow) Retry parts of a workflow

You can configure retries for individual tasks in a workflow to limit the scope of a retry.

Copy

```
import random

import httpx
from prefect import flow, task


@task
def consistent_task() -> dict:
    print("I won't rerun even if the task after me fails")


@task(retries=4, retry_delay_seconds=5)
def mercurial_task() -> dict:
    # Will fail half of the time
    url = f"https://httpbin.org/status/{random.choice([200, 500])}"

    response = httpx.get(url)
    response.raise_for_status()
    

@flow
def my_workflow():
    consistent_task()
    mercurial_task()
```

### [​](#retry-with-configurable-delay) Retry with configurable delay

A task’s retry delays can also be defined as a list of integers for different delays between retries.

Copy

```
from prefect import task


@task(retries=4, retry_delay_seconds=[1, 2, 4, 8])
def melancholic_task():
    raise Exception("We used to see each other so much more often")
```

You can also use the `exponential_backoff` utility to generate a list of retry delays that correspond to an exponential backoff retry strategy.

Copy

```
from prefect import task
from prefect.tasks import exponential_backoff


@task(retries=4, retry_delay_seconds=exponential_backoff(backoff_factor=2))
def melancholic_task():
    raise Exception("We used to see each other so much more often")
```

### [​](#retry-with-a-custom-condition) Retry with a custom condition

Whether or not a task should be retried can be determined dynamically by passing a callable to the `retry_condition_fn` parameter.

Copy

```
import httpx
from prefect import flow, task


def retry_handler(task, task_run, state) -> bool:
    """
    Retry handler that skips retries if the HTTP status code is 401 or 404.
    """
    try:
        state.result()
    except httpx.HTTPStatusError as exc:
        do_not_retry_on_these_codes = [401, 404]
        return exc.response.status_code not in do_not_retry_on_these_codes
    except httpx.ConnectError:
        return False
    except:
        return True


@task(retries=1, retry_condition_fn=retry_handler)
def api_call_task(url):
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()


@flow
def my_workflow(url):
    api_call_task(url=url)
```

If a callable passed to `retry_condition_fn` returns `True`, the task will be retried. Otherwise, the task will exit with an exception.

### [​](#add-jitter-to-retry-delays) Add jitter to retry delays

To add a random amount of time to retry delays, pass a value to the `retry_jitter_factor` parameter.

Copy

```
import time

from prefect import task
from prefect.tasks import exponential_backoff

last_run_time = time.time()

@task(
    retries=3,
    retry_delay_seconds=exponential_backoff(backoff_factor=5),
    retry_jitter_factor=3,
)
def some_task_with_exponential_backoff_retries():
    global last_run_time
    print(f"Time between retries: {time.time() - last_run_time}")
    if time.time() - last_run_time < 10:
        last_run_time = time.time()
        raise Exception("I could fail some more")
    return "That's enough failure"
```

Adding jitter to the retry delays avoids multiple tasks introducing load to external systems by failing and retrying at the exact same cadence.

### [​](#configure-task-retry-behavior-globally) Configure task retry behavior globally

You can set the default retries and retry delays for all tasks via Prefect’s settings.
The default values can be overridden on a per-task basis via the `retries` and `retry_delay_seconds` parameters.

Copy

```
prefect config set PREFECT_TASK_DEFAULT_RETRIES=2
prefect config set PREFECT_TASK_DEFAULT_RETRY_DELAY_SECONDS="1,10,100"
```

Was this page helpful?

YesNo

[Use assets to track workflow outputs](/v3/how-to-guides/workflows/assets)[Manually retry a flow run](/v3/how-to-guides/workflows/retry-flow-runs)

⌘I