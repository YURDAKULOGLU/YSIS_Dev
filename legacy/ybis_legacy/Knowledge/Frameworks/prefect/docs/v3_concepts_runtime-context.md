Runtime context - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

Runtime context

[Getting Started](/v3/get-started)[Concepts](/v3/concepts)[How-to Guides](/v3/how-to-guides)[Advanced](/v3/advanced)[Examples](/v3/examples)[Integrations](/integrations/integrations)[API Reference](/v3/api-ref)[Contribute](/contribute)[Release Notes](/v3/release-notes)

* [Overview](/v3/concepts)

##### Workflows

* [Flows](/v3/concepts/flows)
* [Tasks](/v3/concepts/tasks)
* [Assets](/v3/concepts/assets)
* [Caching](/v3/concepts/caching)
* [States](/v3/concepts/states)
* [Runtime context](/v3/concepts/runtime-context)
* [Artifacts](/v3/concepts/artifacts)
* [Task runners](/v3/concepts/task-runners)
* [Global concurrency limits](/v3/concepts/global-concurrency-limits)
* [Tag-based concurrency limits](/v3/concepts/tag-based-concurrency-limits)

##### Deployments

* [Deployments](/v3/concepts/deployments)
* [Schedules](/v3/concepts/schedules)
* [Work pools](/v3/concepts/work-pools)
* [Workers](/v3/concepts/workers)

##### Configuration

* [Variables](/v3/concepts/variables)
* [Blocks](/v3/concepts/blocks)
* [Settings and profiles](/v3/concepts/settings-and-profiles)
* [Prefect server](/v3/concepts/server)

##### Automations

* [Events](/v3/concepts/events)
* [Automations](/v3/concepts/automations)
* [Event triggers](/v3/concepts/event-triggers)

##### Prefect Cloud

* [Rate limits and data retention](/v3/concepts/rate-limits)
* [SLAs](/v3/concepts/slas)
* [Webhooks](/v3/concepts/webhooks)

On this page

* [Access runtime information](#access-runtime-information)
* [Access the run context directly](#access-the-run-context-directly)

Prefect tracks information about the current flow or task run with a run context.
The run context is like a global variable that allows the Prefect engine to determine relationships
between your runs, such as which flow your task was called from.
The run context itself contains many internal objects used by Prefect to manage execution of
your run, and is only available in specific situations. For this reason, we expose a simple interface
that only includes the items you care about and dynamically retrieves additional information when necessary.
We call this the “runtime context” as it contains information that’s only accessible during a run.

**Mock values through environment variable**
You may want to mock certain values for testing purposes. For example, by manually setting an ID or
a scheduled start time to ensure your code is functioning properly.Mock values in runtime through an environment variable using the schema
`PREFECT__RUNTIME__{SUBMODULE}__{KEY_NAME}=value`:

Copy

```
export PREFECT__RUNTIME__TASK_RUN__FAKE_KEY='foo'
python -c 'from prefect.runtime import task_run; print(task_run.fake_key)' # "foo"
```

If the environment variable mocks an existing runtime attribute, the value is cast to the same type.
This works for runtime attributes of basic types (`bool`, `int`, `float` and `str`) and `datetime.datetime`.
For complex types like `list` or `dict`, we suggest mocking them using
[monkeypatch](https://docs.pytest.org/en/latest/how-to/monkeypatch.html) or a similar tool.

## [​](#access-runtime-information) Access runtime information

The `prefect.runtime` module is the home for all runtime context access. Each major runtime concept
has its own submodule:

* `deployment`: Access information about the deployment for the current run
* `flow_run`: Access information about the current flow run
* `task_run`: Access information about the current task run

For example:

my\_runtime\_info.py

Copy

```
from prefect import flow, task
from prefect import runtime

@flow(log_prints=True)
def my_flow(x):
    print("My name is", runtime.flow_run.name)
    print("I belong to deployment", runtime.deployment.name)
    my_task(2)

@task
def my_task(y):
    print("My name is", runtime.task_run.name)
    print("Flow run parameters:", runtime.flow_run.parameters)

if __name__ == "__main__":
    my_flow(1)
```

Running this file produces output similar to the following:

Copy

```
10:08:02.948 | INFO    | prefect.engine - Created flow run 'solid-gibbon' for flow 'my-flow'
10:08:03.555 | INFO    | Flow run 'solid-gibbon' - My name is solid-gibbon
10:08:03.558 | INFO    | Flow run 'solid-gibbon' - I belong to deployment None
10:08:03.703 | INFO    | Flow run 'solid-gibbon' - Created task run 'my_task-0' for task 'my_task'
10:08:03.704 | INFO    | Flow run 'solid-gibbon' - Executing 'my_task-0' immediately...
10:08:04.006 | INFO    | Task run 'my_task-0' - My name is my_task-0
10:08:04.007 | INFO    | Task run 'my_task-0' - Flow run parameters: {'x': 1}
10:08:04.105 | INFO    | Task run 'my_task-0' - Finished in state Completed()
10:08:04.968 | INFO    | Flow run 'solid-gibbon' - Finished in state Completed('All states completed.')
```

The above example demonstrates access to information about the current flow run, task run, and deployment.
When run without a deployment (through `python my_runtime_info.py`), you should see `"I belong to deployment None"` logged.
When information is not available, the runtime always returns an empty value.
Because this flow runs outside of a deployment, there is no deployment data.
If this flow was run as part of a deployment, we’d see the name of the deployment instead.
See the [runtime API reference](https://reference.prefect.io/prefect/runtime/flow_run/) for a full list of available attributes.

## [​](#access-the-run-context-directly) Access the run context directly

Access the current run context with `prefect.context.get_run_context()`.
This function raises an exception if no run context is available, meaning you are not in a flow or task run.
If a task run context is available, it is returned even if a flow run context is available.
Alternatively, you can access the flow run or task run context explicitly.
For example, this allows you to access the flow run context from a task run.
Prefect does not send the flow run context to distributed task workers because the context is
costly to serialize and deserialize.

Copy

```
from prefect.context import FlowRunContext, TaskRunContext

flow_run_ctx = FlowRunContext.get()
task_run_ctx = TaskRunContext.get()
```

Unlike `get_run_context`, these method calls do not raise an error if the context is unavailable.
Instead, they return `None`.

Was this page helpful?

YesNo

[States](/v3/concepts/states)[Artifacts](/v3/concepts/artifacts)

⌘I