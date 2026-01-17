How to transfer resources between Prefect environments - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Migrate

How to transfer resources between Prefect environments

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

* [Quick start](#quick-start)
* [What gets transferred](#what-gets-transferred)
* [Common transfer scenarios](#common-transfer-scenarios)
* [Development to production](#development-to-production)
* [Self-hosted to cloud migration](#self-hosted-to-cloud-migration)
* [Workspace consolidation](#workspace-consolidation)
* [Resource handling](#resource-handling)
* [Work pools](#work-pools)
* [Existing resources](#existing-resources)
* [Resource limits](#resource-limits)
* [Limitations](#limitations)
* [Resources not transferred](#resources-not-transferred)
* [Environment-specific configuration](#environment-specific-configuration)
* [Best practices](#best-practices)
* [Pre-transfer checklist](#pre-transfer-checklist)
* [Post-transfer validation](#post-transfer-validation)
* [Troubleshooting](#troubleshooting)
* [Common issues](#common-issues)
* [Debug mode](#debug-mode)
* [See also](#see-also)

The `prefect transfer` command enables you to migrate resources between different Prefect environments, whether moving from development to production, from self-hosted to cloud, or between cloud workspaces.
The command accepts a `--from` and `--to` [profile](/v3/concepts/settings-and-profiles#profiles), and transfers all resources from the source to the destination.

The transfer command is available in Prefect [3.4.14](/v3/release-notes/oss/version-3-4) and later.

## [​](#quick-start) Quick start

Transfer all resources from a development environment to production:

Copy

```
prefect transfer --from local --to cloud
```

The command will:

1. Discover all resources in the source profile
2. Transfer resources to the destination profile
3. Report success, failures, and skipped resources

## [​](#what-gets-transferred) What gets transferred

The transfer command moves the following resources:

* [Flows](/v3/concepts/flows) and [deployments](/v3/concepts/deployments)
* [Work pools](/v3/concepts/work-pools) and [work queues](/v3/concepts/work-pools#work-queues)
* [Blocks](/v3/concepts/blocks) and their associated schemas/types
* [Variables](/v3/concepts/variables)
* [Global concurrency limits](/v3/concepts/global-concurrency-limits)
* [Automations](/v3/concepts/automations)

Resources are transferred in the correct order to preserve relationships between them.

## [​](#common-transfer-scenarios) Common transfer scenarios

### [​](#development-to-production) Development to production

Transfer resources between different environments:

Copy

```
prefect transfer --from dev-profile --to prod-profile
```

### [​](#self-hosted-to-cloud-migration) Self-hosted to cloud migration

Move from a self-hosted Prefect server to Prefect Cloud:

Copy

```
prefect transfer --from self-hosted-profile --to cloud-profile
```

When transferring to Prefect Cloud Hobby tier workspaces, certain resource types may be skipped due to tier limitations.

### [​](#workspace-consolidation) Workspace consolidation

Resources can be transferred between multiple workspaces. Resources that already exist in the destination will be skipped.

## [​](#resource-handling) Resource handling

### [​](#work-pools) Work pools

The transfer command handles different work pool types according to the destination:

* **Hybrid pools** (process, docker, kubernetes): Transfer to any destination (except Prefect Cloud Hobby tier workspaces)
* **Push pools**: Transfer only to Prefect Cloud destinations (except Prefect Cloud Hobby tier workspaces)
* **Managed pools**: Never transferred

### [​](#existing-resources) Existing resources

Resources that already exist in the destination are skipped you can run it multiple times safely.

Copy

```
# First run
prefect transfer --from dev --to prod
# Output: 25 succeeded, 0 skipped

# Second run (idempotent)
prefect transfer --from dev --to prod
# Output: 0 succeeded, 25 skipped
```

### [​](#resource-limits) Resource limits

When transferring to Prefect Cloud workspaces, certain resources may be skipped based on tier limitations. The transfer command will provide clear messages explaining why resources were skipped.

## [​](#limitations) Limitations

### [​](#resources-not-transferred) Resources not transferred

Certain resources are not transferred between environments:

* Flow run history and logs
* Result artifacts and cached data
* Cloud-specific infrastructure resources
* Credentials and secrets (must be recreated in the destination)

### [​](#environment-specific-configuration) Environment-specific configuration

Some resources may require manual configuration after transfer to work correctly in the new environment, particularly those that reference external systems or credentials.

## [​](#best-practices) Best practices

### [​](#pre-transfer-checklist) Pre-transfer checklist

1. **Verify profiles**: Ensure both source and destination profiles are correctly configured

   Copy

   ```
   prefect profile inspect source-profile
   prefect profile inspect dest-profile
   ```
2. **Test connectivity**: Confirm you can connect to both environments

   Copy

   ```
   prefect --profile source-profile config view
   prefect --profile dest-profile config view
   ```
3. **Check tier limitations**: Understand destination workspace capabilities
   * Hobby tier: Managed pools only, 5 deployment limit
   * Standard/Pro tier: Full resource support

### [​](#post-transfer-validation) Post-transfer validation

After transferring resources:

1. **Verify critical resources**:

   Copy

   ```
   prefect --profile dest-profile work-pool ls
   prefect --profile dest-profile deployment ls
   ```
2. **Test a deployment**:

   Copy

   ```
   prefect --profile dest-profile deployment run my-deployment/my-flow
   ```
3. **Check automation status**:

   Copy

   ```
   prefect --profile dest-profile automation ls
   ```

## [​](#troubleshooting) Troubleshooting

### [​](#common-issues) Common issues

**Resources skipped as “already exists”**

* This is expected when resources already exist in the destination
* The transfer can be run multiple times safely

**Resources skipped due to tier limitations**

* Some resource types require specific Prefect Cloud tiers
* Check your workspace tier and capabilities

**Connection errors**

* Verify both profiles are correctly configured
* Check network connectivity and authentication

### [​](#debug-mode) Debug mode

For detailed transfer information, enable debug logging:

Copy

```
PREFECT_LOGGING_LEVEL=DEBUG prefect transfer --from source --to dest
```

## [​](#see-also) See also

* [Settings and profiles](/v3/concepts/settings-and-profiles) for configuring source and destination profiles
* [Work pools](/v3/concepts/work-pools) for understanding pool types
* [Prefect Cloud pricing](https://www.prefect.io/pricing) for workspace capabilities

Was this page helpful?

YesNo

[Upgrade from agents to workers](/v3/how-to-guides/migrate/upgrade-agents-to-workers)

⌘I