How to run work concurrently - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

How to run work concurrently

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

* [Calling tasks directly](#calling-tasks-directly)
* [Using .submit](#using-submit)
* [Using a different task runner](#using-a-different-task-runner)
* [Handling futures](#handling-futures)
* [Using .map](#using-map)
* [Using the unmapped annotation](#using-the-unmapped-annotation)
* [Bulk PrefectFuture operations](#bulk-prefectfuture-operations)
* [Nested mapped tasks](#nested-mapped-tasks)
* [Creating state dependencies](#creating-state-dependencies)
* [Handling failures in concurrent work](#handling-failures-in-concurrent-work)
* [Using asyncio](#using-asyncio)
* [Real-world applications](#real-world-applications)

## [​](#calling-tasks-directly) Calling tasks directly

Tasks can be called directly (i.e. using [`__call__`](https://docs.python.org/3/reference/datamodel.html#object.__call__)), but they **will not** run concurrently.

Copy

```
import time

from prefect import task

@task
def stop_at_floor(floor: int):
    print(f"elevator moving to floor {floor}")
    time.sleep(floor)
    print(f"elevator stops on floor {floor}")

stop_at_floor(0.1) # blocks for 0.1 seconds
stop_at_floor(0.2) # blocks for 0.2 seconds
stop_at_floor(0.3) # blocks for 0.3 seconds
```

When you call a task directly, it will block the main thread until the task completes.
Continue reading to learn how to run tasks concurrently via [task runners](/v3/concepts/task-runners).

## [​](#using-submit) Using `.submit`

Tasks in your workflows can be run concurrently using the `.submit()` method.

Copy

```
import time

from prefect import flow, task
from prefect.futures import wait

@task
def stop_at_floor(floor: int):
    print(f"elevator moving to floor {floor}")
    time.sleep(floor)
    print(f"elevator stops on floor {floor}")

@flow
def elevator():
    floors = []
    for floor in range(10, 0, -1):
        floors.append(stop_at_floor.submit(floor))
    wait(floors)
```

By default, tasks are submitted via the `ThreadPoolTaskRunner`, which runs tasks concurrently in a thread pool.

A common mistake is to pass non-thread-safe objects to tasks that you submit to a task runner. Avoid passing non-thread-safe objects to tasks you intend to run concurrently.See [Design Considerations](/v3/concepts/task-runners#design-considerations) for more information.

### [​](#using-a-different-task-runner) Using a different task runner

To run submitted tasks with a different task runner, you can pass a `task_runner` argument to the `@flow` decorator.

To run this example, you’ll need to install the `prefect[dask]` extra

Copy

```
import time

from prefect import flow, task
from prefect.futures import wait
from prefect_dask.task_runners import DaskTaskRunner

@task
def stop_at_floor(floor: int):
    print(f"elevator moving to floor {floor}")
    time.sleep(floor)
    print(f"elevator stops on floor {floor}")

@flow(task_runner=DaskTaskRunner())
def elevator():
    floors = []
    for floor in range(10, 0, -1):
        floors.append(stop_at_floor.submit(floor))
    wait(floors)
```

### [​](#handling-futures) Handling futures

When you submit a task, you’ll receive a `PrefectFuture` object back which you can use to track the task’s execution. Use the `.result()` method to get the result of the task.

Copy

```
from prefect import task, flow

@task
def cool_task():
    return "sup"
    
@flow
def my_workflow():
    future = cool_task.submit()
    result = future.result()
    print(result)
```

If you don’t need to the result of the task, you can use the `.wait()` method to wait for execution to complete.

Copy

```
from prefect import task, flow

@task
def cool_task():
    return "sup"
    
@flow
def my_workflow():
    future = cool_task.submit()
    future.wait()
```

To wait for multiple futures to complete, use the `wait()` utility.

Copy

```
from prefect import task, flow
from prefect.futures import wait


@task
def cool_task():
    return "sup"
    
    
@flow
def my_workflow():
    futures = [cool_task.submit() for _ in range(10)]
    wait(futures)
```

**Passing futures between tasks**If you pass `PrefectFuture` objects between tasks or flows, the task or flow receiving the future will wait for the future to complete before starting execution.

Copy

```
from prefect import task, flow

@task
def cool_task():
    return "sup"


@task
def what_did_cool_task_say(what_it_said: str):
    return f"cool task said {what_it_said}"

@flow
def my_workflow():
    future = cool_task.submit()
    print(what_did_cool_task_say(future))
```

## [​](#using-map) Using `.map`

For a convenient way to iteratively submit tasks, use the `.map()` method.

Copy

```
import time

from prefect import flow, task
from prefect.futures import wait

@task
def stop_at_floor(floor: int):
    print(f"elevator moving to floor {floor}")
    time.sleep(floor)
    print(f"elevator stops on floor {floor}")

@flow
def elevator():
    floors = list(range(10, 0, -1))
    floors = stop_at_floor.map(floors)
    wait(floors)
```

Like `.submit`, `.map` uses the task runner configured on the parent flow. Changing the task runner will change where mapped tasks are executed.

### [​](#using-the-unmapped-annotation) Using the `unmapped` annotation

Sometimes you may not want to map a task over a certain input value.
By default, non-iterable values will not be mapped over (so `unmapped` is not required):

Copy

```
from prefect import flow, task

@task
def add_together(x, y):
    return x + y

@flow
def sum_it(numbers: list[int], static_value: int):
    futures = add_together.map(numbers, static_value)
    return futures.result()

resulting_sum = sum_it([1, 2, 3], 5)
assert resulting_sum == [6, 7, 8]
```

… but if your argument is an iterable type, wrap it with `unmapped` to tell `.map` to treat it
as static:

Copy

```
from prefect import flow, task, unmapped

@task
def sum_plus(x, static_iterable):
    return x + sum(static_iterable)

@flow
def sum_it(numbers, static_iterable):
    futures = sum_plus.map(numbers, unmapped(static_iterable))
    return futures.result()

resulting_sum = sum_it([4, 5, 6], [1, 2, 3])
assert resulting_sum == [10, 11, 12]
```

### [​](#bulk-prefectfuture-operations) Bulk `PrefectFuture` operations

When using `.map` as in the above example, the result of the task is a list of futures.
You can wait for or retrieve the results from these futures with `wait` or `result` methods:

Copy

```
futures = some_task.map(some_iterable)
results = futures.result()
```

which is syntactic sugar for the corresponding list comprehension:

Copy

```
futures = some_task.map(some_iterable)
results = [future.result() for future in futures]
```

### [​](#nested-mapped-tasks) Nested mapped tasks

To model more complex concurrent workflows, you can map tasks within other tasks:

Copy

```
import re

from prefect import flow, task
from prefect.futures import wait

def count_words(text: str) -> int:
    """Count the number of words in a text."""
    return len(text.split())

def extract_emails(text: str) -> list[str]:
    return re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)

@task
def analyze_texts(texts: list[str]) -> dict[str, list[int | list[str]]]:
    futures = {
        op.__name__: task(op).map(texts) for op in [count_words, extract_emails]
    }
    wait([f for futs in futures.values() for f in futs])
    return {name: [f.result() for f in futs] for name, futs in futures.items()}

@flow
def run_text_analysis():
    """Analyze a batch of social media posts with multiple operations."""
    results = analyze_texts(
        texts=[
            "Just visited #Paris! Contact me at visitor@example.com #travel #vacation",
            "Working on my new #project. Reach out at developer@example.com if interested!",
            "Happy to announce our company event #celebration #milestone email: events@company.org",
        ]
    )
    print("\nAnalysis Results:")
    print(f"  Word counts: {results['count_words']}")
    print(f"  Extracted emails: {results['extract_emails']}\n")
    return results

run_text_analysis()
```

Output

Copy

```
00:03:45.159 | INFO    | Flow run 'hilarious-collie' - Beginning flow run 'hilarious-collie' for flow 'run-text-analysis'
00:03:45.233 | INFO    | Task run 'count_words-01a' - Finished in state Completed()
00:03:45.236 | INFO    | Task run 'extract_emails-7a7' - Finished in state Completed()
00:03:45.237 | INFO    | Task run 'extract_emails-ca2' - Finished in state Completed()
00:03:45.239 | INFO    | Task run 'count_words-01d' - Finished in state Completed()
00:03:45.240 | INFO    | Task run 'count_words-f0a' - Finished in state Completed()
00:03:45.242 | INFO    | Task run 'extract_emails-0c6' - Finished in state Completed()
00:03:45.247 | INFO    | Task run 'analyze_texts-53b' - Finished in state Completed()

Analysis Results:
  Word counts: [9, 11, 10]
  Extracted emails: [['visitor@example.com'], ['developer@example.com'], ['events@company.org']]

00:03:45.491 | INFO    | Flow run 'hilarious-collie' - Finished in state Completed()
```

This pattern is useful when you need to:

1. Process combinations of parameters concurrently
2. Apply multiple transformations to multiple datasets
3. Create a grid of operations where each cell is an independent task

## [​](#creating-state-dependencies) Creating state dependencies

You may also use the [`wait_for=[]`](https://reference.prefect.io/prefect/tasks/#prefect.tasks.Task.submit) parameter
when calling a task by specifying upstream task dependencies. This enables you to control task execution
order for tasks that do not share data dependencies.

Copy

```
from prefect import flow, task
@task
def task_a():
    pass

@task
def task_b():
    pass

@task
def task_c():
    pass
    
@task
def task_d():
    pass

@flow
def my_flow():
    a = task_a.submit()
    b = task_b.submit()
    # Wait for task_a and task_b to complete
    c = task_c.submit(wait_for=[a, b])
    # task_d will wait for task_c to complete
    # Note: If waiting for one task it must still be in a list.
    d = task_d(wait_for=[c])
```

## [​](#handling-failures-in-concurrent-work) Handling failures in concurrent work

Instead of failing your entire workflow when a single concurrent task fails, you may want to run concurrent work to completion, even if some tasks fail. To run tasks concurrently and handle failures afterwards, use the `wait()` utility along with the `.state` attribute on futures:

Copy

```
from typing import Any

from prefect import flow, task
from prefect.futures import wait
from prefect.states import State

@task
def process_data(item: int) -> str:
    if item < 0:
        raise ValueError(f"Cannot process negative value: {item}")
    return f"Processed {item}"

@flow
def batch_processing():
    items = [1, -2, 3, -4, 5]
    
    # Submit all tasks and return the futures
    futures = process_data.map(items)
    
    # Wait for all futures to complete concurrently
    done, not_done = wait(futures)
    
    # Check each future's state
    successful: list[Any] = []
    failed: list[State] = []
    
    for future in done:
        if future.state.is_completed():
            successful.append(future.result())
        else:
            failed.append(future.state)
    
    print(f"Processed {len(successful)} items successfully")
    print(f"Failed to process {len(failed)} items")
    
    return successful
```

The `wait()` function returns two sets of futures: `done` and `not_done`. Each future has a `.state` attribute you can inspect to determine how the associated task run’s result (or exception) should be treated downstream.

The “right way” to handle failures will depend on your use case. Review the [final state determination](/v3/concepts/states#final-state-determination) documentation for more information.

## [​](#using-asyncio) Using `asyncio`

If you have tasks are defined as async functions, you can use `asyncio` from the Python standard library to run them concurrently.

Copy

```
import asyncio

from prefect import flow, task

@task
async def stop_at_floor(floor: int):
    print(f"elevator moving to floor {floor}")
    await asyncio.sleep(floor)
    print(f"elevator stops on floor {floor}")

@flow
async def elevator():
    floors = list(range(10, 0, -1))
    await asyncio.gather(*[stop_at_floor(floor) for floor in floors])


if __name__ == "__main__":
    asyncio.run(elevator())
```

## [​](#real-world-applications) Real-world applications

Mapped tasks are particularly valuable in common data science and ETL workflows such as:

1. **Machine learning model evaluation**: Train multiple models on multiple datasets concurrently
2. **ETL pipelines**: Process multiple data sources with multiple transformations
3. **API data enrichment**: Enrich multiple records with data from multiple external services

For example, imagine you want to find the best training configuration for a series of datasets, and you want to process all datasets concurrently:

Copy

```
import random
from dataclasses import dataclass

from prefect import flow, task
from prefect.futures import PrefectFuture, wait

@dataclass
class Dataset:
    name: str

@dataclass
class ModelConfig:
    name: str

@task(task_run_name="train on {dataset.name} with {model_config.name}")
def train_model(dataset: Dataset, model_config: ModelConfig) -> dict:
    return {
        "dataset": dataset.name,
        "model": model_config.name,
        "score": random.random(),
    }

@flow
def evaluate_models(datasets: list[Dataset], model_configs: list[ModelConfig]):
    all_futures: list[PrefectFuture[dict[str, object]]] = []
    for dataset in datasets:
        futures = train_model.map(
            dataset=dataset,
            model_config=model_configs,
        )
        all_futures.extend(futures)

    results = [future.result() for future in wait(all_futures).done]

    print(f"\nBest model: {max(results, key=lambda r: r['score'])}")

evaluate_models(
    datasets=[
        Dataset("customers"), Dataset("products"), Dataset("orders")
    ],
    model_configs=[
        ModelConfig("random_forest"), ModelConfig("gradient_boosting")
    ],
)
```

Output

Copy

```
00:56:47.873 | INFO    | Flow run 'precious-walrus' - Beginning flow run 'precious-walrus' for flow 'evaluate-models'
00:56:47.981 | INFO    | Task run 'train on customers with random_forest' - Finished in state Completed()
00:56:47.984 | INFO    | Task run 'train on orders with gradient_boosting' - Finished in state Completed()
00:56:47.984 | INFO    | Task run 'train on customers with gradient_boosting' - Finished in state Completed()
00:56:47.985 | INFO    | Task run 'train on products with random_forest' - Finished in state Completed()
00:56:47.988 | INFO    | Task run 'train on orders with random_forest' - Finished in state Completed()
00:56:47.990 | INFO    | Task run 'train on products with gradient_boosting' - Finished in state Completed()

Best model: {'dataset': 'products', 'model': 'random_forest', 'score': 0.5603239415052655}

00:56:48.121 | INFO    | Flow run 'precious-walrus' - Finished in state Completed()
```

Was this page helpful?

YesNo

[Access runtime information](/v3/how-to-guides/workflows/access-runtime-info)[Cache workflow step outputs](/v3/how-to-guides/workflows/cache-workflow-steps)

⌘I