How to upgrade to Prefect 3.0 - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Migrate

How to upgrade to Prefect 3.0

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

* [Quickstart](#quickstart)
* [Upgrade notes](#upgrade-notes)
* [Pydantic V2](#pydantic-v2)
* [Module location and name changes](#module-location-and-name-changes)
* [Async tasks in synchronous flows](#async-tasks-in-synchronous-flows)
* [Flow final states](#flow-final-states)
* [Examples](#examples)
* [Futures interface](#futures-interface)
* [Automatic task caching](#automatic-task-caching)
* [Unmapped mutable objects in mapped tasks](#unmapped-mutable-objects-in-mapped-tasks)
* [Workers](#workers)
* [Resolving common gotchas](#resolving-common-gotchas)
* [AttributeError: 'coroutine' object has no attribute <some attribute>](#attributeerror%3A-coroutine-object-has-no-attribute-%3Csome-attribute%3E)
* [TypeError: object <some Type> can't be used in 'await' expression](#typeerror%3A-object-%3Csome-type%3E-cant-be-used-in-await-expression)
* [TypeError: Flow.deploy() got an unexpected keyword argument 'schedule'](#typeerror%3A-flow-deploy-got-an-unexpected-keyword-argument-schedule)

Prefect 3.0 introduces a number of enhancements to the OSS product: a new events & automations backend for event-driven workflows and observability, improved runtime performance, autonomous task execution and a streamlined caching layer based on transactional semantics.
The majority of these enhancements maintain compatibility with most Prefect 2.0 workflows, but there are a few caveats that you may need to adjust for.
To learn more about the enhanced performance and new features, see [What’s new in Prefect 3.0](/v3/get-started/whats-new-prefect-3).
For the majority of users, upgrading to Prefect 3.0 will be a seamless process that requires few or no code changes.
This guide highlights key changes that you may need to consider when upgrading.

**Prefect 2.0** refers to the 2.x lineage of the open source prefect package, and **Prefect 3.0** refers exclusively to the 3.x lineage of the prefect package. Neither version is strictly tied to any aspect of Prefect’s commercial product, [Prefect Cloud](/v3/how-to-guides/cloud/connect-to-cloud).

## [​](#quickstart) Quickstart

To upgrade to Prefect 3.0, run:

Copy

```
pip install -U prefect
```

If you self-host a Prefect server, run this command to update your database:

Copy

```
prefect server database upgrade
```

If you use a Prefect integration or extra, remember to upgrade it as well. For example:

Copy

```
pip install -U 'prefect[aws]'
```

## [​](#upgrade-notes) Upgrade notes

### [​](#pydantic-v2) Pydantic V2

Prefect 3.0 is built with Pydantic 2.0 for improved performance. All Prefect objects will automatically upgrade, but if you use custom Pydantic models for flow parameters or custom blocks, you’ll need to ensure they are compatible with Pydantic 2.0. You can continue to use Pydantic 1.0 models in your own code if they do not interact directly with Prefect.
Refer to [Pydantic’s migration guide](https://docs.pydantic.dev/latest/migration/) for detailed information on necessary changes.

We recommend pausing all deployment schedules prior to upgrading.
Because of differences in Pydantic datetime handling that affect the scheduler’s idempotency logic, there is a small risk of the scheduler duplicating runs in its first loop.

### [​](#module-location-and-name-changes) Module location and name changes

Some less-commonly used modules have been renamed, reorganized, or removed for clarity. The old import paths will continue to be supported for 6 months, but emit deprecation warnings. You can look at the [deprecation code](https://github.com/PrefectHQ/prefect/blob/main/src/prefect/_internal/compatibility/migration.py) to see a full list of affected paths.

### [​](#async-tasks-in-synchronous-flows) Async tasks in synchronous flows

In Prefect 2.0, it was possible to call native `async` tasks from synchronous flows, a pattern that is not normally supported in Python. Prefect 3.0.0 removes this behavior to reduce complexity and potential issues and edge cases. If you relied on asynchronous tasks in synchronous flows, you must either make your flow asynchronous or use a task runner that supports asynchronous execution.

### [​](#flow-final-states) Flow final states

In Prefect 2.0, the final state of a flow run was influenced by the states of its task runs; if any task run failed, the flow run was marked as failed.
In Prefect 3.0, the final state of a flow run is entirely determined by:

1. The `return` value of the flow function (same as in Prefect 2.0):
   * Literal values are considered successful.
   * Any explicit `State` that is returned will be considered the final state of the flow run. If an iterable of `State` objects is returned, all must be `Completed` for the flow run to be considered `Completed`. If any are `Failed`, the flow run will be marked as `Failed`.
2. Whether the flow function allows an exception to `raise`:
   * Exceptions that are allowed to propagate will result in a `Failed` state.
   * Exceptions suppressed with `raise_on_failure=False` will not affect the flow run state.

This change means that task failures within a flow do not automatically cause the flow run to fail unless they affect the flow’s return value or raise an uncaught exception.

When migrating from Prefect 2.0 to Prefect 3, be aware that flows may now complete successfully even if they contain failed tasks, unless you explicitly handle task failures.

To ensure your flow fails when critical tasks fail, consider these approaches:

1. Allow task exceptions to propagate by not using `raise_on_failure=False`.
2. Use `return_state=True` and explicitly check task states to conditionally `raise` the underlying exception or return a failed state.
3. Use try/except blocks to handle task failures and return appropriate states.

#### [​](#examples) Examples

Allow Unhandled Exceptions

Use return\_state

Use try/except

Copy

```
from prefect import flow, task

@task
def failing_task():
    raise ValueError("Task failed")

@flow
def my_flow():
    failing_task()  # Exception propagates, causing flow failure

try:
    my_flow()
except ValueError as e:
    print(f"Flow failed: {e}")  # Output: Flow failed: Task failed
```

Choose the strategy that best fits your specific use case and error handling requirements.


---

### [​](#futures-interface) Futures interface

PrefectFutures now have a standard synchronous interface, with an asynchronous one [planned soon](https://github.com/PrefectHQ/prefect/issues/15008).

### [​](#automatic-task-caching) Automatic task caching

Prefect 3.0 introduces a powerful idempotency engine. By default, tasks in a flow run are automatically cached if they are called more than once with the same inputs. If you rely on tasks with side effects, this may result in surprising behavior. To disable caching, pass `cache_policy=None` to your task.

### [​](#unmapped-mutable-objects-in-mapped-tasks) Unmapped mutable objects in mapped tasks

In Prefect 2.0, when passing a mutable object (such as a list or dict) using `unmapped()` to a mapped task, each task instance appeared to receive an independent copy of the object. In Prefect 3.0, the unmapped object is shared by reference across all mapped task runs. If any task mutates the object, all other concurrently running tasks will see those mutations, potentially causing race conditions and unexpected behavior.

When migrating from Prefect 2.0 to Prefect 3, be aware that mutable objects passed via `unmapped()` are now shared across all mapped tasks. Mutating these objects can lead to race conditions.

To avoid this issue, create a copy of the mutable object within each task before modifying it:

Problematic (Prefect 3.0)

Recommended (Prefect 3.0)

Alternative: Pass immutable values

Copy

```
from prefect import flow, task, unmapped

@task
def process_item(item: str, shared_state: dict):
    # This mutation affects ALL tasks!
    shared_state["current_item"] = item
    # Race condition: another task may overwrite this before we read it
    print(f"Processing {shared_state['current_item']}")

@flow
def my_flow():
    shared_state = {"current_item": None}

    # All tasks share the same dict reference
    process_item.map(
        item=["A", "B", "C"],
        shared_state=unmapped(shared_state)
    )
```

If you need to share read-only configuration or settings across tasks, consider using immutable types (strings, tuples, frozen dataclasses) instead of mutable objects.

### [​](#workers) Workers

In Prefect 2.0, agents were deprecated in favor of next-generation workers. Workers are now standard in Prefect 3. For detailed information on upgrading from agents to workers, please refer to our [upgrade guide](https://docs-3.prefect.io/v3/resources/upgrade-agents-to-workers).

### [​](#resolving-common-gotchas) Resolving common gotchas

#### [​](#attributeerror:-coroutine-object-has-no-attribute-<some-attribute>) `AttributeError: 'coroutine' object has no attribute <some attribute>`

When within an asynchronous task or flow context, if you do **not** `await` an asynchronous function or method, this error will be raised when you try to use the object.
To fix it, `await` the asynchronous function or method or use `_sync=True`.
For example, `Block`’s `load` method is asynchronous in an async context:

Incorrect

Correct

Also Correct

Copy

```
from prefect.blocks.system import Secret

async def my_async_function():
    my_secret = Secret.load("my-secret")
    print(my_secret.get()) # AttributeError: 'coroutine' object has no attribute 'get'
```

Similarly, if you never use an un-awaited coroutine, you may see a warning like this:

Copy

```
RuntimeWarning: coroutine 'some_async_callable' was never awaited
...
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```

This is the same problem as above, and you may `await` the coroutine to fix it or use `_sync=True`.

#### [​](#typeerror:-object-<some-type>-cant-be-used-in-await-expression) `TypeError: object <some Type> can't be used in 'await' expression`

This error occurs when using the `await` keyword before an object that is not a coroutine.
To fix it, remove the `await`.
For example, `my_task.submit(...)` is *always* synchronous in Prefect 3.x:

Incorrect

Correct

Copy

```
from prefect import flow, task

@task
async def my_task():
    pass

@flow
async def my_flow():
    future = await my_task.submit() # TypeError: object PrefectConcurrentFuture can't be used in 'await' expression
```

See the [Futures interface section](#futures-interface) for more information on this particular gotcha.

#### [​](#typeerror:-flow-deploy-got-an-unexpected-keyword-argument-schedule) `TypeError: Flow.deploy() got an unexpected keyword argument 'schedule'`

In Prefect 3.0, the `schedule` argument has been removed in favor of the `schedules` argument.
This applies to both the `Flow.serve` and `Flow.deploy` methods.

Prefect 2.0

Prefect 3.0

Copy

```
from datetime import timedelta
from prefect import flow
from prefect.client.schemas.schedules import IntervalSchedule

@flow
def my_flow():
    pass

my_flow.serve(
    name="my-flow",
    schedule=IntervalSchedule(interval=timedelta(minutes=1))
)
```

Was this page helpful?

YesNo

[Migrate from Airflow](/v3/how-to-guides/migrate/airflow)[Upgrade from agents to workers](/v3/how-to-guides/migrate/upgrade-agents-to-workers)

⌘I