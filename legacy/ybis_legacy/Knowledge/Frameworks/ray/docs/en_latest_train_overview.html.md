Ray Train Overview — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Ray Train Overview[#](#ray-train-overview "Link to this heading")

To use Ray Train effectively, you need to understand four main concepts:

1. [Training function](#train-overview-training-function): A Python function that contains your model training logic.
2. [Worker](#train-overview-worker): A process that runs the training function.
3. [Scaling configuration:](#train-overview-scaling-config) A configuration of the number of workers and compute resources (for example, CPUs or GPUs).
4. [Trainer](#train-overview-trainers): A Python class that ties together the training function, workers, and scaling configuration to execute a distributed training job.

![../_images/overview.png](../_images/overview.png)

## Training function[#](#training-function "Link to this heading")

The training function is a user-defined Python function that contains the end-to-end model training loop logic.
When launching a distributed training job, each worker executes this training function.

Ray Train documentation uses the following conventions:

1. `train_func` is a user-defined function that contains the training code.
2. `train_func` is passed into the Trainer’s `train_loop_per_worker` parameter.

```
def train_func():
    """User-defined training function that runs on each distributed worker process.

    This function typically contains logic for loading the model,
    loading the dataset, training the model, saving checkpoints,
    and logging metrics.
    """
    ...
```

## Worker[#](#worker "Link to this heading")

Ray Train distributes model training compute to individual worker processes across the cluster.
Each worker is a process that executes the `train_func`.
The number of workers determines the parallelism of the training job and is configured in the [`ScalingConfig`](api/doc/ray.train.ScalingConfig.html#ray.train.ScalingConfig "ray.train.ScalingConfig").

## Scaling configuration[#](#scaling-configuration "Link to this heading")

The [`ScalingConfig`](api/doc/ray.train.ScalingConfig.html#ray.train.ScalingConfig "ray.train.ScalingConfig") is the mechanism for defining the scale of the training job.
Specify two basic parameters for worker parallelism and compute resources:

* [`num_workers`](api/doc/ray.train.ScalingConfig.html#ray.train.ScalingConfig "ray.train.ScalingConfig"): The number of workers to launch for a distributed training job.
* [`use_gpu`](api/doc/ray.train.ScalingConfig.html#ray.train.ScalingConfig "ray.train.ScalingConfig"): Whether each worker should use a GPU or CPU.

```
from ray.train import ScalingConfig

# Single worker with a CPU
scaling_config = ScalingConfig(num_workers=1, use_gpu=False)

# Single worker with a GPU
scaling_config = ScalingConfig(num_workers=1, use_gpu=True)

# Multiple workers, each with a GPU
scaling_config = ScalingConfig(num_workers=4, use_gpu=True)
```

## Trainer[#](#trainer "Link to this heading")

The Trainer ties the previous three concepts together to launch distributed training jobs.
Ray Train provides [Trainer classes](api/api.html#train-api) for different frameworks.
Calling the [`fit()`](api/doc/ray.train.trainer.BaseTrainer.fit.html#ray.train.trainer.BaseTrainer.fit "ray.train.trainer.BaseTrainer.fit") method executes the training job by:

1. Launching workers as defined by the [scaling\_config](#train-overview-scaling-config).
2. Setting up the framework’s distributed environment on all workers.
3. Running the `train_func` on all workers.

```
from ray.train.torch import TorchTrainer

trainer = TorchTrainer(train_func, scaling_config=scaling_config)
trainer.fit()
```

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/train/overview.rst)