Artifacts - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

Artifacts

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

* [Artifact types](#artifact-types)

Prefect artifacts:

* are visually rich annotations on flow and task runs
* are human-readable visual metadata defined in code
* come in standardized formats such as tables, progress indicators, images, Markdown, and links
* are stored in Prefect Cloud or Prefect server and rendered in the Prefect UI
* make it easy to visualize outputs or side effects that your runs produce, and capture updates over time

![Markdown artifact sales report screenshot](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/md-artifact-info.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=0daffdebede0bcf508172cd503fbe873)
Common use cases for artifacts include:

* **Progress** indicators: Publish progress indicators for long-running tasks. This helps monitor the progress of your tasks and flows and ensure they are running as expected.
* **Debugging**: Publish data that you care about in the UI to easily see when and where your results were written. If an artifact doesn’t look the way you expect, you can find out which flow run last updated it, and you can click through a link in the artifact to a storage location (such as an S3 bucket).
* **Data quality checks**: Publish data quality checks from in-progress tasks to ensure that data quality is maintained throughout a pipeline. Artifacts make for great performance graphs. For example, you can visualize a long-running machine learning model training run. You can also track artifact versions, making it easier to identify changes in your data.
* **Documentation**: Publish documentation and sample data to help you keep track of your work and share information.
  For example, add a description to signify why a piece of data is important.

## [​](#artifact-types) Artifact types

There are five artifact types:

* links
* Markdown
* progress
* images
* tables

Each artifact created within a task is displayed individually in the Prefect UI.
This means that each call to `create_link_artifact()` or `create_markdown_artifact()` generates a distinct artifact.Unlike the Python `print()` function (where you can concatenate multiple calls to include additional items in a report),
these artifact creation functions must be called multiple times, if necessary.To create artifacts such as reports or summaries using `create_markdown_artifact()`, define your message string
and then pass it to `create_markdown_artifact()` to create the artifact.

For more information on how to create and use artifacts, see the [how to produce workflow artifacts](/v3/how-to-guides/workflows/artifacts) guide.

Was this page helpful?

YesNo

[Runtime context](/v3/concepts/runtime-context)[Task runners](/v3/concepts/task-runners)

⌘I