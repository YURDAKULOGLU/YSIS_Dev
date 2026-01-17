How to run flows on Kubernetes - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflow Infrastructure

How to run flows on Kubernetes

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

* [Prerequisites](#prerequisites)
* [Create a cluster](#create-a-cluster)
* [Create a container registry](#create-a-container-registry)
* [Create a Kubernetes work pool](#create-a-kubernetes-work-pool)
* [Configure work pool options](#configure-work-pool-options)
* [Create a Prefect Cloud API key](#create-a-prefect-cloud-api-key)
* [Deploy a worker using Helm](#deploy-a-worker-using-helm)
* [Add the Prefect Helm repository](#add-the-prefect-helm-repository)
* [Create a namespace](#create-a-namespace)
* [Create a Kubernetes secret for the Prefect API key](#create-a-kubernetes-secret-for-the-prefect-api-key)
* [Configure Helm chart values](#configure-helm-chart-values)
* [Create a Helm release](#create-a-helm-release)
* [Verify deployment](#verify-deployment)
* [Define a flow](#define-a-flow)
* [Define a Prefect deployment](#define-a-prefect-deployment)
* [Tag images with a Git SHA](#tag-images-with-a-git-sha)
* [Authenticate to Prefect](#authenticate-to-prefect)
* [Deploy the flows](#deploy-the-flows)
* [Run the flows](#run-the-flows)

This guide explains how to run flows on Kubernetes.
Though much of the guide is general to any Kubernetes cluster, it focuses on
Amazon Elastic Kubernetes Service (EKS). Prefect is tested against
Kubernetes 1.26.0 and newer minor versions.

## [​](#prerequisites) Prerequisites

1. A Prefect Cloud account
2. A cloud provider (AWS, GCP, or Azure) account
3. Python and Prefect [installed](/v3/get-started/install)
4. Helm [installed](https://helm.sh/docs/intro/install/)
5. Kubernetes CLI (kubectl)[installed](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
6. Admin access for Prefect Cloud and your cloud provider. You can downgrade it after this setup.

## [​](#create-a-cluster) Create a cluster

If you already have one, skip ahead to the next section.

* AWS
* GCP
* Azure

One easy way to get set up with a cluster in EKS is with [`eksctl`](https://eksctl.io/).
Node pools can be backed by either EC2 instances or FARGATE.
Choose FARGATE so there’s less to manage.
The following command takes around 15 minutes and must not be interrupted:

Copy

```
# Replace the cluster name with your own value
eksctl create cluster --fargate --name <CLUSTER-NAME>

# Authenticate to the cluster.
aws eks update-kubeconfig --name <CLUSTER-NAME>
```

You can get a GKE cluster up and running with a few commands using the
[`gcloud` CLI](https://cloud.google.com/sdk/docs/install).
This builds a bare-bones cluster that is accessible over the open
internet - but it should **not** be used in a production environment.
To deploy the cluster, your project must have a VPC network configured.First, authenticate to GCP by setting the following configuration options:

Copy

```
# Authenticate to gcloud
gcloud auth login

# Specify the project & zone to deploy the cluster to
# Replace the project name with your GCP project name
gcloud config set project <GCP-PROJECT-NAME>
gcloud config set compute/zone <AVAILABILITY-ZONE>
```

Next, deploy the cluster. This command takes ~15 minutes to complete.
Once the cluster has been created, authenticate to the cluster.

Copy

```
# Create cluster
# Replace the cluster name with your own value
gcloud container clusters create <CLUSTER-NAME> --num-nodes=1 \
--machine-type=n1-standard-2

# Authenticate to the cluster
gcloud container clusters <CLUSTER-NAME> --region <AVAILABILITY-ZONE>
```

**GCP potential errors**

Copy

```
ERROR: (gcloud.container.clusters.create) ResponseError: code=400, message=Service account "000000000000-compute@developer.gserviceaccount.com" is disabled.
```

* You must enable the default service account in the IAM console, or
  specify a different service account with the appropriate permissions.

Copy

```
creation failed: Constraint constraints/compute.vmExternalIpAccess violated for project 000000000000. Add instance projects/<GCP-PROJECT-NAME>/zones/us-east1-b/instances/gke-gke-guide-1-default-pool-c369c84d-wcfl to the constraint to use external IP with it."
```

* Organization policy blocks creation of external (public) IPs. Override
  this policy (if you have the appropriate permissions) under the `Organizational Policy`
  page within IAM.

Create an AKS cluster using the
[Azure CLI](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli),
or use the Cloud Shell directly from the Azure portal [shell.azure.com](https://shell.azure.com).First, authenticate to Azure if not already done.

Copy

```
  az login
```

Next, deploy the cluster - this command takes ~4 minutes to complete.
Once the cluster is created, authenticate to the cluster.

Copy

```
  # Create a Resource Group at the desired location, e.g. westus
  az group create --name <RESOURCE-GROUP-NAME> --location <LOCATION>

  # Create a kubernetes cluster with default kubernetes version, default SKU load balancer (Standard) and default vm set type (VirtualMachineScaleSets)
  az aks create --resource-group <RESOURCE-GROUP-NAME> --name <CLUSTER-NAME>

  # Configure kubectl to connect to your Kubernetes cluster
  az aks get-credentials --resource-group <RESOURCE-GROUP-NAME> --name <CLUSTER-NAME>

  # Verify the connection by listing the cluster nodes
  kubectl get nodes
```

## [​](#create-a-container-registry) Create a container registry

Besides a cluster, the other critical resource is a container registry.
A registry is not strictly required, but in most cases you’ll want to use custom
images and/or have more control over where images are stored.
If you already have a registry, skip ahead to the next section.

* AWS
* GCP
* Azure

Create a registry using the AWS CLI and authenticate the docker daemon to
that registry:

Copy

```
# Replace the image name with your own value
aws ecr create-repository --repository-name <IMAGE-NAME>

# Login to ECR
# Replace the region and account ID with your own values
aws ecr get-login-password --region <REGION> | docker login \
  --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
```

Create a registry using the gcloud CLI and authenticate the docker daemon to
that registry:

Copy

```
# Create artifact registry repository to host your custom image
# Replace the repository name with your own value; it can be the
# same name as your image
gcloud artifacts repositories create <REPOSITORY-NAME> \
--repository-format=docker --location=us

# Authenticate to artifact registry
gcloud auth configure-docker us-docker.pkg.dev
```

Create a registry using the Azure CLI and authenticate the docker daemon to
that registry:

Copy

```
# Name must be a lower-case alphanumeric
# Tier SKU can easily be updated later, e.g. az acr update --name <REPOSITORY-NAME> --sku Standard
az acr create --resource-group <RESOURCE-GROUP-NAME> \
  --name <REPOSITORY-NAME> \
  --sku Basic

# Attach ACR to AKS cluster
# You need Owner, Account Administrator, or Co-Administrator role on your Azure subscription as per Azure docs
az aks update --resource-group <RESOURCE-GROUP-NAME> --name <CLUSTER-NAME> --attach-acr <REPOSITORY-NAME>

# You can verify AKS can now reach ACR
az aks check-acr --resource-group RESOURCE-GROUP-NAME> --name <CLUSTER-NAME> --acr <REPOSITORY-NAME>.azurecr.io
```

## [​](#create-a-kubernetes-work-pool) Create a Kubernetes work pool

[Work pools](/v3/deploy/infrastructure-concepts/work-pools) allow you to manage deployment
infrastructure.
This section shows you how to configure the default values for your
Kubernetes base job template.
These values can be overridden by individual deployments.
Switch to the Prefect Cloud UI to create a new Kubernetes work pool.
(Alternatively, you could use the Prefect CLI to create a work pool.)

1. Click on the **Work Pools** tab on the left sidebar
2. Click the **+** button at the top of the page
3. Select **Kubernetes** as the work pool type
4. Click **Next** to configure the work pool settings
5. Set the `namespace` field to `prefect`

If you set a different namespace, use your selected namespace instead of `prefect` in all commands below.

You may come back to this page to configure the work pool options at any time.

### [​](#configure-work-pool-options) Configure work pool options

Here are some popular configuration options.
**Environment Variables**
Add environment variables to set when starting a flow run.
If you are using a Prefect-maintained image and haven’t overwritten the image’s
entrypoint, you can specify Python packages to install at runtime with `{"EXTRA_PIP_PACKAGES":"my_package"}`.
For example `{"EXTRA_PIP_PACKAGES":"pandas==1.2.3"}` installs pandas version 1.2.3.
Alternatively, you can specify package installation in a custom Dockerfile, which
allows you to use image caching.
As shown below, Prefect can help create a Dockerfile with your flow code and the
packages specified in a `requirements.txt` file baked in.
**Namespace**
Set the Kubernetes namespace to create jobs within, such as `prefect`. By default, set
to **default**.
**Image**
Specify the Docker container image for created jobs.
If not set, the latest Prefect 3 image is used (for example, `prefecthq/prefect:3-latest`).
You can override this on each deployment through `job_variables`.
**Image Pull Policy**
Select from the dropdown options to specify when to pull the image.
When using the `IfNotPresent` policy, make sure to use unique image tags, or
old images may get cached on your nodes.
**Finished Job TTL**
Number of seconds before finished jobs are automatically cleaned up by the Kubernetes
controller.
Set to 60 so completed flow runs are cleaned up after a minute.
**Pod Watch Timeout Seconds**
Number of seconds for pod creation to complete before timing out.
Consider setting to 300, especially if using a **serverless** type node pool, as
these tend to have longer startup times.
**Kubernetes cluster config**
Specify a KubernetesClusterConfig block to configure the Kubernetes cluster for job creation.
In most cases, leave the cluster config blank since the worker should already have appropriate
access and permissions.
We recommend using this setting when deploying a worker to a cluster that differs from the one
executing the flow runs.

**Advanced Settings**Modify the default base job template to add other fields or delete existing
fields.Select the **Advanced** tab and edit the JSON representation of the base job template.For example, to set a CPU request, add the following section under variables:

Copy

```
"cpu_request": {
  "title": "CPU Request",
  "description": "The CPU allocation to request for this pod.",
  "default": "default",
  "type": "string"
},
```

Next add the following to the first `containers` item under `job_configuration`:

Copy

```
...
"containers": [
  {
    ...,
    "resources": {
      "requests": {
        "cpu": "{{ cpu_request }}"
      }
    }
  }
],
...
```

Running deployments with this work pool will request the specified CPU.

After configuring the work pool settings, move to the next screen.
Give the work pool a name and save.
Your new Kubernetes work pool should appear in the list of work pools.

## [​](#create-a-prefect-cloud-api-key) Create a Prefect Cloud API key

If you already have a Prefect Cloud API key, you can skip these steps.
To create a Prefect Cloud API key:

1. Log in to the Prefect Cloud UI.
2. Click on your profile avatar picture in the top right corner.
3. Click on your name to go to your profile settings.
4. In the left sidebar, click on [API Keys](https://app.prefect.cloud/my/api-keys).
5. Click the **+** button to create a new API key.
6. Securely store the API key, ideally using a password manager.

## [​](#deploy-a-worker-using-helm) Deploy a worker using Helm

After you create a cluster and work pool, the next step is to deploy a worker.
The worker sets up the necessary Kubernetes infrastructure to run your flows.
The recommended method for deploying a worker is with the [Prefect Helm Chart](https://github.com/PrefectHQ/prefect-helm/tree/main/charts/prefect-worker).

### [​](#add-the-prefect-helm-repository) Add the Prefect Helm repository

Add the Prefect Helm repository to your Helm client:

Copy

```
helm repo add prefect https://prefecthq.github.io/prefect-helm
helm repo update
```

### [​](#create-a-namespace) Create a namespace

Create a new namespace in your Kubernetes cluster to deploy the Prefect worker:

Copy

```
kubectl create namespace prefect
```

### [​](#create-a-kubernetes-secret-for-the-prefect-api-key) Create a Kubernetes secret for the Prefect API key

Copy

```
kubectl create secret generic prefect-api-key \
--namespace=prefect --from-literal=key=your-prefect-cloud-api-key
```

### [​](#configure-helm-chart-values) Configure Helm chart values

Create a `values.yaml` file to customize the Prefect worker configuration.
Add the following contents to the file:

Copy

```
worker:
  cloudApiConfig:
    accountId: <target account ID>
    workspaceId: <target workspace ID>
  config:
    workPool: <target work pool name>
```

These settings ensure that the worker connects to the proper account, workspace,
and work pool.
View your Account ID and Workspace ID in your browser URL when logged into Prefect Cloud.
For example: <[https://app.prefect.cloud/account/abc-my-account-id-is-here/workspaces/123-my-workspace-id-is-here>](https://app.prefect.cloud/account/abc-my-account-id-is-here/workspaces/123-my-workspace-id-is-here%3E).

### [​](#create-a-helm-release) Create a Helm release

Install the Prefect worker using the Helm chart with your custom `values.yaml` file:

Copy

```
helm install prefect-worker prefect/prefect-worker \
  --namespace=prefect \
  -f values.yaml
```

### [​](#verify-deployment) Verify deployment

Check the status of your Prefect worker deployment:

Copy

```
kubectl get pods -n prefect
```

## [​](#define-a-flow) Define a flow

Start simple with a flow that just logs a message.
In a directory named `flows`, create a file named `hello.py` with the following contents:

Copy

```
from prefect import flow, tags
from prefect.logging import get_run_logger

@flow
def hello(name: str = "Marvin"):
    logger = get_run_logger()
    logger.info(f"Hello, {name}!")

if __name__ == "__main__":
    with tags("local"):
        hello()
```

Run the flow locally with `python hello.py` to verify that it works.
Use the `tags` context manager to tag the flow run as `local`.
This step is not required, but does add some helpful metadata.

## [​](#define-a-prefect-deployment) Define a Prefect deployment

Prefect has two recommended options for creating a deployment with dynamic infrastructure.
You can define a deployment in a Python script using the `flow.deploy` mechanics or in a
`prefect.yaml` definition file.
The `prefect.yaml` file currently allows for more customization in terms of push and pull
steps.
To learn about the Python deployment creation method with `flow.deploy` see
[Workers](/v3/how-to-guides/deployment_infra/docker).
The [`prefect.yaml`](/v3/deploy/infrastructure-concepts/prefect-yaml#managing-deployments) file is used
by the `prefect deploy` command to deploy your flows.
As a part of that process it also builds and pushes your image.
Create a new file named `prefect.yaml` with the following contents:

Copy

```
# Generic metadata about this project
name: flows
prefect-version: 3.0.0

# build section allows you to manage and build docker images
build:
- prefect_docker.deployments.steps.build_docker_image:
    id: build-image
    requires: prefect-docker>=0.4.0
    image_name: "{{ $PREFECT_IMAGE_NAME }}"
    tag: latest
    dockerfile: auto
    platform: "linux/amd64"

# push section allows you to manage if and how this project is uploaded to remote locations
push:
- prefect_docker.deployments.steps.push_docker_image:
    requires: prefect-docker>=0.4.0
    image_name: "{{ build-image.image_name }}"
    tag: "{{ build-image.tag }}"

# pull section allows you to provide instructions for cloning this project in remote
locations
pull:
- prefect.deployments.steps.set_working_directory:
    directory: /opt/prefect/flows

# the definitions section allows you to define reusable components for your deployments
definitions:
  tags: &common_tags
    - "eks"
  work_pool: &common_work_pool
    name: "kubernetes"
    job_variables:
      image: "{{ build-image.image }}"

# the deployments section allows you to provide configuration for deploying flows
deployments:
- name: "default"
  tags: *common_tags
  schedule: null
  entrypoint: "flows/hello.py:hello"
  work_pool: *common_work_pool

- name: "arthur"
  tags: *common_tags
  schedule: null
  entrypoint: "flows/hello.py:hello"
  parameters:
    name: "Arthur"
  work_pool: *common_work_pool
```

We define two deployments of the `hello` flow: `default` and `arthur`.
By specifying `dockerfile: auto`, Prefect automatically creates a dockerfile
that installs any `requirements.txt` and copies over the current directory.
You can pass a custom Dockerfile instead with `dockerfile: Dockerfile` or
`dockerfile: path/to/Dockerfile`.
We are specifically building for the `linux/amd64` platform.
This specification is often necessary when images are built on Macs with M series chips
but run on cloud provider instances.

**Deployment specific build, push, and pull**You can override the build, push, and pull steps for each deployment.
This allows for more custom behavior, such as specifying a different image for each
deployment.

Define your requirements in a `requirements.txt` file:

Copy

```
prefect>=3.0.0
prefect-docker>=0.4.0
prefect-kubernetes>=0.3.1
```

The directory should now look something like this:

Copy

```
.
├── prefect.yaml
└── flows
    ├── requirements.txt
    └── hello.py
```

### [​](#tag-images-with-a-git-sha) Tag images with a Git SHA

If your code is stored in a GitHub repository, it’s good practice to tag your images
with the Git SHA of the code used to build it.
Do this in the `prefect.yaml` file with a few minor modifications, since it’s not yet
an option with the Python deployment creation method.
Use the `run_shell_script` command to grab the SHA and pass it to the `tag`
parameter of `build_docker_image`:

Copy

```
build:
- prefect.deployments.steps.run_shell_script:
    id: get-commit-hash
    script: git rev-parse --short HEAD
    stream_output: false
- prefect_docker.deployments.steps.build_docker_image:
    id: build-image
    requires: prefect-docker>=0.4.0
    image_name: "{{ $PREFECT_IMAGE_NAME }}"
    tag: "{{ get-commit-hash.stdout }}"
    dockerfile: auto
    platform: "linux/amd64"
```

Set the SHA as a tag for easy identification in the UI:

Copy

```
definitions:
  tags: &common_tags
    - "eks"
    - "{{ get-commit-hash.stdout }}"
  work_pool: &common_work_pool
    name: "kubernetes"
    job_variables:
      image: "{{ build-image.image }}"
```

## [​](#authenticate-to-prefect) Authenticate to Prefect

Before deploying the flows to Prefect, you need to authenticate through the Prefect CLI.
You also need to ensure that all of your flow’s dependencies are present at `deploy` time.
This example uses a virtual environment to ensure consistency across environments.

Copy

```
# Create a virtualenv & activate it
virtualenv prefect-demo
source prefect-demo/bin/activate

# Install dependencies of your flow
prefect-demo/bin/pip install -r requirements.txt

# Authenticate to Prefect & select the appropriate
# workspace to deploy your flows to
prefect-demo/bin/prefect cloud login
```

## [​](#deploy-the-flows) Deploy the flows

You’re ready to deploy your flows to build your images.
The image name determines its registry.
You have configured our `prefect.yaml` file to get the image name from the
`PREFECT_IMAGE_NAME` environment variable, so set that first:

* AWS
* GCP
* Azure

Copy

```
export PREFECT_IMAGE_NAME=<AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/<IMAGE-NAME>
```

Copy

```
export PREFECT_IMAGE_NAME=us-docker.pkg.dev/<GCP-PROJECT-NAME>/<REPOSITORY-NAME>/<IMAGE-NAME>
```

Copy

```
export PREFECT_IMAGE_NAME=<REPOSITORY-NAME>.azurecr.io/<IMAGE-NAME>
```

To deploy your flows, ensure your Docker daemon is running. Deploy all the
flows with `prefect deploy --all` or deploy them individually by name: `prefect deploy -n hello/default` or `prefect deploy -n hello/arthur`.

## [​](#run-the-flows) Run the flows

Once the deployments are successfully created, you can run them from the UI or the CLI:

Copy

```
prefect deployment run hello/default
prefect deployment run hello/arthur
```

You can now check the status of your two deployments in the UI.

Was this page helpful?

YesNo

[Run flows in a static container](/v3/how-to-guides/deployment_infra/serve-flows-docker)[Run flows on Modal](/v3/how-to-guides/deployment_infra/modal)

⌘I