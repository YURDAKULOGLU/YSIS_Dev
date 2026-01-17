States - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

States

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

* [State types](#state-types)
* [State transitions](#state-transitions)
* [Final state determination](#final-state-determination)
* [Task return values](#task-return-values)
* [Flow return values](#flow-return-values)
* [State change hooks](#state-change-hooks)
* [Further reading](#further-reading)

States are rich objects that contain information about the status of a particular [task](/v3/develop/write-tasks)
run or [flow](/v3/develop/write-flows) run.
You can learn many things about a task or flow by examining its current state or the
history of its states. For example, you might observe that a given run:

* is `Scheduled` to run for the third time in an hour
* is `Late` because the associated worker process is not responding
* was `Scheduled` to run, but later `Cancelled` via button in the UI
* was `Cached` from a previous run instead of `Running` again
* has `Completed` after `Running` among its fellow task runs
* ended up `Failed` because Claude left pydantic 1.x syntax in your code
* ended up `Crashed` because you Ctrl-C’d the process

**Only runs have states**:
Flows and tasks are templates that describe what a system does;
only when we **run** the system does it also take on a state.

## [​](#state-types) State types

Prefect states have names and types.
A state’s name is often, but not always, synonymous with its type. For example, a task run
that is running for the first time has a state with the name Running and the type `RUNNING`. However, if the task retries,
that same task run will have the name Retrying and the type `RUNNING`.
State *types* drive orchestration logic, whereas state *names* provide visual bookkeeping.
The full list of states and state types includes:

| Name | Type | Terminal? | Description |
| --- | --- | --- | --- |
| `Scheduled` | `SCHEDULED` | No | The run will begin at a particular time in the future. |
| `Late` | `SCHEDULED` | No | The run’s scheduled start time has passed, but it has not transitioned to PENDING (15 seconds by default). |
| `AwaitingRetry` | `SCHEDULED` | No | The run did not complete successfully because of a code issue and had remaining retry attempts. |
| `AwaitingConcurrencySlot` | `SCHEDULED` | No | The run is waiting to occupy a concurrency slot prior to submission. |
| `Resuming` | `SCHEDULED` | No | The run is scheduled to resume execution. |
| `Pending` | `PENDING` | No | The run has been submitted to execute, but is waiting on necessary preconditions to be satisfied. |
| `Running` | `RUNNING` | No | The run code is currently executing. |
| `Retrying` | `RUNNING` | No | The run code is currently executing after previously not completing successfully. |
| `Paused` | `PAUSED` | No | The run code has stopped executing until it receives manual approval to proceed. |
| `Suspended` | `PAUSED` | No | The run code has stopped executing and the process has exited. |
| `Cancelling` | `CANCELLING` | No | The infrastructure on which the code was running is being cleaned up. |
| `Cancelled` | `CANCELLED` | Yes | The run did not complete because a user determined that it should not. |
| `Completed` | `COMPLETED` | Yes | The run completed successfully. |
| `Cached` | `COMPLETED` | Yes | The run result was loaded from a previously cached value. |
| `RolledBack` | `COMPLETED` | Yes | The run completed successfully but the transaction rolled back and executed rollback hooks. |
| `Failed` | `FAILED` | Yes | The run did not complete because of a code issue and had no remaining retry attempts. |
| `TimedOut` | `FAILED` | Yes | The run did not complete because it exceeded its time out. |
| `Crashed` | `CRASHED` | Yes | The run did not complete because of an infrastructure issue. |

## [​](#state-transitions) State transitions

When a flow run changes states, you can often tell if it is behaving normally or not.
Here are some common state transitions and what they mean:

|  | From | To | Triggered By | Explanation |
| --- | --- | --- | --- | --- |
| ✅ | None | Scheduled | Manual run, automation, or schedule | A flow run has been created and scheduled for future execution. |
| ✅ | Scheduled | Pending | Worker | A worker is attempting to start the infrastructure for your flow run. |
| ⛔ | Scheduled | Late | Cloud or self-hosted server | Typically means that a worker did not pick up the run because 1) no workers are healthy, 2) workers are not polling the right work pool or work queue, or 3) workers are concurrency limited. |
| ✅ | Pending | Running | Worker | The infrastructure was provisioned and the flow is running |
| ⛔ | Pending | Crashed | Worker or runner | Something went wrong. Some possibilities are 1) the worker could have failed to create the infrastructure, 2) the code is not present in storage or the worker failed to authenticate, or 3) the code has missing or broken imports, or syntax errors. |
| ✅ | Running | Completed | Flow run | The flow completed successfully. |
| ⛔ | Running | Failed | Flow run | This usually means that your code raised an exception, check the flow run logs. |
| ⛔ | Running | Crashed | Worker or flow run | Probably not a raised exception in your code, but could be an infrastructure issue such as 1) an out of memory error, 2) an evicted pod, or 3) a timeout. |

## [​](#final-state-determination) Final state determination

The final state of a flow or task run depends on a number of factors; generally speaking there are three categories of terminal states:

* `COMPLETED`: a run in any `COMPLETED` state did not encounter any errors or exceptions and returned successfully
* `FAILED`: a run in any `FAILED` state encountered an error during execution, such as a raised exception
* `CRASHED`: a run in any `CRASHED` state was interrupted by an OS signal such as a `KeyboardInterrupt` or `SIGTERM`

The flow of state transitions can be visualized here:

States are represented by their name, with boxes behind states clarifying their underlying type. Dotted lines lead to terminal states.

### [​](#task-return-values) Task return values

A task will be placed into a `Completed` state if it returns *any* Python object, with one exception:
if a task explicitly returns a Prefect `Failed` state, the task will be marked `Failed`.

Copy

```
from prefect import task, flow
from prefect.states import Completed, Failed


@task
def toggle_task(fail: bool):
    if fail:
        return Failed(message="I was instructed to fail.")
    else:
        return Completed(message="I was instructed to succeed.")


@flow
def example():
    # this run will be set to a `Failed` state
    state_one = toggle_task(fail=True)

    # this run will be set to a `Completed` state
    state_two = toggle_task(fail=False)

    # similarly, the flow run will fail because we return a `Failed` state
    return state_one, state_two
```

You can also access state objects directly within a flow through the `return_state` flag:

Copy

```
from prefect import flow, task


@task
def add_one(x):
    return x + 1


@flow
def my_flow():
    result = add_one(1)
    assert isinstance(result, int) and result == 2

    state = add_one(1, return_state=True)
    assert state.is_completed() is True
    assert state.result() == 2
```

Returning a `State` via `return_state=True` is useful when you want to conditionally respond to the terminal states of a task or flow. For example, `if state.is_failed(): ...`.

### [​](#flow-return-values) Flow return values

The final state of a flow is determined by its ***return value***. The following rules apply:

* If an exception is raised directly in the flow function, the flow run is marked as `FAILED`.
* If a flow returns a manually created state, it is used as the state of the final flow run. This allows for manual determination of final state.
* If a flow returns an iterable of states, the presence of *any* `FAILED` state will cause the run to be marked as `FAILED`.

In *any other situation* in which the flow returns without error, it will be marked as `COMPLETED`.

If you manipulate states programmatically, you can create situations in which tasks
within a flow can fail and not cause flow run failure.
For example:

Copy

```
from prefect import flow, task 


@task 
def add_one(x):
    return x + 1


@flow 
def my_flow():
    # avoided raising an exception via `return_state=True`
    state = add_one("1", return_state=True)
    assert state.is_failed()

    # the flow function returns successfully!
    return
```

If `state` were returned from the flow function, the run would be marked as `FAILED`.

## [​](#state-change-hooks) State change hooks

State change hooks execute code in response to ***client side*** changes in flow or task run states, enabling you to define actions for
specific state transitions in a workflow.
State hooks have the following signature:

Copy

```
from prefect import Task, Flow
from prefect.states import State
from prefect.client.schemas.objects import TaskRun, FlowRun

def my_task_state_hook(task: Task, run: TaskRun, state: State) -> None:
    ...

def my_flow_state_hook(flow: Flow, run: FlowRun, state: State) -> None:
    ...
```

State change hooks are versatile, allowing you to specify multiple state change hooks for the same state transition,
or to use the same state change hook for different transitions.

### [​](#further-reading) Further reading

* See examples of [how to execute code in response to entering states](/v3/how-to-guides/workflows/state-change-hooks) in your flows and tasks.

Was this page helpful?

YesNo

[Caching](/v3/concepts/caching)[Runtime context](/v3/concepts/runtime-context)

⌘I