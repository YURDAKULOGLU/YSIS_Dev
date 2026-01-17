How to respond to state changes - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

How to respond to state changes

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

* [Available state change hooks](#available-state-change-hooks)
* [Send a notification when a workflow run fails](#send-a-notification-when-a-workflow-run-fails)
* [Execute code when a task starts running](#execute-code-when-a-task-starts-running)
* [Pass kwargs to state change hooks](#pass-kwargs-to-state-change-hooks)

### [​](#available-state-change-hooks) Available state change hooks

| Type | Flow | Task | Description |
| --- | --- | --- | --- |
| `on_completion` | ✓ | ✓ | Executes when a flow or task run enters a `Completed` state. |
| `on_failure` | ✓ | ✓ | Executes when a flow or task run enters a `Failed` state. |
| `on_cancellation` | ✓ | - | Executes when a flow run enters a `Cancelling` state. |
| `on_crashed` | ✓ | - | Executes when a flow run enters a `Crashed` state. |
| `on_running` | ✓ | ✓ | Executes when a flow or task run enters a `Running` state. |

Note that the `on_rollback` hook for tasks is *not* a proper state change hook but instead
is a transaction lifecycle hook.
Rollback hooks accept one argument representing the transaction for the task.

### [​](#send-a-notification-when-a-workflow-run-fails) Send a notification when a workflow run fails

To send a notification when a flow or task run fails, you can specify a `on_failure` hook.

Copy

```
from prefect import flow
from prefect.blocks.core import Block
from prefect.settings import get_current_settings


@flow(retries=1)
def failing_flow():
    raise ValueError("oops!")


@failing_flow.on_failure
def notify_slack(flow, flow_run, state):
    slack_webhook_block = Block.load(
        "slack-webhook/my-slack-webhook"
    )

    PREFECT_API_URL = get_current_settings().api.url

    slack_webhook_block.notify(
        (
            f"Your job {flow_run.name} entered {state.name} "
            f"with message:\n\n"
            f"See <https://{PREFECT_API_URL}/flow-runs/"
            f"flow-run/{flow_run.id}|the flow run in the UI>\n\n"
            f"Tags: {flow_run.tags}\n\n"
            f"Scheduled start: {flow_run.expected_start_time}"
        )
    )

if __name__ == "__main__":
    failing_flow()
```

Retries are configured in this example, so the `on_failure` hook will not run until all `retries` have completed and the flow run enters a `Failed` state.

**State change hooks execute client side**State change hooks run in the same process as your workflow and execution cannot be guaranteed. For more robust execution of logic in response to state changes, use an Automation.

### [​](#execute-code-when-a-task-starts-running) Execute code when a task starts running

The `on_running` hook executes when a task enters a `Running` state, before the task body executes. This is useful for logging, metrics, or setting up runtime state:

Copy

```
from prefect import flow, task
import time

def record_start_time(task, task_run, state):
    print(f"Task {task.name} started at {time.time()}")

@task(on_running=[record_start_time])
def my_task():
    return "hello"

# Or use the decorator pattern
@task
def another_task():
    return "world"

@another_task.on_running
def log_start(task, task_run, state):
    print(f"Starting {task.name}!")

@flow
def my_flow():
    my_task()
    another_task()
```

Note that `on_running` hooks execute **synchronously** before the task body runs. If your hook takes 10 seconds, the task waits 10 seconds before starting.
When retries are configured, `on_running` hooks fire on **each retry attempt**, including the initial run. For example, a task configured with `retries=2` will trigger its `on_running` hooks up to three times: once on the initial run and once for each retry attempt.

### [​](#pass-kwargs-to-state-change-hooks) Pass `kwargs` to state change hooks

You can compose the `with_options` method to effectively pass arbitrary `**kwargs` to your hooks:

Copy

```
from functools import partial
from prefect import flow, task

data = {}

def my_hook(task, task_run, state, **kwargs):
    data.update(state=state, **kwargs)

@task
def bad_task():
    raise ValueError("meh")

@flow
def ok_with_failure_flow(x: str = "foo", y: int = 42):
    bad_task_with_a_hook = bad_task.with_options(
        on_failure=[partial(my_hook, **dict(x=x, y=y))]
    )
    # return a tuple of "bar" and the task run state
    # to avoid raising the task's exception
    return "bar", bad_task_with_a_hook(return_state=True)

_, task_run_state = ok_with_failure_flow()

assert data == {"x": "foo", "y": 42, "state": task_run_state}
```

Was this page helpful?

YesNo

[Run background tasks](/v3/how-to-guides/workflows/run-background-tasks)[Create Artifacts](/v3/how-to-guides/workflows/artifacts)

⌘I