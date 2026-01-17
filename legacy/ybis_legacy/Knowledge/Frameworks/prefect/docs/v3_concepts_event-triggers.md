Define event triggers - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Automations

Define event triggers

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

* [Event triggers](#event-triggers)
* [Resource matching](#resource-matching)
* [Example](#example)
* [Expected events](#expected-events)
* [Evaluation strategy](#evaluation-strategy)
* [Metric triggers](#metric-triggers)
* [Composite triggers](#composite-triggers)
* [Support for event trigger types](#support-for-event-trigger-types)
* [Further reading](#further-reading)

When you need a trigger beyond what the templates in the UI trigger builder provide, you can define a custom trigger in JSON. With custom triggers, you have access to the full capabilities of Prefect’s automation system—allowing you to react to many kinds of events and metrics in your workspace.
Each automation has a single trigger that, when fired, causes all of its associated actions to run. That single
trigger may be a reactive or proactive event trigger, a trigger monitoring the value of a metric, or a composite trigger
that combines several underlying triggers.
You can manage events with the Terraform provider for Prefect.
You can manage events with the Prefect API.

### [​](#event-triggers) Event triggers

Event triggers are the most common type of trigger. They are intended to react to the presence or absence of an event.
Event triggers are indicated with `{"type": "event"}`.
![Viewing a custom trigger for automations in the UI](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/automations-custom.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=3730bde404e00cd0da5c0d1f8f1875a4)
This is the schema that defines an event trigger:

| Name | Type | Supports wildcards and negative matching | Description |
| --- | --- | --- | --- |
| **match** | object | ✅ | Labels for resources which this Automation will match. Supports trailing wildcards (`*`) and negative matching (`!`). |
| **match\_related** | object OR array of object | ✅ | Labels for related resources which this Automation will match. Supports trailing wildcards (`*`) and negative matching (`!`). |
| **posture** | string enum | N/A | The posture of this Automation, either Reactive or Proactive. Reactive automations respond to the presence of the expected events, while Proactive automations respond to the absence of those expected events. |
| **after** | array of strings | ✅ | Event(s), one of which must have first been seen to start this automation. |
| **expect** | array of strings | ✅ | The event(s) this automation expects to see. If empty, this automation will evaluate any matched event. |
| **for\_each** | array of strings | ❌ | Evaluate the Automation separately for each distinct value of these labels on the resource. By default, labels refer to the primary resource of the triggering event. You may also refer to labels from related resources by specifying `related:<role>:<label>`. This will use the value of that label for the first related resource in that role. |
| **threshold** | integer | N/A | The number of events required for this Automation to trigger (for Reactive automations), or the number of events expected (for Proactive automations) |
| **within** | number | N/A | The time period over which the events must occur. For Reactive triggers, this may be as low as 0 seconds, but must be at least 10 seconds for Proactive triggers. |

### [​](#resource-matching) Resource matching

Both the `event` and `metric` triggers support matching events for specific resources in your workspace, including most
Prefect objects (like flows, deployment, blocks, work pools, tags) as well as resources you have defined in any
events you emit yourself.
The `match` and `match_related` fields control which events a trigger considers for evaluation
by filtering on the contents of their `resource` and `related` fields, respectively. Each label added to a `match` filter
is `AND`ed with the other labels, and can accept a single value or a list of multiple values that are `OR`ed together.

#### [​](#example) Example

See the `resource` and `related` fields on the following `prefect.flow-run.Completed` event, truncated for this example.
Its primary resource is a flow run, and since that flow run was started by a deployment, it is related to both its flow and its deployment:

Copy

```
"resource": {
  "prefect.resource.id": "prefect.flow-run.925eacce-7fe5-4753-8f02-77f1511543db",
  "prefect.resource.name": "cute-kittiwake"
}
"related": [
  {
    "prefect.resource.id": "prefect.flow.cb6126db-d528-402f-b439-96637187a8ca",
    "prefect.resource.role": "flow",
    "prefect.resource.name": "hello"
  },
  {
    "prefect.resource.id": "prefect.deployment.37ca4a08-e2d9-4628-a310-cc15a323378e",
    "prefect.resource.role": "deployment",
    "prefect.resource.name": "example"
  },
  {
    "prefect.resource.id": "prefect.work-pool.a67da06b-9427-4a0f-a709-c3b37ac29cbf",
    "prefect.resource.role": "work-pool",
    "prefect.resource.name": "k8s-pool",
    "prefect.work-pool.type": "kubernetes"
  },
  {
    "prefect.resource.id": "prefect.tag.examples",
    "prefect.resource.role": "tag"
  }
]
```

There are a number of valid ways to select the above event for evaluation, and the approach depends on the purpose of
the automation.
The following configuration filters for any events whose primary resource is a flow run, *and* that flow run has a
name starting with `cute-` or `radical-`.

Copy

```
"match": {
  "prefect.resource.id": "prefect.flow-run.*",
  "prefect.resource.name": ["cute-*", "radical-*"]
},
"match_related": {},
...
```

By comparison, this configuration filters for any events this specific deployment is a related
resource to:

Copy

```
"match": {},
"match_related": {
  "prefect.resource.id": "prefect.deployment.37ca4a08-e2d9-4628-a310-cc15a323378e"
},
...
```

Both of the above approaches will select the example `prefect.flow-run.Completed` event, but will permit additional,
possibly undesired events through the filter as well. You can combine `match` and `match_related` for more restrictive
filtering:

Copy

```
"match": {
  "prefect.resource.id": "prefect.flow-run.*",
  "prefect.resource.name": ["cute-*", "radical-*"]
},
"match_related": {
  "prefect.resource.id": "prefect.deployment.37ca4a08-e2d9-4628-a310-cc15a323378e"
},
...
```

Now this trigger will filter only for events whose primary resource is a flow run started by a specific deployment,
*and* that flow run has a name starting with `cute-` or `radical-`.

##### Advanced matching for related resources

`match_related` also supports an array of objects, each of which can contain multiple labels.
This allows for more complex matching on related resources, such as filtering for events that are related to a specific work pool or tag.
To match flow runs on a work pool with specific tags, you can use the following configuration:

Copy

```
"match": {
  "prefect.resource.id": "prefect.flow-run.*",
},
"match_related": [
    {
        "prefect.resource.name": "k8s-pool",
        "prefect.resource.role": "work-pool"
    },
    {
        "prefect.resource.id": "prefect.tag.examples",
        "prefect.resource.role": "tag"
    }
]
...
```

##### Negative matching

Use the `!` prefix to exclude resources with specific label values. This allows you to filter out
events you don’t want to trigger automations.
For example, to match all flow runs *except* those tagged with `dev`:

Copy

```
"match": {
  "prefect.resource.id": "prefect.flow-run.*"
},
"match_related": {
  "prefect.resource.id": "!prefect.tag.dev",
  "prefect.resource.role": "tag"
}
```

You can combine positive and negative patterns in the same label. The following matches flow runs
with names starting with `production-` but NOT `production-test-`:

Copy

```
"match": {
  "prefect.resource.id": "prefect.flow-run.*",
  "prefect.resource.name": ["production-*", "!production-test-*"]
}
```

Combining multiple related resource conditions with exclusions:

Copy

```
"match": {
  "prefect.resource.id": "prefect.flow-run.*"
},
"match_related": [
  {
    "prefect.resource.name": "k8s-pool",
    "prefect.resource.role": "work-pool"
  },
  {
    "prefect.resource.id": "prefect.tag.production",
    "prefect.resource.role": "tag"
  },
  {
    "prefect.resource.id": "!prefect.tag.test",
    "prefect.resource.role": "tag"
  }
]
```

This configuration matches flow runs that:

* Run on the `k8s-pool` work pool
* Are tagged with `production`
* Are NOT tagged with `test`

### [​](#expected-events) Expected events

Once an event has passed through the `match` filters, you must decide if this event counts toward the
trigger’s `threshold`. That is determined by the event names present in `expect`.
This configuration informs the trigger to evaluate *only* `prefect.flow-run.Completed` events that have passed the
`match` filters.

Copy

```
"expect": [
  "prefect.flow-run.Completed"
],
...
```

`threshold` decides the quantity of `expect`ed events needed to satisfy the trigger. Increasing the `threshold`
above 1 requires use of `within` to define a range of time when multiple events are seen. The following
configuration expects two occurrences of `prefect.flow-run.Completed` within 60 seconds:

Copy

```
"expect": [
  "prefect.flow-run.Completed"
],
"threshold": 2,
"within": 60,
...
```

Use `after` to handle scenarios that require more complex event reactivity.
For example, this flow emits an event indicating the table it operates on is missing or empty:

Copy

```
from prefect import flow
from prefect.events import emit_event
from myproject.db import Table


@flow
def transform(table_name: str):
  table = Table(table_name)

  if not table.exists():
    emit_event(
        event="table-missing",
        resource={"prefect.resource.id": "etl-events.transform"}
    )
  elif table.is_empty():
    emit_event(
        event="table-empty",
        resource={"prefect.resource.id": "etl-events.transform"}
    )
  else:
    # transform data
    ...
```

The following configuration uses `after` to prevent this automation from firing unless either a `table-missing` or a
`table-empty` event has occurred before a flow run of this deployment completes.

Note how `match` and `match_related` ensure the trigger only evaluates events that are relevant to its
purpose.

Copy

```
"match": {
  "prefect.resource.id": [
    "prefect.flow-run.*",
    "etl-events.transform"
  ]
},
"match_related": {
  "prefect.resource.id": "prefect.deployment.37ca4a08-e2d9-4628-a310-cc15a323378e"
}
"after": [
  "table-missing",
  "table-empty"
]
"expect": [
  "prefect.flow-run.Completed"
],
...
```

### [​](#evaluation-strategy) Evaluation strategy

All of the previous examples were designed around a reactive `posture`; that is, count up events toward the
`threshold` until it is met, then execute actions. To respond to the absence of events, use a proactive `posture`.
A proactive trigger fires when its `threshold` has *not* been met by the end of the window of time defined by `within`.
Proactive triggers must have a `within` value of at least 10 seconds.
The following trigger fires if a `prefect.flow-run.Completed` event is not seen within 60 seconds after a
`prefect.flow-run.Running` event is seen:

Copy

```
{
  "match": {
    "prefect.resource.id": "prefect.flow-run.*"
  },
  "match_related": {},
  "after": [
    "prefect.flow-run.Running"
  ],
  "expect": [
    "prefect.flow-run.Completed"
  ],
  "for_each": [],
  "posture": "Proactive",
  "threshold": 1,
  "within": 60
}
```

However, without `for_each`, a `prefect.flow-run.Completed` event from a *different* flow run than the one that
started this trigger with its `prefect.flow-run.Running` event could satisfy the condition. Adding a `for_each` of
`prefect.resource.id` causes this trigger to be evaluated separately for each flow run id associated with these events.

Copy

```
{
  "match": {
    "prefect.resource.id": "prefect.flow-run.*"
  },
  "match_related": {},
  "after": [
    "prefect.flow-run.Running"
  ],
  "expect": [
    "prefect.flow-run.Completed"
  ],
  "for_each": [
    "prefect.resource.id"
  ],
  "posture": "Proactive",
  "threshold": 1,
  "within": 60
}
```

### [​](#metric-triggers) Metric triggers

Metric triggers (`{"type": "metric"}`) fire when the value of a metric in your workspace crosses a threshold you defined.
For example, you can trigger an automation when the success rate of flows in your workspace drops below 95% over the course
of an hour.
Prefect’s metrics are all derived by examining your workspace’s events, and if applicable, use the `occurred` times of
those events as the basis for their calculations.
Prefect defines three metrics:

* **Successes** (`{"name": "successes"}`), defined as the number of flow runs that went `Pending` and then the latest
  state we saw was not a failure (`Failed` or `Crashed`). This metric accounts for retries if the ultimate state was
  successful.
* **Duration** (`{"name": "duration"}`), defined as the *length of time* that a flow remains in a `Running` state before
  transitioning to a terminal state such as `Completed`, `Failed`, or `Crashed`. Because this time is derived in terms of
  flow run state change events, it may be greater than the runtime of your function.
* **Lateness** (`{"name": "lateness"}`), defined as the *length of time* that a `Scheduled` flow remains in a `Late`
  state before transitioning to a `Running` and/or `Crashed` state. Only flow runs that the system marks `Late` are included.

This is the schema of a metric trigger:

| Name | Type | Supports trailing wildcards | Description |
| --- | --- | --- | --- |
| **match** | object | ✅ | Labels for resources which this Automation will match. |
| **match\_related** | object OR array of object | ✅ | Labels for related resources which this Automation will match. |
| **metric** | `MetricTriggerQuery` | N/A | The definition of the metric query to run. |

And the `MetricTriggerQuery` query is defined as:

| Name | Type | Description |
| --- | --- | --- |
| **name** | string | The name of the Prefect metric to evaluate (see above). |
| **threshold** | number | The threshold the current metric value is compared to. |
| **operator** | string (`"<"`, `"<="`, `">"`, `">="`) | The comparison operator to use to decide if the threshold value is met. |
| **range** | duration in seconds | How far back to evaluate the metric. |
| **firing\_for** | duration in seconds | How long the value must exceed the threshold before this trigger fires. |

For example, to fire when flow runs tagged `production` in your workspace are failing at a rate of 10% or worse for the last hour (in other words, your success rate is below 90%), create this trigger:

Copy

```
{
  "type": "metric",
  "match": {
    "prefect.resource.id": "prefect.flow-run.*"
  },
  "match_related": {
    "prefect.resource.id": "prefect.tag.production",
    "prefect.resource.role": "tag"
  },
  "metric": {
    "name": "successes",
    "threshold": 0.9,
    "operator": "<",
    "range": 3600,
    "firing_for": 0
  }
}
```

To detect when the average lateness of your Kubernetes workloads (running on a work pool named `kubernetes`) in the
last day exceeds five minutes late—and that number hasn’t gotten better for the last 10 minutes—use a trigger like this:

Copy

```
{
  "type": "metric",
  "match": {
    "prefect.resource.id": "prefect.flow-run.*"
  },
  "match_related": {
    "prefect.resource.id": "prefect.work-pool.kubernetes",
    "prefect.resource.role": "work-pool"
  },
  "metric": {
    "name": "lateness",
    "threshold": 300,
    "operator": ">",
    "range": 86400,
    "firing_for": 600
  }
}
```

### [​](#composite-triggers) Composite triggers

To create a trigger from multiple kinds of events and metrics, use a `compound` or `sequence` trigger.
These higher-order triggers are composed from a set of underlying `event` and `metric` triggers.
For example, if you want to run a deployment only after three different flows in your workspace have written their
results to a remote filesystem, combine them with a ‘compound’ trigger:

Copy

```
{
  "type": "compound",
  "require": "all",
  "within": 3600,
  "triggers": [
    {
      "type": "event",
      "posture": "Reactive",
      "expect": ["prefect.block.remote-file-system.write_path.called"],
      "match_related": {
        "prefect.resource.name": "daily-customer-export",
        "prefect.resource.role": "flow"
      }
    },
    {
      "type": "event",
      "posture": "Reactive",
      "expect": ["prefect.block.remote-file-system.write_path.called"],
      "match_related": {
        "prefect.resource.name": "daily-revenue-export",
        "prefect.resource.role": "flow"
      }
    },
    {
      "type": "event",
      "posture": "Reactive",
      "expect": ["prefect.block.remote-file-system.write_path.called"],
      "match_related": {
        "prefect.resource.name": "daily-expenses-export",
        "prefect.resource.role": "flow"
      }
    }
  ]
}
```

This trigger fires once it sees at least one of each of the underlying event triggers fire within the time
frame specified. Then the trigger resets its state and fires the next time these three events all happen.
The order the events occur doesn’t matter, just that all of the events occur within one hour.
If you want a flow run to complete prior to starting to watch for those three events, you can combine the entire
previous trigger as the second part of a sequence of two triggers:

Copy

```
{
  // the outer trigger is now a "sequence" trigger
  "type": "sequence",
  "within": 7200,
  "triggers": [
    // with the first child trigger expecting a Completed event
    {
      "type": "event",
      "posture": "Reactive",
      "expect": ["prefect.flow-run.Completed"],
      "match_related": {
        "prefect.resource.name": "daily-export-initiator",
        "prefect.resource.role": "flow"
      }
    },
    // and the second child trigger being the compound trigger from the prior example
    {
      "type": "compound",
      "require": "all",
      "within": 3600,
      "triggers": [
        {
          "type": "event",
          "posture": "Reactive",
          "expect": ["prefect.block.remote-file-system.write_path.called"],
          "match_related": {
            "prefect.resource.name": "daily-customer-export",
            "prefect.resource.role": "flow"
          }
        },
        {
          "type": "event",
          "posture": "Reactive",
          "expect": ["prefect.block.remote-file-system.write_path.called"],
          "match_related": {
            "prefect.resource.name": "daily-revenue-export",
            "prefect.resource.role": "flow"
          }
        },
        {
          "type": "event",
          "posture": "Reactive",
          "expect": ["prefect.block.remote-file-system.write_path.called"],
          "match_related": {
            "prefect.resource.name": "daily-expenses-export",
            "prefect.resource.role": "flow"
          }
        }
      ]
    }
  ]
}
```

In this case, the trigger only fires if it sees the `daily-export-initiator` flow complete, and then the three
files written by the other flows.
The `within` parameter for compound and sequence triggers restricts how close in time (in seconds) the child triggers
must fire to satisfy the composite trigger. For example, if the `daily-export-initiator` flow runs, but the other three
flows don’t write their result files until three hours later, this trigger won’t fire. Placing these time constraints
on the triggers can prevent a misfire if you know that the events will generally happen within a specific timeframe—
and you don’t want a stray older event included in the evaluation of the trigger.
If this isn’t a concern for you, you may omit the `within` period, in which case there is no limit to how far apart in time the child triggers occur.
You can compose any type of trigger into higher-order composite triggers, including proactive event triggers and metric
triggers. In the following example, the compound trigger fires if any of the following events occur: a flow run
stuck in `Pending`, a work pool becoming unready, or the average amount of `Late` work in your workspace going over
10 minutes:

Copy

```
{
  "type": "compound",
  "require": "any",
  "triggers": [
    {
      "type": "event",
      "posture": "Proactive",
      "after": ["prefect.flow-run.Pending"],
      "expect": ["prefect.flow-run.Running", "prefect.flow-run.Crashed"],
      "for_each": ["prefect.resource.id"],
      "match_related": {
        "prefect.resource.name": "daily-customer-export",
        "prefect.resource.role": "flow"
      }
    },
    {
      "type": "event",
      "posture": "Reactive",
      "expect": ["prefect.work-pool.not-ready"],
      "match": {
        "prefect.resource.name": "kubernetes-workers",
      }
    },
    {
      "type": "metric",
      "metric": {
        "name": "lateness",
        "operator": ">",
        "threshold": 600,
        "range": 3600,
        "firing_for": 300
      }
    }
  ]
}
```

For compound triggers, the `require` parameter may be `"any"`, `"all"`, or a number between 1 and the number of child
triggers. In the example above, if you feel that you are receiving too many spurious notifications for issues that
resolve on their own, you can specify `{"require": 2}` to express that any **two** of the triggers must fire in order
for the compound trigger to fire. Sequence triggers, on the other hand, always require all of their child triggers to
fire before they fire.
Compound triggers are defined as:

| Name | Type | Description |
| --- | --- | --- |
| **require** | number, `"any"`, or `"all"` | The number of child triggers that must fire for this trigger to fire |
| **within** | time, in seconds | How close in time the child triggers must fire for this trigger to fire |
| **triggers** | array of other triggers |  |

Sequence triggers are defined as:

| Name | Type | Description |
| --- | --- | --- |
| **within** | time, in seconds | How close in time the child triggers must fire for this trigger to fire |
| **triggers** | array of other triggers |  |

### [​](#support-for-event-trigger-types) Support for event trigger types

| Feature | Prefect Open Source | Prefect Cloud |
| --- | --- | --- |
| Event Triggers | ✅ | ✅ |
| Composite Triggers (Compound & Sequence) | ✅ | ✅ |
| Metric Triggers | ❌ | ✅ |

### [​](#further-reading) Further reading

* [How to create automations](/v3/how-to-guides/automations/creating-automations)
* [How to create webhooks](/v3/how-to-guides/cloud/create-a-webhook)

Was this page helpful?

YesNo

[Automations](/v3/concepts/automations)[Rate limits and data retention](/v3/concepts/rate-limits)

⌘I