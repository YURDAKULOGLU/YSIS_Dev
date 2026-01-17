Get Started with Distributed Training using PyTorch — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Get Started with Distributed Training using PyTorch[#](#get-started-with-distributed-training-using-pytorch "Link to this heading")

This tutorial walks through the process of converting an existing PyTorch script to use Ray Train.

Learn how to:

1. Configure a model to run distributed and on the correct CPU/GPU device.
2. Configure a dataloader to shard data across the [workers](overview.html#train-overview-worker) and place data on the correct CPU or GPU device.
3. Configure a [training function](overview.html#train-overview-training-function) to report metrics and save checkpoints.
4. Configure [scaling](overview.html#train-overview-scaling-config) and CPU or GPU resource requirements for a training job.
5. Launch a distributed training job with a [`TorchTrainer`](api/doc/ray.train.torch.TorchTrainer.html#ray.train.torch.TorchTrainer "ray.train.torch.TorchTrainer") class.

## Quickstart[#](#quickstart "Link to this heading")

For reference, the final code will look something like the following:

```
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig

def train_func():
    # Your PyTorch training code here.
    ...

scaling_config = ScalingConfig(num_workers=2, use_gpu=True)
trainer = TorchTrainer(train_func, scaling_config=scaling_config)
result = trainer.fit()
```

1. `train_func` is the Python code that executes on each distributed training worker.
2. [`ScalingConfig`](api/doc/ray.train.ScalingConfig.html#ray.train.ScalingConfig "ray.train.ScalingConfig") defines the number of distributed training workers and whether to use GPUs.
3. [`TorchTrainer`](api/doc/ray.train.torch.TorchTrainer.html#ray.train.torch.TorchTrainer "ray.train.torch.TorchTrainer") launches the distributed training job.

Compare a PyTorch training script with and without Ray Train.

PyTorch + Ray Train

```
import os
import tempfile

import torch
from torch.nn import CrossEntropyLoss
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision.models import resnet18
from torchvision.datasets import FashionMNIST
from torchvision.transforms import ToTensor, Normalize, Compose

import ray.train.torch

def train_func():
    # Model, Loss, Optimizer
    model = resnet18(num_classes=10)
    model.conv1 = torch.nn.Conv2d(
        1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False
    )
    # [1] Prepare model.
    model = ray.train.torch.prepare_model(model)
    # model.to("cuda")  # This is done by `prepare_model`
    criterion = CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=0.001)

    # Data
    transform = Compose([ToTensor(), Normalize((0.28604,), (0.32025,))])
    data_dir = os.path.join(tempfile.gettempdir(), "data")
    train_data = FashionMNIST(root=data_dir, train=True, download=True, transform=transform)
    train_loader = DataLoader(train_data, batch_size=128, shuffle=True)
    # [2] Prepare dataloader.
    train_loader = ray.train.torch.prepare_data_loader(train_loader)

    # Training
    for epoch in range(10):
        if ray.train.get_context().get_world_size() > 1:
            train_loader.sampler.set_epoch(epoch)

        for images, labels in train_loader:
            # This is done by `prepare_data_loader`!
            # images, labels = images.to("cuda"), labels.to("cuda")
            outputs = model(images)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # [3] Report metrics and checkpoint.
        metrics = {"loss": loss.item(), "epoch": epoch}
        with tempfile.TemporaryDirectory() as temp_checkpoint_dir:
            torch.save(
                model.module.state_dict(),
                os.path.join(temp_checkpoint_dir, "model.pt")
            )
            ray.train.report(
                metrics,
                checkpoint=ray.train.Checkpoint.from_directory(temp_checkpoint_dir),
            )
        if ray.train.get_context().get_world_rank() == 0:
            print(metrics)

# [4] Configure scaling and resource requirements.
scaling_config = ray.train.ScalingConfig(num_workers=2, use_gpu=True)

# [5] Launch distributed training job.
trainer = ray.train.torch.TorchTrainer(
    train_func,
    scaling_config=scaling_config,
    # [5a] If running in a multi-node cluster, this is where you
    # should configure the run's persistent storage that is accessible
    # across all worker nodes.
    # run_config=ray.train.RunConfig(storage_path="s3://..."),
)
result = trainer.fit()

# [6] Load the trained model.
with result.checkpoint.as_directory() as checkpoint_dir:
    model_state_dict = torch.load(os.path.join(checkpoint_dir, "model.pt"))
    model = resnet18(num_classes=10)
    model.conv1 = torch.nn.Conv2d(
        1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False
    )
    model.load_state_dict(model_state_dict)
```


PyTorch

```
import os
import tempfile

import torch
from torch.nn import CrossEntropyLoss
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision.models import resnet18
from torchvision.datasets import FashionMNIST
from torchvision.transforms import ToTensor, Normalize, Compose

# Model, Loss, Optimizer
model = resnet18(num_classes=10)
model.conv1 = torch.nn.Conv2d(
    1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False
)
model.to("cuda")
criterion = CrossEntropyLoss()
optimizer = Adam(model.parameters(), lr=0.001)

# Data
transform = Compose([ToTensor(), Normalize((0.28604,), (0.32025,))])
train_data = FashionMNIST(root='./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=128, shuffle=True)

# Training
for epoch in range(10):
    for images, labels in train_loader:
        images, labels = images.to("cuda"), labels.to("cuda")
        outputs = model(images)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    metrics = {"loss": loss.item(), "epoch": epoch}
    checkpoint_dir = tempfile.mkdtemp()
    checkpoint_path = os.path.join(checkpoint_dir, "model.pt")
    torch.save(model.state_dict(), checkpoint_path)
    print(metrics)
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

### Set up a model[#](#set-up-a-model "Link to this heading")

Use the [`ray.train.torch.prepare_model()`](api/doc/ray.train.torch.prepare_model.html#ray.train.torch.prepare_model "ray.train.torch.prepare_model") utility function to:

1. Move your model to the correct device.
2. Wrap it in `DistributedDataParallel`.

```
-from torch.nn.parallel import DistributedDataParallel
+import ray.train.torch

 def train_func():

     ...

     # Create model.
     model = ...

     # Set up distributed training and device placement.
-    device_id = ... # Your logic to get the right device.
-    model = model.to(device_id or "cpu")
-    model = DistributedDataParallel(model, device_ids=[device_id])
+    model = ray.train.torch.prepare_model(model)

     ...
```

### Set up a dataset[#](#set-up-a-dataset "Link to this heading")

Use the [`ray.train.torch.prepare_data_loader()`](api/doc/ray.train.torch.prepare_data_loader.html#ray.train.torch.prepare_data_loader "ray.train.torch.prepare_data_loader") utility function, which:

1. Adds a [`DistributedSampler`](https://docs.pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler "(in PyTorch v2.9)") to your [`DataLoader`](https://docs.pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader "(in PyTorch v2.9)").
2. Moves the batches to the right device.

Note that this step isn’t necessary if you’re passing in Ray Data to your Trainer.
See [Data Loading and Preprocessing](user-guides/data-loading-preprocessing.html#data-ingest-torch).

```
 from torch.utils.data import DataLoader
+import ray.train.torch

 def train_func():

     ...

     dataset = ...

     data_loader = DataLoader(dataset, batch_size=worker_batch_size, shuffle=True)
+    data_loader = ray.train.torch.prepare_data_loader(data_loader)

     for epoch in range(10):
+        if ray.train.get_context().get_world_size() > 1:
+            data_loader.sampler.set_epoch(epoch)

         for X, y in data_loader:
-            X = X.to_device(device)
-            y = y.to_device(device)

     ...
```

Tip

Keep in mind that `DataLoader` takes in a `batch_size` which is the batch size for each worker.
The global batch size can be calculated from the worker batch size (and vice-versa) with the following equation:

```
global_batch_size = worker_batch_size * ray.train.get_context().get_world_size()
```

Note

If you already manually set up your `DataLoader` with a `DistributedSampler`,
[`prepare_data_loader()`](api/doc/ray.train.torch.prepare_data_loader.html#ray.train.torch.prepare_data_loader "ray.train.torch.prepare_data_loader") will not add another one, and will
respect the configuration of the existing sampler.

Note

[`DistributedSampler`](https://docs.pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler "(in PyTorch v2.9)") does not work with a
`DataLoader` that wraps [`IterableDataset`](https://docs.pytorch.org/docs/stable/data.html#torch.utils.data.IterableDataset "(in PyTorch v2.9)").
If you want to work with an dataset iterator,
consider using [Ray Data](../data/data.html#data) instead of PyTorch DataLoader since it
provides performant streaming data ingestion for large scale datasets.

See [Data Loading and Preprocessing](user-guides/data-loading-preprocessing.html#data-ingest-torch) for more details.

### Report checkpoints and metrics[#](#report-checkpoints-and-metrics "Link to this heading")

To monitor progress, you can report intermediate metrics and checkpoints using the [`ray.train.report()`](api/doc/ray.train.report.html#ray.train.report "ray.train.report") utility function.

```
+import os
+import tempfile

+import ray.train

 def train_func():

     ...

     with tempfile.TemporaryDirectory() as temp_checkpoint_dir:
        torch.save(
            model.state_dict(), os.path.join(temp_checkpoint_dir, "model.pt")
        )

+       metrics = {"loss": loss.item()}  # Training/validation metrics.

        # Build a Ray Train checkpoint from a directory
+       checkpoint = ray.train.Checkpoint.from_directory(temp_checkpoint_dir)

        # Ray Train will automatically save the checkpoint to persistent storage,
        # so the local `temp_checkpoint_dir` can be safely cleaned up after.
+       ray.train.report(metrics=metrics, checkpoint=checkpoint)

     ...
```

For more details, see [Monitoring and Logging Metrics](user-guides/monitoring-logging.html#train-monitoring-and-logging) and [Saving and Loading Checkpoints](user-guides/checkpoints.html#train-checkpointing).

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

After you have converted your PyTorch training script to use Ray Train:

* See [User Guides](user-guides.html#train-user-guides) to learn more about how to perform specific tasks.
* Browse the [Examples](examples.html) for end-to-end examples of how to use Ray Train.
* Dive into the [API Reference](api/api.html#train-api) for more details on the classes and methods used in this tutorial.

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/train/getting-started-pytorch.rst)