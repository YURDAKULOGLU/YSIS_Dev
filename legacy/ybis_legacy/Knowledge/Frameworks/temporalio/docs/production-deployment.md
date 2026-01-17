Temporal Platform production deployments | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

**Ready to elevate your durable application into production?**

To take your application to production, you deploy your application code, including your Workflows, Activities, and Workers, on your infrastructure using your existing build, test and deploy tools.

Then you need a production-ready Temporal Service to coordinate the execution of your Workflows and Activities.

You can use Temporal Cloud, a fully-managed platform, or you can self-host the service.

## Use Temporal Cloud[​](#use-temporal-cloud "Direct link to Use Temporal Cloud")

You can let us handle the operations of running the Temporal Service, and focus on your application.
Follow the [Temporal Cloud guide](/cloud) to get started.

![Connect your application instances to Temporal Cloud](/diagrams/basic-platform-topology-cloud.svg)

Connect your application instances to Temporal Cloud

## Run a Self-hosted Temporal Service[​](#run-a-self-hosted-temporal-service "Direct link to Run a Self-hosted Temporal Service")

Alternatively, you can run your own production level Temporal Service to orchestrate your durable applications.
Follow the [Self-hosted guide](/self-hosted-guide) to get started.

![Connect your application instances to your self-hosted Temporal Service](/diagrams/basic-platform-topology-self-hosted.svg)

Connect your application instances to your self-hosted Temporal Service

## Worker deployments[​](#worker-deployments "Direct link to Worker deployments")

Whether you're hosting with Temporal Cloud or on your own, you have control over where to run and scale your Workers.
We provide guidance on [Worker Deployments](/production-deployment/worker-deployments).

* [Use Temporal Cloud](#use-temporal-cloud)* [Run a Self-hosted Temporal Service](#run-a-self-hosted-temporal-service)* [Worker deployments](#worker-deployments)