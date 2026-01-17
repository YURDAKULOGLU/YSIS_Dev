Task runners - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

Task runners

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

* [Available task runners](#available-task-runners)
* [Configure a task runner](#configure-a-task-runner)
* [Submit tasks to a task runner](#submit-tasks-to-a-task-runner)
* [Access results from submitted tasks](#access-results-from-submitted-tasks)
* [Design considerations](#design-considerations)
* [Further reading](#further-reading)

Task runners are a simple and consistent interface to concurrency primitives - they are not required for task execution.
Calling a task function directly executes the function in the main thread by default,
blocking execution of its caller until the task completes.
To enable concurrent, parallel, or distributed execution of tasks, use the `.submit()` or `.map()` methods to submit tasks to a **task runner**.

## [​](#available-task-runners) Available task runners

The default task runner in Prefect is the [`ThreadPoolTaskRunner`](/v3/api-ref/python/prefect-task_runners#threadpooltaskrunner),
which runs tasks concurrently in independent threads.
For CPU-intensive tasks that benefit from process isolation, use the [`ProcessPoolTaskRunner`](/v3/api-ref/python/prefect-task_runners#processpooltaskrunner),
which runs tasks in separate processes using Python’s `multiprocessing` module.
For distributed task execution across multiple machines, you can use one of the following task runners, which are available as extras of the `prefect` library:

* [`DaskTaskRunner`](/integrations/prefect-dask) can run tasks using [`dask.distributed`](http://distributed.dask.org/) (install `prefect[dask]`)
* [`RayTaskRunner`](/integrations/prefect-ray) can run tasks using [Ray](https://www.ray.io/) (install `prefect[ray]`)

**Concurrency vs. parallelism**

* **Concurrency** refers to a system that can do more than one thing simultaneously,
  but not at the *exact* same time. Think of concurrent execution as non-blocking:
  within the restrictions of resources available in the execution environment and data dependencies between tasks,
  execution of one task does not block execution of other tasks in a flow.
* **Parallelism** refers to a system that can do more than one thing at the *exact* same time.
  Within the restrictions of resources available, parallel execution can run tasks at the same time,
  such as for operations mapped across a dataset.

## [​](#configure-a-task-runner) Configure a task runner

To configure a specific task runner, provide a `task_runner` keyword argument to the parent flow:

use threads to run tasks concurrently

use isolated processes to run tasks in parallel

Copy

```
from prefect import flow, task
from prefect.futures import wait
from prefect.task_runners import ThreadPoolTaskRunner
import time

@task
def stop_at_floor(floor):
    print(f"elevator moving to floor {floor}")
    time.sleep(floor)
    print(f"elevator stops on floor {floor}")

@flow(task_runner=ThreadPoolTaskRunner(max_workers=3))
def elevator():
    floors = []

    for floor in range(10, 0, -1):
        floors.append(stop_at_floor.submit(floor))

    wait(floors) # wait for the sequence of futures to complete
```

The `max_workers` parameter of the `ThreadPoolTaskRunner` and `ProcessPoolTaskRunner` controls the number of threads or processes (respectively) that the task runner will use to execute tasks.

## [​](#submit-tasks-to-a-task-runner) Submit tasks to a task runner

When you use `.submit()` to submit a task to a task runner, the task runner creates a
[`PrefectFuture`](/v3/api-ref/python/prefect-futures#prefect.futures.PrefectFuture) for access to the state and
result of the task.
A `PrefectFuture` is an object that provides:

* a reference to the result returned by the task
* a [`State`](/v3/api-ref/python/prefect-server#prefect.server.schemas.states) indicating the current state of the task run

`PrefectFuture` objects must be resolved explicitly before returning from a flow or task.
Dependencies between futures will be automatically resolved whenever their dependents are resolved.
This means that only *terminal* futures need to be resolved, either by:

* returning the terminal futures from your flow or task
* calling `.wait()` or `.result()` on each terminal future
* using one of the top level `wait` or `as_completed` utilities to resolve terminal futures

Not doing so may leave your tasks in an unfinished state.

When you pass a future into a task, Prefect automatically waits for the “upstream” task (the one that the future references),
to reach a final state before starting the downstream task.
This means that the downstream task won’t receive the `PrefectFuture` you passed as an argument.
Instead, the downstream task receives the value that the upstream task returned.
For example:

Copy

```
from prefect import flow, task

@task
def say_hello(name):
    return f"Hello {name}!"

@task
def print_result(result):
    print(type(result))
    print(result)

@flow(name="hello-flow")
def hello_world():
    future = say_hello.submit("Marvin")
    print_result.submit(future).wait()

hello_world()
```

If we run this, we see that we only had to wait for the final `print_result` future as Prefect automatically resolved `say_hello` to a string.

### [​](#access-results-from-submitted-tasks) Access results from submitted tasks

You can access the result of a future explicitly with the `.result()` method.

Copy

```
from prefect import flow, task

@task
def my_task():
    return 42

@flow
def my_flow():
    future = my_task.submit()
    result = future.result()
    print(result)

my_flow()
```

The `.result()` method waits for the task to complete before returning the result to the caller.
If the task run fails, `.result()` will raise the task run’s exception. Disable this behavior
with the `raise_on_failure` option:

Copy

```
from prefect import flow, task

@task
def my_task():
    return "I'm a task!"


@flow
def my_flow():
    future = my_task.submit()
    result = future.result(raise_on_failure=False)
    if future.state.is_failed():
        # `result` is an exception! handle accordingly
        ...
    else:
        # `result` is the expected return value of our task
        ...
```

**A few notes on `.result()`**

* `.result()` is a blocking call.
  This means that calling `.result()` will block the caller until the task run completes.
* Only use `.result()` when you need to interact directly with the return value of your submitted task;
  for example, you **should** use `.result()` if passing the return value to a standard Python function (not a
  Prefect task) but do not need to use `.result()` if you are passing the value to another task (as these futures will be [automatically resolved](/v3/develop/task-runners#submit-tasks-to-a-task-runner)).

## [​](#design-considerations) Design considerations

When choosing how and when to achieve concurrency using task runners, consider the following:

1. **Task granularity**: The “proper” size for tasks depends on the nature and complexity of the work you’re doing, e.g. too many small tasks might create overhead - see [Writing tasks](/v3/develop/write-tasks) for more.
2. **Resource constraints**: Be aware of environment limitations. Using `.map` can create many task instances very quickly, which might exceed your resource availability.
3. **Data transfer**: Large data passed between tasks can impact performance. Consider passing references to external storage when dealing with large datasets.
4. **Parallelism**: For true parallelism (rather than just concurrency), consider using a specialized task runner like the `DaskTaskRunner` or `RayTaskRunner` (or [propose a new task runner type](https://github.com/PrefectHQ/prefect/issues/new?template=2_feature_enhancement.yaml)).
5. **Beware of unsafe global state**: Use of concurrency or parallelism features like `.submit` and `.map` must respect the underlying primitives to avoid unexpected behavior. For example, the default `ThreadPoolTaskRunner` runs each task in a separate thread, which means that any global state must be threadsafe. Similarly, `DaskTaskRunner` and `RayTaskRunner` are multi-process runners that require global state to be [picklable](https://docs.python.org/3/library/pickle.html).

## [​](#further-reading) Further reading

* [Run tasks concurrently](/v3/how-to-guides/workflows/run-work-concurrently)

Was this page helpful?

YesNo

[Artifacts](/v3/concepts/artifacts)[Global concurrency limits](/v3/concepts/global-concurrency-limits)

⌘I