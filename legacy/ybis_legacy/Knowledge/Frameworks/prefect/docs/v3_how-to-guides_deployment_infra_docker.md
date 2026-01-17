How to run flows in Docker containers - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflow Infrastructure

How to run flows in Docker containers

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

* [Create a work pool](#create-a-work-pool)
* [Start a worker](#start-a-worker)
* [Create the deployment](#create-the-deployment)
* [Automatically bake your code into a Docker image](#automatically-bake-your-code-into-a-docker-image)
* [Automatically build a custom Docker image with a local Dockerfile](#automatically-build-a-custom-docker-image-with-a-local-dockerfile)
* [Store your code in git-based cloud storage](#store-your-code-in-git-based-cloud-storage)
* [Additional configuration with .deploy](#additional-configuration-with-deploy)
* [Work with multiple deployments with deploy](#work-with-multiple-deployments-with-deploy)
* [Learn more](#learn-more)

In this example, you will set up:

* a Docker [**work pool**](/v3/deploy/infrastructure-concepts/work-pools): stores the infrastructure configuration for your deployment
* a Docker [**worker**](/v3/deploy/infrastructure-concepts/workers): process that polls the Prefect API for flow runs to execute as Docker containers
* a [**deployment**](/v3/deploy/index): a flow that should run according to the configuration on your Docker work pool

Then you can execute your deployment via the Prefect API (through the SDK, CLI, UI, etc).
You must have [Docker](https://docs.docker.com/engine/install/) installed and running on your machine.

**Executing flows in a long-lived container**This guide shows how to run a flow in an ephemeral container that is removed after the flow run completes.
To instead learn how to run flows in a static, long-lived container, see [this](/v3/deploy/static-infrastructure-examples/docker) guide.

### [​](#create-a-work-pool) Create a work pool

A work pool provides default infrastructure configurations that all jobs inherit and can override.
You can adjust many defaults, such as the base Docker image, container cleanup behavior, and resource limits.
To set up a **Docker** type work pool with the default values, run:

Copy

```
prefect work-pool create --type docker my-docker-pool
```

… or create the work pool in the UI.
To confirm the work pool creation was successful, run:

Copy

```
prefect work-pool ls
```

You should see your new `my-docker-pool` listed in the output.
Next, check that you can see this work pool in your Prefect UI.
Navigate to the **Work Pools** tab and verify that you see `my-docker-pool` listed.
When you click into `my-docker-pool`, you should see a red status icon signifying that this work pool is not ready.
To make the work pool ready, you’ll need to start a worker.
We’ll show how to do this next.

### [​](#start-a-worker) Start a worker

Workers are a lightweight polling process that kick off scheduled flow runs on a specific type of infrastructure (such as Docker).
To start a worker on your local machine, open a new terminal and confirm that your virtual environment has `prefect` installed.
Run the following command in this new terminal to start the worker:

Copy

```
prefect worker start --pool my-docker-pool
```

You should see the worker start.
It’s now polling the Prefect API to check for any scheduled flow runs it should pick up and then submit for execution.
You’ll see your new worker listed in the UI under the **Workers** tab of the Work Pools page with a recent last polled date.
The work pool should have a `Ready` status indicator.

**Pro Tip:**If `my-docker-pool` does not already exist, the below command will create it for you automatically with the default settings for that work pool type, in this case `docker`.

Copy

```
prefect worker start --pool my-docker-pool --type docker
```

Keep this terminal session active for the worker to continue to pick up jobs.
Since you are running this worker locally, the worker will if you close the terminal.
In a production setting this worker should run as a [daemonized or managed process](/v3/deploy/daemonize-processes).

## [​](#create-the-deployment) Create the deployment

From the previous steps, you now have:

* A work pool
* A worker

Next, you’ll create a deployment from your flow code.

### [​](#automatically-bake-your-code-into-a-docker-image) Automatically bake your code into a Docker image

Create a deployment from Python code by calling the `.deploy` method on a flow:

deploy\_buy.py

Copy

```
from prefect import flow

@flow(log_prints=True)
def buy():
    print("Buying securities")

if __name__ == "__main__":
    buy.deploy(
        name="my-code-baked-into-an-image-deployment",
        work_pool_name="my-docker-pool",
        image="my_registry/my_image:my_image_tag" # YOUR IMAGE REGISTRY
    )
```

Now, run the script to create a deployment (in future examples this step is omitted for brevity):

Copy

```
python deploy_buy.py
```

You should see messages in your terminal that Docker is building your image.
When the deployment build succeeds, you will see information in your terminal showing you how to start a worker for your
deployment, and how to run your deployment.
Your deployment is visible on the `Deployments` page in the UI.
By default, `.deploy` builds a Docker image with your flow code baked into it and pushes the image to the
[Docker Hub](https://hub.docker.com/) registry implied by the `image` argument to `.deploy`.

**Authentication to Docker Hub**Your environment must be authenticated to your Docker registry to push an image to it.

You can specify a registry other than Docker Hub by providing the full registry path in the `image` argument.

If building a Docker image, your environment with your deployment needs Docker installed and running.

To avoid pushing to a registry, set `push=False` in the `.deploy` method:

Copy

```
if __name__ == "__main__":
    buy.deploy(
        name="my-code-baked-into-an-image-deployment",
        work_pool_name="my-docker-pool",
        image="my_registry/my_image:my_image_tag",
        push=False
    )
```

To avoid building an image, set `build=False` in the `.deploy` method:

Copy

```
if __name__ == "__main__":
    buy.deploy(
        name="my-code-baked-into-an-image-deployment",
        work_pool_name="my-docker-pool",
        image="my_registry/already-built-image:1.0",
        build=False
    )
```

The specified image must be available in your deployment’s execution environment for accessible flow code.
Prefect generates a Dockerfile for you that builds an image based off of one of Prefect’s published images.
The generated Dockerfile copies the current directory into the Docker image and installs any dependencies listed
in a `requirements.txt` file.

### [​](#automatically-build-a-custom-docker-image-with-a-local-dockerfile) Automatically build a custom Docker image with a local Dockerfile

If you want to use a custom image, specify the path to your Dockerfile via `DockerImage`:

my\_flow.py

Copy

```
from prefect import flow
from prefect.docker import DockerImage


@flow(log_prints=True)
def buy():
    print("Buying securities")


if __name__ == "__main__":
    buy.deploy(
        name="my-custom-dockerfile-deployment",
        work_pool_name="my-docker-pool",
        image=DockerImage(
            name="my_image",
            tag="deploy-guide",
            dockerfile="Dockerfile"
    ),
    push=False
)
```

The `DockerImage` object enables image customization.
For example, you can install a private Python package from GCP’s artifact registry like this:

1. Create a custom base Dockerfile.

   sample.Dockerfile

   Copy

   ```
   FROM python:3.12

   ARG AUTHED_ARTIFACT_REG_URL
   COPY ./requirements.txt /requirements.txt

   RUN pip install --extra-index-url ${AUTHED_ARTIFACT_REG_URL} -r /requirements.txt
   ```
2. Create your deployment with the `DockerImage` class:

   deploy\_using\_private\_package.py

   Copy

   ```
   from prefect import flow
   from prefect.deployments.runner import DockerImage
   from prefect.blocks.system import Secret
   from myproject.cool import do_something_cool


   @flow(log_prints=True)
   def my_flow():
       do_something_cool()


   if __name__ == "__main__":
       artifact_reg_url = Secret.load("artifact-reg-url")

       my_flow.deploy(
           name="my-deployment",
           work_pool_name="my-docker-pool",
           image=DockerImage(
               name="my-image",
               tag="test",
               dockerfile="sample.Dockerfile",
               buildargs={"AUTHED_ARTIFACT_REG_URL": artifact_reg_url.get()},
           ),
       )
   ```

Note that this example used a [Prefect Secret block](/v3/develop/blocks) to load the URL configuration for
the artifact registry above.
See all the optional keyword arguments for the [`DockerImage` class](https://docker-py.readthedocs.io/en/stable/images.html#docker.models.images.ImageCollection.build).

**Default Docker namespace**You can set the `PREFECT_DEFAULT_DOCKER_BUILD_NAMESPACE` setting to append a default Docker namespace to all images
you build with `.deploy`. This is helpful if you use a private registry to store your images.To set a default Docker namespace for your current profile run:

Copy

```
prefect config set PREFECT_DEFAULT_DOCKER_BUILD_NAMESPACE=<docker-registry-url>/<organization-or-username>
```

Once set, you can omit the namespace from your image name when creating a deployment:

with\_default\_docker\_namespace.py

Copy

```
if __name__ == "__main__":
    buy.deploy(
        name="my-code-baked-into-an-image-deployment",
        work_pool_name="my-docker-pool",
        image="my_image:my_image_tag"
    )
```

The above code builds an image with the format `<docker-registry-url>/<organization-or-username>/my_image:my_image_tag`
when `PREFECT_DEFAULT_DOCKER_BUILD_NAMESPACE` is set.

### [​](#store-your-code-in-git-based-cloud-storage) Store your code in git-based cloud storage

While baking code into Docker images is a popular deployment option, many teams store their workflow code in git-based
storage, such as GitHub, Bitbucket, or GitLab.
If you don’t specify an `image` argument for `.deploy`, you must specify where to pull the flow code from at runtime
with the `from_source` method.
Here’s how to pull your flow code from a GitHub repository:

git\_storage.py

Copy

```
from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        "https://github.com/my_github_account/my_repo/my_file.git",
        entrypoint="flows/no-image.py:hello_world",
    ).deploy(
        name="no-image-deployment",
        work_pool_name="my-docker-pool",
        build=False
    )
```

The `entrypoint` is the path to the file the flow is located in and the function name, separated by a colon.
See the [Store flow code](/v3/deploy/infrastructure-concepts/store-flow-code) guide for more flow code storage options.

### [​](#additional-configuration-with-deploy) Additional configuration with `.deploy`

Next, see deployment configuration options.
To pass parameters to your flow, you can use the `parameters` argument in the `.deploy` method. Just pass in a dictionary of
key-value pairs.

pass\_params.py

Copy

```
from prefect import flow


@flow
def hello_world(name: str):
    print(f"Hello, {name}!")


if __name__ == "__main__":
    hello_world.deploy(
        name="pass-params-deployment",
        work_pool_name="my-docker-pool",
        parameters=dict(name="Prefect"),
        image="my_registry/my_image:my_image_tag",
    )
```

The `job_variables` parameter allows you to fine-tune the infrastructure settings for a deployment.
The values passed in override default values in the specified work pool’s
[base job template](/v3/deploy/infrastructure-concepts/work-pools#base-job-template).
You can override environment variables, such as `image_pull_policy` and `image`, for a specific deployment with the `job_variables`
argument.

job\_var\_image\_pull.py

Copy

```
if __name__ == "__main__":
    get_repo_info.deploy(
        name="my-deployment-never-pull",
        work_pool_name="my-docker-pool",
        job_variables={"image_pull_policy": "Never"},
        image="my-image:my-tag",
        push=False
    )
```

Similarly, you can override the environment variables specified in a work pool through the `job_variables` parameter:

job\_var\_env\_vars.py

Copy

```
if __name__ == "__main__":
    get_repo_info.deploy(
        name="my-deployment-never-pull",
        work_pool_name="my-docker-pool",
        job_variables={"env": {"EXTRA_PIP_PACKAGES": "boto3"} },
        image="my-image:my-tag",
        push=False
    )
```

The dictionary key “EXTRA\_PIP\_PACKAGES” denotes a special environment variable that Prefect uses to install additional
Python packages at runtime.
This approach is an alternative to building an image with a custom `requirements.txt` copied into it.
See [Override work pool job variables](/v3/deploy/infrastructure-concepts/customize) for more information about how to customize these variables.

### [​](#work-with-multiple-deployments-with-deploy) Work with multiple deployments with `deploy`

Create multiple deployments from one or more Python files that use `.deploy`.
You can manage these deployments independently of one another to deploy the same flow with different configurations
in the same codebase.
To create multiple deployments at once, use the `deploy` function, which is analogous to the `serve` function:

Copy

```
from prefect import deploy, flow


@flow(log_prints=True)
def buy():
    print("Buying securities")


if __name__ == "__main__":
    deploy(
        buy.to_deployment(name="dev-deploy", work_pool_name="my-docker-pool"),
        buy.to_deployment(name="prod-deploy", work_pool_name="my-other-docker-pool"),
        image="my-registry/my-image:dev",
        push=False,
    )
```

In the example above you created two deployments from the same flow, but with different work pools.
Alternatively, you can create two deployments from different flows:

Copy

```
from prefect import deploy, flow


@flow(log_prints=True)
def buy():
    print("Buying securities.")


@flow(log_prints=True)
def sell():
    print("Selling securities.")


if __name__ == "__main__":
    deploy(
        buy.to_deployment(name="buy-deploy"),
        sell.to_deployment(name="sell-deploy"),
        work_pool_name="my-docker-pool",
        image="my-registry/my-image:dev",
        push=False,
    )
```

In the example above, the code for both flows is baked into the same image.
You can specify one or more flows to pull from a remote location at runtime with the `from_source` method.
Here’s an example of deploying two flows, one defined locally and one defined in a remote repository:

Copy

```
from prefect import deploy, flow


@flow(log_prints=True)
def local_flow():
    print("I'm a flow!")


if __name__ == "__main__":
    deploy(
        local_flow.to_deployment(name="example-deploy-local-flow"),
        flow.from_source(
            source="https://github.com/org/repo.git",
            entrypoint="flows.py:my_flow",
        ).to_deployment(
            name="example-deploy-remote-flow",
        ),
        work_pool_name="my-docker-pool",
        image="my-registry/my-image:dev",
    )
```

You can pass any number of flows to the `deploy` function.
This is useful if using a monorepo approach to your workflows.

## [​](#learn-more) Learn more

* [Deploy flows on Kubernetes](/v3/how-to-guides/deployment_infra/kubernetes)
* [Deploy flows on serverless infrastructure](/v3/how-to-guides/deployment_infra/serverless)
* [Daemonize workers](/v3/deploy/daemonize-processes)

Was this page helpful?

YesNo

[Run flows on serverless compute](/v3/how-to-guides/deployment_infra/serverless)[Run flows in a static container](/v3/how-to-guides/deployment_infra/serve-flows-docker)

⌘I