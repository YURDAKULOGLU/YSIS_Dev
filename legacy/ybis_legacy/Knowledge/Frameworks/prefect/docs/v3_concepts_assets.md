Assets - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

Assets

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

* [Core concepts](#core-concepts)
* [Asset lifecycle](#asset-lifecycle)
* [Materializations](#materializations)
* [References](#references)
* [Metadata](#metadata)
* [Dependency modeling](#dependency-modeling)
* [Asset metadata and properties](#asset-metadata-and-properties)
* [Asset health monitoring](#asset-health-monitoring)
* [Event emission and integration](#event-emission-and-integration)
* [Event types](#event-types)
* [Event emission rules](#event-emission-rules)
* [Event payloads](#event-payloads)
* [Asset organization and discovery](#asset-organization-and-discovery)
* [Further Reading](#further-reading)

Assets in Prefect represent any outcome or output of your Prefect workflows. They provide an interface to model all forms of data and model lineage, track dependencies between data transformations, and monitor the health of pipelines at the asset level rather than just the compute level.

## [​](#core-concepts) Core concepts

An asset is fundamentally defined by its **key**, a URI that uniquely identifies an asset, often specifying an external storage system in which that asset lives.
Asset keys serve as both identifiers and organizational structures—assets are automatically grouped by their URI scheme (e.g., `s3://`, `postgres://`, `snowflake://`) and can be hierarchically organized based on their path structure.
Assets exist in three primary states within Prefect:

* **Materialized**: The asset has been created, updated, or overwritten by a Prefect workflow
* **Referenced**: The asset is consumed as input by a workflow but not produced by it
* **External**: The asset exists outside the Prefect ecosystem but is referenced as a dependency

## [​](#asset-lifecycle) Asset lifecycle

### [​](#materializations) Materializations

A **materialization** occurs when a workflow mutates an asset through creation, updating, or overwriting. Materializations are declared using the `@materialize` decorator, which functions as a specialized task decorator that tracks asset creation intent.
The materialization process operates on an “intent to materialize” model: when a function decorated with `@materialize` executes, Prefect records the materialization attempt. Success or failure of the materialization is determined by the underlying task’s execution state.

Copy

```
from prefect.assets import materialize

@materialize("s3://data-lake/processed/customer-data.csv")
def process_customer_data():
    # Asset materialization logic
    pass
```

### [​](#references) References

A **reference** occurs when an asset appears as an upstream dependency in another asset’s materialization. References are automatically inferred from the task execution graph—when the output of one materialization flows as input to another, the dependency relationship is captured.
References can also be explicitly declared through the `asset_deps` parameter, which is particularly useful for modeling dependencies on external systems or when the task graph alone doesn’t fully capture the data dependencies.

### [​](#metadata) Metadata

Asset definitions include optional metadata about that asset. These asset properties should have one source of truth to avoid conflicts. When you materialize an asset with properties, those properties perform a complete overwrite of all metadata fields for that asset.
Updates to asset metadata occur at runtime from any workflow that specifies metadata fields.

## [​](#dependency-modeling) Dependency modeling

Asset dependencies are determined through two complementary mechanisms:
**Task graph inference**: When materialized assets flow through task parameters, Prefect automatically constructs the dependency graph. Each materialization acts as a dependency accumulation point, gathering all upstream assets and serving as the foundation for downstream materializations.
**Explicit declaration**: The `asset_deps` parameter allows direct specification of asset dependencies, enabling modeling of relationships that aren’t captured in the task execution flow.

Copy

```
from prefect.assets import materialize


@materialize(
    "s3://warehouse/enriched-data.csv",
    asset_deps=["postgres://db/reference-tables", "s3://external/vendor-data.csv"]
)
def enrich_data():
    # Explicitly depends on external database and vendor data
    pass
```

The backend will track these dependencies *across workflow boundaries*, exposing a global view of asset dependencies within your workspace.

## [​](#asset-metadata-and-properties) Asset metadata and properties

Assets support rich metadata through the `AssetProperties` class, which provides organizational context and improves discoverability:

* **Name**: Human-readable identifier for the asset
* **Description**: Detailed documentation supporting Markdown formatting
* **Owners**: Responsible parties, with special UI treatment for Prefect users and teams
* **URL**: Web location for accessing or viewing the asset

Additionally, assets support dynamic metadata through the `add_asset_metadata()` function, allowing runtime information like row counts, processing times, and data quality metrics to be attached to materialization events.

## [​](#asset-health-monitoring) Asset health monitoring

Currently asset health provides a *visual* indicator of the operational status of data artifacts based on their most recent materialization attempt:

* **Green**: Last materialization succeeded
* **Red**: Last materialization failed
* **Gray**: No materialization recorded, or asset has only been referenced

This health model enables data teams to quickly identify problematic data pipelines at the artifact level, complementing traditional task-level monitoring with data-centric observability. Soon these statuses will be backed by a corresponding event.

## [​](#event-emission-and-integration) Event emission and integration

Assets integrate deeply with Prefect’s event system, automatically emitting structured events that enable downstream automation and monitoring:

### [​](#event-types) Event types

* **Materialization events**: These events look like `prefect.asset.materialization.{succeeded|failed}` and are emitted when assets are referenced by the `@materialize` decorator, with status determined by the underlying task execution state.
* **Reference events**: These events look like `prefect.asset.referenced` and are emitted for all upstream assets when a materialization occurs, independent of success or failure.

### [​](#event-emission-rules) Event emission rules

Asset events follow specific emission patterns based on task execution state:

* **Completed states**: Emit `prefect.asset.materialization.succeeded` for downstream assets and `prefect.asset.referenced` for upstream assets
* **Failed states**: Emit `prefect.asset.materialization.failed` for downstream assets and `prefect.asset.referenced` for upstream assets
* **Cached states**: No asset events are emitted, as cached executions don’t represent new asset state changes

Reference events are always emitted for upstream assets regardless of materialization success, enabling comprehensive dependency tracking even when downstream processes fail.

### [​](#event-payloads) Event payloads

Materialization events include any metadata added during task execution through `add_asset_metadata()`, while reference events contain basic asset identification information. This enables rich event-driven automation based on both asset state changes and associated metadata.

## [​](#asset-organization-and-discovery) Asset organization and discovery

Assets are automatically organized in the Prefect UI based on their URI structure:

* **Grouping by scheme**: Assets with the same URI scheme (e.g., `s3://`, `postgres://`) are grouped together
* **Hierarchical organization**: URI paths create nested organization structures
* **Search and filtering**: Asset metadata enables discovery through names, descriptions, and ownership information

## [​](#further-reading) Further Reading

* [How to use assets to track workflow outputs](/v3/how-to-guides/workflows/assets)
* [How to customize asset metadata](/v3/advanced/assets)

Was this page helpful?

YesNo

[Tasks](/v3/concepts/tasks)[Caching](/v3/concepts/caching)

⌘I