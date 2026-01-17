How to run flows on serverless compute - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflow Infrastructure

How to run flows on serverless compute

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

* [Automatic infrastructure provisioning](#automatic-infrastructure-provisioning)
* [Prerequisites](#prerequisites)
* [Automatically create a new push work pool and provision infrastructure](#automatically-create-a-new-push-work-pool-and-provision-infrastructure)
* [Use existing resources with automatic infrastructure provisioning](#use-existing-resources-with-automatic-infrastructure-provisioning)
* [Provision infrastructure for an existing push work pool](#provision-infrastructure-for-an-existing-push-work-pool)
* [Manual infrastructure provisioning](#manual-infrastructure-provisioning)
* [Work pool configuration](#work-pool-configuration)
* [Create a Credentials block](#create-a-credentials-block)
* [Create a push work pool](#create-a-push-work-pool)
* [Deployment](#deployment)
* [Putting it all together](#putting-it-all-together)
* [Usage Limits](#usage-limits)
* [Next steps](#next-steps)

Push [work pools](/v3/deploy/infrastructure-concepts/work-pools) are a special type of work pool. They allow
Prefect Cloud to submit flow runs for execution to serverless computing infrastructure without requiring you to run a worker.
Push work pools currently support execution in AWS ECS tasks, Azure Container Instances, Google Cloud Run jobs, Modal, and Coiled.
In this guide you will:

* Create a push work pool that sends work to Amazon Elastic Container Service (AWS ECS), Azure Container Instances (ACI),
  Google Cloud Run, Modal, or Coiled
* Deploy a flow to that work pool
* Execute a flow without having to run a worker process to poll for flow runs

You can automatically provision infrastructure and create your push work pool using the `prefect work-pool create`
CLI command with the `--provision-infra` flag.
This approach greatly simplifies the setup process.

First, you will set up automatic infrastructure provisioning for push work pools. Then you will learn how to manually
set up your push work pool.

## [​](#automatic-infrastructure-provisioning) Automatic infrastructure provisioning

With Perfect Cloud you can provision infrastructure for use with an AWS ECS, Google Cloud Run, ACI push work pool.
Push work pools in Prefect Cloud simplify the setup and management of the infrastructure necessary to run your flows.
However, setting up infrastructure on your cloud provider can still be a time-consuming process.
Prefect dramatically simplifies this process by automatically provisioning the necessary infrastructure for you.
We’ll use the `prefect work-pool create` CLI command with the `--provision-infra` flag to automatically provision your
serverless cloud resources and set up your Prefect workspace to use a new push pool.

### [​](#prerequisites) Prerequisites

To use automatic infrastructure provisioning, you need:

* the relevant cloud CLI library installed
* to be authenticated with your cloud provider

* AWS ECS
* Azure Container Instances
* Google Cloud Run
* Modal
* Coiled

Install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html),
[authenticate with your AWS account](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html),
and [set a default region](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-methods).If you already have the AWS CLI installed, be sure to [update to the latest version](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions).You will need the following permissions in your authenticated AWS account:IAM Permissions:

* iam:CreatePolicy
* iam:GetPolicy
* iam:ListPolicies
* iam:CreateUser
* iam:GetUser
* iam:AttachUserPolicy
* iam:CreateRole
* iam:GetRole
* iam:AttachRolePolicy
* iam:ListRoles
* iam:PassRole

Amazon ECS Permissions:

* ecs:CreateCluster
* ecs:DescribeClusters

Amazon EC2 Permissions:

* ec2:CreateVpc
* ec2:DescribeVpcs
* ec2:CreateInternetGateway
* ec2:AttachInternetGateway
* ec2:CreateRouteTable
* ec2:CreateRoute
* ec2:CreateSecurityGroup
* ec2:DescribeSubnets
* ec2:CreateSubnet
* ec2:DescribeAvailabilityZones
* ec2:AuthorizeSecurityGroupIngress
* ec2:AuthorizeSecurityGroupEgress

Amazon ECR Permissions:

* ecr:CreateRepository
* ecr:DescribeRepositories
* ecr:GetAuthorizationToken

If you want to use AWS managed policies, you can use the following:

* AmazonECS\_FullAccess
* AmazonEC2FullAccess
* IAMFullAccess
* AmazonEC2ContainerRegistryFullAccess

The above policies give you all the permissions needed, but are more permissive than necessary.[Docker](https://docs.docker.com/get-docker/) is also required to build and push images to your registry.

Install the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) and
[authenticate with your Azure account](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli).If you already have the Azure CLI installed, be sure to update to the latest version with `az upgrade`.You will also need the following roles in your Azure subscription:

* Contributor
* User Access Administrator
* Application Administrator
* Managed Identity Operator
* Azure Container Registry Contributor

Docker is also required to build and push images to your registry. You can install Docker
[here](https://docs.docker.com/get-docker/).

Install the [gcloud CLI](https://cloud.google.com/sdk/docs/install) and
[authenticate with your GCP project](https://cloud.google.com/docs/authentication/gcloud).If you already have the gcloud CLI installed, be sure to update to the latest version with `gcloud components update`.You will also need the following permissions in your GCP project:

* resourcemanager.projects.list
* serviceusage.services.enable
* iam.serviceAccounts.create
* iam.serviceAccountKeys.create
* resourcemanager.projects.setIamPolicy
* artifactregistry.repositories.create

Docker is also required to build and push images to your registry. You can install Docker
[here](https://docs.docker.com/get-docker/).

Install `modal` by running:

Copy

```
pip install modal
```

Create a Modal API token by running:

Copy

```
modal token new
```

See [Run flows on Modal](/v3/how-to-guides/deployment_infra/modal) for more details.

Install `coiled` by running:

Copy

```
pip install coiled prefect-coiled
```

Create a Coiled API token by running:

Copy

```
coiled login
```

Connect Coiled to your cloud account by running

Copy

```
coiled setup
```

or by navigating to [cloud.coiled.io/get-started](https://cloud.coiled.io/get-started)

### [​](#automatically-create-a-new-push-work-pool-and-provision-infrastructure) Automatically create a new push work pool and provision infrastructure

To create a new push work pool and configure the necessary infrastructure,
run this command for your particular cloud provider:

* AWS ECS
* Azure Container Instances
* Google Cloud Run
* Modal
* Coiled

Copy

```
prefect work-pool create --type ecs:push --provision-infra my-ecs-pool
```

The `--provision-infra` flag automatically sets up your default AWS account to execute
flows with ECS tasks.
In your AWS account, this command creates a new IAM user, IAM policy, and
ECS cluster that uses AWS Fargate, VPC, and ECR repository (if they don’t already exist).
In your Prefect workspace, this command creates an
[`AWSCredentials` block](/integrations/prefect-aws/index#save-credentials-to-an-aws-credentials-block) for storing the generated credentials.Here’s an abbreviated example output from running the command:

Copy

```
_____________________________________________________________________________________________
| Provisioning infrastructure for your work pool my-ecs-pool will require:                   |
|                                                                                            |
|          - Creating an IAM user for managing ECS tasks: prefect-ecs-user                   |
|          - Creating and attaching an IAM policy for managing ECS tasks: prefect-ecs-policy |
|          - Storing generated AWS credentials in a block                                    |
|          - Creating an ECS cluster for running Prefect flows: prefect-ecs-cluster          |
|          - Creating a VPC with CIDR 172.31.0.0/16 for running ECS tasks: prefect-ecs-vpc   |
|          - Creating an ECR repository for storing Prefect images: prefect-flows            |
_____________________________________________________________________________________________
Proceed with infrastructure provisioning? [y/n]: y
Provisioning IAM user
Creating IAM policy
Generating AWS credentials
Creating AWS credentials block
Provisioning ECS cluster
Provisioning VPC
Creating internet gateway
Setting up subnets
Setting up security group
Provisioning ECR repository
Authenticating with ECR
Setting default Docker build namespace
Provisioning Infrastructure ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Infrastructure successfully provisioned!
Created work pool 'my-ecs-pool'!
```

**Default Docker build namespace**After infrastructure provisioning completes, you will be logged into your new ECR repository and the default
Docker build namespace will be set to the URL of the registry.

While the default namespace is set, you do not need to provide the registry URL when building images as
part of your deployment process.To take advantage of this, you can write your deploy scripts like this:

example\_deploy\_script.py

Copy

```
from prefect import flow
from prefect.docker import DockerImage

@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello {name}! I'm a flow running in a ECS task!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment",
        work_pool_name="my-work-pool",
        image=DockerImage(
            name="my-repository:latest",
            platform="linux/amd64",
        )
    )
```

This builds an image with the tag `<ecr-registry-url>/my-image:latest` and push it to the registry.Your image name needs to match the name of the repository created with your work pool. You can create
new repositories in the ECR console.

Copy

```
prefect work-pool create --type azure-container-instance:push --provision-infra my-aci-pool
```

The `--provision-infra` flag automatically sets up your default Azure account to execute
flows through Azure Container Instances.
In your Azure account, this command creates a resource group, app registration, service account with necessary permission,
generates a secret for the app registration, and creates an Azure Container Registry, (if they don’t already exist).
In your Prefect workspace, this command creates an
[`AzureContainerInstanceCredentials` block](/integrations/prefect-azure)
to store the client secret value from the generated secret.Here’s an abbreviated example output from running the command:

Copy

```
_____________________________________________________________________________________________
| Provisioning infrastructure for your work pool my-aci-work-pool will require:             |
|                                                                                           |
|     Updates in subscription Azure subscription 1                                          |
|                                                                                           |
|         - Create a resource group in location eastus                                      |
|         - Create an app registration in Azure AD prefect-aci-push-pool-app                |
|         - Create/use a service principal for app registration                             |
|         - Generate a secret for app registration                                          |
|         - Create an Azure Container Registry with prefix prefect                           |
|         - Create an identity prefect-acr-identity to allow access to the created registry |
|         - Assign Contributor role to service account                                      |
|         - Create an ACR registry for image hosting                                        |
|         - Create an identity for Azure Container Instance to allow access to the registry |
|                                                                                           |
|     Updates in Prefect workspace                                                          |
|                                                                                           |
|         - Create Azure Container Instance credentials block aci-push-pool-credentials     |
|                                                                                           |
_____________________________________________________________________________________________
Proceed with infrastructure provisioning? [y/n]:
Creating resource group
Creating app registration
Generating secret for app registration
Creating ACI credentials block
ACI credentials block 'aci-push-pool-credentials' created in Prefect Cloud
Assigning Contributor role to service account
Creating Azure Container Registry
Creating identity
Provisioning infrastructure... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Infrastructure successfully provisioned for 'my-aci-work-pool' work pool!
Created work pool 'my-aci-work-pool'!
```

**Default Docker build namespace**
After infrastructure provisioning completes, you are logged into your new Azure Container Registry and
the default Docker build namespace is set to the URL of the registry.

While the default namespace is set, any images you build without specifying a registry or username/organization
are pushed to the registry.To use this capability, write your deploy scripts like this:

example\_deploy\_script.py

Copy

```
from prefect import flow
from prefect.docker import DockerImage


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello {name}! I'm a flow running on an Azure Container Instance!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment",
        work_pool_name="my-work-pool",
        image=DockerImage(
            name="my-image:latest",
            platform="linux/amd64",
        )
    )
```

This builds an image with the tag `<acr-registry-url>/my-image:latest` and pushes it to the registry.

Copy

```
prefect work-pool create --type cloud-run:push --provision-infra my-cloud-run-pool
```

The `--provision-infra` flag allows you to select a GCP project to use for your work pool and automatically
configures it to execute flows through Cloud Run.
In your GCP project, this command activates the Cloud Run API, creates a service account, and creates a key for the
service account, (if they don’t already exist).
In your Prefect workspace, this command creates a
[`GCPCredentials` block](/integrations/prefect-gcp/index#authenticate-using-a-gcp-credentials-block) to store the service account key.Here’s an abbreviated example output from running the command:

Copy

```
____________________________________________________________________________________________________________
| Provisioning infrastructure for your work pool my-cloud-run-pool will require:                           |
|                                                                                                          |
|     Updates in GCP project central-kit-405415 in region us-central1                                      |
|                                                                                                          |
|         - Activate the Cloud Run API for your project                                                    |
|         - Activate the Artifact Registry API for your project                                            |
|         - Create an Artifact Registry repository named prefect-images                                    |
|         - Create a service account for managing Cloud Run jobs: prefect-cloud-run                        |
|             - Service account will be granted the following roles:                                       |
|                 - Service Account User                                                                   |
|                 - Cloud Run Developer                                                                    |
|         - Create a key for service account prefect-cloud-run                                             |
|                                                                                                          |
|     Updates in Prefect workspace                                                                         |
|                                                                                                          |
|         - Create GCP credentials block my--pool-push-pool-credentials to store the service account key   |
|                                                                                                          |
____________________________________________________________________________________________________________
Proceed with infrastructure provisioning? [y/n]: y
Activating Cloud Run API
Activating Artifact Registry API
Creating Artifact Registry repository
Configuring authentication to Artifact Registry
Setting default Docker build namespace
Creating service account
Assigning roles to service account
Creating service account key
Creating GCP credentials block
Provisioning Infrastructure ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Infrastructure successfully provisioned!
Created work pool 'my-cloud-run-pool'!
```

**Default Docker build namespace**After infrastructure provisioning completes, you are logged into your new Artifact Registry repository
and the default Docker build namespace is set to the URL of the repository.

While the default namespace is set, any images you build without specifying a registry or username/organization
are pushed to the repository.To use this capability, write your deploy scripts like this:

example\_deploy\_script.py

Copy

```
from prefect import flow
from prefect.docker import DockerImage


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello {name}! I'm a flow running on Cloud Run!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment",
        work_pool_name="above-ground",
        image=DockerImage(
            name="my-image:latest",
            platform="linux/amd64",
        )
    )
```

This builds an image with the tag `<region>-docker.pkg.dev/<project>/<repository-name>/my-image:latest`
and pushes it to the repository.

Copy

```
prefect work-pool create --type modal:push --provision-infra my-modal-pool
```

Using the `--provision-infra` flag triggers the creation of a `ModalCredentials` block in your Prefect Cloud workspace.
This block stores your Modal API token, which authenticates with Modal’s API. By default, the token for your
current Modal profile is used for the new `ModalCredentials` block. If Prefect is unable to discover a Modal
API token for your current profile, you will be prompted to create a new one.

Copy

```
prefect work-pool create --type coiled:push --provision-infra my-coiled-pool
```

Using the `--provision-infra` flag triggers the creation of a `CoiledCredentials` block in your Prefect Cloud workspace.
This block stores your Coiled API token, which authenticates with Coiled’s API.

You’re ready to create and schedule deployments that use your new push work pool.
Reminder that no worker is required to run flows with a push work pool.

### [​](#use-existing-resources-with-automatic-infrastructure-provisioning) Use existing resources with automatic infrastructure provisioning

If you already have the necessary infrastructure set up, Prefect detects that at work pool creation and the
infrastructure provisioning for that resource is skipped.
For example, here’s how `prefect work-pool create my-work-pool --provision-infra` looks when existing Azure resources are detected:

Copy

```
Proceed with infrastructure provisioning? [y/n]: y
Creating resource group
Resource group 'prefect-aci-push-pool-rg' already exists in location 'eastus'.
Creating app registration
App registration 'prefect-aci-push-pool-app' already exists.
Generating secret for app registration
Provisioning infrastructure
ACI credentials block 'bb-push-pool-credentials' created
Assigning Contributor role to service account...
Service principal with object ID '4be6fed7-...' already has the 'Contributor' role assigned in
'/subscriptions/.../'
Creating Azure Container Instance
Container instance 'prefect-aci-push-pool-container' already exists.
Creating Azure Container Instance credentials block
Provisioning infrastructure... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Infrastructure successfully provisioned!
Created work pool 'my-work-pool'!
```

## [​](#provision-infrastructure-for-an-existing-push-work-pool) Provision infrastructure for an existing push work pool

If you already have a push work pool set up, but haven’t configured the necessary infrastructure, you can use the
`provision-infra` sub-command to provision the infrastructure for that work pool.
For example, you can run the following command if you have a work pool named “my-work-pool”.

Copy

```
prefect work-pool provision-infra my-work-pool
```

Prefect creates the necessary infrastructure for the `my-work-pool` work pool and provides you with a summary
of the changes:

Copy

```
__________________________________________________________________________________________________________________
| Provisioning infrastructure for your work pool my-work-pool will require:                                      |
|                                                                                                                |
|     Updates in subscription Azure subscription 1                                                               |
|                                                                                                                |
|         - Create a resource group in location eastus                                                           |
|         - Create an app registration in Azure AD prefect-aci-push-pool-app                                     |
|         - Create/use a service principal for app registration                                                  |
|         - Generate a secret for app registration                                                               |
|         - Assign Contributor role to service account                                                           |
|         - Create Azure Container Instance 'aci-push-pool-container' in resource group prefect-aci-push-pool-rg |
|                                                                                                                |
|     Updates in Prefect workspace                                                                               |
|                                                                                                                |
|         - Create Azure Container Instance credentials block aci-push-pool-credentials                          |
|                                                                                                                |
__________________________________________________________________________________________________________________
Proceed with infrastructure provisioning? [y/n]: y
```

This command speeds up your infrastructure setup process.
As with the examples above, you need to have the related cloud CLI library installed and to be authenticated with
your cloud provider.

## [​](#manual-infrastructure-provisioning) Manual infrastructure provisioning

If you prefer to set up your infrastructure manually, exclude the `--provision-infra` flag in the CLI command.
In the examples below, you’ll create a push work pool through the Prefect Cloud UI.

* AWS ECS
* Azure Container Instances
* Google Cloud Run
* Modal
* Coiled

To push work to ECS, AWS credentials are required.Create a user and attach the *AmazonECS\_FullAccess* permissions.From that user’s page, create credentials and store them somewhere safe for use in the next section.

To push work to Azure, you need an Azure subscription, resource group, and tenant secret.**Create Subscription and Resource Group**

1. In the Azure portal, create a subscription.
2. Create a resource group within your subscription.

**Create App Registration**

1. In the Azure portal, create an app registration.
2. In the app registration, create a client secret. Copy the value and store it somewhere safe.

**Add App Registration to Resource Group**

1. Navigate to the resource group you created earlier.
2. Choose the “Access control (IAM)” blade in the left-hand side menu. Click ”+ Add” button at the top, then
   “Add role assignment”.
3. Go to the “Privileged administrator roles” tab, click on “Contributor”, then click “Next” at the bottom of the page.
4. Click on ”+ Select members”. Type the name of the app registration (otherwise it may not autopopulate) and click to add it.
   Then hit “Select” and click “Next”. The default permissions associated with a role like “Contributor” may
   not be sufficient for all operations related to Azure Container Instances (ACI). The specific permissions
   required depend on the operations you need to perform (like creating, running, and deleting ACI container groups)
   and your organization’s security policies. In some cases, additional permissions or custom roles are necessary.
5. Click “Review + assign” to finish.

You need a GCP service account and an API Key to push work to Cloud Run.Create a service account by navigating to the service accounts page and clicking *Create*. Name and describe your service account,
and click *continue* to configure permissions.The service account must have two roles at a minimum: *Cloud Run Developer* and *Service Account User*.![Configuring service account permissions in GCP](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/guides/gcr-service-account-setup.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=6fc561f651b41f62449f14c6f2fa9b57)Once you create the Service account, navigate to its *Keys* page to add an API key. Create a JSON type key, download it,
and store it somewhere safe for use in the next section.

You need a Modal API token to push work to Modal.Navigate to **Settings** in the Modal UI to create a Modal API token. In the **API Tokens** section of the Settings page,
click **New Token**.Copy the token ID and token secret and store them somewhere safe for use in the next section.

You need a Coiled API token to push work to Coiled.In the Coiled UI click on your avatar and select **Profile**. Then press the **Create API Token** button and copy the result. You will need it in the next section.

### [​](#work-pool-configuration) Work pool configuration

The push work pool stores information about what type of infrastructure the flow will run on, what default values to
provide to compute jobs, and other important execution environment parameters. Because the push work pool needs to
integrate securely with your serverless infrastructure, you need to store your credentials in Prefect Cloud by making a block.

### [​](#create-a-credentials-block) Create a Credentials block

* AWS ECS
* Azure Container Instances
* Google Cloud Run
* Modal
* Coiled

Navigate to the blocks page, click create new block, and select AWS Credentials for the type.For use in a push work pool, set the region, access key, and access key secret.Provide any other optional information and create your block.

Navigate to the blocks page and click the ”+” at the top to create a new block. Find the Azure Container
Instance Credentials block and click “Add +”.Locate the client ID and tenant ID on your app registration and use the client secret you saved earlier.
Make sure the value of the secret, not the secret ID.Provide any other optional information and click “Create”.

Navigate to the blocks page, click create new block, and select GCP Credentials for the type.For use in a push work pool, this block must have the contents of the JSON key stored in the
Service Account Info field, as such:![Configuring GCP Credentials block for use in cloud run push work pools](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/guides/gcp-creds-block-setup.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=93b1d4a0324a6100442e9b231f6c6ad7)Provide any other optional information and create your block.

Navigate to the blocks page, click create new block, and select Modal Credentials for the type.For use in a push work pool, this block must have the token ID and token secret stored in the Token ID and Token
Secret fields, respectively.

Navigate to the blocks page, click create new block, and select Coiled Credentials for the type. Provide the API token from the previous section.

### [​](#create-a-push-work-pool) Create a push work pool

Now navigate to the work pools page.
Click **Create** to configure your push work pool by selecting a push option in the infrastructure type step.

* AWS ECS
* Azure Container Instances
* Google Cloud Run
* Modal
* Coiled

Each step has several optional fields that are detailed in the
[work pools documentation](/v3/deploy/infrastructure-concepts/work-pools).
Select the block you created under the AWS Credentials field.
This allows Prefect Cloud to securely interact with your ECS cluster.

Fill in the subscription ID and resource group name from the resource group you created.
Add the Azure Container Instance Credentials block you created in the step above.

Each step has several optional fields that are detailed in
[Manage infrastructure with work pools](/v3/deploy/infrastructure-concepts/work-pools).
Select the block you created under the GCP Credentials field.
This allows Prefect Cloud to securely interact with your GCP project.

Each step has several optional fields that are detailed in the
[work pools documentation](/v3/deploy/infrastructure-concepts/work-pools).
Select the block you created under the Modal Credentials field.
This allows Prefect Cloud to securely interact with your Modal account.

Each step has several optional fields that are detailed in the
[work pools documentation](/v3/deploy/infrastructure-concepts/work-pools).
Select the block you created under the Coiled Credentials field.
This allows Prefect Cloud to securely interact with your Coiled account.

Create your pool to be ready to deploy flows to your Push work pool.

## [​](#deployment) Deployment

You need to configure your [deployment](/v3/how-to-guides/deployment_infra/docker) to send flow runs to your push work pool.
For example, if you create a deployment through the interactive command line experience,
choose the work pool you just created. If you are deploying an existing `prefect.yaml` file, the deployment would contain:

Copy

```
  work_pool:
    name: my-push-pool
```

Deploying your flow to the `my-push-pool` work pool ensures that runs that are ready for execution are
submitted immediately—without the need for a worker to poll for them.

**Serverless infrastructure may require a certain image architecture**Serverless infrastructure may assume a certain Docker image architecture; for example,
Google Cloud Run will fail to run images built with `linux/arm64` architecture. If using Prefect to build your image,
you can change the image architecture through the `platform` keyword (for example, `platform="linux/amd64"`).

## [​](#putting-it-all-together) Putting it all together

With your deployment created, navigate to its detail page and create a new flow run.
You’ll see the flow start running without polling the work pool, because Prefect Cloud securely connected
to your serverless infrastructure, created a job, ran the job, and reported on its execution.

## [​](#usage-limits) Usage Limits

Push work pool usage is unlimited. However push work pools limit flow runs to 24 hours.

## [​](#next-steps) Next steps

Learn more about [work pools](/v3/deploy/infrastructure-concepts/work-pools) and [workers](/v3/deploy/infrastructure-concepts/workers).
Learn about installing dependencies at runtime or baking them into your Docker image in the [Deploy to Docker](/v3/how-to-guides/deployment_infra/docker#automatically-build-a-custom-docker-image-with-a-local-dockerfile) guide.

Was this page helpful?

YesNo

[Run flows on Prefect Managed infrastructure](/v3/how-to-guides/deployment_infra/managed)[Run flows in Docker containers](/v3/how-to-guides/deployment_infra/docker)

⌘I