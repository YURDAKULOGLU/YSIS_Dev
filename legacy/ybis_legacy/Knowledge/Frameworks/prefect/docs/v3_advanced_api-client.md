How to use and configure the API client - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Extensibility

How to use and configure the API client

[Getting Started](/v3/get-started)[Concepts](/v3/concepts)[How-to Guides](/v3/how-to-guides)[Advanced](/v3/advanced)[Examples](/v3/examples)[Integrations](/integrations/integrations)[API Reference](/v3/api-ref)[Contribute](/contribute)[Release Notes](/v3/release-notes)

* [Overview](/v3/advanced)

##### Workflows

* [Customize asset metadata](/v3/advanced/assets)
* [Customize caching behavior](/v3/advanced/caching)
* [Customize logging](/v3/advanced/logging-customization)
* [Write transactional workflows](/v3/advanced/transactions)
* [Workflow cancellation](/v3/advanced/cancel-workflows)
* [Write interactive workflows](/v3/advanced/interactive)
* [Configure UI forms for validating workflow inputs](/v3/advanced/form-building)
* [Persist workflow results](/v3/advanced/results)
* [Deploy a web app powered by background tasks](/v3/advanced/background-tasks)

##### Automations

* [Detect Zombie Flows](/v3/advanced/detect-zombie-flows)
* [Emit and Use Custom Events](/v3/advanced/use-custom-event-grammar)

##### Workflow Infrastructure

* [Worker Healthchecks](/v3/advanced/worker-healthchecks)
* [Daemonize Worker Processes](/v3/advanced/daemonize-processes)
* [Submit Flows Directly to Dynamic Infrastructure](/v3/advanced/submit-flows-directly-to-dynamic-infrastructure)

##### Platform

* [Scale self-hosted Prefect](/v3/advanced/self-hosted)
* [Maintain your Prefect database](/v3/advanced/database-maintenance)
* [Build deployments via CI/CD](/v3/advanced/deploy-ci-cd)
* [Manage resources using Infrastructure as Code](/v3/advanced/infrastructure-as-code)
* [Self-host the Prefect Server with Helm](/v3/advanced/server-helm)
* [Secure self-hosted Prefect](/v3/advanced/security-settings)

##### Extensibility

* [Use and configure the API client](/v3/advanced/api-client)
* [Create custom blocks](/v3/advanced/custom-blocks)
* [Develop a custom worker](/v3/advanced/developing-a-custom-worker)
* [Write a plugin](/v3/advanced/experimental-plugins)

On this page

* [Overview](#overview)
* [Getting a client](#getting-a-client)
* [Configure custom headers](#configure-custom-headers)
* [Setting custom headers](#setting-custom-headers)
* [Examples](#examples)
* [Reschedule late flow runs](#reschedule-late-flow-runs)
* [Get the last N completed flow runs from your workspace](#get-the-last-n-completed-flow-runs-from-your-workspace)
* [Transition all running flows to cancelled through the Client](#transition-all-running-flows-to-cancelled-through-the-client)
* [Query events with pagination](#query-events-with-pagination)
* [Create, read, or delete artifacts](#create%2C-read%2C-or-delete-artifacts)

## [​](#overview) Overview

The [`PrefectClient`](https://reference.prefect.io/prefect/client/)
offers methods to simplify common operations against Prefect’s REST API that may not be abstracted away by the SDK.
For example, to [reschedule flow runs](/v3/develop/interact-with-api#reschedule-late-flow-runs), one might use methods like:

* `read_flow_runs` with a `FlowRunFilter` to read certain flow runs
* `create_flow_run_from_deployment` to schedule new flow runs
* `delete_flow_run` to delete a very `Late` flow run

### [​](#getting-a-client) Getting a client

By default, `get_client()` returns an asynchronous client to be used as a context manager, but you may also use a synchronous client.

async

sync

Copy

```
from prefect import get_client

async with get_client() as client:
    response = await client.hello()
    print(response.json()) # 👋
```

## [​](#configure-custom-headers) Configure custom headers

You can configure custom HTTP headers to be sent with every API request by setting the `PREFECT_CLIENT_CUSTOM_HEADERS` setting. This is useful for adding authentication headers, API keys, or other custom headers required by proxies, CDNs, or security systems.

### [​](#setting-custom-headers) Setting custom headers

Custom headers can be configured via environment variables or settings. The headers are specified as key-value pairs in JSON format.

Environment variable

CLI

prefect.toml

Copy

```
export PREFECT_CLIENT_CUSTOM_HEADERS='{"CF-Access-Client-Id": "your-client-id", "CF-Access-Client-Secret": "your-secret"}'
```

**Protected headers**Certain headers are protected and cannot be overridden by custom headers for security reasons:

* `User-Agent` - Managed by Prefect to identify client version
* `Prefect-Csrf-Token` - Used for CSRF protection
* `Prefect-Csrf-Client` - Used for CSRF protection

If you attempt to override these headers, Prefect will log a warning and ignore the custom header value.

## [​](#examples) Examples

These examples are meant to illustrate how one might develop their own utilities for interacting with the API.

If you believe a client method is missing, or you’d like to see a specific pattern better represented in the SDK generally, please [open an issue](https://github.com/PrefectHQ/prefect/issues/new/choose).

### [​](#reschedule-late-flow-runs) Reschedule late flow runs

To bulk reschedule flow runs that are late, delete the late flow runs and create new ones in a
`Scheduled` state with a delay. This is useful if you accidentally scheduled many
flow runs of a deployment to an inactive work pool, for example.
The following example reschedules the last three late flow runs of a deployment named
`healthcheck-storage-test` to run six hours later than their original expected start time.
It also deletes any remaining late flow runs of that deployment.
First, define the rescheduling function:

Copy

```
async def reschedule_late_flow_runs(
    deployment_name: str,
    delay: timedelta,
    most_recent_n: int,
    delete_remaining: bool = True,
    states: list[str] | None = None
) -> list[FlowRun]:
    states = states or ["Late"]

    async with get_client() as client:
        flow_runs = await client.read_flow_runs(
            flow_run_filter=FlowRunFilter(
                state=dict(name=dict(any_=states)),
                expected_start_time=dict(before_=datetime.now(timezone.utc)),
            ),
            deployment_filter=DeploymentFilter(name={'like_': deployment_name}),
            sort=FlowRunSort.START_TIME_DESC,
            limit=most_recent_n if not delete_remaining else None
        )

        rescheduled_flow_runs: list[FlowRun] = []
        for i, run in enumerate(flow_runs):
            await client.delete_flow_run(flow_run_id=run.id)
            if i < most_recent_n:
                new_run = await client.create_flow_run_from_deployment(
                    deployment_id=run.deployment_id,
                    state=Scheduled(scheduled_time=run.expected_start_time + delay),
                )
                rescheduled_flow_runs.append(new_run)
            
        return rescheduled_flow_runs
```

Then use it to reschedule flows:

Copy

```
rescheduled_flow_runs = asyncio.run(
    reschedule_late_flow_runs(
        deployment_name="healthcheck-storage-test",
        delay=timedelta(hours=6),
        most_recent_n=3,
    )
)
```

View the complete example

reschedule\_late\_flows.py

Copy

```
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from prefect import get_client
from prefect.client.schemas.filters import DeploymentFilter, FlowRunFilter
from prefect.client.schemas.objects import FlowRun
from prefect.client.schemas.sorting import FlowRunSort
from prefect.states import Scheduled

async def reschedule_late_flow_runs(
    deployment_name: str,
    delay: timedelta,
    most_recent_n: int,
    delete_remaining: bool = True,
    states: list[str] | None = None
) -> list[FlowRun]:
    states = states or ["Late"]

    async with get_client() as client:
        flow_runs = await client.read_flow_runs(
            flow_run_filter=FlowRunFilter(
                state=dict(name=dict(any_=states)),
                expected_start_time=dict(before_=datetime.now(timezone.utc)),
            ),
            deployment_filter=DeploymentFilter(name={'like_': deployment_name}),
            sort=FlowRunSort.START_TIME_DESC,
            limit=most_recent_n if not delete_remaining else None
        )

        if not flow_runs:
            print(f"No flow runs found in states: {states!r}")
            return []
        
        rescheduled_flow_runs: list[FlowRun] = []
        for i, run in enumerate(flow_runs):
            await client.delete_flow_run(flow_run_id=run.id)
            if i < most_recent_n:
                new_run = await client.create_flow_run_from_deployment(
                    deployment_id=run.deployment_id,
                    state=Scheduled(scheduled_time=run.expected_start_time + delay),
                )
                rescheduled_flow_runs.append(new_run)
            
        return rescheduled_flow_runs


if __name__ == "__main__":
    rescheduled_flow_runs = asyncio.run(
        reschedule_late_flow_runs(
            deployment_name="healthcheck-storage-test",
            delay=timedelta(hours=6),
            most_recent_n=3,
        )
    )
    
    print(f"Rescheduled {len(rescheduled_flow_runs)} flow runs")
    
    assert all(run.state.is_scheduled() for run in rescheduled_flow_runs)
    assert all(
        run.expected_start_time > datetime.now(timezone.utc)
        for run in rescheduled_flow_runs
    )
```

### [​](#get-the-last-n-completed-flow-runs-from-your-workspace) Get the last `N` completed flow runs from your workspace

To get the last `N` completed flow runs from your workspace, use `read_flow_runs` and `prefect.client.schemas`.
This example gets the last three completed flow runs from your workspace:

Copy

```
async def get_most_recent_flow_runs(
    n: int,
    states: list[str] | None = None
) -> list[FlowRun]:    
    async with get_client() as client:
        return await client.read_flow_runs(
            flow_run_filter=FlowRunFilter(
                state={'type': {'any_': states or ["COMPLETED"]}}
            ),
            sort=FlowRunSort.END_TIME_DESC,
            limit=n,
        )
```

Use it to get the last 3 completed runs:

Copy

```
flow_runs: list[FlowRun] = asyncio.run(
    get_most_recent_flow_runs(n=3)
)
```

View the complete example

get\_recent\_flows.py

Copy

```
from __future__ import annotations

import asyncio

from prefect import get_client
from prefect.client.schemas.filters import FlowRunFilter
from prefect.client.schemas.objects import FlowRun
from prefect.client.schemas.sorting import FlowRunSort

async def get_most_recent_flow_runs(
    n: int,
    states: list[str] | None = None
) -> list[FlowRun]:    
    async with get_client() as client:
        return await client.read_flow_runs(
            flow_run_filter=FlowRunFilter(
                state={'type': {'any_': states or ["COMPLETED"]}}
            ),
            sort=FlowRunSort.END_TIME_DESC,
            limit=n,
        )


if __name__ == "__main__":
    flow_runs: list[FlowRun] = asyncio.run(
        get_most_recent_flow_runs(n=3)
    )
    assert len(flow_runs) == 3
    
    assert all(
        run.state.is_completed() for run in flow_runs
    )
    assert (
        end_times := [run.end_time for run in flow_runs]
    ) == sorted(end_times, reverse=True)
```

Instead of the last three from the whole workspace, you can also use the `DeploymentFilter`
to get the last three completed flow runs of a specific deployment.

### [​](#transition-all-running-flows-to-cancelled-through-the-client) Transition all running flows to cancelled through the Client

Use `get_client`to set multiple runs to a `Cancelled` state.
This example cancels all flow runs that are in `Pending`, `Running`, `Scheduled`, or `Late` states when the script is run.

Copy

```
async def list_flow_runs_with_states(states: list[str]) -> list[FlowRun]:
    async with get_client() as client:
        return await client.read_flow_runs(
            flow_run_filter=FlowRunFilter(
                state=FlowRunFilterState(
                    name=FlowRunFilterStateName(any_=states)
                )
            )
        )

async def cancel_flow_runs(flow_runs: list[FlowRun]):
    async with get_client() as client:
        for flow_run in flow_runs:
            state = flow_run.state.copy(
                update={"name": "Cancelled", "type": StateType.CANCELLED}
            )
            await client.set_flow_run_state(flow_run.id, state, force=True)
```

Cancel all pending, running, scheduled or late flows:

Copy

```
async def bulk_cancel_flow_runs():
    states = ["Pending", "Running", "Scheduled", "Late"]
    flow_runs = await list_flow_runs_with_states(states)

    while flow_runs:
        print(f"Cancelling {len(flow_runs)} flow runs")
        await cancel_flow_runs(flow_runs)
        flow_runs = await list_flow_runs_with_states(states)

asyncio.run(bulk_cancel_flow_runs())
```

View the complete example

cancel\_flows.py

Copy

```
import asyncio

from prefect import get_client
from prefect.client.schemas.filters import FlowRunFilter, FlowRunFilterState, FlowRunFilterStateName
from prefect.client.schemas.objects import FlowRun, StateType

async def list_flow_runs_with_states(states: list[str]) -> list[FlowRun]:
    async with get_client() as client:
        return await client.read_flow_runs(
            flow_run_filter=FlowRunFilter(
                state=FlowRunFilterState(
                    name=FlowRunFilterStateName(any_=states)
                )
            )
        )


async def cancel_flow_runs(flow_runs: list[FlowRun]):
    async with get_client() as client:
        for idx, flow_run in enumerate(flow_runs):
            print(f"[{idx + 1}] Cancelling flow run '{flow_run.name}' with ID '{flow_run.id}'")
            state_updates: dict[str, str] = {}
            state_updates.setdefault("name", "Cancelled")
            state_updates.setdefault("type", StateType.CANCELLED)
            state = flow_run.state.copy(update=state_updates)
            await client.set_flow_run_state(flow_run.id, state, force=True)


async def bulk_cancel_flow_runs():
    states = ["Pending", "Running", "Scheduled", "Late"]
    flow_runs = await list_flow_runs_with_states(states)

    while len(flow_runs) > 0:
        print(f"Cancelling {len(flow_runs)} flow runs\n")
        await cancel_flow_runs(flow_runs)
        flow_runs = await list_flow_runs_with_states(states)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(bulk_cancel_flow_runs())
```

### [​](#query-events-with-pagination) Query events with pagination

Query historical events from the Prefect API with support for filtering and pagination. This is useful for analyzing past activity, debugging issues, or building custom monitoring tools.
The following example queries events from the last hour and demonstrates how to paginate through results:

Copy

```
from datetime import datetime, timedelta, timezone

from prefect import get_client
from prefect.events.filters import EventFilter, EventOccurredFilter


async def query_recent_events():
    async with get_client() as client:
        # query events from the last hour
        now = datetime.now(timezone.utc)
        event_filter = EventFilter(
            occurred=EventOccurredFilter(
                since=now - timedelta(hours=1),
                until=now,
            )
        )

        # get first page
        page = await client.read_events(filter=event_filter, limit=10)
        print(f"Total events: {page.total}")

        # iterate through all pages
        while page:
            for event in page.events:
                print(f"{event.occurred} - {event.event}")
            page = await page.get_next_page(client)
```

View the complete example

query\_events.py

Copy

```
import asyncio
from datetime import datetime, timedelta, timezone

from prefect import get_client
from prefect.events.filters import EventFilter, EventOccurredFilter


async def query_recent_events():
    async with get_client() as client:
        # query events from the last hour
        now = datetime.now(timezone.utc)
        event_filter = EventFilter(
            occurred=EventOccurredFilter(
                since=now - timedelta(hours=1),
                until=now,
            )
        )

        # get first page with small limit to demonstrate pagination
        print("=== first page ===")
        event_page = await client.read_events(filter=event_filter, limit=5)
        print(f"total events: {event_page.total}")
        print(f"events on this page: {len(event_page.events)}")
        for event in event_page.events:
            print(f"  {event.occurred} - {event.event}")
        print()

        # if there are more pages, fetch the next one
        second_page = await event_page.get_next_page(client)
        if second_page:
            print("=== second page ===")
            print(f"events on this page: {len(second_page.events)}")
            for event in second_page.events:
                print(f"  {event.occurred} - {event.event}")
            print()

        # demonstrate iterating through all pages
        print("=== collecting all events ===")
        all_events = []
        page = await client.read_events(filter=event_filter, limit=5)

        page_count = 0
        while page:
            all_events.extend(page.events)
            page_count += 1
            page = await page.get_next_page(client)

        print(f"collected {len(all_events)} events across {page_count} pages")


if __name__ == "__main__":
    asyncio.run(query_recent_events())
```

### [​](#create,-read,-or-delete-artifacts) Create, read, or delete artifacts

Create, read, or delete artifacts programmatically through the [Prefect REST API](/v3/api-ref/rest-api).
With the Artifacts API, you can automate the creation and management of artifacts as part of your workflow.
For example, to read the five most recently created Markdown, table, and link artifacts, you can run the following:

fixture:mock\_post\_200

Copy

```
import requests


PREFECT_API_URL="https://api.prefect.cloud/api/accounts/abc/workspaces/xyz"
PREFECT_API_KEY="pnu_ghijk"
data = {
    "sort": "CREATED_DESC",
    "limit": 5,
    "artifacts": {
        "key": {
            "exists_": True
        }
    }
}

headers = {"Authorization": f"Bearer {PREFECT_API_KEY}"}
endpoint = f"{PREFECT_API_URL}/artifacts/filter"

response = requests.post(endpoint, headers=headers, json=data)
assert response.status_code == 200
for artifact in response.json():
    print(artifact)
```

If you don’t specify a key or that a key must exist, you will also return results, which are a type of key-less artifact.
See the [Prefect REST API documentation](/v3/api-ref/rest-api) on artifacts for more information.

Was this page helpful?

YesNo

[Secure self-hosted Prefect](/v3/advanced/security-settings)[Create custom blocks](/v3/advanced/custom-blocks)

⌘I