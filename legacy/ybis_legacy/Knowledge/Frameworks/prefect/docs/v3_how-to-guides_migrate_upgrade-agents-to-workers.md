How to upgrade from agents to workers - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Migrate

How to upgrade from agents to workers

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

* [About workers and agents](#about-workers-and-agents)
* [Upgrade enhancements](#upgrade-enhancements)
* [Workers](#workers)
* [Work pools](#work-pools)
* [Improved deployment interfaces](#improved-deployment-interfaces)
* [Upgrade changes](#upgrade-changes)
* [What’s similar](#what%E2%80%99s-similar)
* [Upgrade steps](#upgrade-steps)
* [Use flow.deploy](#use-flow-deploy)
* [Deploying from a local file](#deploying-from-a-local-file)
* [Deploying using a storage block](#deploying-using-a-storage-block)
* [Deploy using an infrastructure block and a storage block](#deploy-using-an-infrastructure-block-and-a-storage-block)
* [Deploy via a Docker image](#deploy-via-a-docker-image)
* [Use prefect deploy](#use-prefect-deploy)

Upgrading from agents to workers significantly enhances the experience of deploying flows
by simplifying the specification of each flow’s infrastructure and runtime environment.

This guide is for users who are upgrading from agents (a deployment pattern specific to `prefect>2.0,<3.0`) to workers.
If you are new to Prefect, we recommend starting with the
[Prefect Quickstart](/v3/get-started/quickstart).

## [​](#about-workers-and-agents) About workers and agents

A [worker](/v3/concepts/workers) is the fusion of an
agent with an infrastructure block.
Like agents, workers poll a work pool for flow runs that are scheduled to start.
Like infrastructure blocks, workers are typed. They work with only one kind of infrastructure,
and they specify the default configuration for jobs submitted to that infrastructure.
Accordingly, workers are not a drop-in replacement for agents. **Using workers requires
deploying flows differently.** In particular, deploying a flow with a worker does not involve
specifying an infrastructure block. Instead, infrastructure configuration is specified on the
[work pool](/v3/concepts/work-pools) and passed to each worker that polls work
from that pool.

## [​](#upgrade-enhancements) Upgrade enhancements

### [​](#workers) Workers

* Improved visibility into the status of each worker, including when a worker was started
  and when it last polled.
* Better handling of race conditions for high availability use cases.

### [​](#work-pools) Work pools

* Work pools allow greater customization and governance of infrastructure parameters for deployments
  through their [base job template](/v3/how-to-guides/deployment_infra/manage-work-pools#base-job-template).
* Prefect Cloud [push work pools](/v3/how-to-guides/deployment_infra/serverless) enable flow
  execution in your cloud provider environment without the need to host a worker.
* Prefect Cloud [managed work pools](/v3/how-to-guides/deployment_infra/managed) allow you to run flows on
  Prefect’s infrastructure, without the need to host a worker or configure cloud provider infrastructure.

### [​](#improved-deployment-interfaces) Improved deployment interfaces

* The Python deployment experience with [`.deploy()`](/v3/how-to-guides/deployments/deploy-via-python) or the alternative deployment experience with
  `prefect.yaml` are more flexible and easier to use than block and agent-based deployments.
* Both options allow you to [deploy multiple flows](/v3/deploy/infrastructure-concepts/prefect-yaml#work-with-multiple-deployments-with-prefect-yaml)
  with a single command.
* Both options allow you to build Docker images for your flows to create portable execution environments.
* The YAML-based API supports [templating](/v3/deploy/infrastructure-concepts/prefect-yaml#templating-options)
  to enable [dryer deployment definitions](/v3/how-to-guides/deployments/prefect-yaml#reuse-configuration-across-deployments).

## [​](#upgrade-changes) Upgrade changes

1. **Deployment CLI and Python SDK:**
   `prefect deployment build <entrypoint>`/`prefect deployment apply` —> [`prefect deploy`](/v3/deploy/infrastructure-concepts/prefect-yaml#deployment-declaration-reference)
   Prefect now automatically detects flows in your repo and provides a [wizard](/v3#step-5-deploy-the-flow)
   to guide you through setting required attributes for your deployments.
   `Deployment.build_from_flow` —> [`flow.deploy`](https://reference.prefect.io/prefect/flows/#prefect.flows.Flow.deploy)
2. **Configuring remote flow code storage:**
   storage blocks —> [pull action](/v3/deploy/infrastructure-concepts/prefect-yaml#the-pull-action)
   When using the YAML-based deployment API, you can configure a pull action in your `prefect.yaml`
   file to specify how to retrieve flow code for your deployments. You can use configuration from your
   existing storage blocks to define your pull action [through templating](/v3/deploy/infrastructure-concepts/prefect-yaml#templating-options).
   When using the Python deployment API, you can pass any storage block to the `flow.deploy` method to
   specify how to retrieve flow code for your deployment.
3. **Configuring flow run infrastructure:**
   infrastructure blocks —> [typed work pool](/v3/deploy/infrastructure-concepts/workers#worker-types)
   Default infrastructure config is now set on the typed work pool, and can be overwritten by
   individual deployments.
4. **Managing multiple deployments:**
   Create and/or update many deployments at once through a
   [`prefect.yaml`](/v3/deploy/infrastructure-concepts/prefect-yaml#work-with-multiple-deployments-with-prefect-yaml)
   file or use the [`deploy`](/v3/how-to-guides/deployments/deploy-via-python)
   function.

## [​](#what’s-similar) What’s similar

* You can set storage blocks as the pull action in a `prefect.yaml` file.
* Infrastructure blocks have configuration fields similar to typed work pools.
* Deployment-level infrastructure overrides operate in much the same way.
  `infra_override` -> [`job_variable`](/v3/deploy/infrastructure-concepts/prefect-yaml#work-pool-fields)
* The process for starting an agent and [starting a worker](/v3/deploy/infrastructure-concepts/workers#start-a-worker)
  in your environment are virtually identical.
  `prefect agent start --pool <work pool name>` —> `prefect worker start --pool <work pool name>`

**Worker Helm chart**If you host your agents in a Kubernetes cluster, you can use the [Prefect worker Helm chart](https://github.com/PrefectHQ/prefect-helm/tree/main/charts/prefect-worker)
to host workers in your cluster.

## [​](#upgrade-steps) Upgrade steps

If you have existing deployments that use infrastructure blocks, you can quickly upgrade them to
be compatible with workers by following these steps:

1. **[Create a work pool](/v3/deploy/infrastructure-concepts/work-pools#work-pool-configuration)**

This new work pool replaces your infrastructure block.
You can use the [`.publish_as_work_pool`](https://docs.prefect.io/2.19.2/api-ref/prefect/infrastructure/#prefect.infrastructure.Infrastructure.publish_as_work_pool)
method on any infrastructure block to create a work pool with the same configuration.
For example, if you have a `KubernetesJob` infrastructure block named ‘my-k8s-job’, you can
create a work pool with the same configuration with this script:

Copy

```
from prefect.infrastructure import KubernetesJob


KubernetesJob.load("my-k8s-job").publish_as_work_pool()
```

Running this script creates a work pool named ‘my-k8s-job’ with the same configuration as your infrastructure block.

**Serving flows**
If you are using a `Process` infrastructure block and a `LocalFilesystem` storage block
(or aren’t using an infrastructure and storage block at all), you can use [`flow.serve`](/v3/deploy/index)
to create a deployment without specifying a work pool name or start a worker.This is a quick way to create a deployment for a flow and manage your
deployments if you don’t need the dynamic infrastructure creation or configuration offered
by workers.

2. **[Start a worker](/v3/deploy/infrastructure-concepts/workers#start-a-worker)**

This worker replaces your agent and polls your new work pool for flow runs to execute.

Copy

```
prefect worker start -p <work pool name>
```

3. **Deploy your flows to the new work pool**

To deploy your flows to the new work pool, use `flow.deploy` for a Pythonic deployment
experience or `prefect deploy` for a YAML-based deployment experience.
If you currently use `Deployment.build_from_flow`, we recommend using `flow.deploy`.
If you currently use `prefect deployment build` and `prefect deployment apply`, we recommend
using `prefect deploy`.

### [​](#use-flow-deploy) Use `flow.deploy`

If you have a Python script that uses `Deployment.build_from_flow` to create a deployment, you
can replace it with `flow.deploy`.
You can translate most arguments to `Deployment.build_from_flow` directly to `flow.deploy`,
but here are some possible changes you may need:

* Replace `infrastructure` with `work_pool_name`.
  + If you’ve used the `.publish_as_work_pool` method on your infrastructure block, use the
    name of the created work pool.
* Replace `infra_overrides` with `job_variables`.
* Replace `storage` with a call to [`flow.from_source`](/v3/deploy/index).
  + `flow.from_source` loads your flow from a remote storage location and makes it deployable.
    You can pass your existing storage block to the `source` argument of `flow.from_source`.

Below are some examples of how to translate `Deployment.build_from_flow` into `flow.deploy`.

#### [​](#deploying-from-a-local-file) Deploying from a local file

Using agents and `Deployment.build_from_flow` to deploy a flow from a local file looked like:

Copy

```
from prefect import flow


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello {name}! I'm a flow from a Python script!")


if __name__ == "__main__":
    Deployment.build_from_flow(
        my_flow,
        name="my-deployment",
        parameters=dict(name="Marvin"),
    )
```

When using workers, you can accomplish the same local-storage deployment with `flow.deploy`:

example.py

Copy

```
from pathlib import Path
from prefect import flow


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello {name}! I'm a flow from a Python script!")


if __name__ == "__main__":
    my_flow.from_source(
        source=str(Path(__file__).parent),
        entrypoint="example.py:my_flow",
    ).deploy(
        name="my-deployment",
        parameters=dict(name="Marvin"),
        work_pool_name="local",
    )
```

You can then start a worker to execute scheduled runs, pulling the flow code from `example.py`:

Copy

```
# starts a worker and creates `local` Process work pool if it doesn't exist
prefect worker start --pool local
```

If you’d like to immediately serve this flow as a deployment without running a worker or using work pools, you can [use `flow.serve`](/v3/how-to-guides/deployment_infra/run-flows-in-local-processes).

#### [​](#deploying-using-a-storage-block) Deploying using a storage block

If you currently use a storage block to load your flow code but no infrastructure block:

Copy

```
from prefect import flow
from prefect.filesystems import GitHub


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello {name}! I'm a flow from a GitHub repo!")


if __name__ == "__main__":
    Deployment.build_from_flow(
        my_flow,
        name="my-deployment",
        storage=GitHub.load("demo-repo"),
        parameters=dict(name="Marvin"),
    )
```

You can use `flow.from_source` to load your flow from the same location and `flow.deploy` to
create a deployment:

example.py

Copy

```
from prefect import flow
from prefect.blocks.system import Secret
from prefect.runner.storage import GitRepository

@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello {name}! I'm a flow from a GitHub repo!")

if __name__ == "__main__":
    flow.from_source(
        source=GitRepository(
            url="https://github.com/me/myrepo.git",
            credentials={"username": "oauth2", "access_token": Secret.load("my-github-pat")},
        ),
        entrypoint="example.py:my_flow"
    ).deploy(
        name="my-deployment",
        parameters=dict(name="Marvin"),
        work_pool_name="local", # or the name of your work pool
    )
```

#### [​](#deploy-using-an-infrastructure-block-and-a-storage-block) Deploy using an infrastructure block and a storage block

For the code below, you need to create a work pool from your infrastructure block and pass it to
`flow.deploy` as the `work_pool_name` argument. You also need to pass your storage block to
`flow.from_source` as the `source` argument.

example.py

Copy

```
from prefect import flow
from prefect.deployments import Deployment
from prefect.filesystems import GitHub # this block class no longer exists
from prefect.infrastructure.kubernetes import KubernetesJob


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello {name}! I'm a flow from a GitHub repo!")

repo = GitHub.load("demo-repo")

if __name__ == "__main__":
    Deployment.build_from_flow(
        my_flow,
        name="my-deployment",
        storage=repo,
        entrypoint="example.py:my_flow",
        infrastructure=KubernetesJob.load("my-k8s-job"),
        infra_overrides=dict(pull_policy="Never"),
        parameters=dict(name="Marvin"),
    )
```

The equivalent deployment code using `flow.deploy` should look like this:

example.py

Copy

```
from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/me/myrepo.git",
        entrypoint="example.py:my_flow"
    ).deploy(
        name="my-deployment",
        work_pool_name="my-k8s-job",
        job_variables=dict(pull_policy="Never"),
        parameters=dict(name="Marvin"),
    )
```

When using `flow.from_source().deploy()` with a remote `source`such as a `GitHub` block or `str` URL like <https://github.com/me/myrepo.git>), the flow you’re deploying doesn’t need to be available locally before running your script.
See the [SDK reference](https://reference.prefect.io/prefect/#prefect.Flow.from_source) for more info on `from_source`.

#### [​](#deploy-via-a-docker-image) Deploy via a Docker image

If you currently bake your flow code into a Docker image before deploying, you can use the
`image` argument of `flow.deploy` to build a Docker image as part of your deployment process:

Copy

```
from prefect import flow

@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello {name}! I'm a flow from a Docker image!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment",
        image="my-repo/my-image:latest",
        work_pool_name="my-k8s-job",
        job_variables=dict(pull_policy="Never"),
        parameters=dict(name="Marvin"),
    )
```

You can skip a `flow.from_source` call when building an image with `flow.deploy`. Prefect
keeps track of the flow’s source code location in the image and loads it from that location when the
flow is executed.

### [​](#use-prefect-deploy) Use `prefect deploy`

**Always run `prefect deploy` commands from the `root` level of your repo!**With agents, you may have multiple `deployment.yaml` files. But under worker deployment
patterns, each repo has a single `prefect.yaml` file located at the **root** of the repo
that contains [deployment configuration](/v3/deploy/infrastructure-concepts/prefect-yaml#work-with-multiple-deployments-with-prefect-yaml)
for all flows in that repo.

To set up a new `prefect.yaml` file for your deployments, run the following command from the root
level of your repo:

Copy

```
prefect deploy
```

This starts a wizard that guides you through setting up your deployment.

**For step 4, select `y` on the last prompt to save the configuration for the deployment.**Saving the configuration for your deployment results in a `prefect.yaml` file populated
with your first deployment. You can use this YAML file to edit and [define multiple deployments](/v3/deploy/infrastructure-concepts/prefect-yaml#work-with-multiple-deployments-with-prefect-yaml)
for this repo.

You can add more [deployments](/v3/deploy/infrastructure-concepts/prefect-yaml#deployment-declaration-reference)
to the `deployments` list in your `prefect.yaml` file and/or by continuing to use the deployment
creation wizard.
For more information on deployments, check out our [in-depth guide for deploying flows to work pools](/v3/how-to-guides/deployment_infra/serve-flows-docker).

Was this page helpful?

YesNo

[Upgrade to Prefect 3.0](/v3/how-to-guides/migrate/upgrade-to-prefect-3)[Transfer resources between environments](/v3/how-to-guides/migrate/transfer-resources)

⌘I