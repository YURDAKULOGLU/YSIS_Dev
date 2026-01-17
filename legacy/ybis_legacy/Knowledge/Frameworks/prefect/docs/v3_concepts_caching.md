Caching - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

Caching

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

* [Cache keys](#cache-keys)
* [Cache policies](#cache-policies)
* [Customizing the cache](#customizing-the-cache)
* [Cache expiration](#cache-expiration)
* [Cache policies](#cache-policies-2)
* [Cache key functions](#cache-key-functions)
* [Cache storage](#cache-storage)
* [Cache isolation](#cache-isolation)
* [Recommended Lock Managers by Execution Context](#recommended-lock-managers-by-execution-context)
* [Multi-task caching](#multi-task-caching)

Caching refers to the ability of a task run to enter a `Completed` state and return a predetermined
value without actually running the code that defines the task.
Caching allows you to efficiently reuse [results of tasks](/v3/develop/results) that may be expensive to compute
and ensure that your pipelines are idempotent when retrying them due to unexpected failure.
By default Prefect’s caching logic is based on the following attributes of a task invocation:

* the inputs provided to the task
* the code definition of the task
* the prevailing flow run ID, or if executed autonomously, the prevailing task run ID

These values are hashed to compute the task’s *cache key*.
This implies that, by default, calling the same task with the same inputs more than once within a flow
will result in cached behavior for all calls after the first.
This behavior can be configured - see [customizing the cache](/v3/develop/write-tasks#customizing-the-cache) below.

**Caching requires result persistence**Caching requires result persistence, which is off by default.
To turn on result persistence for all of your tasks use the `PREFECT_RESULTS_PERSIST_BY_DEFAULT` setting:

Copy

```
prefect config set PREFECT_RESULTS_PERSIST_BY_DEFAULT=true
```

See [managing results](/v3/develop/results) for more details on managing your result configuration, and
[settings](/v3/develop/settings-and-profiles) for more details on managing Prefect settings.

## [​](#cache-keys) Cache keys

To determine whether a task run should retrieve a cached state, Prefect uses the concept of a “cache key”.
A cache key is a computed string value that determines where the task’s return value will be persisted within
its configured result storage.
When a task run begins, Prefect first computes its cache key and uses this key to lookup a record in the task’s result
storage.
If an unexpired record is found, this result is returned and the task does not run, but instead, enters a
`Cached` state with the corresponding result value.
Cache keys can be shared by the same task across different flows, and even among different tasks,
so long as they all share a common result storage location.
By default Prefect stores results locally in `~/.prefect/storage/`.
The filenames in this directory will correspond exactly to computed cache keys from your task runs.

**Relationship with result persistence**Task caching and result persistence are intimately related. Because task caching relies on loading a
known result, task caching will only work when your task can persist its output
to a fixed and known location.Therefore any configuration which explicitly avoids result persistence will result in your task never
using a cache, for example setting `persist_result=False`.

## [​](#cache-policies) Cache policies

Cache key computation can be configured through the use of *cache policies*.
A cache policy is a recipe for computing cache keys for a given task.
Prefect comes prepackaged with a few common cache policies:

* `DEFAULT`: this cache policy uses the task’s inputs, its code definition, as well as the prevailing flow run ID
  to compute the task’s cache key.
* `INPUTS`: this cache policy uses *only* the task’s inputs to compute the cache key.
* `TASK_SOURCE`: this cache policy only considers raw lines of code in the task (and not the source code of nested tasks) to compute the cache key.
* `FLOW_PARAMETERS`: this cache policy uses *only* the parameter values provided to the parent flow run
  to compute the cache key.
* `NO_CACHE`: this cache policy always returns `None` and therefore avoids caching and result persistence altogether.

These policies can be set using the `cache_policy` keyword on the [task decorator](https://reference.prefect.io/prefect/tasks/#prefect.tasks.task).

## [​](#customizing-the-cache) Customizing the cache

Prefect allows you to configure task caching behavior in numerous ways.

### [​](#cache-expiration) Cache expiration

All cache keys can optionally be given an *expiration* through the `cache_expiration` keyword on
the [task decorator](https://reference.prefect.io/prefect/tasks/#prefect.tasks.task).
This keyword accepts a `datetime.timedelta` specifying a duration for which the cached value should be
considered valid.
Providing an expiration value results in Prefect persisting an expiration timestamp alongside the result
record for the task.
This expiration is then applied to *all* other tasks that may share this cache key.

### [​](#cache-policies-2) Cache policies

Cache policies can be composed and altered using basic Python syntax to form more complex policies.
For example, all task policies except for `NO_CACHE` can be *added* together to form new policies that combine
the individual policies’ logic into a larger cache key computation.
Combining policies in this way results in caches that are *easier* to invalidate.
For example:

Copy

```
from prefect import task
from prefect.cache_policies import TASK_SOURCE, INPUTS
@task(cache_policy=TASK_SOURCE + INPUTS)
def my_cached_task(x: int):
    return x + 42
```

This task will rerun anytime you provide new values for `x`, *or* anytime you change the underlying code.
The `INPUTS` policy is a special policy that allows you to *subtract* string values to ignore
certain task inputs:

Copy

```
from prefect import task
from prefect.cache_policies import INPUTS


my_custom_policy = INPUTS - 'debug'

@task(cache_policy=my_custom_policy)
def my_cached_task(x: int, debug: bool = False):
    print('running...')
    return x + 42


my_cached_task(1)
my_cached_task(1, debug=True) # still uses the cache
```

### [​](#cache-key-functions) Cache key functions

You can configure custom cache policy logic through the use of cache key functions.
A cache key function is a function that accepts two positional arguments:

* The first argument corresponds to the `TaskRunContext`, which stores task run metadata. For example,
  this object has attributes `task_run_id`, `flow_run_id`, and `task`, all of which can be used in your
  custom logic.
* The second argument corresponds to a dictionary of input values to the task. For example,
  if your task has the signature `fn(x, y, z)` then the dictionary will have keys “x”, “y”, and “z” with corresponding values that can be used to compute your cache key.

This function can then be specified using the `cache_key_fn` argument on
the [task decorator](https://reference.prefect.io/prefect/tasks/#prefect.tasks.task).
For example:

Copy

```
from prefect import task


def static_cache_key(context, parameters):
    # return a constant
    return "static cache key"


@task(cache_key_fn=static_cache_key)
def my_cached_task(x: int):
    return x + 1
```

### [​](#cache-storage) Cache storage

By default, cache records are collocated with task results and files containing task results will include metadata used for caching.
Configuring a cache policy with a `key_storage` argument allows cache records to be stored separately from task results.
When cache key storage is configured, persisted task results will only include the return value of your task and cache records can be deleted or modified
without effecting your task results.
You can configure where cache records are stored by using the `.configure` method with a `key_storage` argument on a cache policy.
The `key_storage` argument accepts either a path to a local directory or a storage block.

### [​](#cache-isolation) Cache isolation

Cache isolation controls how concurrent task runs interact with cache records. Prefect supports two isolation levels: `READ_COMMITTED` and `SERIALIZABLE`.
By default, cache records operate with a `READ_COMMITTED` isolation level. This guarantees that reading a cache record will see the latest committed cache value,
but allows multiple executions of the same task to occur simultaneously.
For stricter isolation, you can use the `SERIALIZABLE` isolation level. This ensures that only one execution of a task occurs at a time for a given cache
record via a locking mechanism.
To configure the isolation level, use the `.configure` method with an `isolation_level` argument on a cache policy. When using `SERIALIZABLE`, you must
also provide a `lock_manager` that implements locking logic for your system.

#### [​](#recommended-lock-managers-by-execution-context) Recommended Lock Managers by Execution Context

We recommend using a locking implementation that matches how you are running your work concurrently.

| Execution Context | Recommended Lock Manager | Notes |
| --- | --- | --- |
| Threads/Coroutines | `MemoryLockManager` | In-memory locking suitable for single-process execution |
| Processes | `FileSystemLockManager` | File-based locking for multiple processes on same machine |
| Multiple Machines | `RedisLockManager` | Distributed locking via Redis for cross-machine coordination |

## [​](#multi-task-caching) Multi-task caching

There are some situations in which multiple tasks need to always run together or not at all.
This can be achieved in Prefect by configuring these tasks to always write to their caches within
a single [*transaction*](/v3/develop/transactions).

Was this page helpful?

YesNo

[Assets](/v3/concepts/assets)[States](/v3/concepts/states)

⌘I