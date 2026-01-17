Fine-tune dolly-v2-7b with Ray Train, PyTorch Lightning and FSDP — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Fine-tune `dolly-v2-7b` with Ray Train, PyTorch Lightning and FSDP[#](#fine-tune-dolly-v2-7b-with-ray-train-pytorch-lightning-and-fsdp "Link to this heading")

[![try-anyscale-quickstart](../../../_static/img/run-on-anyscale.svg)](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=dolly_lightning_fsdp_finetuning)
  

In this example, we demonstrate how to use Ray Train to fine-tune a [`dolly-v2-7b`](https://huggingface.co/databricks/dolly-v2-7b) model. `dolly-v2-7b` is a 7 billion parameter causal language model created by Databricks, derived from EleutherAI’s [Pythia-6.9b](https://huggingface.co/EleutherAI/pythia-6.9b), and fine-tuned on a [~15K record instruction corpus](https://github.com/databrickslabs/dolly/tree/master/data).

We load the pre-trained model from the HuggingFace model hub into a LightningModule and launch an FSDP fine-tuning job across 16 T4 GPUs with the help of [`Ray TorchTrainer`](../../api/doc/ray.train.torch.TorchTrainer.html#ray.train.torch.TorchTrainer "ray.train.torch.TorchTrainer"). It is also straightforward to fine-tune other similar large language models in a similar manner as shown in this example.

Before starting this example, we highly recommend reading [Ray Train Key Concepts](../../overview.html#train-key-concepts) and [Ray Data Quickstart](../../../data/quickstart.html#data-quickstart).

In this , we demonstrate how to use Ray Train to fine-tune a [`dolly-v2-7b`](https://huggingface.co/databricks/dolly-v2-7b) model. `dolly-v2-7b` is a 7 billion parameter causal language model created by Databricks, derived from EleutherAI’s [Pythia-6.9b](https://huggingface.co/EleutherAI/pythia-6.9b), and fine-tuned on a [~15K record instruction corpus](https://github.com/databrickslabs/dolly/tree/master/data).

We load the pre-trained model from the HuggingFace model hub into a LightningModule and launch an FSDP fine-tuning job across 16 T4 GPUs with the help of [`Ray TorchTrainer`](../../api/doc/ray.train.torch.TorchTrainer.html#ray.train.torch.TorchTrainer "ray.train.torch.TorchTrainer"). It is also straightforward to fine-tune other similar large language models in a similar manner as shown in this example.

Before starting this example, we highly recommend reading [Ray Train Key Concepts](../../overview.html#train-key-concepts) and [Ray Data Quickstart](../../../data/quickstart.html#data-quickstart).

## Set up ray cluster[#](#set-up-ray-cluster "Link to this heading")

In this example, we are using a Ray cluster with a `m5.2xlarge` head node and 4 `g4dn.12xlarge` worker nodes. Each `g4dn.12xlarge has four Tesla T4 GPUs.

```
import ray
ray.init()
```

We then install the necessary dependencies on each node:

```
%%bash
pip install datasets
pip install evaluate
pip install "transformers>=4.26.0"
pip install "torch>=1.12.0"
pip install "lightning>=2.0"
pip install "pydantic>=2,<3"
```

```
MODEL_NAME = "databricks/dolly-v2-7b"
```

## Prepare your data[#](#prepare-your-data "Link to this heading")

We are using tiny\_shakespeare for fine-tuning, which contains 40,000 lines of Shakespeare from a variety of Shakespeare’s plays. Featured in Andrej Karpathy’s blog post [‘The Unreasonable Effectiveness of Recurrent Neural Networks’](http://karpathy.github.io/2015/05/21/rnn-effectiveness/).

Dataset samples:

```
BAPTISTA:
I know him well: you are welcome for his sake.

GREMIO:
Saving your tale, Petruchio, I pray,
Let us, that are poor petitioners, speak too:
Baccare! you are marvellous forward.

PETRUCHIO:
O, pardon me, Signior Gremio; I would fain be doing.
```

Here, we have adopted similar pre-processing logic from another demo: [GPT-J-6B Fine-Tuning with Ray Train and DeepSpeed](../deepspeed/gptj_deepspeed_fine_tuning.html).

```
import ray
import pandas as pd
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM

def split_text(batch: pd.DataFrame) -> pd.DataFrame:
    text = list(batch["text"])
    flat_text = "".join(text)
    split_text = [
        x.strip()
        for x in flat_text.split("\n")
        if x.strip() and not x.strip()[-1] == ":"
    ]
    return pd.DataFrame(split_text, columns=["text"])


def tokenize(batch: pd.DataFrame) -> dict:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, padding_side="left")
    tokenizer.pad_token = tokenizer.eos_token
    ret = tokenizer(
        list(batch["text"]),
        truncation=True,
        max_length=256,
        padding="max_length",
        return_tensors="np",
    )
    ret["labels"] = ret["input_ids"].copy()
    return dict(ret)

hf_dataset = load_dataset("tiny_shakespeare", trust_remote_code=True)
train_ds = ray.data.from_huggingface(hf_dataset["train"])
```

We first split the original paragraphs into multiple sentences, then tokenize them. Here are some samples:

```
# First split the dataset into multiple sentences.
train_ds = train_ds.map_batches(split_text, batch_format="pandas")
train_ds.take(10)
```

```
# Then tokenize the dataset.
train_ds = train_ds.map_batches(tokenize, batch_format="pandas")
```

## Define your lightning model[#](#define-your-lightning-model "Link to this heading")

In this example, we use the [dolly-v2-7b](https://huggingface.co/databricks/dolly-v2-7b) model for finetuning. It is an instruction-following large language model trained on the Databricks machine learning platform that is licensed for commercial use. We load the model weights from Huggingface Model Hub and encapsulate it into a `pl.LightningModule`.

Note

Make sure you pass the FSDP wrapped model parameters `self.trainer.model.parameters()` into the optimizer, instead of `self.model.parameters()`.

```
import torch
import lightning.pytorch as pl

class DollyV2Model(pl.LightningModule):
    def __init__(self, lr=2e-5, eps=1e-8):
        super().__init__()
        self.save_hyperparameters()
        self.lr = lr
        self.eps = eps
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    def forward(self, batch):
        outputs = self.model(
            batch["input_ids"], 
            attention_mask=batch["attention_mask"], 
            labels=batch["labels"]
        )
        return outputs.loss

    def training_step(self, batch, batch_idx):
        loss = self.forward(batch)
        self.log("train_loss", loss, prog_bar=True, on_step=True)
        return loss

    def configure_optimizers(self):
        if self.global_rank == 0:
            print(self.trainer.model)
        return torch.optim.AdamW(self.trainer.model.parameters(), lr=self.lr, eps=self.eps)
```

## Configure your FSDP strategy[#](#configure-your-fsdp-strategy "Link to this heading")

As `dolly-v2-7b` is a relatively large model, it cannot be properly fit into a single commercial GPU. In this example, we use the FSDP strategy to shard model parameters across multiple workers. This allows us to avoid GPU out-of-memory issues and support a larger global batch size.

![](https://user-images.githubusercontent.com/26745457/236892936-d4b91751-4689-421e-ac5f-edfd2eeeb635.png)
Image source: [Fully Sharded Data Parallel: faster AI training with fewer GPUs](https://engineering.fb.com/2021/07/15/open-source/fsdp/)

Note

FSDP is a type of data parallelism that shards model parameters, optimizer states and gradients across DDP ranks. This was inspired by Xu et al. as well as the ZeRO Stage 3 from DeepSpeed. You may refer to these blogs for more information:

* [Fully Sharded Data Parallel: faster AI training with fewer GPUs](https://engineering.fb.com/2021/07/15/open-source/fsdp/)
* [Getting Started with Fully Sharded Data Parallel(FSDP)](https://pytorch.org/tutorials/intermediate/FSDP_tutorial.html#:~:text=FSDP%20is%20a%20type%20of,sizes%20for%20our%20training%20job.)
* [PyTorch FSDP Tutorial](https://www.youtube.com/watch?v=8_k76AHu__s&amp;list=PL_lsbAsL_o2BT6aerEKgIoufVD_fodnuT)

To start training with Lightning’s [FSDPStrategy](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.strategies.FSDPStrategy.html#lightning.pytorch.strategies.FSDPStrategy), you only need to create a [`RayFSDPStrategy`](../../api/doc/ray.train.lightning.RayFSDPStrategy.html#ray.train.lightning.RayFSDPStrategy "ray.train.lightning.RayFSDPStrategy") with the same initialization arguments.

```
import functools
import lightning.pytorch as pl 

from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
from torch.distributed.fsdp import ShardingStrategy, BackwardPrefetch
from transformers.models.gpt_neox.modeling_gpt_neox import GPTNeoXLayer

from ray.train.lightning import RayFSDPStrategy


# Define the model sharding policy:
# Wrap every GPTNeoXLayer as its own FSDP instance
auto_wrap_policy = functools.partial(
    transformer_auto_wrap_policy,
    transformer_layer_cls = {GPTNeoXLayer}
)

fsdp_strategy = RayFSDPStrategy(
    sharding_strategy=ShardingStrategy.FULL_SHARD,
    backward_prefetch=BackwardPrefetch.BACKWARD_PRE,
    forward_prefetch=True,
    auto_wrap_policy=auto_wrap_policy,
    limit_all_gathers=True,
    activation_checkpointing=[GPTNeoXLayer],
    cpu_offload=True
)
```

Tip

Some tips for FSDP configuration:

* `sharding_strategy`:

  + `ShardingStrategy.NO_SHARD`: Parameters, gradients, and optimizer states are not sharded. Similar to DDP.
  + `ShardingStrategy.SHARD_GRAD_OP`: Gradients and optimizer states are sharded during computation, and additionally, parameters are sharded outside computation. Similar to ZeRO stage-2.
  + `ShardingStrategy.FULL_SHARD`: Parameters, gradients, and optimizer states are sharded. It has minimal GRAM usage among the 3 options. Similar to ZeRO stage-3.
* `auto_wrap_policy`:

  + Model layers are often wrapped with FSDP in a layered fashion. This means that only the layers in a single FSDP instance are required to aggregate all parameters to a single device during forwarding or backward calculations.
  + Use `transformer_auto_wrap_policy` to automatically wrap each Transformer Block into a single FSDP instance.
* `backward_prefetch` and `forward_prefetch`:

  + Overlap the upcoming all-gather while executing the current forward/backward pass. It can improve throughput but may slightly increase peak memory usage.

## Fine-tune with Ray TorchTrainer[#](#fine-tune-with-ray-torchtrainer "Link to this heading")

Ray TorchTrainer allows you to scale your PyTorch Lightning training workload over multiple nodes. See [Configuring Scale and GPUs](../../user-guides/using-gpus.html#train-scaling-config) for more details.

```
num_workers = 16
batch_size_per_worker = 5
```

Additionally, remember to define a Lightning callback that saves and reports checkpoints. Ray Train offers a simple implementation, [`RayTrainReportCallback()`](../../api/doc/ray.train.lightning.RayTrainReportCallback.html#ray.train.lightning.RayTrainReportCallback "ray.train.lightning.RayTrainReportCallback"), which persists your checkpoint and metrics in remote storage at the end of each training epoch.

Note you can also implement your own report callback with customized logics, such as saving customized checkpoint files or reporting at a different frequency.

```
from ray.train import Checkpoint
from ray.train.lightning import RayLightningEnvironment, RayTrainReportCallback, prepare_trainer

# Training function for each worker
def train_func(config):
    lr = config["lr"]
    eps = config["eps"]
    strategy = config["strategy"]
    batch_size_per_worker = config["batch_size_per_worker"]

    # Model
    model = DollyV2Model(lr=lr, eps=eps)

    # Ray Data Ingestion
    train_ds = ray.train.get_dataset_shard("train")
    train_dataloader = train_ds.iter_torch_batches(batch_size=batch_size_per_worker)

    # Lightning Trainer
    trainer = pl.Trainer(
        max_epochs=1, 
        devices="auto",
        accelerator="auto", 
        precision="16-mixed",
        strategy=strategy,
        plugins=[RayLightningEnvironment()],
        callbacks=[RayTrainReportCallback()],
        enable_checkpointing=False,
    )

    trainer = prepare_trainer(trainer)

    trainer.fit(model, train_dataloaders=train_dataloader)
```

Note

Since this example runs with multiple nodes, we need to persist checkpoints
and other outputs to some external storage for access after training has completed.
**You should set up cloud storage or NFS, then replace `storage_path` with your own cloud bucket URI or NFS path.**

See the [storage guide](../../../tune/tutorials/tune-storage.html#tune-storage-options) for more details.

```
storage_path="s3://your-bucket-here"  # TODO: Set up cloud storage
# storage_path="/mnt/path/to/nfs"     # TODO: Alternatively, set up NFS
```

```
from ray.train.torch import TorchTrainer
from ray.train import RunConfig, ScalingConfig, CheckpointConfig

# Save Ray Train checkpoints according to the performance on validation set
run_config = RunConfig(
    name="finetune_dolly-v2-7b-trial1",
    storage_path=storage_path,
    checkpoint_config=CheckpointConfig(num_to_keep=1),
)

# Scale the FSDP training workload across 16 GPUs
# You can change this config based on your compute resources.
scaling_config = ScalingConfig(
    num_workers=num_workers, use_gpu=True
)

# Configuration to pass into train_func
train_config = {
    "lr": 2e-5,
    "eps": 1e-8,
    "strategy": fsdp_strategy,
    "batch_size_per_worker": batch_size_per_worker
}

# Define a TorchTrainer and launch you training workload
ray_trainer = TorchTrainer(
    train_func,
    train_loop_config=train_config,
    run_config=run_config,
    scaling_config=scaling_config,
    datasets={"train": train_ds},
)
result = ray_trainer.fit()

result
```

```
(TrainController pid=6878) /home/ray/anaconda3/lib/python3.10/site-packages/transformers/utils/generic.py:441: UserWarning: torch.utils._pytree._register_pytree_node is deprecated. Please use torch.utils._pytree.register_pytree_node instead.
(TrainController pid=6878)   _torch_pytree._register_pytree_node(
(TrainController pid=6878) /home/ray/anaconda3/lib/python3.10/site-packages/transformers/utils/generic.py:309: UserWarning: torch.utils._pytree._register_pytree_node is deprecated. Please use torch.utils._pytree.register_pytree_node instead.
(TrainController pid=6878)   _torch_pytree._register_pytree_node(
(TrainController pid=6878) [State Transition] INITIALIZING -> SCHEDULING.
(TrainController pid=6878) Attempting to start training worker group of size 16 with the following resources: [{'GPU': 1}] * 16
(RayTrainWorker pid=4349, ip=10.0.157.249) /home/ray/anaconda3/lib/python3.10/site-packages/transformers/utils/generic.py:441: UserWarning: torch.utils._pytree._register_pytree_node is deprecated. Please use torch.utils._pytree.register_pytree_node instead.
(RayTrainWorker pid=4349, ip=10.0.157.249)   _torch_pytree._register_pytree_node(
(RayTrainWorker pid=4350, ip=10.0.157.249) /home/ray/anaconda3/lib/python3.10/site-packages/transformers/utils/generic.py:441: UserWarning: torch.utils._pytree._register_pytree_node is deprecated. Please use torch.utils._pytree.register_pytree_node instead.
(RayTrainWorker pid=4350, ip=10.0.157.249)   _torch_pytree._register_pytree_node(
(RayTrainWorker pid=4088, ip=10.0.163.141) Setting up process group for: env:// [rank=0, world_size=16]
(RayTrainWorker pid=4349, ip=10.0.157.249) /home/ray/anaconda3/lib/python3.10/site-packages/huggingface_hub/file_download.py:795: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
(RayTrainWorker pid=4349, ip=10.0.157.249)   warnings.warn(
(TrainController pid=6878) Started training worker group of size 16: 
(TrainController pid=6878) - (ip=10.0.163.141, pid=4088) world_rank=0, local_rank=0, node_rank=0
(TrainController pid=6878) - (ip=10.0.163.141, pid=4089) world_rank=1, local_rank=1, node_rank=0
(TrainController pid=6878) - (ip=10.0.163.141, pid=4090) world_rank=2, local_rank=2, node_rank=0
(TrainController pid=6878) - (ip=10.0.163.141, pid=4091) world_rank=3, local_rank=3, node_rank=0
(TrainController pid=6878) - (ip=10.0.166.248, pid=4338) world_rank=4, local_rank=0, node_rank=1
(TrainController pid=6878) - (ip=10.0.166.248, pid=4337) world_rank=5, local_rank=1, node_rank=1
(TrainController pid=6878) - (ip=10.0.166.248, pid=4340) world_rank=6, local_rank=2, node_rank=1
(TrainController pid=6878) - (ip=10.0.166.248, pid=4339) world_rank=7, local_rank=3, node_rank=1
(TrainController pid=6878) - (ip=10.0.191.43, pid=4090) world_rank=8, local_rank=0, node_rank=2
(TrainController pid=6878) - (ip=10.0.191.43, pid=4248) world_rank=9, local_rank=1, node_rank=2
(TrainController pid=6878) - (ip=10.0.191.43, pid=4246) world_rank=10, local_rank=2, node_rank=2
(TrainController pid=6878) - (ip=10.0.191.43, pid=4247) world_rank=11, local_rank=3, node_rank=2
(TrainController pid=6878) - (ip=10.0.157.249, pid=4349) world_rank=12, local_rank=0, node_rank=3
(TrainController pid=6878) - (ip=10.0.157.249, pid=4350) world_rank=13, local_rank=1, node_rank=3
(TrainController pid=6878) - (ip=10.0.157.249, pid=4347) world_rank=14, local_rank=2, node_rank=3
(TrainController pid=6878) - (ip=10.0.157.249, pid=4348) world_rank=15, local_rank=3, node_rank=3
(TrainController pid=6878) [State Transition] SCHEDULING -> RUNNING.
(RayTrainWorker pid=4246, ip=10.0.191.43) /home/ray/anaconda3/lib/python3.10/site-packages/transformers/utils/generic.py:309: UserWarning: torch.utils._pytree._register_pytree_node is deprecated. Please use torch.utils._pytree.register_pytree_node instead. [repeated 31x across cluster] (Ray deduplicates logs by default. Set RAY_DEDUP_LOGS=0 to disable log deduplication, or see https://docs.ray.io/en/master/ray-observability/user-guides/configure-logging.html#log-deduplication for more options.)
(RayTrainWorker pid=4246, ip=10.0.191.43)   _torch_pytree._register_pytree_node( [repeated 31x across cluster]
```

```
(raylet) WARNING: 4 PYTHON worker processes have been started on node: 3ffdd02cd1be6b69a64a97e08f75fc0a80eddcf0caa627f3f4266c95 with address: 10.0.150.21. This could be a result of using a large number of actors, or due to tasks blocked in ray.get() calls (see https://github.com/ray-project/ray/issues/3644 for some discussion of workarounds).
```

```
(RayTrainWorker pid=4088, ip=10.0.163.141) GPU available: True (cuda), used: True
(RayTrainWorker pid=4088, ip=10.0.163.141) TPU available: False, using: 0 TPU cores
(RayTrainWorker pid=4088, ip=10.0.163.141) HPU available: False, using: 0 HPUs
(RayTrainWorker pid=4246, ip=10.0.191.43) /home/ray/anaconda3/lib/python3.10/site-packages/huggingface_hub/file_download.py:795: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`. [repeated 15x across cluster]
(RayTrainWorker pid=4246, ip=10.0.191.43)   warnings.warn( [repeated 15x across cluster]
(RayTrainWorker pid=4088, ip=10.0.163.141) 2025-09-30 14:20:07.970624: I tensorflow/core/util/port.cc:113] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
(RayTrainWorker pid=4088, ip=10.0.163.141) 2025-09-30 14:20:08.208262: E external/local_xla/xla/stream_executor/cuda/cuda_dnn.cc:9261] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered
(RayTrainWorker pid=4088, ip=10.0.163.141) 2025-09-30 14:20:08.208291: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:607] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered
(RayTrainWorker pid=4088, ip=10.0.163.141) 2025-09-30 14:20:08.231782: E external/local_xla/xla/stream_executor/cuda/cuda_blas.cc:1515] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered
(RayTrainWorker pid=4088, ip=10.0.163.141) 2025-09-30 14:20:08.277889: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
(RayTrainWorker pid=4088, ip=10.0.163.141) To enable the following instructions: AVX2 AVX512F AVX512_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
(SplitCoordinator pid=7661) /home/ray/anaconda3/lib/python3.10/site-packages/transformers/utils/generic.py:441: UserWarning: torch.utils._pytree._register_pytree_node is deprecated. Please use torch.utils._pytree.register_pytree_node instead.
(SplitCoordinator pid=7661)   _torch_pytree._register_pytree_node(
(RayTrainWorker pid=4088, ip=10.0.163.141) 2025-09-30 14:20:10.134645: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:38] TF-TRT Warning: Could not find TensorRT
(RayTrainWorker pid=4088, ip=10.0.163.141) LOCAL_RANK: 0 - CUDA_VISIBLE_DEVICES: [0,1,2,3]
(RayTrainWorker pid=4088, ip=10.0.163.141) FullyShardedDataParallel(
(RayTrainWorker pid=4088, ip=10.0.163.141)   (_fsdp_wrapped_module): DollyV2Model(
(RayTrainWorker pid=4088, ip=10.0.163.141)     (model): GPTNeoXForCausalLM(
(RayTrainWorker pid=4088, ip=10.0.163.141)       (gpt_neox): GPTNeoXModel(
(RayTrainWorker pid=4088, ip=10.0.163.141)         (embed_in): Embedding(50280, 4096)
(RayTrainWorker pid=4088, ip=10.0.163.141)         (emb_dropout): Dropout(p=0.0, inplace=False)
(RayTrainWorker pid=4088, ip=10.0.163.141)         (layers): ModuleList(
(RayTrainWorker pid=4088, ip=10.0.163.141)           (0-31): 32 x FullyShardedDataParallel(
(RayTrainWorker pid=4088, ip=10.0.163.141)             (_fsdp_wrapped_module): CheckpointWrapper(
(RayTrainWorker pid=4088, ip=10.0.163.141)               (_checkpoint_wrapped_module): GPTNeoXLayer(
(RayTrainWorker pid=4088, ip=10.0.163.141)                 (input_layernorm): LayerNorm((4096,), eps=1e-05, elementwise_affine=True)
(RayTrainWorker pid=4088, ip=10.0.163.141)                 (post_attention_layernorm): LayerNorm((4096,), eps=1e-05, elementwise_affine=True)
(RayTrainWorker pid=4088, ip=10.0.163.141)                 (post_attention_dropout): Dropout(p=0.0, inplace=False)
(RayTrainWorker pid=4088, ip=10.0.163.141)                 (post_mlp_dropout): Dropout(p=0.0, inplace=False)
(RayTrainWorker pid=4088, ip=10.0.163.141)                 (attention): GPTNeoXAttention(
(RayTrainWorker pid=4088, ip=10.0.163.141)                   (rotary_emb): GPTNeoXRotaryEmbedding()
(RayTrainWorker pid=4088, ip=10.0.163.141)                   (query_key_value): Linear(in_features=4096, out_features=12288, bias=True)
(RayTrainWorker pid=4088, ip=10.0.163.141)                   (dense): Linear(in_features=4096, out_features=4096, bias=True)
(RayTrainWorker pid=4088, ip=10.0.163.141)                   (attention_dropout): Dropout(p=0.0, inplace=False)
(RayTrainWorker pid=4088, ip=10.0.163.141)                 )
(RayTrainWorker pid=4088, ip=10.0.163.141)                 (mlp): GPTNeoXMLP(
(RayTrainWorker pid=4088, ip=10.0.163.141)                   (dense_h_to_4h): Linear(in_features=4096, out_features=16384, bias=True)
(RayTrainWorker pid=4088, ip=10.0.163.141)                   (dense_4h_to_h): Linear(in_features=16384, out_features=4096, bias=True)
(RayTrainWorker pid=4088, ip=10.0.163.141)                   (act): GELUActivation()
(RayTrainWorker pid=4088, ip=10.0.163.141)                 )
(RayTrainWorker pid=4088, ip=10.0.163.141)               )
(RayTrainWorker pid=4088, ip=10.0.163.141)             )
(RayTrainWorker pid=4088, ip=10.0.163.141)           )
(RayTrainWorker pid=4088, ip=10.0.163.141)         )
(RayTrainWorker pid=4088, ip=10.0.163.141)         (final_layer_norm): LayerNorm((4096,), eps=1e-05, elementwise_affine=True)
(RayTrainWorker pid=4088, ip=10.0.163.141)       )
(RayTrainWorker pid=4088, ip=10.0.163.141)       (embed_out): Linear(in_features=4096, out_features=50280, bias=False)
(RayTrainWorker pid=4088, ip=10.0.163.141)     )
(RayTrainWorker pid=4088, ip=10.0.163.141)   )
(RayTrainWorker pid=4088, ip=10.0.163.141) )
(RayTrainWorker pid=4088, ip=10.0.163.141) /tmp/ray/session_2025-09-30_14-10-46_627006_2395/runtime_resources/pip/72a6e451f55d87eb50ebbf5bc30a4a57ed513d34/virtualenv/lib/python3.10/site-packages/lightning/pytorch/utilities/model_summary/model_summary.py:231: Precision 16-mixed is not supported by the model summary.  Estimated model size in MB will not be accurate. Using 32 bits instead.
(RayTrainWorker pid=4088, ip=10.0.163.141) 
(RayTrainWorker pid=4088, ip=10.0.163.141)   | Name  | Type               | Params | Mode
(RayTrainWorker pid=4088, ip=10.0.163.141) ----------------------------------------------------
(RayTrainWorker pid=4088, ip=10.0.163.141) 0 | model | GPTNeoXForCausalLM | 428 M  | eval
(RayTrainWorker pid=4088, ip=10.0.163.141) ----------------------------------------------------
(RayTrainWorker pid=4088, ip=10.0.163.141) 428 M     Trainable params
(RayTrainWorker pid=4088, ip=10.0.163.141) 0         Non-trainable params
(RayTrainWorker pid=4088, ip=10.0.163.141) 428 M     Total params
(RayTrainWorker pid=4088, ip=10.0.163.141) 1,714.014 Total estimated model params size (MB)
(RayTrainWorker pid=4088, ip=10.0.163.141) 64        Modules in train mode
(RayTrainWorker pid=4088, ip=10.0.163.141) 455       Modules in eval mode
(RayTrainWorker pid=4246, ip=10.0.191.43) LOCAL_RANK: 2 - CUDA_VISIBLE_DEVICES: [0,1,2,3] [repeated 15x across cluster]
(SplitCoordinator pid=7661) Registered dataset logger for dataset train_12_0
(SplitCoordinator pid=7661) Starting execution of Dataset train_12_0. Full logs are in /tmp/ray/session_2025-09-30_14-10-46_627006_2395/logs/ray-data
(SplitCoordinator pid=7661) Execution plan of Dataset train_12_0: InputDataBuffer[Input] -> TaskPoolMapOperator[MapBatches(split_text)->MapBatches(tokenize)] -> LimitOperator[limit=400] -> OutputSplitter[split(16, equal=True)]
(SplitCoordinator pid=7661) ⚠️  Ray's object store is configured to use only 28.7% of available memory (229.3GiB out of 800.0GiB total). For optimal Ray Data performance, we recommend setting the object store to at least 50% of available memory. You can do this by setting the 'object_store_memory' parameter when calling ray.init() or by setting the RAY_DEFAULT_OBJECT_STORE_MEMORY_PROPORTION environment variable.
```

```
(MapBatches(split_text)->MapBatches(tokenize) pid=4089, ip=10.0.191.43) /home/ray/anaconda3/lib/python3.10/site-packages/transformers/utils/generic.py:441: UserWarning: torch.utils._pytree._register_pytree_node is deprecated. Please use torch.utils._pytree.register_pytree_node instead.
(MapBatches(split_text)->MapBatches(tokenize) pid=4089, ip=10.0.191.43)   _torch_pytree._register_pytree_node(
(MapBatches(split_text)->MapBatches(tokenize) pid=4089, ip=10.0.191.43) /home/ray/anaconda3/lib/python3.10/site-packages/huggingface_hub/file_download.py:795: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
(MapBatches(split_text)->MapBatches(tokenize) pid=4089, ip=10.0.191.43)   warnings.warn(
(MapBatches(split_text)->MapBatches(tokenize) pid=4089, ip=10.0.191.43) Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.
(SplitCoordinator pid=7661) /home/ray/anaconda3/lib/python3.10/site-packages/ray/anyscale/data/_internal/cluster_autoscaler/productivity_calculator.py:174: RuntimeWarning: invalid value encountered in divide
(SplitCoordinator pid=7661)   gpu_fraction_per_op = (optimal_num_tasks_per_op * num_gpus_per_op) / np.sum(
(SplitCoordinator pid=7661) ✔️  Dataset train_12_0 execution finished in 5.10 seconds
(RayTrainWorker pid=4088, ip=10.0.163.141) /tmp/ray/session_2025-09-30_14-10-46_627006_2395/runtime_resources/pip/72a6e451f55d87eb50ebbf5bc30a4a57ed513d34/virtualenv/lib/python3.10/site-packages/lightning/pytorch/loops/fit_loop.py:527: Found 455 module(s) in eval mode at the start of training. This may lead to unexpected behavior during training. If this is intentional, you can ignore this warning.
```

```
Epoch 0: |          | 0/? [00:00<?, ?it/s] 141) 
Epoch 0: |          | 1/? [00:20<00:00,  0.05it/s, v_num=0, train_loss=14.60]
Epoch 0: |          | 2/? [00:36<00:00,  0.06it/s, v_num=0, train_loss=13.90]
Epoch 0: |          | 3/? [00:52<00:00,  0.06it/s, v_num=0, train_loss=14.80]
Epoch 0: |          | 4/? [01:09<00:00,  0.06it/s, v_num=0, train_loss=14.10]
Epoch 0: |          | 5/? [01:27<00:00,  0.06it/s, v_num=0, train_loss=14.90]
```

```
(RayTrainWorker pid=4090, ip=10.0.191.43) Checkpoint successfully created at: Checkpoint(filesystem=local, path=/mnt/cluster_storage/finetune_dolly-v2-7b-trial1/checkpoint_2025-09-30_14-23-45.998076)
(RayTrainWorker pid=4090, ip=10.0.191.43) Reporting training result 1: TrainingResult(checkpoint=Checkpoint(filesystem=local, path=/mnt/cluster_storage/finetune_dolly-v2-7b-trial1/checkpoint_2025-09-30_14-23-45.998076), metrics={'train_loss': 14.9804105758667, 'epoch': 0, 'step': 5})
(RayTrainWorker pid=4088, ip=10.0.163.141) Checkpoint successfully created at: Checkpoint(filesystem=local, path=/mnt/cluster_storage/finetune_dolly-v2-7b-trial1/checkpoint_2025-09-30_14-23-45.998076) [repeated 12x across cluster]
(RayTrainWorker pid=4088, ip=10.0.163.141) Reporting training result 1: TrainingResult(checkpoint=Checkpoint(filesystem=local, path=/mnt/cluster_storage/finetune_dolly-v2-7b-trial1/checkpoint_2025-09-30_14-23-45.998076), metrics={'train_loss': 14.879826545715332, 'epoch': 0, 'step': 5}) [repeated 12x across cluster]
(RayTrainWorker pid=4088, ip=10.0.163.141) `Trainer.fit` stopped: `max_epochs=1` reached.
```

```
Epoch 0: |          | 5/? [06:07<00:00,  0.01it/s, v_num=0, train_loss=14.90]
```

```
Result(metrics={'train_loss': 14.879826545715332, 'epoch': 0, 'step': 5}, checkpoint=Checkpoint(filesystem=local, path=/mnt/cluster_storage/finetune_dolly-v2-7b-trial1/checkpoint_2025-09-30_14-23-45.998076), error=None, path='/mnt/cluster_storage/finetune_dolly-v2-7b-trial1', metrics_dataframe=   train_loss  epoch  step
0   14.879827      0     5, best_checkpoints=[(Checkpoint(filesystem=local, path=/mnt/cluster_storage/finetune_dolly-v2-7b-trial1/checkpoint_2025-09-30_14-23-45.998076), {'train_loss': 14.879826545715332, 'epoch': 0, 'step': 5})], _storage_filesystem=<pyarrow._fs.LocalFileSystem object at 0x737af20de5b0>)
```

We finished training in 2877s. The price for an on-demand g4dn.4xlarge instance is `$1.204/hour`, while a g4dn.8xlarge instance costs `$2.176/hour`. The total cost would be `($1.204 * 15 + $2.176) * 2877 / 3600 = $16.17`.

## Text-generation with HuggingFace Pipeline[#](#text-generation-with-huggingface-pipeline "Link to this heading")

We can use the [HuggingFace Pipeline](https://huggingface.co/docs/transformers/main_classes/pipelines) to generate predictions from our fine-tuned model. Let’s input some prompts and see if our tuned Dolly can speak like Shakespeare:

```
import os
from transformers import pipeline

@ray.remote(num_gpus=1)
def generate_tokens():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, padding_side="right")

    ckpt_path = os.path.join(result.checkpoint.path, "checkpoint.ckpt")

    dolly = DollyV2Model.load_from_checkpoint(ckpt_path, map_location=torch.device("cpu"))

    nlp_pipeline = pipeline(
        task="text-generation", 
        model=dolly.model, 
        tokenizer=tokenizer, 
        device_map="auto"
    )

    tokens = []
    for prompt in ["This is", "I am", "Once more"]:
        tokens.append(nlp_pipeline(prompt, max_new_tokens=20, do_sample=True, pad_token_id=tokenizer.eos_token_id))

    return tokens

ref = generate_tokens.remote()
output = ray.get(ref)
```

```
for generated_tokens in output:
    print(generated_tokens)
```

```
[{'generated_text': "This is more like it:\n\nIt's just a guess, but maybe the extra processing power of Intel"}]
[{'generated_text': "I am the biggest fan of your wife's writing, and this novella was fantastic. So interesting to see"}]
[{'generated_text': 'Once more I wish I could make sense of it." "My friend, you can leave all this behind you'}]
```

References:

* [PyTorch FSDP Tutorial](https://www.youtube.com/watch?v=8_k76AHu__s&amp;list=PL_lsbAsL_o2BT6aerEKgIoufVD_fodnuT)
* [Getting Started with Fully Sharded Data Parallel(FSDP)](https://pytorch.org/tutorials/intermediate/FSDP_tutorial.html#:~:text=FSDP%20is%20a%20type%20of,sizes%20for%20our%20training%20job.)
* [Fully Sharded Data Parallel: faster AI training with fewer GPUs](https://engineering.fb.com/2021/07/15/open-source/fsdp/)
* [Hugging Face: dolly-v2-7b Model Card](https://huggingface.co/databricks/dolly-v2-7b)
* [Hugging Face: Handling big models for inference](https://huggingface.co/docs/accelerate/usage_guides/big_modeling)

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/train/examples/lightning/dolly_lightning_fsdp_finetuning.ipynb)