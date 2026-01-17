How to write and run a workflow - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

How to write and run a workflow

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

* [Define a workflow](#define-a-workflow)
* [Create tasks and child workflows](#create-tasks-and-child-workflows)
* [Cancel a workflow if it runs for too long](#cancel-a-workflow-if-it-runs-for-too-long)
* [Configure flows and tasks](#configure-flows-and-tasks)
* [Flow configuration](#flow-configuration)
* [Task configuration](#task-configuration)

### [​](#define-a-workflow) Define a workflow

Make a Python function a workflow by adding the `@flow` decorator to it:

Copy

```
from prefect import flow


@flow
def my_workflow() -> str:
    return "Hello, world!"
```

Run the workflow by calling it like a normal Python function:

Copy

```
my_workflow()
```

You can create a workflow from a method on a class:

Copy

```
from prefect import flow


class MyClass:

    @flow
    def my_instance_method(self):
        return "Hello, from an instance method!"


    @flow
    @classmethod
    def my_class_method(cls):
        return "Hello, from a class method!"


    @flow
    @staticmethod
    def my_static_method():
        return "Hello, from a static method!"


MyClass().my_instance_method()
MyClass.my_class_method()
MyClass.my_static_method()
```

or from a generator function:

Copy

```
from prefect import flow


@flow
def generator():
    for i in range(10):
        yield i


for val in generator():
    print(val)
```

You can view all workflow runs in the Prefect UI.

### [​](#create-tasks-and-child-workflows) Create tasks and child workflows

You can create tasks and child flows to organize your workflow logic.

Copy

```
from prefect import flow, task


@task
def generate_a_number():
    return random.randint(0, 100)


@flow
def is_number_even(number: int):
    return number % 2 == 0


@flow
def even_or_odd():
    number = generate_a_number()
    if is_number_even(number):
        print("The number is even")
    else:
        print("The number is odd")
```

Each task and child flow is a separate unit of work and is displayed in the Prefect UI.

### [​](#cancel-a-workflow-if-it-runs-for-too-long) Cancel a workflow if it runs for too long

To apply a timeout to a flow or task to prevent it from running for too long, use the `timeout_seconds` keyword argument.

Copy

```
from prefect import flow
import time

@flow(timeout_seconds=1, log_prints=True)
def show_timeouts():
    print("I will execute")
    time.sleep(5)
    print("I will not execute")
```

## [​](#configure-flows-and-tasks) Configure flows and tasks

### [​](#flow-configuration) Flow configuration

All flows can be configured by passing arguments to the decorator. Flows accept the following optional settings:

| Argument | Description |
| --- | --- |
| `description` | An optional string description for the flow. If not provided, the description is pulled from the docstring for the decorated function. |
| `name` | An optional name for the flow. If not provided, the name is inferred from the function. |
| `retries` | An optional number of times to retry on flow run failure. |
| `retry_delay_seconds` | An optional number of seconds to wait before retrying the flow after failure. This is only applicable if `retries` is nonzero. |
| `flow_run_name` | An optional name to distinguish runs of this flow; this name can be provided as a string template with the flow’s parameters as variables; you can also provide this name as a function that returns a string. |
| `task_runner` | An optional [task runner](/v3/concepts/task-runners) to use for task execution within the flow when you `.submit()` tasks. If not provided and you `.submit()` tasks, the `ThreadPoolTaskRunner` is used. |
| `timeout_seconds` | An optional number of seconds indicating a maximum runtime for the flow. If the flow exceeds this runtime, it is marked as failed. Flow execution may continue until the next task is called. |
| `validate_parameters` | Boolean indicating whether parameters passed to flows are validated by Pydantic. Default is `True`. |
| `version` | An optional version string for the flow. If not provided, we will attempt to create a version string as a hash of the file containing the wrapped function. If the file cannot be located, the version will be null. |

### [​](#task-configuration) Task configuration

Tasks allow for customization through optional arguments that can be provided to the [task decorator](https://reference.prefect.io/prefect/tasks/#prefect.tasks.task).

| Argument | Description |
| --- | --- |
| `name` | An optional name for the task. If not provided, the name is inferred from the function name. |
| `description` | An optional string description for the task. If not provided, the description is pulled from the docstring for the decorated function. |
| `tags` | An optional set of tags associated with runs of this task. These tags are combined with any tags defined by a `prefect.tags` context at task runtime. |
| `timeout_seconds` | An optional number of seconds indicating a maximum runtime for the task. If the task exceeds this runtime, it will be marked as failed. |
| `cache_key_fn` | An optional callable that, given the task run context and call parameters, generates a string key. If the key matches a previous completed state, that state result is restored instead of running the task again. |
| `cache_policy` | An optional policy that determines what information is used to generate cache keys. Available policies include `INPUTS`, `TASK_SOURCE`, `RUN_ID`, `FLOW_PARAMETERS`, and `NO_CACHE`. Can be combined using the + operator. |
| `cache_expiration` | An optional amount of time indicating how long cached states for this task are restorable; if not provided, cached states will never expire. |
| `retries` | An optional number of times to retry on task run failure. |
| `retry_delay_seconds` | An optional number of seconds to wait before retrying the task after failure. This is only applicable if `retries` is nonzero. |
| `log_prints` | An optional boolean indicating whether to log print statements. |

See all possible options in the [Python SDK docs](https://reference.prefect.io/prefect/tasks/#prefect.tasks.task).
For example, provide optional `name` and `description` arguments to a task:

Copy

```
from prefect import task


@task(name="hello-task", description="This task says hello.")
def my_task():
    print("Hello, I'm a task")
```

Distinguish runs of this task by providing a `task_run_name`.  
Python’s standard string formatting syntax applies:

Copy

```
import datetime
from prefect import flow, task


@task(name="My Example Task", 
      description="An example task for a tutorial.",
      task_run_name="hello-{name}-on-{date:%A}")
def my_task(name, date):
    pass


@flow
def my_flow():
    # creates a run with a name like "hello-marvin-on-Thursday"
    my_task(name="marvin", date=datetime.datetime.now(datetime.timezone.utc))

if __name__ == "__main__":
    my_flow()
```

Additionally, this setting accepts a function that returns a string for the task run name:

Copy

```
import datetime
from prefect import flow, task


def generate_task_name():
    date = datetime.datetime.now(datetime.timezone.utc)
    return f"{date:%A}-is-a-lovely-day"


@task(name="My Example Task",
      description="An example task for the docs.",
      task_run_name=generate_task_name)
def my_task(name):
    pass


@flow
def my_flow():
    # creates a run with a name like "Thursday-is-a-lovely-day"
    my_task(name="marvin")


if __name__ == "__main__":
    my_flow()
```

Was this page helpful?

YesNo

[Overview](/v3/how-to-guides)[Use assets to track workflow outputs](/v3/how-to-guides/workflows/assets)

⌘I