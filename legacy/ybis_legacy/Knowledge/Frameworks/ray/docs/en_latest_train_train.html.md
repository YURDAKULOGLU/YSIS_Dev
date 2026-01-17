Ray Train: Scalable Model Training — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Ray Train: Scalable Model Training[#](#ray-train-scalable-model-training "Link to this heading")

Ray Train is a scalable machine learning library for distributed training and fine-tuning.

Ray Train allows you to scale model training code from a single machine to a cluster of machines in the cloud, and abstracts away the complexities of distributed computing.
Whether you have large models or large datasets, Ray Train is the simplest solution for distributed training.

Ray Train provides support for many frameworks:

| PyTorch Ecosystem | More Frameworks |
| --- | --- |
| PyTorch | TensorFlow |
| PyTorch Lightning | Keras |
| Hugging Face Transformers | Horovod |
| Hugging Face Accelerate | XGBoost |
| DeepSpeed | LightGBM |

## Install Ray Train[#](#install-ray-train "Link to this heading")

To install Ray Train, run:

```
$ pip install -U "ray[train]"
```

To learn more about installing Ray and its libraries, see
[Installing Ray](../ray-overview/installation.html#installation).

## Get started[#](#get-started "Link to this heading")

**Overview**

Understand the key concepts for distributed training with Ray Train.

[Learn the basics](overview.html#train-overview)

**PyTorch**

Get started on distributed model training with Ray Train and PyTorch.

[Try Ray Train with PyTorch](getting-started-pytorch.html#train-pytorch)

**PyTorch Lightning**

Get started on distributed model training with Ray Train and Lightning.

[Try Ray Train with Lightning](getting-started-pytorch-lightning.html#train-pytorch-lightning)

**Hugging Face Transformers**

Get started on distributed model training with Ray Train and Transformers.

[Try Ray Train with Transformers](getting-started-transformers.html#train-pytorch-transformers)

**JAX**

Get started on distributed model training with Ray Train and JAX.

[Try Ray Train with JAX](getting-started-jax.html#train-jax)

## Learn more[#](#learn-more "Link to this heading")

**More Frameworks**

Don’t see your framework? See these guides.

[Try Ray Train with other frameworks](more-frameworks.html#train-more-frameworks)

**User Guides**

Get how-to instructions for common training tasks with Ray Train.

[Read how-to guides](user-guides.html#train-user-guides)

**Examples**

Browse end-to-end code examples for different use cases.

[Learn through examples](examples.html)

**API**

Consult the API Reference for full descriptions of the Ray Train API.

[Read the API Reference](api/api.html#train-api)

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/train/train.rst)