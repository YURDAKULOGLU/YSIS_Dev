User Guides — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# User Guides[#](#user-guides "Link to this heading")

If you’re new to Ray Data, start with the
[Ray Data Quickstart](quickstart.html#data-quickstart).
This user guide helps you navigate the Ray Data project and
shows you how to achieve several tasks.

* [Loading Data](loading-data.html)
  + [Reading files](loading-data.html#reading-files)
  + [Loading data from other libraries](loading-data.html#loading-data-from-other-libraries)
  + [Reading databases](loading-data.html#reading-databases)
  + [Reading from Kafka](loading-data.html#reading-from-kafka)
  + [Creating synthetic data](loading-data.html#creating-synthetic-data)
  + [Loading other datasources](loading-data.html#loading-other-datasources)
  + [Performance considerations](loading-data.html#performance-considerations)
* [Inspecting Data](inspecting-data.html)
  + [Describing datasets](inspecting-data.html#describing-datasets)
  + [Inspecting rows](inspecting-data.html#inspecting-rows)
  + [Inspecting batches](inspecting-data.html#inspecting-batches)
  + [Inspecting execution statistics](inspecting-data.html#inspecting-execution-statistics)
* [Transforming Data](transforming-data.html)
  + [Transforming rows](transforming-data.html#transforming-rows)
  + [Transforming batches](transforming-data.html#transforming-batches)
  + [Ordering of rows](transforming-data.html#ordering-of-rows)
  + [Stateful Transforms](transforming-data.html#stateful-transforms)
  + [Avoiding out-of-memory errors](transforming-data.html#avoiding-out-of-memory-errors)
  + [Group-by and transforming groups](transforming-data.html#group-by-and-transforming-groups)
* [Aggregating Data](aggregating-data.html)
  + [Basic Aggregations](aggregating-data.html#basic-aggregations)
  + [Custom Aggregations](aggregating-data.html#custom-aggregations)
* [Iterating over Data](iterating-over-data.html)
  + [Iterating over rows](iterating-over-data.html#iterating-over-rows)
  + [Iterating over batches](iterating-over-data.html#iterating-over-batches)
  + [Iterating over batches with shuffling](iterating-over-data.html#iterating-over-batches-with-shuffling)
  + [Splitting datasets for distributed parallel training](iterating-over-data.html#splitting-datasets-for-distributed-parallel-training)
* [Joining Data](joining-data.html)
  + [Configuring Joins](joining-data.html#configuring-joins)
  + [Configuring number of partitions](joining-data.html#configuring-number-of-partitions)
  + [Configuring number of Aggregators](joining-data.html#configuring-number-of-aggregators)
* [Shuffling Data](shuffling-data.html)
  + [Types of shuffling](shuffling-data.html#types-of-shuffling)
  + [Advanced: Optimizing shuffles](shuffling-data.html#advanced-optimizing-shuffles)
* [Saving Data](saving-data.html)
  + [Writing data to files](saving-data.html#writing-data-to-files)
  + [Converting Datasets to other Python libraries](saving-data.html#converting-datasets-to-other-python-libraries)
* [Working with Images](working-with-images.html)
  + [Reading images](working-with-images.html#reading-images)
  + [Transforming images](working-with-images.html#transforming-images)
  + [Performing inference on images](working-with-images.html#performing-inference-on-images)
  + [Saving images](working-with-images.html#saving-images)
* [Working with Text](working-with-text.html)
  + [Reading text files](working-with-text.html#reading-text-files)
  + [Transforming text](working-with-text.html#transforming-text)
  + [Performing inference on text](working-with-text.html#performing-inference-on-text)
  + [Saving text](working-with-text.html#saving-text)
* [Working with Tensors / NumPy](working-with-tensors.html)
  + [Tensor data representation](working-with-tensors.html#tensor-data-representation)
  + [Transforming tensor data](working-with-tensors.html#transforming-tensor-data)
  + [Saving tensor data](working-with-tensors.html#saving-tensor-data)
* [Working with PyTorch](working-with-pytorch.html)
  + [Iterating over Torch tensors for training](working-with-pytorch.html#iterating-over-torch-tensors-for-training)
  + [Transformations with Torch tensors](working-with-pytorch.html#transformations-with-torch-tensors)
  + [Batch inference with PyTorch](working-with-pytorch.html#batch-inference-with-pytorch)
  + [Saving Datasets containing Torch tensors](working-with-pytorch.html#saving-datasets-containing-torch-tensors)
  + [Migrating from PyTorch Datasets and DataLoaders](working-with-pytorch.html#migrating-from-pytorch-datasets-and-dataloaders)
* [Working with LLMs](working-with-llms.html)
  + [Quickstart: vLLM batch inference](working-with-llms.html#quickstart-vllm-batch-inference)
  + [Perform batch inference with LLMs](working-with-llms.html#perform-batch-inference-with-llms)
  + [Configure vLLM for LLM inference](working-with-llms.html#configure-vllm-for-llm-inference)
  + [Batch inference with vision-language-model (VLM)](working-with-llms.html#batch-inference-with-vision-language-model-vlm)
  + [Batch inference with embedding models](working-with-llms.html#batch-inference-with-embedding-models)
  + [Batch inference with an OpenAI-compatible endpoint](working-with-llms.html#batch-inference-with-an-openai-compatible-endpoint)
  + [Batch inference with serve deployments](working-with-llms.html#batch-inference-with-serve-deployments)
  + [Cross-node parallelism](working-with-llms.html#cross-node-parallelism)
  + [Usage Data Collection](working-with-llms.html#usage-data-collection)
  + [Frequently Asked Questions (FAQs)](working-with-llms.html#frequently-asked-questions-faqs)
* [Monitoring Your Workload](monitoring-your-workload.html)
  + [Ray Data progress bars](monitoring-your-workload.html#ray-data-progress-bars)
  + [Ray Data dashboard](monitoring-your-workload.html#ray-data-dashboard)
  + [Ray Data logs](monitoring-your-workload.html#ray-data-logs)
  + [Ray Data stats](monitoring-your-workload.html#ray-data-stats)
* [Execution Configurations](execution-configurations.html)
  + [Configuring `ExecutionOptions`](execution-configurations.html#configuring-executionoptions)
  + [Configuring `DataContext`](execution-configurations.html#configuring-datacontext)
* [End-to-end: Offline Batch Inference](batch_inference.html)
  + [Quickstart](batch_inference.html#quickstart)
  + [Configuration and troubleshooting](batch_inference.html#configuration-and-troubleshooting)
* [Advanced: Performance Tips and Tuning](performance-tips.html)
  + [Optimizing transforms](performance-tips.html#optimizing-transforms)
  + [Optimizing reads](performance-tips.html#optimizing-reads)
  + [Reducing memory usage](performance-tips.html#reducing-memory-usage)
  + [Configuring execution](performance-tips.html#configuring-execution)
  + [Reproducibility](performance-tips.html#reproducibility)
* [Advanced: Read and Write Custom File Types](custom-datasource-example.html)
  + [Read data from files](custom-datasource-example.html#read-data-from-files)
  + [Write data to files](custom-datasource-example.html#write-data-to-files)

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/data/user-guide.rst)