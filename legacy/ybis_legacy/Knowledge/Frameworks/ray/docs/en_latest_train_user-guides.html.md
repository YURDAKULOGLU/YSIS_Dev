Ray Train User Guides — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Ray Train User Guides[#](#ray-train-user-guides "Link to this heading")

* [Data Loading and Preprocessing](user-guides/data-loading-preprocessing.html)
  + [Quickstart](user-guides/data-loading-preprocessing.html#quickstart)
  + [Starting with PyTorch data](user-guides/data-loading-preprocessing.html#starting-with-pytorch-data)
  + [Splitting datasets](user-guides/data-loading-preprocessing.html#splitting-datasets)
  + [Random shuffling](user-guides/data-loading-preprocessing.html#random-shuffling)
  + [Enabling reproducibility](user-guides/data-loading-preprocessing.html#enabling-reproducibility)
  + [Preprocessing structured data](user-guides/data-loading-preprocessing.html#preprocessing-structured-data)
  + [Performance tips](user-guides/data-loading-preprocessing.html#performance-tips)
* [Configuring Scale and GPUs](user-guides/using-gpus.html)
  + [Increasing the number of workers](user-guides/using-gpus.html#increasing-the-number-of-workers)
  + [Using GPUs](user-guides/using-gpus.html#using-gpus)
  + [Setting the resources per worker](user-guides/using-gpus.html#setting-the-resources-per-worker)
  + [(Deprecated) Trainer resources](user-guides/using-gpus.html#deprecated-trainer-resources)
* [Local Mode](user-guides/local_mode.html)
  + [What is local mode?](user-guides/local_mode.html#what-is-local-mode)
  + [How to enable local mode](user-guides/local_mode.html#how-to-enable-local-mode)
  + [When to use local mode](user-guides/local_mode.html#when-to-use-local-mode)
  + [Single-process local mode](user-guides/local_mode.html#single-process-local-mode)
  + [Multi-process local mode with `torchrun`](user-guides/local_mode.html#multi-process-local-mode-with-torchrun)
  + [Transitioning from local mode to distributed training](user-guides/local_mode.html#transitioning-from-local-mode-to-distributed-training)
  + [Limitations and API differences](user-guides/local_mode.html#limitations-and-api-differences)
* [Configuring Persistent Storage](user-guides/persistent-storage.html)
  + [Cloud storage (AWS S3, Google Cloud Storage)](user-guides/persistent-storage.html#cloud-storage-aws-s3-google-cloud-storage)
  + [Shared filesystem (NFS, HDFS)](user-guides/persistent-storage.html#shared-filesystem-nfs-hdfs)
  + [Local storage](user-guides/persistent-storage.html#local-storage)
  + [Custom storage](user-guides/persistent-storage.html#custom-storage)
  + [Overview of Ray Train outputs](user-guides/persistent-storage.html#overview-of-ray-train-outputs)
  + [Advanced configuration](user-guides/persistent-storage.html#advanced-configuration)
  + [Deprecated](user-guides/persistent-storage.html#deprecated)
* [Monitoring and Logging Metrics](user-guides/monitoring-logging.html)
  + [How to obtain and aggregate results from different workers?](user-guides/monitoring-logging.html#how-to-obtain-and-aggregate-results-from-different-workers)
  + [(Deprecated) Reporting free-floating metrics](user-guides/monitoring-logging.html#deprecated-reporting-free-floating-metrics)
* [Saving and Loading Checkpoints](user-guides/checkpoints.html)
  + [Saving checkpoints during training](user-guides/checkpoints.html#saving-checkpoints-during-training)
  + [Checkpoint upload modes](user-guides/checkpoints.html#checkpoint-upload-modes)
  + [Configure checkpointing](user-guides/checkpoints.html#configure-checkpointing)
  + [Using checkpoints during training](user-guides/checkpoints.html#using-checkpoints-during-training)
  + [Using checkpoints after training](user-guides/checkpoints.html#using-checkpoints-after-training)
  + [Restore training state from a checkpoint](user-guides/checkpoints.html#restore-training-state-from-a-checkpoint)
* [Validating checkpoints asynchronously](user-guides/asynchronous-validation.html)
  + [Tutorial](user-guides/asynchronous-validation.html#tutorial)
  + [Write a distributed validation function](user-guides/asynchronous-validation.html#write-a-distributed-validation-function)
  + [Checkpoint metrics lifecycle](user-guides/asynchronous-validation.html#checkpoint-metrics-lifecycle)
* [Experiment Tracking](user-guides/experiment-tracking.html)
  + [Getting Started](user-guides/experiment-tracking.html#getting-started)
  + [Examples](user-guides/experiment-tracking.html#examples)
  + [Common Errors](user-guides/experiment-tracking.html#common-errors)
* [Inspecting Training Results](user-guides/results.html)
  + [Viewing metrics](user-guides/results.html#viewing-metrics)
  + [Retrieving checkpoints](user-guides/results.html#retrieving-checkpoints)
  + [Accessing storage location](user-guides/results.html#accessing-storage-location)
  + [Catching Errors](user-guides/results.html#catching-errors)
  + [Finding results on persistent storage](user-guides/results.html#finding-results-on-persistent-storage)
* [Handling Failures and Node Preemption](user-guides/fault-tolerance.html)
  + [Worker Process and Node Fault Tolerance](user-guides/fault-tolerance.html#worker-process-and-node-fault-tolerance)
  + [Job Driver Fault Tolerance](user-guides/fault-tolerance.html#job-driver-fault-tolerance)
  + [Fault Tolerance API Deprecations](user-guides/fault-tolerance.html#fault-tolerance-api-deprecations)
* [Ray Train Metrics](user-guides/monitor-your-application.html)
* [Reproducibility](user-guides/reproducibility.html)
* [Hyperparameter Optimization](user-guides/hyperparameter-optimization.html)
  + [Quickstart](user-guides/hyperparameter-optimization.html#quickstart)
  + [What does Ray Tune provide?](user-guides/hyperparameter-optimization.html#what-does-ray-tune-provide)
  + [Configuring resources for multiple trials](user-guides/hyperparameter-optimization.html#configuring-resources-for-multiple-trials)
  + [Reporting metrics and checkpoints](user-guides/hyperparameter-optimization.html#reporting-metrics-and-checkpoints)
  + [`Tuner(trainer)` API Deprecation](user-guides/hyperparameter-optimization.html#tuner-trainer-api-deprecation)
* [Advanced: Scaling out expensive collate functions](user-guides/scaling-collation-functions.html)
  + [Moving the collate function to Ray Data](user-guides/scaling-collation-functions.html#moving-the-collate-function-to-ray-data)
  + [Creating a custom collate function that runs in Ray Data](user-guides/scaling-collation-functions.html#creating-a-custom-collate-function-that-runs-in-ray-data)
  + [Ensuring batch size alignment](user-guides/scaling-collation-functions.html#ensuring-batch-size-alignment)
  + [Putting things together](user-guides/scaling-collation-functions.html#putting-things-together)
  + [Advanced: Handling custom data types](user-guides/scaling-collation-functions.html#advanced-handling-custom-data-types)

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/train/user-guides.rst)