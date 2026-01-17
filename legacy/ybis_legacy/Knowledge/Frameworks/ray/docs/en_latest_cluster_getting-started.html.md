Ray Clusters Overview — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Ray Clusters Overview[#](#ray-clusters-overview "Link to this heading")

Ray enables seamless scaling of workloads from a laptop to a large cluster. While Ray
works out of the box on single machines with just a call to `ray.init`, to run Ray
applications on multiple nodes you must first *deploy a Ray cluster*.

A Ray cluster is a set of worker nodes connected to a common [Ray head node](key-concepts.html#cluster-head-node).
Ray clusters can be fixed-size, or they may [autoscale up and down](key-concepts.html#cluster-autoscaler) according
to the resources requested by applications running on the cluster.

## Where can I deploy Ray clusters?[#](#where-can-i-deploy-ray-clusters "Link to this heading")

Ray provides native cluster deployment support on the following technology stacks:

* On [AWS, GCP, and Azure](vms/index.html#cloud-vm-index). Community-supported Aliyun and vSphere integrations also exist.
* On [Kubernetes](kubernetes/index.html#kuberay-index), via the officially supported KubeRay project.
* On [Anyscale](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=ray-doc-upsell&utm_content=ray-cluster-deployment), a fully managed Ray platform by the creators of Ray. You can either bring an existing AWS, GCP, Azure and Kubernetes clusters, or use the Anyscale hosted compute layer.

Advanced users may want to [deploy Ray manually](vms/user-guides/launching-clusters/on-premises.html#on-prem)
or onto [platforms not listed here](vms/user-guides/community/index.html#ref-cluster-setup).

Note

Multi-node Ray clusters are only supported on Linux. At your own risk, you
may deploy Windows and OSX clusters by setting the environment variable
`RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER=1` during deployment.

## What’s next?[#](#what-s-next "Link to this heading")

**I want to learn key Ray cluster concepts**

Understand the key concepts and main ways of interacting with a Ray cluster.

[Learn Key Concepts](key-concepts.html#cluster-key-concepts)

**I want to run Ray on Kubernetes**

Deploy a Ray application to a Kubernetes cluster. You can run the tutorial on a
Kubernetes cluster or on your laptop via Kind.

[Get Started with Ray on Kubernetes](kubernetes/getting-started.html#kuberay-quickstart)

**I want to run Ray on a cloud provider**

Take a sample application designed to run on a laptop and scale it up in the
cloud. Access to an AWS or GCP account is required.

[Get Started with Ray on VMs](vms/getting-started.html#vm-cluster-quick-start)

**I want to run my application on an existing Ray cluster**

Guide to submitting applications as Jobs to existing Ray clusters.

[Job Submission](running-applications/job-submission/quickstart.html#jobs-quickstart)

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/cluster/getting-started.rst)