Rate limits and data retention - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Prefect Cloud

Rate limits and data retention

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

* [API rate limits](#api-rate-limits)
* [Request limits by plan](#request-limits-by-plan)
* [Query limits](#query-limits)
* [Metadata retention](#metadata-retention)
* [Retention periods by plan](#retention-periods-by-plan)

## [​](#api-rate-limits) API rate limits

**Rate limits are subject to change.**Contact Prefect support at [help@prefect.io](mailto:help@prefect.io) with questions about rate limits.

Prefect Cloud applies rate limits to API endpoints to ensure system stability. When limits are exceeded, endpoints return a `429` response with a `Retry-After` header.

### [​](#request-limits-by-plan) Request limits by plan

The `flow_runs`, `task_runs`, and `flows` endpoints and their subroutes:

* **Hobby**: 250 requests per minute
* **Starter**: 500 requests per minute
* **Team**: 1,000 requests per minute
* **Pro**: 2,000 requests per minute
* **Enterprise**: Custom limits

The `logs` endpoint:

* **Hobby**: 500 logs per minute
* **Starter**: 1,600 logs per minute
* **Team**: 2,000 logs per minute
* **Pro**: 10,000 logs per minute
* **Enterprise**: Custom limits

The Prefect SDK automatically retries rate-limited requests up to 5 times, using the delay specified in the `Retry-After` header. You can customize this behavior through [client settings](/v3/develop/settings-ref#clientsettings).

## [​](#query-limits) Query limits

Event queries are limited to a 14-day window per request. You can query any 14-day period within your retention period, but each individual query cannot span more than 14 days. If your plan’s retention period is shorter than 14 days, the query window is limited to your retention period.

## [​](#metadata-retention) Metadata retention

Prefect Cloud retains flow run, task run, and artifact metadata for a limited time based on your plan. This applies to all workspaces in your account.

### [​](#retention-periods-by-plan) Retention periods by plan

* **Hobby and Starter**: 7 days
* **Team**: 14 days
* **Pro**: 30 days
* **Enterprise**: Custom retention periods

Metadata is retained from creation until the specified period expires. For flow and task runs, retention is calculated from when the run reaches a [terminal state](/v3/develop/manage-states#state-types). Subflow runs are retained independently from their parent flows.
For custom retention periods, [contact Prefect’s sales team](https://www.prefect.io/pricing).

Was this page helpful?

YesNo

[Event triggers](/v3/concepts/event-triggers)[SLAs](/v3/concepts/slas)

⌘I