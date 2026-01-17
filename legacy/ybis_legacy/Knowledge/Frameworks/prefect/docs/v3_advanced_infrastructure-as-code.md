How to manage Prefect resources using Infrastructure as Code - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Platform

How to manage Prefect resources using Infrastructure as Code

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

* [Terraform](#terraform)
* [Terraform Modules](#terraform-modules)
* [Pulumi](#pulumi)
* [Managing Resources with Pulumi](#managing-resources-with-pulumi)
* [Example: Deploying a Flow with Pulumi](#example%3A-deploying-a-flow-with-pulumi)
* [Helm](#helm)

You can manage many Prefect resources with tools like
[Terraform](https://www.terraform.io/) and [Helm](https://helm.sh/). These
options are a viable alternative to Prefect’s CLI and UI.

## [​](#terraform) Terraform

You can manage resources with the [Terraform provider for Prefect](https://registry.terraform.io/providers/PrefectHQ/prefect/latest/docs/guides/getting-started).
This documentation represents all Prefect resources that are supported by Terraform.
This Terraform provider is maintained by the Prefect team, and is undergoing active development
to reach [parity with the Prefect API](https://github.com/PrefectHQ/terraform-provider-prefect/milestone/1).
The Prefect team welcomes contributions, feature requests, and bug reports
via our [issue tracker](https://github.com/PrefectHQ/terraform-provider-prefect/issues).

### [​](#terraform-modules) Terraform Modules

Prefect maintains several Terraform modules to help you get started with common infrastructure patterns:

* [Bucket Sensors for AWS, Azure, and GCP](https://github.com/PrefectHQ/terraform-prefect-bucket-sensor)
* [ECS Worker on AWS Fargate](https://github.com/PrefectHQ/terraform-prefect-ecs-worker)
* [ACI Worker on Azure Container Instances](https://github.com/PrefectHQ/terraform-prefect-aci-worker)

## [​](#pulumi) Pulumi

Prefect does not maintain an official Pulumi package.
However, you can use Pulumi’s terraform-provider to automatically generate a Pulumi SDK from the Prefect Terraform provider.
For details, refer to the [Pulumi documentation on Terraform providers](www.pulumi.com/registry/packages/terraform-provider/).

You will need to be using Pulumi version >= 3.147.0.

In this example, we will use Pulumi to deploy a flow to Prefect.
Prefect recommends using the `uv` for managing Python dependencies.
This example will show you how to set up a Pulumi project using the `uv` toolchain.

Creating a new Pulumi project

To create a new Python Pulumi project using the `uv` toolchain, run the following command:

Copy

```
pulumi new python \
--yes \
--generate-only \
--name "my-prefect-pulumi-project" \
--description "A Pulumi project to manage Prefect resources" \
--runtime-options toolchain=uv \
--runtime-options virtualenv=.venv
```

Don’t name your project any of the following, otherwise you will have package name conflicts:

* `pulumi`
* `prefect`
* `pulumi-prefect`

An explanation of the [flags](https://www.pulumi.com/docs/iac/cli/commands/pulumi_new/#options) used:

* The `--yes` flag skips the interactive prompts and accepts the defaults. You can omit this flag,
  or edit the generated `Pulumi.yaml` file later to customize your project settings.
* The `--generate-only` just creates a new Pulumi project. It does not create a stack, save config,
  or install dependencies.
* The `--name` and `--description` flags set the name and description of your Pulumi project.
* The `--runtime-options toolchain=uv` and `--runtime-options virtualenv=.venv` flags configures
  the Pulumi project to use the `uv` toolchain instead of the default, `pip`.

To finish setting up your new Pulumi project, navigate to the project directory and install the dependencies:

Copy

```
pulumi install
```

Using an existing Pulumi project

If you already have a Pulumi project, you can switch to the `uv` toolchain by updating
your `pulumi.yaml` file `runtime` settings as shown below:

Pulumi.yaml

Copy

```
# other project settings...
runtime:
  name: python
  options:
    toolchain: uv
    virtualenv: .venv
```

This configures your Pulumi project to use the `uv` toolchain and the virtual environment located at `.venv`.Run the following to update Pulumi to use the `uv` toolchain:

Copy

```
pulumi install
```

### [​](#managing-resources-with-pulumi) Managing Resources with Pulumi

To manage resources with Pulumi, add the Prefect Terraform provider to your Pulumi project:

Copy

```
pulumi package add terraform-provider prefecthq/prefect
```

Optionally, you can specify a specific version, e.g.:

Copy

```
pulumi package add terraform-provider prefecthq/prefect 2.90.0
```

This will auto-generate a `pulumi-prefect` Python package.
The code will be placed in the `sdks/prefect` directory inside the Pulumi project.

### [​](#example:-deploying-a-flow-with-pulumi) Example: Deploying a Flow with Pulumi

This simple example shows you how to deploy a flow to Prefect.

Copy

```
import json
import pulumi
import pulumi_prefect as prefect
from prefect.utilities.callables import parameter_schema
from typing import Callable, Any

# Import your flow here
from my_flow import test as example_flow


def generate_openapi_schema_for_flow(flow_obj: Callable[..., Any]) -> str:
    """
    Utility function to generate an OpenAPI schema for a flow's parameters.
    This is used to provide type information for deployments created via Pulumi.
    
    See also:
        * `parameter_schema <https://github.com/PrefectHQ/prefect/blob/main/src/prefect/utilities/callables.py#L331>`_
        * `model_dump_for_openapi <https://github.com/PrefectHQ/prefect/blob/main/src/prefect/utilities/callables.py#L247>`_
    """
    return json.dumps(parameter_schema(flow_obj).model_dump_for_openapi())

# Configure the Provider
provider = prefect.Provider(
    "prefect",
    # endpoint="https://api.prefect.cloud/api/account/<account>/workspace/<workspace>",
    # api_key="<your_api_key>",  # or use pulumi.Config to manage secrets
)

# Register the Flow
flow = prefect.Flow(
    "example-flow",
    name="example-flow",
    tags=["example", "pulumi"],
    opts=pulumi.ResourceOptions(provider=provider)
)

# Create a Deployment resource
deployment = prefect.Deployment(
    "example-deployment",
    name="example-deployment",
    flow_id=flow.id,
    work_pool_name="example-work-pool",
    work_queue_name="default",
    parameters=json.dumps({"foo": "bar"}),
    tags=["example", "pulumi"],
    enforce_parameter_schema=True,
    parameter_openapi_schema=generate_openapi_schema_for_flow(example_flow),
    opts=pulumi.ResourceOptions(provider=provider),

    # specify how to get the flow code to the worker
    # the Deployment resource does not have the same support as `prefect.yaml` for automatically packaging flow code
    # see: https://registry.terraform.io/providers/PrefectHQ/prefect/latest/docs/resources/deployment#deployment-actions

    # option 1: clone the repo at runtime
    # pull_steps = [
    #     {
    #         "type": "git_clone",
    #         "repository": "https://github.com/some/repo",
    #         "branch": "main",
    #         "include_submodules": True,
    #     }
    # ],
    # entrypoint="flow.py:hello_flow",

    # option 2: use a pre-built container image
    # note: you will need to build this image yourself and push it to a registry
    # job_variables = json.dumps({
    #     "image": "example.registry.com/example-repo/example-image:v1"
    # })
)

# Add a schedule to the deployment to run every minute
schedule = prefect.DeploymentSchedule(
    "example-schedule",
    deployment_id=deployment.id,
    active=True,
    cron="0 * * * *",
    timezone="UTC",
    opts=pulumi.ResourceOptions(provider=provider),
)
```

Now you can run `pulumi up` to create the resources in your Prefect workspace.

## [​](#helm) Helm

You can manage resources with the [Prefect Helm charts](https://github.com/PrefectHQ/prefect-helm/tree/main/charts).
Each Helm chart subdirectory contains usage documentation. There are two main charts:

* The `prefect-server` chart is used to a deploy a Prefect server. This is an alternative to using
  [Prefect Cloud](https://app.prefect.cloud/).
* The `prefect-worker` chart is used to deploy a [Prefect worker](/v3/deploy/infrastructure-concepts/workers).

Finally, there is a `prefect-prometheus-exporter` chart that is used to deploy a Prometheus exporter,
exposing Prefect metrics for monitoring and alerting.

Was this page helpful?

YesNo

[Build deployments via CI/CD](/v3/advanced/deploy-ci-cd)[Self-host the Prefect Server with Helm](/v3/advanced/server-helm)

⌘I