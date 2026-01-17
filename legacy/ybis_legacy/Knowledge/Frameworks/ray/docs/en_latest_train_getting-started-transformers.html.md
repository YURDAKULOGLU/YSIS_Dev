Get Started with Distributed Training using Hugging Face Transformers — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Get Started with Distributed Training using Hugging Face Transformers[#](#get-started-with-distributed-training-using-hugging-face-transformers "Link to this heading")

This tutorial shows you how to convert an existing Hugging Face Transformers script to use Ray Train for distributed training.

In this guide, learn how to:

1. Configure a [training function](overview.html#train-overview-training-function) that properly reports metrics and saves checkpoints.
2. Configure [scaling](overview.html#train-overview-scaling-config) and resource requirements for CPUs or GPUs for your distributed training job.
3. Launch a distributed training job with [`TorchTrainer`](api/doc/ray.train.torch.TorchTrainer.html#ray.train.torch.TorchTrainer "ray.train.torch.TorchTrainer").

## Requirements[#](#requirements "Link to this heading")

Install the necessary packages before you begin:

```
pip install "ray[train]" torch "transformers[torch]" datasets evaluate numpy scikit-learn
```

## Quickstart[#](#quickstart "Link to this heading")

Here’s a quick overview of the final code structure:

```
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig

def train_func():
    # Your Transformers training code here
    ...

scaling_config = ScalingConfig(num_workers=2, use_gpu=True)
trainer = TorchTrainer(train_func, scaling_config=scaling_config)
result = trainer.fit()
```

The key components are:

1. `train_func`: Python code that runs on each distributed training worker.
2. [`ScalingConfig`](api/doc/ray.train.ScalingConfig.html#ray.train.ScalingConfig "ray.train.ScalingConfig"): Defines the number of distributed training workers and GPU usage.
3. [`TorchTrainer`](api/doc/ray.train.torch.TorchTrainer.html#ray.train.torch.TorchTrainer "ray.train.torch.TorchTrainer"): Launches and manages the distributed training job.

## Code Comparison: Hugging Face Transformers vs. Ray Train Integration[#](#code-comparison-hugging-face-transformers-vs-ray-train-integration "Link to this heading")

Compare a standard Hugging Face Transformers script with its Ray Train equivalent:

Hugging Face Transformers + Ray Train

```
import os

import numpy as np
import evaluate
from datasets import load_dataset
from transformers import (
    Trainer,
    TrainingArguments,
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

import ray.train.huggingface.transformers
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer


# [1] Encapsulate data preprocessing, training, and evaluation
# logic in a training function
# ============================================================
def train_func():
    # Datasets
    dataset = load_dataset("yelp_review_full")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    small_train_dataset = (
        dataset["train"].select(range(100)).map(tokenize_function, batched=True)
    )
    small_eval_dataset = (
        dataset["test"].select(range(100)).map(tokenize_function, batched=True)
    )

    # Model
    model = AutoModelForSequenceClassification.from_pretrained(
        "bert-base-cased", num_labels=5
    )

    # Evaluation Metrics
    metric = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)

    # Hugging Face Trainer
    training_args = TrainingArguments(
        output_dir="test_trainer",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        compute_metrics=compute_metrics,
    )

    # [2] Report Metrics and Checkpoints to Ray Train
    # ===============================================
    callback = ray.train.huggingface.transformers.RayTrainReportCallback()
    trainer.add_callback(callback)

    # [3] Prepare Transformers Trainer
    # ================================
    trainer = ray.train.huggingface.transformers.prepare_trainer(trainer)

    # Start Training
    trainer.train()


# [4] Define a Ray TorchTrainer to launch `train_func` on all workers
# ===================================================================
ray_trainer = TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(num_workers=2, use_gpu=True),
    # [4a] For multi-node clusters, configure persistent storage that is
    # accessible across all worker nodes
    # run_config=ray.train.RunConfig(storage_path="s3://..."),
)
result: ray.train.Result = ray_trainer.fit()

# [5] Load the trained model
with result.checkpoint.as_directory() as checkpoint_dir:
    checkpoint_path = os.path.join(
        checkpoint_dir,
        ray.train.huggingface.transformers.RayTrainReportCallback.CHECKPOINT_NAME,
    )
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint_path)
```


Hugging Face Transformers

```
# Adapted from Hugging Face tutorial: https://huggingface.co/docs/transformers/training

import numpy as np
import evaluate
from datasets import load_dataset
from transformers import (
    Trainer,
    TrainingArguments,
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

# Datasets
dataset = load_dataset("yelp_review_full")
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

small_train_dataset = dataset["train"].select(range(100)).map(tokenize_function, batched=True)
small_eval_dataset = dataset["test"].select(range(100)).map(tokenize_function, batched=True)

# Model
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-cased", num_labels=5
)

# Metrics
metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

# Hugging Face Trainer
training_args = TrainingArguments(
    output_dir="test_trainer", evaluation_strategy="epoch", report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=small_train_dataset,
    eval_dataset=small_eval_dataset,
    compute_metrics=compute_metrics,
)

# Start Training
trainer.train()
```

## Set up a training function[#](#set-up-a-training-function "Link to this heading")

First, update your training code to support distributed training.
Begin by wrapping your code in a [training function](overview.html#train-overview-training-function):

```
def train_func():
    # Your model training code here.
    ...
```

Each distributed training worker executes this function.

You can also specify the input argument for `train_func` as a dictionary via the Trainer’s `train_loop_config`. For example:

```
def train_func(config):
    lr = config["lr"]
    num_epochs = config["num_epochs"]

config = {"lr": 1e-4, "num_epochs": 10}
trainer = ray.train.torch.TorchTrainer(train_func, train_loop_config=config, ...)
```

Warning

Avoid passing large data objects through `train_loop_config` to reduce the
serialization and deserialization overhead. Instead, it’s preferred to
initialize large objects (e.g. datasets, models) directly in `train_func`.

```
 def load_dataset():
     # Return a large in-memory dataset
     ...

 def load_model():
     # Return a large in-memory model instance
     ...

-config = {"data": load_dataset(), "model": load_model()}

 def train_func(config):
-    data = config["data"]
-    model = config["model"]

+    data = load_dataset()
+    model = load_model()
     ...

 trainer = ray.train.torch.TorchTrainer(train_func, train_loop_config=config, ...)
```

Ray Train sets up the distributed process group on each worker before entering the training function.
Put all your logic into this function, including:

* Dataset construction and preprocessing
* Model initialization
* Transformers trainer definition

Note

When using Hugging Face Datasets or Evaluate, always call `datasets.load_dataset` and `evaluate.load`
inside the training function. Don’t pass loaded datasets and metrics from outside the training
function, as this can cause serialization errors when transferring objects to workers.

### Report checkpoints and metrics[#](#report-checkpoints-and-metrics "Link to this heading")

To persist checkpoints and monitor training progress, add a
[`ray.train.huggingface.transformers.RayTrainReportCallback`](api/doc/ray.train.huggingface.transformers.RayTrainReportCallback.html#ray.train.huggingface.transformers.RayTrainReportCallback "ray.train.huggingface.transformers.RayTrainReportCallback") utility callback to your Trainer:

```
 import transformers
 from ray.train.huggingface.transformers import RayTrainReportCallback

 def train_func():
     ...
     trainer = transformers.Trainer(...)
+    trainer.add_callback(RayTrainReportCallback())
     ...
```

Reporting metrics and checkpoints to Ray Train enables integration with Ray Tune and [fault-tolerant training](user-guides/fault-tolerance.html#train-fault-tolerance).
The [`ray.train.huggingface.transformers.RayTrainReportCallback`](api/doc/ray.train.huggingface.transformers.RayTrainReportCallback.html#ray.train.huggingface.transformers.RayTrainReportCallback "ray.train.huggingface.transformers.RayTrainReportCallback") provides a basic implementation, and you can [customize it](user-guides/checkpoints.html#train-dl-saving-checkpoints) to fit your needs.

### Prepare a Transformers Trainer[#](#prepare-a-transformers-trainer "Link to this heading")

Pass your Transformers Trainer into
[`prepare_trainer()`](api/doc/ray.train.huggingface.transformers.prepare_trainer.html#ray.train.huggingface.transformers.prepare_trainer "ray.train.huggingface.transformers.prepare_trainer") to validate
configurations and enable Ray Data integration:

```
 import transformers
 import ray.train.huggingface.transformers

 def train_func():
     ...
     trainer = transformers.Trainer(...)
+    trainer = ray.train.huggingface.transformers.prepare_trainer(trainer)
     trainer.train()
     ...
```

## Configure scale and GPUs[#](#configure-scale-and-gpus "Link to this heading")

Outside of your training function, create a [`ScalingConfig`](api/doc/ray.train.ScalingConfig.html#ray.train.ScalingConfig "ray.train.ScalingConfig") object to configure:

1. [`num_workers`](api/doc/ray.train.ScalingConfig.html#ray.train.ScalingConfig "ray.train.ScalingConfig") - The number of distributed training worker processes.
2. [`use_gpu`](api/doc/ray.train.ScalingConfig.html#ray.train.ScalingConfig "ray.train.ScalingConfig") - Whether each worker should use a GPU (or CPU).

```
from ray.train import ScalingConfig
scaling_config = ScalingConfig(num_workers=2, use_gpu=True)
```

For more details, see [Configuring Scale and GPUs](user-guides/using-gpus.html#train-scaling-config).

## Configure persistent storage[#](#configure-persistent-storage "Link to this heading")

Create a [`RunConfig`](api/doc/ray.train.RunConfig.html#ray.train.RunConfig "ray.train.RunConfig") object to specify the path where results
(including checkpoints and artifacts) will be saved.

```
from ray.train import RunConfig

# Local path (/some/local/path/unique_run_name)
run_config = RunConfig(storage_path="/some/local/path", name="unique_run_name")

# Shared cloud storage URI (s3://bucket/unique_run_name)
run_config = RunConfig(storage_path="s3://bucket", name="unique_run_name")

# Shared NFS path (/mnt/nfs/unique_run_name)
run_config = RunConfig(storage_path="/mnt/nfs", name="unique_run_name")
```

Warning

Specifying a *shared storage location* (such as cloud storage or NFS) is
*optional* for single-node clusters, but it is **required for multi-node clusters.**
Using a local path will [raise an error](user-guides/persistent-storage.html#multinode-local-storage-warning)
during checkpointing for multi-node clusters.

For more details, see [Configuring Persistent Storage](user-guides/persistent-storage.html#persistent-storage-guide).

## Launch a training job[#](#launch-a-training-job "Link to this heading")

Tying this all together, you can now launch a distributed training job
with a [`TorchTrainer`](api/doc/ray.train.torch.TorchTrainer.html#ray.train.torch.TorchTrainer "ray.train.torch.TorchTrainer").

```
from ray.train.torch import TorchTrainer

trainer = TorchTrainer(
    train_func, scaling_config=scaling_config, run_config=run_config
)
result = trainer.fit()
```

## Access training results[#](#access-training-results "Link to this heading")

After training completes, a [`Result`](api/doc/ray.train.Result.html#ray.train.Result "ray.train.Result") object is returned which contains
information about the training run, including the metrics and checkpoints reported during training.

```
result.metrics     # The metrics reported during training.
result.checkpoint  # The latest checkpoint reported during training.
result.path        # The path where logs are stored.
result.error       # The exception that was raised, if training failed.
```

For more usage examples, see [Inspecting Training Results](user-guides/results.html#train-inspect-results).

## Next steps[#](#next-steps "Link to this heading")

Now that you’ve converted your Hugging Face Transformers script to use Ray Train:

* Explore [User Guides](user-guides.html#train-user-guides) to learn about specific tasks
* Browse the [Examples](examples.html) for end-to-end Ray Train applications
* Consult the [API Reference](api/api.html#train-api) for detailed information on the classes and methods

## TransformersTrainer Migration Guide[#](#transformerstrainer-migration-guide "Link to this heading")

Ray 2.1 introduced `TransformersTrainer` with a `trainer_init_per_worker` interface
to define `transformers.Trainer` and execute a pre-defined training function.

Ray 2.7 introduced the unified [`TorchTrainer`](api/doc/ray.train.torch.TorchTrainer.html#ray.train.torch.TorchTrainer "ray.train.torch.TorchTrainer") API,
which offers better transparency, flexibility, and simplicity. This API aligns more closely
with standard Hugging Face Transformers scripts, giving you better control over your
training code.

(Deprecating) TransformersTrainer

```
import transformers
from transformers import AutoConfig, AutoModelForCausalLM
from datasets import load_dataset

import ray
from ray.train.huggingface import TransformersTrainer
from ray.train import ScalingConfig
from huggingface_hub import HfFileSystem


# Load datasets using HfFileSystem
path = "hf://datasets/Salesforce/wikitext/wikitext-2-raw-v1/"
fs = HfFileSystem()
# List the parquet files for each split
all_files = [f["name"] for f in fs.ls(path)]
train_files = [f for f in all_files if "train" in f and f.endswith(".parquet")]
validation_files = [f for f in all_files if "validation" in f and f.endswith(".parquet")]
ray_train_ds = ray.data.read_parquet(train_files, filesystem=fs)
ray_eval_ds = ray.data.read_parquet(validation_files, filesystem=fs)

# Define the Trainer generation function
def trainer_init_per_worker(train_dataset, eval_dataset, **config):
    MODEL_NAME = "gpt2"
    model_config = AutoConfig.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_config(model_config)
    args = transformers.TrainingArguments(
        output_dir=f"{MODEL_NAME}-wikitext2",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_strategy="epoch",
        learning_rate=2e-5,
        weight_decay=0.01,
        max_steps=100,
    )
    return transformers.Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )

# Build a Ray TransformersTrainer
scaling_config = ScalingConfig(num_workers=4, use_gpu=True)
ray_trainer = TransformersTrainer(
    trainer_init_per_worker=trainer_init_per_worker,
    scaling_config=scaling_config,
    datasets={"train": ray_train_ds, "validation": ray_eval_ds},
)
result = ray_trainer.fit()
```


(New API) TorchTrainer

```
import transformers
from transformers import AutoConfig, AutoModelForCausalLM
from datasets import load_dataset

import ray
from ray.train.torch import TorchTrainer
from ray.train.huggingface.transformers import (
    RayTrainReportCallback,
    prepare_trainer,
)
from ray.train import ScalingConfig
from huggingface_hub import HfFileSystem


# Load datasets using HfFileSystem
path = "hf://datasets/Salesforce/wikitext/wikitext-2-raw-v1/"
fs = HfFileSystem()
# List the parquet files for each split
all_files = [f["name"] for f in fs.ls(path)]
train_files = [f for f in all_files if "train" in f and f.endswith(".parquet")]
validation_files = [f for f in all_files if "validation" in f and f.endswith(".parquet")]
ray_train_ds = ray.data.read_parquet(train_files, filesystem=fs)
ray_eval_ds = ray.data.read_parquet(validation_files, filesystem=fs)

# [1] Define the full training function
# =====================================
def train_func():
    MODEL_NAME = "gpt2"
    model_config = AutoConfig.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_config(model_config)

    # [2] Build Ray Data iterables
    # ============================
    train_dataset = ray.train.get_dataset_shard("train")
    eval_dataset = ray.train.get_dataset_shard("validation")

    train_iterable_ds = train_dataset.iter_torch_batches(batch_size=8)
    eval_iterable_ds = eval_dataset.iter_torch_batches(batch_size=8)

    args = transformers.TrainingArguments(
        output_dir=f"{MODEL_NAME}-wikitext2",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_strategy="epoch",
        learning_rate=2e-5,
        weight_decay=0.01,
        max_steps=100,
    )

    trainer = transformers.Trainer(
        model=model,
        args=args,
        train_dataset=train_iterable_ds,
        eval_dataset=eval_iterable_ds,
    )

    # [3] Add Ray Train Report Callback
    # =================================
    trainer.add_callback(RayTrainReportCallback())

    # [4] Prepare your trainer
    # ========================
    trainer = prepare_trainer(trainer)
    trainer.train()

# Build a Ray TorchTrainer
scaling_config = ScalingConfig(num_workers=4, use_gpu=True)
ray_trainer = TorchTrainer(
    train_func,
    scaling_config=scaling_config,
    datasets={"train": ray_train_ds, "validation": ray_eval_ds},
)
result = ray_trainer.fit()
```

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/train/getting-started-transformers.rst)