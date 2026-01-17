Tasks - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

Tasks

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

* [What is a task?](#what-is-a-task)
* [Running a task](#running-a-task)
* [The life of a task run](#the-life-of-a-task-run)
* [Different ways to create a task run](#different-ways-to-create-a-task-run)
* [Task orchestration model](#task-orchestration-model)
* [Client-side orchestration](#client-side-orchestration)
* [State dependencies](#state-dependencies)
* [Task composition within flows](#task-composition-within-flows)
* [Background tasks](#background-tasks)

Copy

```
from prefect import task

@task(log_prints=True)
def explain_tasks():
    print("run any python code here!")
    print("but maybe just a little bit")

if __name__ == "__main__":
    explain_tasks()
```

## [​](#what-is-a-task) What is a task?

Tasks are defined as decorated Python functions. Above, `explain_tasks` is an instance of a task.
Tasks are cache-able and retryable units of work that are easy to execute concurrently, in parallel, and/or with [transactional semantics](/v3/advanced/transactions).
Like flows, tasks are free to call other tasks or flows, there is no required nesting pattern.
Generally, tasks behave like normal Python functions, but they have some additional capabilities:

* Metadata about task runs, such as run time and final state, is automatically tracked
* Each [state](/v3/concepts/states) the task enters is recorded, enabling observability and state-based logic
* [Futures](/v3/how-to-guides/workflows/run-work-concurrently#handling-futures) from upstream tasks are automatically resolved by downstream tasks
* [Retries](/v3/how-to-guides/workflows/retries) can be performed on failure, with configurable delay and retry limits
* [Caching](/v3/how-to-guides/workflows/cache-workflow-steps) enables result reuse across workflow executions
* [Concurrency](/v3/how-to-guides/workflows/run-work-concurrently) via `.submit()` and `.map()` allow concurrent execution within and across workflows
* [Timeouts](/v3/how-to-guides/workflows/write-and-run#cancel-a-workflow-if-it-runs-for-too-long) can be enforced to prevent unintentional, long-running operations

Tasks are uniquely identified by a task key, which is a hash composed of the task name and the fully qualified name of the function.

## [​](#running-a-task) Running a task

A **task run** is a representation of a single invocation of a task.

### [​](#the-life-of-a-task-run) The life of a task run

Like flow runs, each task run has its own state lifecycle. Task states provide observability into execution progress and enable sophisticated runtime logic based on upstream outcomes.
Like flow runs, each task run can be observed in the Prefect UI or CLI.
A normal task run lifecycle looks like this:


**[Background tasks](#background-tasks) have an additional state**When using `.delay()`, background tasks start in a `Scheduled` state before transitioning to `Pending`. This allows them to be queued and distributed to available workers.

### [​](#different-ways-to-create-a-task-run) Different ways to create a task run

The simplest way to create a task run is to call a `@task` decorated function (i.e. `__call__`), just like a normal Python function.

Copy

```
from prefect import task

@task
def add_integers(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    add_integers(1, 2)
```

Tasks may be submitted to a [task runner](/v3/how-to-guides/workflows/run-work-concurrently#task-runners) for concurrent execution where the eventual result is desired.
When the result of a task is not required by the caller, it may be delayed to static infrastructure in the background for execution by an available [task worker](/v3/how-to-guides/workflows/run-background-tasks#task-workers).

## [​](#task-orchestration-model) Task orchestration model

### [​](#client-side-orchestration) Client-side orchestration

Prefect tasks are orchestrated client-side, which means that task runs are created and updated locally. This allows for efficient handling of large-scale workflows with many tasks and improves reliability when connectivity fails intermittently.
Task updates are logged in batch, leading to eventual consistency for task states in the UI and API queries.

### [​](#state-dependencies) State dependencies

Tasks automatically resolve dependencies based on data flow between them. When a task receives the result or future of an upstream task as input, Prefect establishes an implicit state dependency such that a downstream task cannot begin until the upstream task has `Completed`.
Explicit state dependencies can be introduced with [the `wait_for` parameter.](/v3/how-to-guides/workflows/run-work-concurrently#creating-state-dependencies)

## [​](#task-composition-within-flows) Task composition within flows

Tasks are typically organized into [flows](/v3/concepts/flows#organize-flows-with-subflows-and-tasks) to create comprehensive workflows.
Each task offers isolated observability within the Prefect UI. Task-level metrics, logs, and state information help identify bottlenecks and troubleshoot issues at a granular level. Tasks can also be reused across multiple flows, promoting consistency and modularity across an organization’s data ecosystem.

**How big should a task be?**Prefect encourages “small tasks.” As a rule of thumb, each task should represent a logical step or significant “side effect” in your workflow.
This allows task-level observability and orchestration to narrate your workflow out-of-the-box.![Narrative encapsulation](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/concepts/narrative-encapsulation.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=0375ef77dac4dbf1fb99b31fb1582aab)

For detailed configuration options and implementation guidance, see [how to write and run workflows](/v3/how-to-guides/workflows/write-and-run).

## [​](#background-tasks) Background tasks

Background tasks are an alternate task execution model where tasks are submitted in a non-blocking manner by one process and executed by a pool of processes. This execution model is particularly valuable for web applications and workflows that need to dispatch heavy or long-running work without waiting for completion to dedicated, horizontally scaled infrastructure.
When a task is executed with `.delay()`, it pushes the resulting task run onto a server-side topic, which is distributed to an available [task worker](/v3/how-to-guides/workflows/run-background-tasks#task-workers) for execution.

Prefect background tasks can be used in place of tools like [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) and [RabbitMQ](https://www.rabbitmq.com/) for task queue functionality.

Background tasks are useful for scenarios such as:

* Web applications that need to trigger long-running processes without blocking HTTP responses
* Workflows that dispatch work to specialized infrastructure or resource pools
* Systems that need to scale task execution independently from the main application

For implementation details, see [how to run background tasks](/v3/how-to-guides/workflows/run-background-tasks).

Was this page helpful?

YesNo

[Flows](/v3/concepts/flows)[Assets](/v3/concepts/assets)

⌘I