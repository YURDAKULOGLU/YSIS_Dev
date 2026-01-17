Ray Data: Scalable Data Processing for AI Workloads — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Ray Data: Scalable Data Processing for AI Workloads[#](#ray-data-scalable-data-processing-for-ai-workloads "Link to this heading")

Ray Data is a scalable data processing library for AI workloads built on Ray.
Ray Data provides flexible and performant APIs for common operations such as [batch inference](batch_inference.html#batch-inference-home), data preprocessing, and data loading for ML training. Unlike other distributed data systems, Ray Data features a [streaming execution engine](key-concepts.html#streaming-execution) to efficiently process large datasets and maintain high utilization across both CPU and GPU workloads.

## Quick start[#](#quick-start "Link to this heading")

First, install Ray Data. To learn more about installing Ray and its libraries, see
[Installing Ray](../ray-overview/installation.html#installation):

```
$ pip install -U 'ray[data]'
```

Here is an example of how to do perform a simple batch text classification task with Ray Data:

```
import ray
import pandas as pd

class ClassificationModel:
    def __init__(self):
        from transformers import pipeline
        self.pipe = pipeline("text-classification")

    def __call__(self, batch: pd.DataFrame):
        results = self.pipe(list(batch["text"]))
        result_df = pd.DataFrame(results)
        return pd.concat([batch, result_df], axis=1)

ds = ray.data.read_text("s3://anonymous@ray-example-data/sms_spam_collection_subset.txt")
ds = ds.map_batches(
    ClassificationModel,
    compute=ray.data.ActorPoolStrategy(size=2),
    batch_size=64,
    batch_format="pandas"
    # num_gpus=1  # this will set 1 GPU per worker
)
ds.show(limit=1)
```

```
{'text': 'ham\tGo until jurong point, crazy.. Available only in bugis n great world la e buffet... Cine there got amore wat...', 'label': 'NEGATIVE', 'score': 0.9935141801834106}
```

## Why choose Ray Data?[#](#why-choose-ray-data "Link to this heading")

Modern AI workloads revolve around the usage of deep learning models, which are computationally intensive and often require specialized hardware such as GPUs.
Unlike CPUs, GPUs often come with less memory, have different semantics for scheduling, and are much more expensive to run.
Systems built to support traditional data processing pipelines often don’t utilize such resources well.

Ray Data supports AI workloads as a first-class citizen and offers several key advantages:

* **Faster and cheaper for deep learning**: Ray Data streams data between CPU preprocessing and GPU inference/training tasks, maximizing resource utilization and reducing costs by keeping GPUs active.
* **Framework friendly**: Ray Data provides performant, first-class integration with common AI frameworks (vLLM, PyTorch, HuggingFace, TensorFlow) and common cloud providers (AWS, GCP, Azure)
* **Support for multi-modal data**: Ray Data leverages Apache Arrow and Pandas and provides support for many data formats used in ML workloads such as Parquet, Lance, images, JSON, CSV, audio, video, and more.
* **Scalable by default**: Built on Ray for automatic scaling across heterogeneous clusters with different CPU and GPU machines. Code runs unchanged from one machine to hundreds of nodes processing hundreds of TB of data.

## Learn more[#](#learn-more "Link to this heading")

**Quickstart**

Get started with Ray Data with a simple example.

[Quickstart](quickstart.html#data-quickstart)

**Key Concepts**

Learn the key concepts behind Ray Data. Learn what
Datasets are and how they’re used.

[Key Concepts](key-concepts.html#data-key-concepts)

**User Guides**

Learn how to use Ray Data, from basic usage to end-to-end guides.

[Learn how to use Ray Data](user-guide.html#data-user-guide)

**Examples**

Find both simple and scaling-out examples of using Ray Data.

[Ray Data Examples](examples.html)

**API**

Get more in-depth information about the Ray Data API.

[Read the API Reference](api/api.html#data-api)

## Case studies for Ray Data[#](#case-studies-for-ray-data "Link to this heading")

**Training ingest using Ray Data**

* [Pinterest uses Ray Data to do last mile data processing for model training](https://medium.com/pinterest-engineering/last-mile-data-processing-with-ray-629affbf34ff)
* [DoorDash elevates model training with Ray Data](https://www.youtube.com/watch?v=pzemMnpctVY)
* [Instacart builds distributed machine learning model training on Ray Data](https://tech.instacart.com/distributed-machine-learning-at-instacart-4b11d7569423)
* [Predibase speeds up image augmentation for model training using Ray Data](https://predibase.com/blog/ludwig-v0-7-fine-tuning-pretrained-image-and-text-models-50x-faster-and)

**Batch inference using Ray Data**

* [ByteDance scales offline inference with multi-modal LLMs to 200 TB on Ray Data](https://www.anyscale.com/blog/how-bytedance-scales-offline-inference-with-multi-modal-llms-to-200TB-data)
* [Spotify’s new ML platform built on Ray Data for batch inference](https://engineering.atspotify.com/2023/02/unleashing-ml-innovation-at-spotify-with-ray/)
* [Sewer AI speeds up object detection on videos 3x using Ray Data](https://www.anyscale.com/blog/inspecting-sewer-line-safety-using-thousands-of-hours-of-video)

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/data/data.rst)