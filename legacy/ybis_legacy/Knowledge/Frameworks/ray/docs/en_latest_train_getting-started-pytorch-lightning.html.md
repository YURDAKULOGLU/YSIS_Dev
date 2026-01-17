Get Started with Distributed Training using PyTorch Lightning — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Get Started with Distributed Training using PyTorch Lightning[#](#get-started-with-distributed-training-using-pytorch-lightning "Link to this heading")

This tutorial walks through the process of converting an existing PyTorch Lightning script to use Ray Train.

Learn how to:

1. Configure the Lightning Trainer so that it runs distributed with Ray and on the correct CPU or GPU device.
2. Configure [training function](overview.html#train-overview-training-function) to report metrics and save checkpoints.
3. Configure [scaling](overview.html#train-overview-scaling-config) and CPU or GPU resource requirements for a training job.
4. Launch a distributed training job with a [`TorchTrainer`](api/doc/ray.train.torch.TorchTrainer.html#ray.train.torch.TorchTrainer "ray.train.torch.TorchTrainer").

## Quickstart[#](#quickstart "Link to this heading")

For reference, the final code is as follows:

```
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig

def train_func():
    # Your PyTorch Lightning training code here.

scaling_config = ScalingConfig(num_workers=2, use_gpu=True)
trainer = TorchTrainer(train_func, scaling_config=scaling_config)
result = trainer.fit()
```

1. `train_func` is the Python code that executes on each distributed training worker.
2. [`ScalingConfig`](api/doc/ray.train.ScalingConfig.html#ray.train.ScalingConfig "ray.train.ScalingConfig") defines the number of distributed training workers and whether to use GPUs.
3. [`TorchTrainer`](api/doc/ray.train.torch.TorchTrainer.html#ray.train.torch.TorchTrainer "ray.train.torch.TorchTrainer") launches the distributed training job.

Compare a PyTorch Lightning training script with and without Ray Train.

PyTorch Lightning + Ray Train

```
import os
import tempfile

import torch
from torch.utils.data import DataLoader
from torchvision.models import resnet18
from torchvision.datasets import FashionMNIST
from torchvision.transforms import ToTensor, Normalize, Compose
import lightning.pytorch as pl

import ray.train.lightning
from ray.train.torch import TorchTrainer

# Model, Loss, Optimizer
class ImageClassifier(pl.LightningModule):
    def __init__(self):
        super(ImageClassifier, self).__init__()
        self.model = resnet18(num_classes=10)
        self.model.conv1 = torch.nn.Conv2d(
            1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False
        )
        self.criterion = torch.nn.CrossEntropyLoss()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        outputs = self.forward(x)
        loss = self.criterion(outputs, y)
        self.log("loss", loss, on_step=True, prog_bar=True)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.model.parameters(), lr=0.001)


def train_func():
    # Data
    transform = Compose([ToTensor(), Normalize((0.28604,), (0.32025,))])
    data_dir = os.path.join(tempfile.gettempdir(), "data")
    train_data = FashionMNIST(root=data_dir, train=True, download=True, transform=transform)
    train_dataloader = DataLoader(train_data, batch_size=128, shuffle=True)

    # Training
    model = ImageClassifier()
    # [1] Configure PyTorch Lightning Trainer.
    trainer = pl.Trainer(
        max_epochs=10,
        devices="auto",
        accelerator="auto",
        strategy=ray.train.lightning.RayDDPStrategy(),
        plugins=[ray.train.lightning.RayLightningEnvironment()],
        callbacks=[ray.train.lightning.RayTrainReportCallback()],
        # [1a] Optionally, disable the default checkpointing behavior
        # in favor of the `RayTrainReportCallback` above.
        enable_checkpointing=False,
    )
    trainer = ray.train.lightning.prepare_trainer(trainer)
    trainer.fit(model, train_dataloaders=train_dataloader)

# [2] Configure scaling and resource requirements.
scaling_config = ray.train.ScalingConfig(num_workers=2, use_gpu=True)

# [3] Launch distributed training job.
trainer = TorchTrainer(
    train_func,
    scaling_config=scaling_config,
    # [3a] If running in a multi-node cluster, this is where you
    # should configure the run's persistent storage that is accessible
    # across all worker nodes.
    # run_config=ray.train.RunConfig(storage_path="s3://..."),
)
result: ray.train.Result = trainer.fit()

# [4] Load the trained model.
with result.checkpoint.as_directory() as checkpoint_dir:
    model = ImageClassifier.load_from_checkpoint(
        os.path.join(
            checkpoint_dir,
            ray.train.lightning.RayTrainReportCallback.CHECKPOINT_NAME,
        ),
    )
```


PyTorch Lightning

```
import torch
from torchvision.models import resnet18
from torchvision.datasets import FashionMNIST
from torchvision.transforms import ToTensor, Normalize, Compose
from torch.utils.data import DataLoader
import lightning.pytorch as pl

# Model, Loss, Optimizer
class ImageClassifier(pl.LightningModule):
    def __init__(self):
        super(ImageClassifier, self).__init__()
        self.model = resnet18(num_classes=10)
        self.model.conv1 = torch.nn.Conv2d(
            1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False
        )
        self.criterion = torch.nn.CrossEntropyLoss()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        outputs = self.forward(x)
        loss = self.criterion(outputs, y)
        self.log("loss", loss, on_step=True, prog_bar=True)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.model.parameters(), lr=0.001)

# Data
transform = Compose([ToTensor(), Normalize((0.28604,), (0.32025,))])
train_data = FashionMNIST(root='./data', train=True, download=True, transform=transform)
train_dataloader = DataLoader(train_data, batch_size=128, shuffle=True)

# Training
model = ImageClassifier()
trainer = pl.Trainer(max_epochs=10)
trainer.fit(model, train_dataloaders=train_dataloader)
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

Ray Train sets up your distributed process group on each worker. You only need to
make a few changes to your Lightning Trainer definition.

```
 import lightning.pytorch as pl
-from pl.strategies import DDPStrategy
-from pl.plugins.environments import LightningEnvironment
+import ray.train.lightning

 def train_func():
     ...
     model = MyLightningModule(...)
     datamodule = MyLightningDataModule(...)

     trainer = pl.Trainer(
-        devices=[0, 1, 2, 3],
-        strategy=DDPStrategy(),
-        plugins=[LightningEnvironment()],
+        devices="auto",
+        accelerator="auto",
+        strategy=ray.train.lightning.RayDDPStrategy(),
+        plugins=[ray.train.lightning.RayLightningEnvironment()]
     )
+    trainer = ray.train.lightning.prepare_trainer(trainer)

     trainer.fit(model, datamodule=datamodule)
```

The following sections discuss each change.

### Configure the distributed strategy[#](#configure-the-distributed-strategy "Link to this heading")

Ray Train offers several sub-classed distributed strategies for Lightning.
These strategies retain the same argument list as their base strategy classes.
Internally, they configure the root device and the distributed
sampler arguments.

* [`RayDDPStrategy`](api/doc/ray.train.lightning.RayDDPStrategy.html#ray.train.lightning.RayDDPStrategy "ray.train.lightning.RayDDPStrategy")
* [`RayFSDPStrategy`](api/doc/ray.train.lightning.RayFSDPStrategy.html#ray.train.lightning.RayFSDPStrategy "ray.train.lightning.RayFSDPStrategy")
* [`RayDeepSpeedStrategy`](api/doc/ray.train.lightning.RayDeepSpeedStrategy.html#ray.train.lightning.RayDeepSpeedStrategy "ray.train.lightning.RayDeepSpeedStrategy")

```
 import lightning.pytorch as pl
-from pl.strategies import DDPStrategy
+import ray.train.lightning

 def train_func():
     ...
     trainer = pl.Trainer(
         ...
-        strategy=DDPStrategy(),
+        strategy=ray.train.lightning.RayDDPStrategy(),
         ...
     )
     ...
```

### Configure the Ray cluster environment plugin[#](#configure-the-ray-cluster-environment-plugin "Link to this heading")

Ray Train also provides a [`RayLightningEnvironment`](api/doc/ray.train.lightning.RayLightningEnvironment.html#ray.train.lightning.RayLightningEnvironment "ray.train.lightning.RayLightningEnvironment") class
as a specification for the Ray Cluster. This utility class configures the worker’s
local, global, and node rank and world size.

```
 import lightning.pytorch as pl
-from pl.plugins.environments import LightningEnvironment
+import ray.train.lightning

 def train_func():
     ...
     trainer = pl.Trainer(
         ...
-        plugins=[LightningEnvironment()],
+        plugins=[ray.train.lightning.RayLightningEnvironment()],
         ...
     )
     ...
```

### Configure parallel devices[#](#configure-parallel-devices "Link to this heading")

In addition, Ray TorchTrainer has already configured the correct
`CUDA_VISIBLE_DEVICES` for you. One should always use all available
GPUs by setting `devices="auto"` and `acelerator="auto"`.

```
 import lightning.pytorch as pl

 def train_func():
     ...
     trainer = pl.Trainer(
         ...
-        devices=[0,1,2,3],
+        devices="auto",
+        accelerator="auto",
         ...
     )
     ...
```

### Report checkpoints and metrics[#](#report-checkpoints-and-metrics "Link to this heading")

To persist your checkpoints and monitor training progress, add a
[`ray.train.lightning.RayTrainReportCallback`](api/doc/ray.train.lightning.RayTrainReportCallback.html#ray.train.lightning.RayTrainReportCallback "ray.train.lightning.RayTrainReportCallback") utility callback to your Trainer.

```
 import lightning.pytorch as pl
 from ray.train.lightning import RayTrainReportCallback

 def train_func():
     ...
     trainer = pl.Trainer(
         ...
-        callbacks=[...],
+        callbacks=[..., RayTrainReportCallback()],
     )
     ...
```

Reporting metrics and checkpoints to Ray Train enables you to support [fault-tolerant training](user-guides/fault-tolerance.html#train-fault-tolerance) and [hyperparameter optimization](user-guides/hyperparameter-optimization.html#train-tune).
Note that the [`ray.train.lightning.RayTrainReportCallback`](api/doc/ray.train.lightning.RayTrainReportCallback.html#ray.train.lightning.RayTrainReportCallback "ray.train.lightning.RayTrainReportCallback") class only provides a simple implementation, and can be [further customized](user-guides/checkpoints.html#train-dl-saving-checkpoints).

### Prepare your Lightning Trainer[#](#prepare-your-lightning-trainer "Link to this heading")

Finally, pass your Lightning Trainer into
[`prepare_trainer()`](api/doc/ray.train.lightning.prepare_trainer.html#ray.train.lightning.prepare_trainer "ray.train.lightning.prepare_trainer") to validate
your configurations.

```
 import lightning.pytorch as pl
 import ray.train.lightning

 def train_func():
     ...
     trainer = pl.Trainer(...)
+    trainer = ray.train.lightning.prepare_trainer(trainer)
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

After you have converted your PyTorch Lightning training script to use Ray Train:

* See [User Guides](user-guides.html#train-user-guides) to learn more about how to perform specific tasks.
* Browse the [Examples](examples.html) for end-to-end examples of how to use Ray Train.
* Consult the [API Reference](api/api.html#train-api) for more details on the classes and methods from this tutorial.

## Version Compatibility[#](#version-compatibility "Link to this heading")

Ray Train is tested with `pytorch_lightning` versions `1.6.5` and `2.1.2`. For full compatibility, use `pytorch_lightning>=1.6.5` .
Earlier versions aren’t prohibited but may result in unexpected issues. If you run into any compatibility issues, consider upgrading your PyTorch Lightning version or
[file an issue](https://github.com/ray-project/ray/issues).

Note

If you are using Lightning 2.x, please use the import path `lightning.pytorch.xxx` instead of `pytorch_lightning.xxx`.

## LightningTrainer Migration Guide[#](#lightningtrainer-migration-guide "Link to this heading")

Ray 2.4 introduced the `LightningTrainer`, and exposed a
`LightningConfigBuilder` to define configurations for `pl.LightningModule`
and `pl.Trainer`.

It then instantiates the model and trainer objects and runs a pre-defined
training function in a black box.

This version of the LightningTrainer API was constraining and limited
your ability to manage the training functionality.

Ray 2.7 introduced the newly unified [`TorchTrainer`](api/doc/ray.train.torch.TorchTrainer.html#ray.train.torch.TorchTrainer "ray.train.torch.TorchTrainer") API, which offers
enhanced transparency, flexibility, and simplicity. This API is more aligned
with standard PyTorch Lightning scripts, ensuring users have better
control over their native Lightning code.

(Deprecating) LightningTrainer

```
from ray.train.lightning import LightningConfigBuilder, LightningTrainer

config_builder = LightningConfigBuilder()
# [1] Collect model configs
config_builder.module(cls=MyLightningModule, lr=1e-3, feature_dim=128)

# [2] Collect checkpointing configs
config_builder.checkpointing(monitor="val_accuracy", mode="max", save_top_k=3)

# [3] Collect pl.Trainer configs
config_builder.trainer(
    max_epochs=10,
    accelerator="gpu",
    log_every_n_steps=100,
)

# [4] Build datasets on the head node
datamodule = MyLightningDataModule(batch_size=32)
config_builder.fit_params(datamodule=datamodule)

# [5] Execute the internal training function in a black box
ray_trainer = LightningTrainer(
    lightning_config=config_builder.build(),
    scaling_config=ScalingConfig(num_workers=4, use_gpu=True),
    run_config=RunConfig(
        checkpoint_config=CheckpointConfig(
            num_to_keep=3,
            checkpoint_score_attribute="val_accuracy",
            checkpoint_score_order="max",
        ),
    )
)
result = ray_trainer.fit()

# [6] Load the trained model from an opaque Lightning-specific checkpoint.
lightning_checkpoint = result.checkpoint
model = lightning_checkpoint.get_model(MyLightningModule)
```


(New API) TorchTrainer

```
import os

import lightning.pytorch as pl

import ray.train
from ray.train.torch import TorchTrainer
from ray.train.lightning import (
    RayDDPStrategy,
    RayLightningEnvironment,
    RayTrainReportCallback,
    prepare_trainer
)

def train_func():
    # [1] Create a Lightning model
    model = MyLightningModule(lr=1e-3, feature_dim=128)

    # [2] Report Checkpoint with callback
    ckpt_report_callback = RayTrainReportCallback()

    # [3] Create a Lighting Trainer
    trainer = pl.Trainer(
        max_epochs=10,
        log_every_n_steps=100,
        # New configurations below
        devices="auto",
        accelerator="auto",
        strategy=RayDDPStrategy(),
        plugins=[RayLightningEnvironment()],
        callbacks=[ckpt_report_callback],
    )

    # Validate your Lightning trainer configuration
    trainer = prepare_trainer(trainer)

    # [4] Build your datasets on each worker
    datamodule = MyLightningDataModule(batch_size=32)
    trainer.fit(model, datamodule=datamodule)

# [5] Explicitly define and run the training function
ray_trainer = TorchTrainer(
    train_func,
    scaling_config=ray.train.ScalingConfig(num_workers=4, use_gpu=True),
    run_config=ray.train.RunConfig(
        checkpoint_config=ray.train.CheckpointConfig(
            num_to_keep=3,
            checkpoint_score_attribute="val_accuracy",
            checkpoint_score_order="max",
        ),
    )
)
result = ray_trainer.fit()

# [6] Load the trained model from a simplified checkpoint interface.
checkpoint: ray.train.Checkpoint = result.checkpoint
with checkpoint.as_directory() as checkpoint_dir:
    print("Checkpoint contents:", os.listdir(checkpoint_dir))
    checkpoint_path = os.path.join(checkpoint_dir, "checkpoint.ckpt")
    model = MyLightningModule.load_from_checkpoint(checkpoint_path)
```

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/train/getting-started-pytorch-lightning.rst)