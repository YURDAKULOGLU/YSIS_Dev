Ray on Kubernetes — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Ray on Kubernetes[#](#ray-on-kubernetes "Link to this heading")

## Overview[#](#overview "Link to this heading")

In this section we cover how to execute your distributed Ray programs on a Kubernetes cluster.

Using the [KubeRay operator](https://github.com/ray-project/kuberay) is the
recommended way to do so. The operator provides a Kubernetes-native way to manage Ray clusters.
Each Ray cluster consists of a head node pod and a collection of worker node pods. Optional
autoscaling support allows the KubeRay operator to size your Ray clusters according to the
requirements of your Ray workload, adding and removing Ray pods as needed. KubeRay supports
heterogenous compute nodes (including GPUs) as well as running multiple Ray clusters with
different Ray versions in the same Kubernetes cluster.

![../../_images/ray_on_kubernetes.png](../../_images/ray_on_kubernetes.png)

KubeRay introduces three distinct Kubernetes Custom Resource Definitions (CRDs): **RayCluster**, **RayJob**, and **RayService**.
These CRDs assist users in efficiently managing Ray clusters tailored to various use cases.

See [Getting Started](getting-started.html#kuberay-quickstart) to learn the basics of KubeRay and follow the quickstart guides to run your first Ray application on Kubernetes with KubeRay.

* [RayCluster Quick Start](getting-started/raycluster-quick-start.html#kuberay-raycluster-quickstart)
* [RayJob Quick Start](getting-started/rayjob-quick-start.html#kuberay-rayjob-quickstart)
* [RayService Quick Start](getting-started/rayservice-quick-start.html#kuberay-rayservice-quickstart)

Additionally, [Anyscale](https://console.anyscale.com/register/ha?render_flow=ray&amp;utm_source=ray_docs&amp;utm_medium=docs&amp;utm_campaign=ray-doc-upsell&amp;utm_content=deploy-ray-on-k8s) is the managed Ray platform developed by the creators of Ray. It offers an easy path to deploy Ray clusters on your existing Kubernetes infrastructure, including EKS, GKE, AKS, or self-hosted Kubernetes.

## Learn More[#](#learn-more "Link to this heading")

The Ray docs present all the information you need to start running Ray workloads on Kubernetes.

**Getting Started**

Learn how to start a Ray cluster and deploy Ray applications on Kubernetes.

[Get Started with Ray on Kubernetes](getting-started.html#kuberay-quickstart)

**User Guides**

Learn best practices for configuring Ray clusters on Kubernetes.

[Read the User Guides](user-guides.html#kuberay-guides)

**Examples**

Try example Ray workloads on Kubernetes.

[Try example workloads](examples.html#kuberay-examples)

**Ecosystem**

Integrate KubeRay with third party Kubernetes ecosystem tools.

[Ecosystem Guides](k8s-ecosystem.html#kuberay-ecosystem-integration)

**Benchmarks**

Check the KubeRay benchmark results.

[Benchmark results](benchmarks.html#kuberay-benchmarks)

**Troubleshooting**

Consult the KubeRay troubleshooting guides.

[Troubleshooting guides](troubleshooting.html#kuberay-troubleshooting)

## About KubeRay[#](#about-kuberay "Link to this heading")

Ray’s Kubernetes support is developed at the [KubeRay GitHub repository](https://github.com/ray-project/kuberay), under the broader [Ray project](https://github.com/ray-project/). KubeRay is used by several companies to run production Ray deployments.

* Visit the [KubeRay GitHub repo](https://github.com/ray-project/kuberay) to track progress, report bugs, propose new features, or contribute to
  the project.

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/cluster/kubernetes/index.md)