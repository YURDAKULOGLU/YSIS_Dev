Tag-based concurrency limits - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

Tag-based concurrency limits

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

* [How tag-based limits work](#how-tag-based-limits-work)
* [Execution behavior](#execution-behavior)
* [Use cases](#use-cases)

Tag-based concurrency limits prevent too many tasks from running simultaneously by using [task tags](/v3/how-to-guides/workflows/tag-based-concurrency-limits). You can specify a maximum number of concurrent task runs in a `Running` state for tasks with a given tag.

As of Prefect 3.4.19, tag-based concurrency limits are backed by [global concurrency limits](/v3/concepts/global-concurrency-limits). When you create a tag-based limit, Prefect automatically creates a corresponding global concurrency limit with the name `tag:{tag_name}`. This implementation detail is generally transparent to users, but you may see these global limits in your UI or API responses.

## [​](#how-tag-based-limits-work) How tag-based limits work

If a task has multiple tags, it will run only if ***all*** tags have available concurrency.
Tags without specified concurrency limits are treated as unlimited. Setting a tag’s concurrency limit to 0 causes immediate abortion of any task runs with that tag, rather than delaying them.

Tag-based task concurrency is different from manually created global concurrency limits, though they can be used to achieve similar outcomes. Global concurrency limits are a more general way to control concurrency for any Python-based operation, whereas tag-based concurrency limits are specific to Prefect tasks.

## [​](#execution-behavior) Execution behavior

Task tag limits are checked whenever a task run attempts to enter a `Running` state.
If there are no concurrency slots available for any one of your task’s tags, it delays the transition to a `Running` state and instructs the client to try entering a `Running` state again in 30 seconds (or the value specified by the `PREFECT_TASK_RUN_TAG_CONCURRENCY_SLOT_WAIT_SECONDS` setting).

## [​](#use-cases) Use cases

Tag-based concurrency limits are useful when you have tasks that interact with shared resources. For example:

* **Database connections**: If many tasks across multiple flows interact with a database that only allows 10 connections, you can tag all database tasks with `database` and set a limit of 10.
* **API rate limiting**: Tasks that call external APIs can be tagged and limited to respect rate limits.
* **Resource contention**: Tasks that use memory-intensive operations can be limited to prevent system overload.

Was this page helpful?

YesNo

[Global concurrency limits](/v3/concepts/global-concurrency-limits)[Deployments](/v3/concepts/deployments)

⌘I