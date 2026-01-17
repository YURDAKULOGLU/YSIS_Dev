Introduction - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Get started

Introduction

[Getting Started](/v3/get-started)[Concepts](/v3/concepts)[How-to Guides](/v3/how-to-guides)[Advanced](/v3/advanced)[Examples](/v3/examples)[Integrations](/integrations/integrations)[API Reference](/v3/api-ref)[Contribute](/contribute)[Release Notes](/v3/release-notes)

##### Get started

* [Welcome](/v3/get-started)
* [Install Prefect](/v3/get-started/install)
* [Quickstart](/v3/get-started/quickstart)

On this page

* [Essential features](#essential-features)
* [Quickstart](#quickstart)
* [How-to guides](#how-to-guides)
* [Advanced](#advanced)
* [Examples](#examples)
* [Mini-history of Prefect](#mini-history-of-prefect)
* [Join our community](#join-our-community)
* [LLM-friendly docs](#llm-friendly-docs)
* [MCP server](#mcp-server)
* [Plain text formats](#plain-text-formats)

Prefect is an open-source orchestration engine that turns your Python functions into production-grade data pipelines with minimal friction. You can build and schedule workflows in pure Python—no DSLs or complex config files—and run them anywhere you can run Python. Prefect handles the heavy lifting for you out of the box: automatic state tracking, failure handling, real-time monitoring, and more.

### [​](#essential-features) Essential features

| Feature | Description |
| --- | --- |
| **Pythonic** | Write workflows in native Python—no DSLs, YAML, or special syntax. Full support for type hints, async/await, and modern Python patterns. Use your existing IDE, debugger, and testing tools. |
| **State & Recovery** | Robust state management that tracks success, failure, and retry states. Resume interrupted runs from the last successful point, and cache expensive computations to avoid unnecessary rework. |
| **Flexible & Portable Execution** | Start flows locally for easy development, then deploy them anywhere—from a single process to containers, Kubernetes, or cloud services—without locking into a vendor. Infrastructure is defined by code (not just configuration), making it simple to scale or change environments. |
| **Event-Driven** | Trigger flows on schedules, external events, or via API. Pause flows for human intervention or approval. Chain flows together based on states, conditions, or any custom logic. |
| **Dynamic Runtime** | Create tasks dynamically at runtime based on actual data or conditions. Easily spawn new tasks and branches during execution for truly data-driven workflows. |
| **Modern UI** | Real-time flow run monitoring, logging, and state tracking through an intuitive interface. View dependency graphs and DAGs automatically—just run your flow and open the UI. |
| **CI/CD First** | Test and simulate flows like normal Python code, giving you fast feedback during development. Integrate seamlessly into your existing CI/CD pipeline for automated testing and deployment. |

## [​](#quickstart) Quickstart

[## Quickstart

Quickly create your first deployable workflow tracked by Prefect.](/v3/get-started/quickstart)[## Install Prefect

Install Prefect and get connected to Prefect Cloud or a self-hosted server.](/v3/get-started/install)[## Upgrade to Prefect 3

Upgrade from Prefect 2 to Prefect 3 to get the latest features and performance enhancements.](/v3/how-to-guides/migrate/upgrade-to-prefect-3)

## [​](#how-to-guides) How-to guides

[## Build workflows

Learn how to write and customize your Prefect workflows with tasks and flows.](/v3/how-to-guides/workflows/write-and-run)[## Deploy workflows

Deploy and manage your workflows as Prefect deployments.](/v3/how-to-guides/deployments/create-deployments)[## Configure infrastructure

Deploy your workflows to specific infrastructure platforms.](/v3/how-to-guides/deployment_infra/managed)[## Set up automations

Work with events, triggers, and automations to build reactive workflows.](/v3/how-to-guides/automations/creating-automations)[## Configure Prefect

Configure your Prefect environment, secrets, and variables.](/v3/how-to-guides/configuration/manage-settings)[## Use Prefect Cloud

Set up and manage your Prefect Cloud account.](/v3/how-to-guides/cloud/connect-to-cloud)

## [​](#advanced) Advanced

[## Interactive workflows

Build interactive workflows that can pause and receive input.](/v3/advanced/interactive)[## Platform engineering

Use Prefect as a platform for your teams’ data pipelines.](/v3/advanced/infrastructure-as-code)[## Extend Prefect

Extend Prefect with custom blocks and API integrations.](/v3/advanced/api-client)

## [​](#examples) Examples

Check out the gallery of [examples](/v3/examples/index) to see Prefect in action.

## [​](#mini-history-of-prefect) Mini-history of Prefect

**2018-2021:** Our story begins in 2018, when we introduced the idea that workflow orchestration should be Pythonic.
Inspired by distributed tools like Dask, and building on the experience of our founder, Jeremiah Lowin (a PMC member of Apache Airflow), we created a system based on simple Python decorators for tasks and flows.
But what made Prefect truly special was our introduction of task mapping—a feature that would later become foundational to our dynamic execution capabilities (and eventually imitated by other orchestration SDKs).
**2022:** Prefect’s 2.0 release became inevitable once we recognized that real-world workflows don’t always fit into neat, pre-planned DAG structures: sometimes you need to update a job definition based on runtime information, for example by skipping a branch of your workflow.
So we removed a key constraint that workflows be written explicitly as DAGs, fully embracing native Python control flow—if/else conditionals, while loops-everything that makes Python…Python.
**2023-present:** With our release of Prefect 3.0 in 2024, we fully embraced these dynamic patterns by open-sourcing our events and automations backend, allowing users to natively represent event-driven workflows and gain additional observability into their execution.
Prefect 3.0 also unlocked a leap forward in performance, improving the runtime overhead of Prefect by up to 90%.

## [​](#join-our-community) Join our community

Join Prefect’s vibrant [community of nearly 30,000 engineers](/contribute/index) to learn with others and share your knowledge!

## [​](#llm-friendly-docs) LLM-friendly docs

### [​](#mcp-server) MCP server

Connect to `https://docs.prefect.io/mcp` in Claude Desktop, Cursor, or VS Code for AI-powered documentation search and assistance.
You can also install the [Prefect MCP server](/v3/how-to-guides/ai/use-prefect-mcp-server) to get both documentation access and direct integration with your Prefect workflows to enable AI assistants to monitor deployments, debug flow runs, and query your Prefect infrastructure.

### [​](#plain-text-formats) Plain text formats

The docs are also available in [llms.txt format](https://llmstxt.org/):

* [llms.txt](https://docs.prefect.io/llms.txt) - A sitemap listing all documentation pages
* [llms-full.txt](https://docs.prefect.io/llms-full.txt) - The entire documentation in one file (may exceed context windows)

Any page can be accessed as markdown by appending `.md` to the URL. For example, this page becomes `https://docs.prefect.io/v3/get-started.md`.
You can also copy any page as markdown by pressing “Cmd+C” (or “Ctrl+C” on Windows) on your keyboard.

Was this page helpful?

YesNo

[Install Prefect](/v3/get-started/install)

⌘I