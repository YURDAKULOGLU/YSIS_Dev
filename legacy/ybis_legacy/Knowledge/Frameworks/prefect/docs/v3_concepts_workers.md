Workers - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Deployments

Workers

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

* [Worker types](#worker-types)
* [Worker options](#worker-options)
* [Worker status](#worker-status)
* [Worker logs](#worker-logs)
* [Worker details](#worker-details)
* [Start a worker](#start-a-worker)
* [Configure prefetch](#configure-prefetch)
* [Polling for work](#polling-for-work)
* [Install policy](#install-policy)
* [Further reading](#further-reading)

Workers are lightweight polling services that retrieve scheduled runs from a work pool and execute them.
Workers each have a type corresponding to the execution environment to submit flow runs to.
Workers can only poll work pools that match their type.
As a result, when deployments are assigned to a work pool, you know in which execution environment scheduled flow runs for that deployment will run.
The following diagram summarizes the architecture of a worker-based work pool deployment:

The worker is in charge of provisioning the *flow run infrastructure*.

### [​](#worker-types) Worker types

Below is a list of available worker types. Most worker types require installation of an additional package.

| Worker Type | Description | Required Package |
| --- | --- | --- |
| [`process`](https://reference.prefect.io/prefect/workers/process/) | Executes flow runs in subprocesses |  |
| [`kubernetes`](https://reference.prefect.io/prefect_kubernetes/worker/) | Executes flow runs as Kubernetes jobs | `prefect-kubernetes` |
| [`docker`](https://reference.prefect.io/prefect_docker/worker/) | Executes flow runs within Docker containers | `prefect-docker` |
| [`ecs`](https://reference.prefect.io/prefect_aws/workers/ecs_worker/) | Executes flow runs as ECS tasks | `prefect-aws` |
| [`cloud-run-v2`](https://reference.prefect.io/prefect_gcp/workers/cloud_run_v2/) | Executes flow runs as Google Cloud Run jobs | `prefect-gcp` |
| [`vertex-ai`](https://reference.prefect.io/prefect_gcp/workers/vertex/) | Executes flow runs as Google Cloud Vertex AI jobs | `prefect-gcp` |
| [`azure-container-instance`](https://reference.prefect.io/prefect_azure/workers/container_instance/) | Execute flow runs in ACI containers | `prefect-azure` |
| [`coiled`](https://github.com/coiled/prefect-worker/blob/main/example/README.md) | Execute flow runs in your cloud with Coiled | `prefect-coiled` |

If you don’t see a worker type that meets your needs, consider
[developing a new worker type](/contribute/develop-a-new-worker-type).

### [​](#worker-options) Worker options

Workers poll for work from one or more queues within a work pool. If the worker references a work queue that doesn’t exist, it is created automatically.
The worker CLI infers the worker type from the work pool.
Alternatively, you can specify the worker type explicitly.
If you supply the worker type to the worker CLI, a work pool is created automatically if it doesn’t exist (using default job settings).
Configuration parameters you can specify when starting a worker include:

| Option | Description |
| --- | --- |
| `--name`, `-n` | The name to give to the started worker. If not provided, a unique name will be generated. |
| `--pool`, `-p` | The work pool the started worker should poll. |
| `--work-queue`, `-q` | One or more work queue names for the worker to pull from. If not provided, the worker pulls from all work queues in the work pool. |
| `--type`, `-t` | The type of worker to start. If not provided, the worker type is inferred from the work pool. |
| `--prefetch-seconds` | The amount of time before a flow run’s scheduled start time to begin submission. Default is the value of `PREFECT_WORKER_PREFETCH_SECONDS`. |
| `--run-once` | Only run worker polling once. By default, the worker runs forever. |
| `--limit`, `-l` | The maximum number of flow runs to execute concurrently. |
| `--with-healthcheck` | Start a healthcheck server for the worker. |
| `--install-policy` | Install policy to use workers from Prefect integration packages. |

You must start a worker within an environment to access or create the required infrastructure to execute flow runs.
The worker will deploy flow runs to the infrastructure corresponding to the worker type. For example, if you start a worker with
type `kubernetes`, the worker deploys flow runs to a Kubernetes cluster.
Prefect must be installed in any environment (for example, virtual environment, Docker container) where you intend to run the worker or
execute a flow run.

**`PREFECT_API_URL` and `PREFECT_API_KEY`settings for workers**`PREFECT_API_URL` must be set for the environment where your worker is running. When using Prefect Cloud, you must also have a user or service account
with the `Worker` role, which you can configure by setting the `PREFECT_API_KEY`.

### [​](#worker-status) Worker status

Workers have two statuses: `ONLINE` and `OFFLINE`. A worker is online if it sends regular heartbeat messages to the Prefect API.
If a worker misses three heartbeats, it is considered offline. By default, a worker is considered offline a maximum of 90 seconds
after it stopped sending heartbeats, but you can configure the threshold with the `PREFECT_WORKER_HEARTBEAT_SECONDS` setting.

### [​](#worker-logs) Worker logs

 Workers send logs to the Prefect Cloud API if you’re connected to Prefect Cloud.

* All worker logs are automatically sent to the Prefect Cloud API
* Logs are accessible through both the Prefect Cloud UI and API
* Each flow run will include a link to its associated worker’s logs

### [​](#worker-details) Worker details

 The **Worker Details** page shows you three key areas of information:

* Worker status
* Installed Prefect version
* Installed Prefect integrations (e.g., `prefect-aws`, `prefect-gcp`)
* Live worker logs (if worker logging is enabled)

Access a worker’s details by clicking on the worker’s name in the Work Pool list.

### [​](#start-a-worker) Start a worker

Use the `prefect worker start` CLI command to start a worker. You must pass at least the work pool name.
If the work pool does not exist, it will be created if the `--type` flag is used.

Copy

```
prefect worker start -p [work pool name]
```

For example:

Copy

```
prefect worker start -p "my-pool"
```

Results in output like this:

Copy

```
Discovered worker type 'process' for work pool 'my-pool'.
Worker 'ProcessWorker 65716280-96f8-420b-9300-7e94417f2673' started!
```

In this case, Prefect automatically discovered the worker type from the work pool.
To create a work pool and start a worker in one command, use the `--type` flag:

Copy

```
prefect worker start -p "my-pool" --type "process"
```

Copy

```
Worker 'ProcessWorker d24f3768-62a9-4141-9480-a056b9539a25' started!
06:57:53.289 | INFO    | prefect.worker.process.processworker d24f3768-62a9-4141-9480-a056b9539a25 - Worker pool 'my-pool' created.
```

In addition, workers can limit the number of flow runs to start simultaneously with the `--limit` flag.
For example, to limit a worker to five concurrent flow runs:

Copy

```
prefect worker start --pool "my-pool" --limit 5
```

You can manage workers with the [Prefect Helm charts](https://github.com/PrefectHQ/prefect-helm/tree/main/charts/prefect-server).

### [​](#configure-prefetch) Configure prefetch

By default, the worker submits flow runs 10 seconds before they are scheduled to run.
This allows time for the infrastructure to be created so the flow run can start on time.
In some cases, infrastructure takes longer than 10 seconds to start the flow run. You can increase the prefetch time with the
`--prefetch-seconds` option or the `PREFECT_WORKER_PREFETCH_SECONDS` setting.
If this value is *more* than the amount of time it takes for the infrastructure to start, the flow run will *wait* until its
scheduled start time.

### [​](#polling-for-work) Polling for work

Workers poll for work every 15 seconds by default. You can configure this interval in your [profile settings](/v3/develop/settings-and-profiles)
with the
`PREFECT_WORKER_QUERY_SECONDS` setting.

### [​](#install-policy) Install policy

The Prefect CLI can install the required package for Prefect-maintained worker types automatically. Configure this behavior
with the `--install-policy` option. The following are valid install policies:

| Install Policy | Description |
| --- | --- |
| `always` | Always install the required package. Updates the required package to the most recent version if already installed. |
| `if-not-present` | Install the required package if it is not already installed. |
| `never` | Never install the required package. |
| `prompt` | Prompt the user to choose whether to install the required package. This is the default install policy. |
| If `prefect worker start` is run non-interactively, the `prompt` install policy behaves the same as `never`. |  |

### [​](#further-reading) Further reading

* See how to [daemonize a Prefect worker](/v3/advanced/daemonize-processes).
* See more information on [overriding a work pool’s job variables](/v3/deploy/infrastructure-concepts/customize).

---

Was this page helpful?

YesNo

[Work pools](/v3/concepts/work-pools)[Variables](/v3/concepts/variables)

⌘I