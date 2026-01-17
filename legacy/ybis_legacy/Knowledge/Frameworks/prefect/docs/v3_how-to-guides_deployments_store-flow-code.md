How to retrieve code from storage - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Deployments

How to retrieve code from storage

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

* [Deployment creation options](#deployment-creation-options)
* [Store code locally](#store-code-locally)
* [Git-based storage](#git-based-storage)
* [Prefect Cloud GitHub Integration](#prefect-cloud-github-integration)
* [Docker-based storage](#docker-based-storage)
* [Custom Docker image](#custom-docker-image)
* [Blob storage](#blob-storage)

When a deployment runs, the execution environment needs access to the flow code.
Flow code is not stored directly in Prefect server or Prefect Cloud; instead, it must be made available to the execution environment. There are two main ways to achieve this:

1. **Include source code directly in your runtime:** Often, this means [building your code into a Docker image](/v3/how-to-guides/deployment_infra/docker#automatically-build-a-custom-docker-image-with-a-local-dockerfile).
2. **Retrieve code from storage at runtime:** The [worker](/v3/concepts/workers) pulls code from a specified location before starting the flow run.

This page focuses on the second approach: retrieving code from a storage location at runtime.
You have several options for where your code can be stored and pulled from:

* Local filesystem
* Git-based storage (GitHub, GitLab, Bitbucket)
* Blob storage (AWS S3, Azure Blob Storage, GCP GCS)

The ideal choice depends on your team’s needs and tools.
In the examples below, we show how to create a deployment configured to run on [dynamic infrastructure](/v3/concepts/work-pools) for each of these storage options.

## [​](#deployment-creation-options) Deployment creation options

As detailed in the [Deployment overview](/v3/deploy), you can create a deployment in one of two main ways:

* [Python code with the `flow.deploy` method](/v3/how-to-guides/deployments/deploy-via-python)
  + When using `.deploy`, specify a storage location for your flow with the `flow.from_source` method.
  + The `source` is either a URL to a git repository or a storage object. For example:
    - A local directory: `source=Path(__file__).parent` or `source="/path/to/file"`
    - A URL to a git repository: `source="https://github.com/org/my-repo.git"`
    - A storage object: `source=GitRepository(url="https://github.com/org/my-repo.git")`
  + The `entrypoint` is the path to the file the flow is located in and the function name, separated by a colon.
* [YAML specification defined in a `prefect.yaml` file](/v3/how-to-guides/deployments/prefect-yaml)
  + To create a `prefect.yaml` file interactively, run `prefect deploy` from the CLI and follow the prompts.
  + The `prefect.yaml` file may define a `pull` section that specifies the storage location for your flow. For example:
    - Set the working directory:

    Copy

    ```
    pull:
        - prefect.deployments.steps.set_working_directory:
            directory: /path/to/directory
    ```

    - Clone a git repository:

    Copy

    ```
    pull:
        - prefect.deployments.steps.git_clone:
            repository: https://github.com/org/my-repo.git
    ```

    - Pull from blob storage:

    Copy

    ```
    pull:
        - prefect.deployments.steps.pull_from_blob_storage:
            container: my-container
            folder: my-folder
    ```

Whether you use `from_source` or `prefect.yaml` to specify the storage location for your flow code, the resulting deployment will have a set of `pull` steps that your worker will use to retrieve the flow code at runtime.

## [​](#store-code-locally) Store code locally

If using a Process work pool, you can use one of the remote code storage options shown above, or you can store your flow code in a local folder.
Here is an example of how to create a deployment with flow code stored locally:

local\_process\_deploy\_local\_code.py

prefect.yaml

Copy

```
from prefect import flow
from pathlib import Path


@flow(log_prints=True)
def my_flow(name: str = "World"):
    print(f"Hello {name}!")


if __name__ == "__main__":
    my_flow.from_source(
        source=str(Path(__file__).parent),  # code stored in local directory
        entrypoint="local_process_deploy_local_code.py:my_flow",
    ).deploy(
        name="local-process-deploy-local-code",
        work_pool_name="my-process-pool",
    )
```

## [​](#git-based-storage) Git-based storage

Git-based version control platforms provide redundancy, version control, and collaboration capabilities. Prefect supports:

* [GitHub](https://github.com/)
* [GitLab](https://www.gitlab.com)
* [Bitbucket](https://bitbucket.org/)

For a public repository, you can use the repository URL directly.
If you are using a private repository and are authenticated in your environment at deployment creation and deployment execution, you can use the repository URL directly.
Alternatively, for a private repository, you can create a `Secret` block or `git`-platform-specific credentials [block](/v3/develop/blocks) to store your credentials:

* [`GitHubCredentials`](https://docs.prefect.io/integrations/prefect-github/)
* [`BitBucketCredentials`](https://docs.prefect.io/integrations/prefect-bitbucket/)
* [`GitLabCredentials`](https://docs.prefect.io/integrations/prefect-gitlab/)

Then you can reference this block in the Python `deploy` method or the `prefect.yaml` file pull step.
If using the Python `deploy` method with a private repository that references a block, provide a [`GitRepository`](https://reference.prefect.io/prefect/flows/#prefect.runner.storage.GitRepository) object instead of a URL, as shown below.

* GitHub
* Bitbucket
* GitLab

gh\_public\_repo.py

gh\_private\_repo\_credentials\_block.py

gh\_private\_repo\_secret\_block.py

prefect.yaml

Copy

```
from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/org/my-public-repo.git",
        entrypoint="gh_public_repo.py:my_flow",
    ).deploy(
        name="my-github-deployment",
        work_pool_name="my_pool",
    )
```

For accessing a private repository, we suggest creating a [Personal Access Tokens (PATs)](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).
We recommend using HTTPS with [fine-grained Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token) to limit access by repository.

**Personal Access Token Permissions**When using a fine-grained token, ensure to add permissions to the token prior to saving. Per least privilege, we recommend granting the token the ability to read **Contents** and **Metadata** for your repository.

If using a `Secret` block, you can create it through code or the UI ahead of time and reference it at deployment creation as shown above.If using a `GitHubCredentials` block to store your credentials, you can create it ahead of time and reference it at deployment creation.

1. Install `prefect-github` with `pip install -U prefect-github`
2. Register all block types defined in `prefect-github` with `prefect block register -m prefect_github`
3. Create a `GitHubCredentials` block through code or the Prefect UI and reference it at deployment creation as shown above.

bb\_public\_repo.py

bb\_private\_repo\_credentials\_block.py

bb\_private\_repo\_secret\_block.py

prefect.yaml

Copy

```
from prefect import flow


if __name__ == "__main__":
    flow.from_source(
        source="https://bitbucket.com/org/my-public-repo.git",
        entrypoint="bb_public_repo.py:my_flow",
    ).deploy(
        name="my-bitbucket-deployment",
        work_pool_name="my_pool",
    )
```

For accessing a private repository, we recommend using HTTPS with Repository, Project, or Workspace [Access Tokens](https://support.atlassian.com/bitbucket-cloud/docs/access-tokens/).[Create a token](https://support.atlassian.com/bitbucket-cloud/docs/create-a-repository-access-token/) with **read** access to the repository.Bitbucket requires you prepend the token string with `x-token-auth:` The full string looks like this: `x-token-auth:abc_123_this_is_a_token`.If using a `Secret` block, you can create it through code or the UI ahead of time and reference it at deployment creation as shown above.If using a `BitBucketCredentials` block to store your credentials, you can create it ahead of time and reference it at deployment creation.

1. Install `prefect-bitbucket` with `pip install -U prefect-bitbucket`
2. Register all block types defined in `prefect-bitbucket` with `prefect block register -m prefect_bitbucket`
3. Create a `BitBucketCredentials` block in code or the Prefect UI and reference at deployment creation as shown above.

gl\_public\_repo.py

gl\_private\_repo\_credentials\_block.py

gl\_private\_repo\_secret\_block.py

prefect.yaml

Copy

```
from prefect import flow


if __name__ == "__main__":
    gitlab_repo = "https://gitlab.com/org/my-public-repo.git"

    flow.from_source(
        source=gitlab_repo,
        entrypoint="gl_public_repo.py:my_flow"
    ).deploy(
        name="my-gitlab-deployment",
        work_pool_name="my_pool",
    )
```

For accessing a private repository, we recommend using HTTPS with [Project Access Tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html).[Create a token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) with the **read\_repository** scope.If using a `Secret` block, you can create it through code or the UI ahead of time and reference it at deployment creation as shown above.If using a `GitLabCredentials` block to store your credentials, you can create it ahead of time and reference it at deployment creation.

1. Install `prefect-gitlab` with `pip install -U prefect-gitlab`
2. Register all block types defined in `prefect-gitlab` with `prefect block register -m prefect_gitlab`
3. Create a `GitLabCredentials` block in code or the Prefect UI and reference it at deployment creation as shown above.

Note that you can specify a `branch` if creating a `GitRepository` object.
The default is `"main"`.

**Push your code**When you make a change to your code, Prefect does not push your code to your `git`-based version control platform.
This is intentional to avoid confusion about the `git` history and push process.

### [​](#prefect-cloud-github-integration) Prefect Cloud GitHub Integration

 If you’re using Prefect Cloud you can use the Prefect Cloud GitHub App
to authenticate to GitHub at runtime and access private repositories without creating a block and storing long
lived credentials.

1. [Install the Prefect Cloud GitHub App](https://github.com/apps/prefect-cloud/installations/new?) and select the
   repositories you want to be able to access.
2. Add the following pull steps to your `prefect.yaml` file. Make sure to replace `owner/repository` with the name of your repository:

Copy

```
pull:
    - prefect.deployments.steps.run_shell_script:
        id: get-github-token
        script: uv tool run prefect-cloud github token owner/repository
    - prefect.deployments.steps.git_clone:
        id: git-clone
        repository: https://x-access-token:{{ get-github-token.stdout }}@github.com/owner/repository.git
```

## [​](#docker-based-storage) Docker-based storage

Another popular flow code storage option is to include it in a Docker image.
All work pool options except **Process** and **Prefect Managed** allow you to bake your code into a Docker image.
To create a deployment with Docker-based flow code storage use the Python `deploy` method or create a `prefect.yaml` file.

If you use the Python `deploy` method to store the flow code in a Docker image, you don’t need to use the `from_source` method.

The `prefect.yaml` file below was generated by running `prefect deploy` from the CLI (a few lines of metadata were excluded from the top of the file output for brevity).
Note that the `build` section is necessary if baking your flow code into a Docker image.

docker\_deploy.py

prefect.yaml

Copy

```
from prefect import flow


@flow
def my_flow():
    print("Hello from inside a Docker container!")

if __name__ == "__main__":
    my_flow.deploy(
        name="my-docker-deploy",
        work_pool_name="my_pool",
        image="my-docker-image:latest",
        push=False
    )
```

By default, `.deploy` will build a Docker image that includes your flow code and any `pip` packages specified in a `requirements.txt` file.
In the examples above, we elected not to push the resulting image to a remote registry.
To push the image to a remote registry, pass `push=True` in the Python `deploy` method or add a `push_docker_image` step to the `push` section of the `prefect.yaml` file.

### [​](#custom-docker-image) Custom Docker image

If an `image` is not specified by one of the methods above, deployment flow runs associated with a Docker work pool will use the base Prefect image (e.g. `prefecthq/prefect:3-latest`) when executing.
Alternatively, you can create a custom Docker image outside of Prefect by running `docker build` && `docker push` elsewhere (e.g. in your CI/CD pipeline) and then reference the resulting `image` in the `job_variables` section of your deployment definition, or set the `image` as a default directly on the work pool.
For more information, see [this discussion of custom Docker images](/v3/how-to-guides/deployment_infra/docker#automatically-build-a-custom-docker-image-with-a-local-dockerfile).

## [​](#blob-storage) Blob storage

Another option for flow code storage is any [fsspec](https://filesystem-spec.readthedocs.io/en/latest/)-supported storage location, such as AWS S3, Azure Blob Storage, or GCP GCS.
If the storage location is publicly available, or if you are authenticated in the environment where you are creating and running your deployment, you can reference the storage location directly.
You don’t need to pass credentials explicitly.
To pass credentials explicitly to authenticate to your storage location, you can use either of the following block types:

* Prefect integration library storage blocks, such as the `prefect-aws` library’s `S3Bucket` block, which can use a `AWSCredentials` block when it is created.
* `Secret` blocks

If you use a storage block such as the `S3Bucket` block, you need to have the `prefect-aws` library available in the environment where your flow code runs.You can do any of the following to make the library available:

1. Install the library into the execution environment directly
2. Specify the library in the work pool’s Base Job Template in the **Environment Variables** section like this:`{"EXTRA_PIP_PACKAGES":"prefect-aws"}`
3. Specify the library in the environment variables of the `deploy` method as shown in the examples below
4. Specify the library in a `requirements.txt` file and reference the file in the `pull` step of the `prefect.yaml` file like this:

Copy

```
    - prefect.deployments.steps.pip_install_requirements:
        directory: "{{ pull_code.directory }}" 
        requirements_file: requirements.txt
```

The examples below show how to create a deployment with flow code in a cloud provider storage location.
For each example, we show how to access code that is publicly available.
The `prefect.yaml` example includes an additional line to reference a credentials block if authenticating to a private storage location through that option.
We also include Python code that shows how to use an existing storage block and an example of that creates, but doesn’t save, a storage block that references an existing nested credentials block.

* AWS S3 bucket
* Azure Blob Storage container
* GCP GCS bucket

s3\_no\_block.py

s3\_block.py

prefect.yaml

Copy

```
from prefect import flow


if __name__ == "__main__":
    flow.from_source(
        source="s3://my-bucket/my-folder",
        entrypoint="my_file.py:my_flow",
    ).deploy(
        name="my-aws-s3-deployment",
        work_pool_name="my-work-pool"
    )
```

To create an `AwsCredentials` block:

1. Install the [prefect-aws](/integrations/prefect-aws) library with `pip install -U prefect-aws`
2. Register the blocks in prefect-aws with `prefect block register -m prefect_aws`
3. Create a user with a role with read and write permissions to access the bucket. If using the UI, create an access key pair with *IAM -> Users -> Security credentials -> Access keys -> Create access key*. Choose *Use case -> Other* and then copy the *Access key* and *Secret access key* values.
4. Create an [`AWSCredentials` block](/integrations/prefect-aws/index#save-credentials-to-an-aws-credentials-block) in code or the Prefect UI. In addition to the block name, most users will fill in the *AWS Access Key ID* and *AWS Access Key Secret* fields.
5. Reference the block as shown above.

azure\_no\_block.py

azure\_block.py

prefect.yaml

Copy

```
from prefect import flow


if __name__ == "__main__":
    flow.from_source(
        source="az://mycontainer/myfolder",
        entrypoint="my_file.py:my_flow",
    ).deploy(
        name="my-azure-deployment",
        work_pool_name="my-work-pool",
        job_variables={"env": {"EXTRA_PIP_PACKAGES": "prefect-azure"} }, 
    )
```

To create an `AzureBlobCredentials` block:

1. Install the [prefect-azure](/integrations/prefect-azure) library with `pip install -U prefect-azure`
2. Register the blocks in prefect-azure with `prefect block register -m prefect_azure`
3. Create an access key for a role with sufficient (read and write) permissions to access the blob.
   You can create a connection string containing all required information in the UI under *Storage Account -> Access keys*.
4. Create an Azure Blob Storage Credentials block in code or the Prefect UI. Enter a name for the block and paste the
   connection string into the *Connection String* field.
5. Reference the block as shown above.

gcs\_no\_block.py

gcs\_block.py

prefect.yaml

Copy

```
from prefect import flow


if __name__ == "__main__":
    flow.from_source(
        source="gs://my-bucket/my-folder",  
        entrypoint="my_file.py:my_flow",
    ).deploy(
        name="my-gcs-deployment",
        work_pool_name="my-work-pool"
    )
```

To create a `GcpCredentials` block:

1. Install the [prefect-gcp](/integrations/prefect-gcp) library with `pip install -U prefect-gcp`
2. Register the blocks in prefect-gcp with `prefect block register -m prefect_gcp`
3. Create a service account in GCP for a role with read and write permissions to access the bucket contents.
   If using the GCP console, go to *IAM & Admin -> Service accounts -> Create service account*.
   After choosing a role with the required permissions,
   see your service account and click on the three dot menu in the *Actions* column.
   Select *Manage Keys -> ADD KEY -> Create new key -> JSON*. Download the JSON file.
4. Create a GCP Credentials block in code or the Prefect UI. Enter a name for the block and paste the entire contents of the JSON key file into the *Service Account Info* field.
5. Reference the block as shown above.

Another authentication option is to give the worker access to the storage location at runtime through SSH keys.

Was this page helpful?

YesNo

[Define deployments with YAML](/v3/how-to-guides/deployments/prefect-yaml)[Version Deployments](/v3/how-to-guides/deployments/versioning)

⌘I