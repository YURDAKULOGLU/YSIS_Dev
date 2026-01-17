How to deploy flows with Python - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Deployments

How to deploy flows with Python

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

* [When to use flow.deploy instead of flow.serve](#when-to-use-flow-deploy-instead-of-flow-serve)
* [Prerequisites](#prerequisites)
* [Deploy a flow with flow.deploy](#deploy-a-flow-with-flow-deploy)
* [Trigger a run](#trigger-a-run)
* [Deploy with a schedule](#deploy-with-a-schedule)
* [Use remote code storage](#use-remote-code-storage)
* [Set default parameters](#set-default-parameters)
* [Set job variables](#set-job-variables)
* [Deploy multiple flows](#deploy-multiple-flows)
* [Further reading](#further-reading)

As an alternative to defining deployments in a `prefect.yaml` file, you can use the Python SDK to create deployments with [dynamic infrastructure](/v3/concepts/work-pools).
This can be more flexible if you have to programmatically gather configuration at deployment time.

## [​](#when-to-use-flow-deploy-instead-of-flow-serve) When to use `flow.deploy` instead of `flow.serve`

The `flow.serve` method is one [simple way to create a deployment with the Python SDK](/v3/how-to-guides/deployment_infra/run-flows-in-local-processes#serve-a-flow). It’s ideal when you have readily available, static infrastructure for your flow runs and you don’t need the dynamic dispatch of infrastructure per flow run offered by work pools.
However, you might want to consider using `flow.deploy` to associate your flow with a work pool that enables dynamic dispatch of infrastructure per flow run for the following reasons:

1. **Cost optimization:** Dynamic infrastructure can help reduce costs by scaling resources up or down based on demand.
2. **Resource scarcity:** If you have limited persistent infrastructure, dynamic provisioning can help manage resource allocation more efficiently.
3. **Varying workloads:** For workflows with inconsistent resource needs, dynamic infrastructure can adapt to changing requirements.
4. **Cloud-native deployments:** When working with cloud providers that offer serverless or auto-scaling options.

Let’s explore how to create a deployment using the Python SDK and leverage dynamic infrastructure through work pools.

## [​](#prerequisites) Prerequisites

Before deploying your flow using `flow.deploy`, ensure you have the following:

1. **A running Prefect server or Prefect Cloud workspace:** You can either run a Prefect server locally or use a Prefect Cloud workspace.
   To start a local server, run `prefect server start`. To use Prefect Cloud, sign up for an account at [app.prefect.cloud](https://app.prefect.cloud)
   and follow the [Connect to Prefect Cloud](/v3/manage/cloud/connect-to-cloud) guide.
2. **A Prefect flow:** You should have a flow defined in your Python script. If you haven’t created a flow yet, refer to the
   [Write Workflows](/v3/how-to-guides/workflows/write-and-run) guide.
3. **A work pool:** You need a work pool to manage the infrastructure for running your flow. If you haven’t created a work pool, you can do so through
   the Prefect UI or using the Prefect CLI. For more information, see the [Work Pools](/v3/concepts/work-pools) guide.
   For examples in this guide, we’ll use a Docker work pool created by running:

   Copy

   ```
   prefect work-pool create --type docker my-work-pool
   ```
4. **Docker:** Docker will be used to build and store the image containing your flow code. You can download and install
   Docker from the [official Docker website](https://www.docker.com/get-started/). If you don’t want to use Docker, you
   can see other options in the [Use remote code storage](#use-remote-code-storage) section.
5. **(Optional) A Docker registry:** While not strictly necessary for local development, having an account with a Docker registry (such as
   Docker Hub) is recommended for storing and sharing your Docker images.

With these prerequisites in place, you’re ready to deploy your flow using `flow.deploy`.

## [​](#deploy-a-flow-with-flow-deploy) Deploy a flow with `flow.deploy`

To deploy a flow using `flow.deploy` and Docker, follow these steps:

1

Write a flow

Ensure your flow is defined in a Python file. Let’s use a simple example:

example.py

Copy

```
from prefect import flow


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello, {name}!")
```

2

Add deployment configuration

Add a call to `flow.deploy` to tell Prefect how to deploy your flow.

example.py

Copy

```
from prefect import flow


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment",
        work_pool_name="my-work-pool",
        image="my-registry.com/my-docker-image:my-tag",
        push=False # switch to True to push to your image registry
    )
```

3

Deploy!

Run your script to deploy your flow.

Copy

```
python example.py
```

Running this script will:

1. Build a Docker image containing your flow code and dependencies.
2. Create a deployment associated with the specified work pool and image.

Building a Docker image for our flow allows us to have a consistent environment for our flow to run in. Workers for our work pool will use the image to run our flow.
In this example, we set `push=False` to skip pushing the image to a registry. This is useful for local development, and you can push your image to a registry such as Docker Hub in a production environment.

**Where’s the Dockerfile?**In the above example, we didn’t specify a Dockerfile. By default, Prefect will generate a Dockerfile for us that copies the flow code into an image and installs
any additional dependencies.If you want to write and use your own Dockerfile, you can do so by using `DockerImage`:

Copy

```
from prefect import flow
from prefect.docker import DockerImage


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment",
        work_pool_name="my-work-pool",
        image=DockerImage(
            name="my-registry.com/my-docker-image:my-tag",
            dockerfile="Dockerfile",
        ),
        push=False,
    )
```

### [​](#trigger-a-run) Trigger a run

Now that we have our flow deployed, we can trigger a run via either the Prefect CLI or UI.
First, we need to start a worker to run our flow:

Copy

```
prefect worker start --pool my-work-pool
```

Then, we can trigger a run of our flow using the Prefect CLI:

Copy

```
prefect deployment run 'my-flow/my-deployment'
```

After a few seconds, you should see logs from your worker showing that the flow run has started and see the state update in the UI.

## [​](#deploy-with-a-schedule) Deploy with a schedule

To deploy a flow with a schedule, you can use one of the following options:

* `interval`
  Defines the interval at which the flow should run. Accepts an integer or float value representing the number of seconds between runs or a `datetime.timedelta` object.


  Show Example

  interval.py

  Copy

  ```
  from datetime import timedelta
  from prefect import flow


  @flow(log_prints=True)
  def my_flow(name: str = "world"):
      print(f"Hello, {name}!")


  if __name__ == "__main__":
      my_flow.deploy(
          name="my-deployment",
          work_pool_name="my-work-pool",
          image="my-registry.com/my-docker-image:my-tag",
          push=False,
          # Run once a minute
          interval=timedelta(minutes=1)
      )
  ```
* `cron`
  Defines when a flow should run using a cron string.


  Show Example

  cron.py

  Copy

  ```
  from prefect import flow


  @flow(log_prints=True)
  def my_flow(name: str = "world"):
      print(f"Hello, {name}!")


  if __name__ == "__main__":
      my_flow.deploy(
          name="my-deployment",
          work_pool_name="my-work-pool",
          image="my-registry.com/my-docker-image:my-tag",
          push=False,
          # Run once a day at midnight
          cron="0 0 * * *"
      )
  ```
* `rrule`
  Defines a complex schedule using an `rrule` string.


  Show Example

  rrule.py

  Copy

  ```
  from prefect import flow


  @flow(log_prints=True)
  def my_flow(name: str = "world"):
      print(f"Hello, {name}!")


  if __name__ == "__main__":
      my_flow.deploy(
          name="my-deployment",
          work_pool_name="my-work-pool",
          image="my-registry.com/my-docker-image:my-tag",
          push=False,
          # Run every weekday at 9 AM
          rrule="FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=9;BYMINUTE=0"
      )
  ```
* `schedules`
  Defines multiple schedules for a deployment. This option provides flexibility for:
  + Setting up various recurring schedules
  + Implementing complex scheduling logic
  + Applying timezone offsets to schedules

  Show Example

  schedules.py

  Copy

  ```
  from datetime import datetime, timedelta
  from prefect import flow
  from prefect.schedules import Interval


  @flow(log_prints=True)
  def my_flow(name: str = "world"):
      print(f"Hello, {name}!")


  if __name__ == "__main__":
      my_flow.deploy(
          name="my-deployment",
          work_pool_name="my-work-pool",
          image="my-registry.com/my-docker-image:my-tag",
          push=False,
          # Run every 10 minutes starting from January 1, 2023
          # at 00:00 Central Time
          schedules=[
              Interval(
                  timedelta(minutes=10),
                  anchor_date=datetime(2023, 1, 1, 0, 0),
                  timezone="America/Chicago"
              )
          ]
      )
  ```

  Learn more about schedules [here](/v3/how-to-guides/deployments/create-schedules).

## [​](#use-remote-code-storage) Use remote code storage

In addition to storing your code in a Docker image, Prefect also supports deploying your code to remote storage. This approach allows you to
store your flow code in a remote location, such as a Git repository or cloud storage service.
Using remote storage for your code has several advantages:

1. Faster iterations: You can update your flow code without rebuilding Docker images.
2. Reduced storage requirements: You don’t need to store large Docker images for each code version.
3. Flexibility: You can use different storage backends based on your needs and infrastructure.

Using an existing remote Git repository like GitHub, GitLab, or Bitbucket works really well as remote code storage because:

1. Your code is already there.
2. You can deploy to multiple environments via branches and tags.
3. You can roll back to previous versions of your flows.

To deploy using remote storage, you’ll need to specify where your code is stored by using `flow.from_source` to first load your flow code from a remote location.
Here’s an example of loading a flow from a Git repository and deploying it:

git-deploy.py

Copy

```
from prefect import flow


if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/username/repository.git",
        entrypoint="path/to/your/flow.py:your_flow_function"
    ).deploy(
        name="my-deployment",
        work_pool_name="my-work-pool",
    )
```

The `source` parameter can accept a variety of remote storage options including:

* Git repositories
* S3 buckets (using the `s3://` scheme)
* Google Cloud Storage buckets (using the `gs://` scheme)
* Azure Blob Storage (using the `az://` scheme)

The `entrypoint` parameter is the path to the flow function within your repository combined with the name of the flow function.
Learn more about remote code storage [here](/v3/deploy/infrastructure-concepts/store-flow-code).

## [​](#set-default-parameters) Set default parameters

You can set default parameters for a deployment using the `parameters` keyword argument in `flow.deploy`.

default-parameters.py

Copy

```
from prefect import flow


@flow
def my_flow(name: str = "world"):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment",
        work_pool_name="my-work-pool",
        # Will print "Hello, Marvin!" by default instead of "Hello, world!"
        parameters={"name": "Marvin"},
        image="my-registry.com/my-docker-image:my-tag",
        push=False,
    )
```

Note these parameters can still be overridden on a per-deployment basis.

## [​](#set-job-variables) Set job variables

You can set default job variables for a deployment using the `job_variables` keyword argument in `flow.deploy`.
The job variables provided will override the values set on the work pool.

job-variables.py

Copy

```
import os
from prefect import flow


@flow
def my_flow():
    name = os.getenv("NAME", "world")
    print(f"Hello, {name}!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment",
        work_pool_name="my-work-pool",
        # Will print "Hello, Marvin!" by default instead of "Hello, world!"
        job_variables={"env": {"NAME": "Marvin"}},
        image="my-registry.com/my-docker-image:my-tag",
        push=False,
    )
```

Job variables can be used to customize environment variables, resources limits, and other infrastructure options, allowing fine-grained control over your infrastructure on a per-deployment or per-flow-run basis.
Any variable defined in the base job template of the associated work pool can be overridden by a job variable.
You can learn more about job variables [here](/v3/how-to-guides/deployments/customize-job-variables).

## [​](#deploy-multiple-flows) Deploy multiple flows

To deploy multiple flows at once, use the `deploy` function.

multi-deploy.py

Copy

```
from prefect import flow, deploy


@flow
def my_flow_1():
    print("I'm number one!")


@flow
def my_flow_2():
    print("Always second...")


if __name__ == "__main__":
    deploy(
        # Use the `to_deployment` method to specify configuration
        #specific to each deployment
        my_flow_1.to_deployment("my-deployment-1"),
        my_flow_2.to_deployment("my-deployment-2"),

        # Specify shared configuration for both deployments
        image="my-registry.com/my-docker-image:my-tag",
        push=False,
        work_pool_name="my-work-pool",
    )
```

When we run the above script, it will build a single Docker image for both deployments.
This approach offers the following benefits:

* Saves time and resources by avoiding redundant image builds.
* Simplifies management by maintaining a single image for multiple flows.

## [​](#further-reading) Further reading

* [Work Pools](/v3/concepts/work-pools)
* [Store Flow Code](/v3/deploy/infrastructure-concepts/store-flow-code)
* [Customize Infrastructure](/v3/how-to-guides/deployments/customize-job-variables)
* [Schedules](/v3/how-to-guides/deployments/create-schedules)
* [Write Workflows](/v3/how-to-guides/workflows/write-and-run)

Was this page helpful?

YesNo

[Manage Deployment schedules](/v3/how-to-guides/deployments/manage-schedules)[Define deployments with YAML](/v3/how-to-guides/deployments/prefect-yaml)

⌘I