Prefect server - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Configuration

Prefect server

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

* [The Prefect database](#the-prefect-database)
* [Database migrations](#database-migrations)
* [How to guides](#how-to-guides)

After installing Prefect, you have a Python SDK client that can communicate with either [Prefect Cloud](/v3/how-to-guides/cloud/connect-to-cloud) or a self-hosted Prefect server, backed by a database and a UI.
Prefect Cloud and self-hosted Prefect server share a common set of capabilities. Prefect Cloud provides the additional features required by organizations such as RBAC, Audit logs, and SSO. See the [Prefect Cloud overview](/v3/how-to-guides/cloud/connect-to-cloud) for more information.

We recommend using the same version of `prefect` for the client and server.
Old clients are compatible with new servers, but new clients can be incompatible with old servers as new fields are added to the REST API.
The server will typically return a 422 status code if any issues occur.

## [​](#the-prefect-database) The Prefect database

The Prefect database persists data to track the state of your flow runs and related Prefect concepts, including:

* Flow run and task run state
* Run history
* Logs
* Deployments
* Flow and task run concurrency limits
* Storage blocks for flow and task results
* Variables
* Artifacts
* Work pool status
* Events
* Automations

Prefect supports the following databases:

* **SQLite** (default): Recommended for lightweight, single-server deployments. SQLite requires essentially no setup.
* **PostgreSQL**: Best for production use, high availability, and multi-server deployments. Requires PostgreSQL 14.9 or higher. Prefect uses the [`pg_trgm`](https://www.postgresql.org/docs/current/pgtrgm.html) extension, so it must be installed and enabled.

## [​](#database-migrations) Database migrations

Prefect uses [Alembic](https://alembic.sqlalchemy.org/en/latest/) to manage database migrations. Alembic is a database migration tool that provides a framework for generating and applying schema changes to a database.
When you start a Prefect server, it automatically runs any necessary migrations. You can also manage migrations manually using the CLI.

## [​](#how-to-guides) How to guides

* [Self-host via CLI](/v3/how-to-guides/self-hosted/server-cli) - Start a local server instance
* [Self-host via Docker](/v3/how-to-guides/self-hosted/server-docker) - Run server in containers
* [Scale self-hosted Prefect](/v3/advanced/self-hosted) - Deploy multiple server instances for high availability

Was this page helpful?

YesNo

[Settings and profiles](/v3/concepts/settings-and-profiles)[Events](/v3/concepts/events)

⌘I