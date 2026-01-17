How to cache workflow step outputs - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

How to cache workflow step outputs

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

* [Cache based on inputs](#cache-based-on-inputs)
* [Cache based on a subset of inputs](#cache-based-on-a-subset-of-inputs)
* [Cache with an expiration](#cache-with-an-expiration)
* [Ignore the cache](#ignore-the-cache)
* [Cache on multiple criteria](#cache-on-multiple-criteria)
* [Cache in a distributed environment](#cache-in-a-distributed-environment)
* [Further reading](#further-reading)

The simplest way to cache the results of tasks within in a flow is to set `persist_result=True` on a task definition.

Copy

```
from prefect import task, flow

@task(persist_result=True)
def add_one(x: int):
    return x + 1

@flow
def my_flow():
    add_one(1) # will not be cached
    add_one(1) # will be cached
    add_one(2) # will not be cached

if __name__ == "__main__":
    my_flow()
```

Output

Copy

```
16:28:51.230 | INFO    | Flow run 'outgoing-cicada' - Beginning flow run 'outgoing-cicada' for flow 'my-flow'
16:28:51.257 | INFO    | Task run 'add_one-d85' - Finished in state Completed()
16:28:51.276 | INFO    | Task run 'add_one-eff' - Finished in state Cached(type=COMPLETED)
16:28:51.294 | INFO    | Task run 'add_one-d16' - Finished in state Completed()
16:28:51.311 | INFO    | Flow run 'outgoing-cicada' - Finished in state Completed()
```

This will implicitly use the `DEFAULT` cache policy, which is a composite cache policy defined as:

Copy

```
DEFAULT = INPUTS + TASK_SOURCE + RUN_ID
```

This means subsequent calls of a task with identical inputs from within the same parent run will return cached results without executing the body of the function.

The `TASK_SOURCE` component of the `DEFAULT` cache policy helps avoid naming collisions between similar tasks that should not share a cache.

### [​](#cache-based-on-inputs) Cache based on inputs

To cache the result of a task based only on task inputs, set `cache_policy=INPUTS` in the task decorator:

Copy

```
from prefect import task
from prefect.cache_policies import INPUTS

import time


@task(cache_policy=INPUTS)
def my_stateful_task(x: int):
    print('sleeping')
    time.sleep(10)
    return x + 1

my_stateful_task(x=1) # sleeps
my_stateful_task(x=1) # does not sleep
my_stateful_task(x=2) # sleeps
```

The above task will sleep the first time it is called with `x=1`, but will not sleep for any subsequent calls with the same input.
Prefect ships with several [cache policies](/v3/concepts/caching#cache-policies) that can be used to customize caching behavior.

### [​](#cache-based-on-a-subset-of-inputs) Cache based on a subset of inputs

To cache based on a subset of inputs, you can subtract kwargs from the `INPUTS` cache policy.

Copy

```
from prefect import task
from prefect.cache_policies import INPUTS

import time


@task(cache_policy=INPUTS - 'debug')
def my_stateful_task(x: int, debug: bool = False):
    print('sleeping')
    time.sleep(10)
    return x + 1

my_stateful_task(x=1) # sleeps
my_stateful_task(x=1, debug=True) # does not sleep
my_stateful_task(x=1, debug=False) # does not sleep
```

### [​](#cache-with-an-expiration) Cache with an expiration

To cache with an expiration, set the `cache_expiration` parameter on the task decorator.

Copy

```
from prefect import task
from prefect.cache_policies import INPUTS

import time
from datetime import timedelta


@task(cache_policy=INPUTS, cache_expiration=timedelta(seconds=10))
def my_stateful_task(x: int):
    print('sleeping')
    time.sleep(10)
    return x + 1

my_stateful_task(x=1) # sleeps
my_stateful_task(x=1) # does not sleep
# ... 10 seconds pass ...
my_stateful_task(x=1) # sleeps again
```

### [​](#ignore-the-cache) Ignore the cache

To ignore the cache regardless of the cache policy, set the `refresh_cache` parameter on the task decorator.

Copy

```
import random

from prefect import task
from prefect.cache_policies import TASK_SOURCE


@task(cache_policy=TASK_SOURCE, refresh_cache=True)
def never_caching_task():
    return random.random()
```

To refresh the cache for all tasks, use the `PREFECT_TASKS_REFRESH_CACHE` setting.
Setting `PREFECT_TASKS_REFRESH_CACHE=true` changes the default behavior of all tasks to refresh.
If you have tasks that should not refresh when this setting is enabled, set `refresh_cache` to `False`. These tasks will never write to the cache. If a cache key exists it will be read, not updated.
If a cache key does *not* exist yet, these tasks can still write to the cache.

Copy

```
import random

from prefect import task
from prefect.cache_policies import TASK_SOURCE


@task(cache_policy=TASK_SOURCE, refresh_cache=False)
def caching_task():
    return random.random()
```

### [​](#cache-on-multiple-criteria) Cache on multiple criteria

Cache policies can be combined using the `+` operator.

Copy

```
from prefect import task
from prefect.cache_policies import INPUTS, TASK_SOURCE

@task(cache_policy=INPUTS + TASK_SOURCE)
def my_task(x: int):
    return x + 1
```

The above task will use a cached result as long as the same inputs and task source are used.

### [​](#cache-in-a-distributed-environment) Cache in a distributed environment

By default Prefect stores results locally in `~/.prefect/storage/`. To share the cache across tasks running on different machines, provide a storage block to the `result_storage` parameter on the task decorator.
Here’s an example with of a task that uses an S3 bucket to store cache records:

Copy

```
from prefect import task
from prefect.cache_policies import INPUTS

from prefect_aws import AwsCredentials, S3Bucket

s3_bucket = S3Bucket(
    credentials=AwsCredentials(
        aws_access_key_id="my-access-key-id",
        aws_secret_access_key="my-secret-access-key",
    ),
    bucket_name="my-bucket",
)
# save the block to ensure it is available across machines
s3_bucket.save("my-cache-bucket")

@task(cache_policy=INPUTS, result_storage=s3_bucket)
def my_cached_task(x: int):
    return x + 42
```

When using a storage block from a Prefect integration package, the package the storage block is imported from must be installed in all environments where the task will run.For example, the `prefect_aws` package must be installed to use the `S3Bucket` storage block.

### [​](#further-reading) Further reading

For more advanced caching examples, see the [advanced caching how-to guide](/v3/advanced/caching).
For more information on Prefect’s caching system, see the [caching concepts page](/v3/concepts/caching).

Was this page helpful?

YesNo

[Run work concurrently](/v3/how-to-guides/workflows/run-work-concurrently)[Run background tasks](/v3/how-to-guides/workflows/run-background-tasks)

⌘I