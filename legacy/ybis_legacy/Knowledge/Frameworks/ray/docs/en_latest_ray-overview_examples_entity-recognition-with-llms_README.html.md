LLM training and inference — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# LLM training and inference[#](#llm-training-and-inference "Link to this heading")

[![\"Run](https://raw.githubusercontent.com/ray-project/ray/c34b74c22a9390aa89baf80815ede59397786d2e/doc/source/_static/img/run-on-anyscale.svg)](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=entity-recognition-with-llms&redirectTo=/v2/template-preview/entity-recognition-with-llms\)
  

[![](https://img.shields.io/static/v1?label=&message=View%20On%20GitHub&color=586069&logo=github&labelColor=2f363d)](https://github.com/anyscale/e2e-llm-workflows)

This end-to-end tutorial **fine-tunes** an LLM to perform **batch inference** and **online serving** at scale. While entity recognition (NER) is the main task in this tutorial, you can easily extend these end-to-end workflows to any use case.

[![https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/e2e_llm.png](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/e2e_llm.png)](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/e2e_llm.png)

**Note**: The intent of this tutorial is to show how you can use Ray to implement end-to-end LLM workflows that can extend to any use case, including multimodal.

This tutorial uses the [Ray library](https://github.com/ray-project/ray) to implement these workflows, namely the LLM APIs:

[`ray.data.llm`](https://docs.ray.io/en/latest/data/working-with-llms.html):

* Batch inference over distributed datasets
* Streaming and async execution for throughput
* Built-in metrics and tracing, including observability
* Zero-copy GPU data transfer
* Composable with preprocessing and postprocessing steps

[`ray.serve.llm`](https://docs.ray.io/en/latest/serve/llm/serving-llms.html):

* Automatic scaling and load balancing
* Unified multi-node multi-model deployment
* Multi-LoRA support with shared base models
* Deep integration with inference engines, vLLM to start
* Composable multi-model LLM pipelines

And all of these workloads come with all the observability views you need to debug and tune them to **maximize throughput/latency**.

## Set up[#](#set-up "Link to this heading")

### Compute[#](#compute "Link to this heading")

This [Anyscale Workspace](https://docs.anyscale.com/platform/workspaces/) automatically provisions and autoscales the compute your workloads need. If you’re not on Anyscale, then you need to provision the appropriate compute (L4) for this tutorial.

[![https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/compute.png](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/compute.png)](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/compute.png)

### Dependencies[#](#dependencies "Link to this heading")

Start by downloading the dependencies required for this tutorial. Notice in your [`containerfile`](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/containerfile) you have a base image [`anyscale/ray-llm:latest-py311-cu124`](https://hub.docker.com/layers/anyscale/ray-llm/latest-py311-cu124/images/sha256-5a1c55f7f416d2d2eb5f4cdd13afeda25d4f7383406cfee1f1f60da495d1b50f) followed by a list of pip packages. If you’re not on [Anyscale](https://console.anyscale.com/), you can pull this Docker image yourself and install the dependencies.

```
%%bash
# Install dependencies
pip install -q \
    "xgrammar==0.1.11" \
    "pynvml==12.0.0" \
    "hf_transfer==0.1.9" \
    "tensorboard==2.19.0" \
    "llamafactory@git+https://github.com/hiyouga/LLaMA-Factory.git@ac8c6fdd3ab7fb6372f231f238e6b8ba6a17eb16#egg=llamafactory"
```

```
Successfully registered `ray, vllm` and 5 other packages to be installed on all cluster nodes.
View and update dependencies here: https://console.anyscale.com/cld_kvedZWag2qA8i5BjxUevf5i7/prj_cz951f43jjdybtzkx1s5sjgz99/workspaces/expwrk_mp8cxvgle2yeumgcpu1yua2r3e?workspace-tab=dependencies
```

## Data ingestion[#](#data-ingestion "Link to this heading")

```
import json
import textwrap
from IPython.display import Code, Image, display
```

Start by downloading the data from cloud storage to local shared storage.

```
%%bash
rm -rf /mnt/cluster_storage/viggo  # clean up
mkdir /mnt/cluster_storage/viggo
wget https://viggo-ds.s3.amazonaws.com/train.jsonl -O /mnt/cluster_storage/viggo/train.jsonl
wget https://viggo-ds.s3.amazonaws.com/val.jsonl -O /mnt/cluster_storage/viggo/val.jsonl
wget https://viggo-ds.s3.amazonaws.com/test.jsonl -O /mnt/cluster_storage/viggo/test.jsonl
wget https://viggo-ds.s3.amazonaws.com/dataset_info.json -O /mnt/cluster_storage/viggo/dataset_info.json
```

```
download: s3://viggo-ds/train.jsonl to ../../../mnt/cluster_storage/viggo/train.jsonl
download: s3://viggo-ds/val.jsonl to ../../../mnt/cluster_storage/viggo/val.jsonl
download: s3://viggo-ds/test.jsonl to ../../../mnt/cluster_storage/viggo/test.jsonl
download: s3://viggo-ds/dataset_info.json to ../../../mnt/cluster_storage/viggo/dataset_info.json
```

```
%%bash
head -n 1 /mnt/cluster_storage/viggo/train.jsonl | python3 -m json.tool
```

```
{
    "instruction": "Given a target sentence construct the underlying meaning representation of the input sentence as a single function with attributes and attribute values. This function should describe the target string accurately and the function must be one of the following ['inform', 'request', 'give_opinion', 'confirm', 'verify_attribute', 'suggest', 'request_explanation', 'recommend', 'request_attribute']. The attributes must be one of the following: ['name', 'exp_release_date', 'release_year', 'developer', 'esrb', 'rating', 'genres', 'player_perspective', 'has_multiplayer', 'platforms', 'available_on_steam', 'has_linux_release', 'has_mac_release', 'specifier']",
    "input": "Blizzard North is mostly an okay developer, but they released Diablo II for the Mac and so that pushes the game from okay to good in my view.",
    "output": "give_opinion(name[Diablo II], developer[Blizzard North], rating[good], has_mac_release[yes])"
}
```

```
with open("/mnt/cluster_storage/viggo/train.jsonl", "r") as fp:
    first_line = fp.readline()
    item = json.loads(first_line)
system_content = item["instruction"]
print(textwrap.fill(system_content, width=80))
```

```
Given a target sentence construct the underlying meaning representation of the
input sentence as a single function with attributes and attribute values. This
function should describe the target string accurately and the function must be
one of the following ['inform', 'request', 'give_opinion', 'confirm',
'verify_attribute', 'suggest', 'request_explanation', 'recommend',
'request_attribute']. The attributes must be one of the following: ['name',
'exp_release_date', 'release_year', 'developer', 'esrb', 'rating', 'genres',
'player_perspective', 'has_multiplayer', 'platforms', 'available_on_steam',
'has_linux_release', 'has_mac_release', 'specifier']
```

You also have an info file that identifies the datasets and format (Alpaca and ShareGPT formats) to use for post training.

```
display(Code(filename="/mnt/cluster_storage/viggo/dataset_info.json", language="json"))
```

```
{
    "viggo-train": {
        "file_name": "/mnt/cluster_storage/viggo/train.jsonl",
        "formatting": "alpaca",
        "columns": {
            "prompt": "instruction",
            "query": "input",
            "response": "output"
        }
    },
    "viggo-val": {
        "file_name": "/mnt/cluster_storage/viggo/val.jsonl",
        "formatting": "alpaca",
        "columns": {
            "prompt": "instruction",
            "query": "input",
            "response": "output"
        }
    }
}
```

## Distributed fine-tuning[#](#distributed-fine-tuning "Link to this heading")

Use [Ray Train](https://docs.ray.io/en/latest/train/train.html) + [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) to perform multi-node training. Find the parameters for the training workload, post-training method, dataset location, train/val details, etc. in the `llama3_lora_sft_ray.yaml` config file. See the recipes for even more post-training methods, like SFT, pretraining, PPO, DPO, KTO, etc. [on GitHub](https://github.com/hiyouga/LLaMA-Factory/tree/main/examples).

**Note**: Ray also supports using other tools like [axolotl](https://axolotl-ai-cloud.github.io/axolotl/docs/ray-integration.html) or even [Ray Train + HF Accelerate + FSDP/DeepSpeed](https://docs.ray.io/en/latest/train/huggingface-accelerate.html) directly for complete control of your post-training workloads.

[![https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/distributed_training.png](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/distributed_training.png)](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/distributed_training.png)

### `config`[#](#config "Link to this heading")

```
import os
from pathlib import Path
import yaml
```

```
display(Code(filename="lora_sft_ray.yaml", language="yaml"))
```

```
### model
model_name_or_path: Qwen/Qwen2.5-7B-Instruct
trust_remote_code: true

### method
stage: sft
do_train: true
finetuning_type: lora
lora_rank: 8
lora_target: all

### dataset
dataset: viggo-train
dataset_dir: /mnt/cluster_storage/viggo  # shared storage workers have access to
template: qwen
cutoff_len: 2048
max_samples: 1000
overwrite_cache: true
preprocessing_num_workers: 16
dataloader_num_workers: 4

### output
output_dir: /mnt/cluster_storage/viggo/outputs  # should be somewhere workers have access to (ex. s3, nfs)
logging_steps: 10
save_steps: 500
plot_loss: true
overwrite_output_dir: true
save_only_model: false

### ray
ray_run_name: lora_sft_ray
ray_storage_path: /mnt/cluster_storage/viggo/saves  # should be somewhere workers have access to (ex. s3, nfs)
ray_num_workers: 4
resources_per_worker:
  GPU: 1
  anyscale/accelerator_shape:4xL4: 0.001  # Use this to specify a specific node shape,
  # accelerator_type:L4: 1           # Or use this to simply specify a GPU type.
  # see https://docs.ray.io/en/master/ray-core/accelerator-types.html#accelerator-types for a full list of accelerator types
placement_strategy: PACK

### train
per_device_train_batch_size: 1
gradient_accumulation_steps: 8
learning_rate: 1.0e-4
num_train_epochs: 5.0
lr_scheduler_type: cosine
warmup_ratio: 0.1
bf16: true
ddp_timeout: 180000000
resume_from_checkpoint: null

### eval
eval_dataset: viggo-val  # uses same dataset_dir as training data
# val_size: 0.1  # only if using part of training data for validation
per_device_eval_batch_size: 1
eval_strategy: steps
eval_steps: 500
```

```
model_id = "ft-model"  # call it whatever you want
model_source = yaml.safe_load(open("lora_sft_ray.yaml"))["model_name_or_path"]  # HF model ID, S3 mirror config, or GCS mirror config
print (model_source)
```

```
Qwen/Qwen2.5-7B-Instruct
```

### Multi-node training[#](#multi-node-training "Link to this heading")

Use Ray Train + LlamaFactory to perform the mult-node train loop.

**Ray Train**

Using [Ray Train](https://docs.ray.io/en/latest/train/train.html) has several advantages:

* it automatically handles **multi-node, multi-GPU** setup with no manual SSH setup or `hostfile` configs.
* you can define **per-worker fractional resource requirements**, for example, 2 CPUs and 0.5 GPU per worker.
* you can run on **heterogeneous machines** and scale flexibly, for example, CPU for preprocessing and GPU for training.
* it has built-in **fault tolerance** through retry of failed workers, and continue from last checkpoint.
* it supports Data Parallel, Model Parallel, Parameter Server, and even custom strategies.
* [Ray Compiled graphs](https://docs.ray.io/en/latest/ray-core/compiled-graph/ray-compiled-graph.html) allow you to even define different parallelism for jointly optimizing multiple models. Megatron, DeepSpeed, and similar frameworks only allow for one global setting.

[RayTurbo Train](https://docs.anyscale.com/rayturbo/rayturbo-train) offers even more improvement to the price-performance ratio, performance monitoring, and more:

* **elastic training** to scale to a dynamic number of workers, and continue training on fewer resources, even on spot instances.
* **purpose-built dashboard** designed to streamline the debugging of Ray Train workloads:

  + Monitoring: View the status of training runs and train workers.
  + Metrics: See insights on training throughput and training system operation time.
  + Profiling: Investigate bottlenecks, hangs, or errors from individual training worker processes.

[![https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/train_dashboard.png](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/train_dashboard.png)](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/train_dashboard.png)

```
%%bash
# Run multi-node distributed fine-tuning workload
USE_RAY=1 llamafactory-cli train lora_sft_ray.yaml
```

```
Training started with configuration:
    ╭──────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ Training config                                                                                      │
    ├──────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │ train_loop_config/args/bf16                                                                     True │
    │ train_loop_config/args/cutoff_len                                                               2048 │
    │ train_loop_config/args/dataloader_num_workers                                                      4 │
    │ train_loop_config/args/dataset                                                           viggo-train │
    │ train_loop_config/args/dataset_dir                                              ...ter_storage/viggo │
    │ train_loop_config/args/ddp_timeout                                                         180000000 │
    │ train_loop_config/args/do_train                                                                 True │
    │ train_loop_config/args/eval_dataset                                                        viggo-val │
    │ train_loop_config/args/eval_steps                                                                500 │
    │ train_loop_config/args/eval_strategy                                                           steps │
    │ train_loop_config/args/finetuning_type                                                          lora │
    │ train_loop_config/args/gradient_accumulation_steps                                                 8 │
    │ train_loop_config/args/learning_rate                                                          0.0001 │
    │ train_loop_config/args/logging_steps                                                              10 │
    │ train_loop_config/args/lora_rank                                                                   8 │
    │ train_loop_config/args/lora_target                                                               all │
    │ train_loop_config/args/lr_scheduler_type                                                      cosine │
    │ train_loop_config/args/max_samples                                                              1000 │
    │ train_loop_config/args/model_name_or_path                                       ...en2.5-7B-Instruct │
    │ train_loop_config/args/num_train_epochs                                                          5.0 │
    │ train_loop_config/args/output_dir                                               ...age/viggo/outputs │
    │ train_loop_config/args/overwrite_cache                                                          True │
    │ train_loop_config/args/overwrite_output_dir                                                     True │
    │ train_loop_config/args/per_device_eval_batch_size                                                  1 │
    │ train_loop_config/args/per_device_train_batch_size                                                 1 │
    │ train_loop_config/args/placement_strategy                                                       PACK │
    │ train_loop_config/args/plot_loss                                                                True │
    │ train_loop_config/args/preprocessing_num_workers                                                  16 │
    │ train_loop_config/args/ray_num_workers                                                             4 │
    │ train_loop_config/args/ray_run_name                                                     lora_sft_ray │
    │ train_loop_config/args/ray_storage_path                                         ...orage/viggo/saves │
    │ train_loop_config/args/resources_per_worker/GPU                                                    1 │
    │ train_loop_config/args/resources_per_worker/anyscale/accelerator_shape:4xA10G                      1 │
    │ train_loop_config/args/resume_from_checkpoint                                                        │
    │ train_loop_config/args/save_only_model                                                         False │
    │ train_loop_config/args/save_steps                                                                500 │
    │ train_loop_config/args/stage                                                                     sft │
    │ train_loop_config/args/template                                                                 qwen │
    │ train_loop_config/args/trust_remote_code                                                        True │
    │ train_loop_config/args/warmup_ratio                                                              0.1 │
    │ train_loop_config/callbacks                                                     ... 0x7e1262910e10>] │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────╯

    100%|██████████| 155/155 [07:12<00:00,  2.85s/it][INFO|trainer.py:3942] 2025-04-11 14:57:59,207 >> Saving model checkpoint to /mnt/cluster_storage/viggo/outputs/checkpoint-155
    
    Training finished iteration 1 at 2025-04-11 14:58:02. Total running time: 10min 24s
    ╭─────────────────────────────────────────╮
    │ Training result                         │
    ├─────────────────────────────────────────┤
    │ checkpoint_dir_name   checkpoint_000000 │
    │ time_this_iter_s              521.83827 │
    │ time_total_s                  521.83827 │
    │ training_iteration                    1 │
    │ epoch                             4.704 │
    │ grad_norm                       0.14288 │
    │ learning_rate                        0. │
    │ loss                             0.0065 │
    │ step                                150 │
    ╰─────────────────────────────────────────╯
    Training saved a checkpoint for iteration 1 at: (local)/mnt/cluster_storage/viggo/saves/lora_sft_ray/TorchTrainer_95d16_00000_0_2025-04-11_14-47-37/checkpoint_000000
```

```
display(Code(filename="/mnt/cluster_storage/viggo/outputs/all_results.json", language="json"))
```

```
{
    "epoch": 4.864,
    "eval_viggo-val_loss": 0.13618840277194977,
    "eval_viggo-val_runtime": 20.2797,
    "eval_viggo-val_samples_per_second": 35.208,
    "eval_viggo-val_steps_per_second": 8.827,
    "total_flos": 4.843098686147789e+16,
    "train_loss": 0.2079355036479331,
    "train_runtime": 437.2951,
    "train_samples_per_second": 11.434,
    "train_steps_per_second": 0.354
}
```

[![https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/loss.png](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/loss.png)](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/loss.png)

### Observability[#](#observability "Link to this heading")

**🔎 Monitoring and debugging with Ray**

OSS Ray offers an extensive [observability suite](https://docs.ray.io/en/latest/ray-observability/index.html) with logs and an observability dashboard that you can use to monitor and debug. The dashboard includes a lot of different components such as:

* memory, utilization, etc., of the tasks running in the [cluster](https://docs.ray.io/en/latest/ray-observability/getting-started.html#dash-node-view)

[![https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/cluster_util.png](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/cluster_util.png)](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/cluster_util.png)

* views to see all running tasks, utilization across instance types, autoscaling, etc.

[![https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/observability_views.png](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/observability_views.png)](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/observability_views.png)

**🔎➕➕ Monitoring and debugging on Anyscale**

OSS Ray comes with an extensive observability suite, and Anyscale takes it many steps further to make monitoring and debugging your workloads even easier and faster with:

* [unified log viewer](https://docs.anyscale.com/monitoring/accessing-logs/) to see logs from *all* driver and worker processes
* Ray workload specific dashboard, like Data, Train, etc., that can breakdown the tasks. For example, you can observe the preceding training workload live through the Train specific Ray Workloads dashboard:

[![https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/train_dashboard.png](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/train_dashboard.png)](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/train_dashboard.png)

### Save to cloud storage[#](#save-to-cloud-storage "Link to this heading")

**🗂️ Storage on Anyscale**

You can always store to data inside [any storage buckets](https://docs.anyscale.com/configuration/storage/#private-storage-buckets) but Anyscale offers a [default storage bucket](https://docs.anyscale.com/configuration/storage/#anyscale-default-storage-bucket) to make things even easier. You also have plenty of other [storage options](https://docs.anyscale.com/configuration/storage/) as well, shared at the cluster, user, and cloud levels.

```
%%bash
# Anyscale default storage bucket.
echo $ANYSCALE_ARTIFACT_STORAGE
```

```
s3://anyscale-test-data-cld-i2w99rzq8b6lbjkke9y94vi5/org_7c1Kalm9WcX2bNIjW53GUT/cld_kvedZWag2qA8i5BjxUevf5i7/artifact_storage
```

```
%%bash
# Save fine-tuning artifacts to cloud storage.
STORAGE_PATH="$ANYSCALE_ARTIFACT_STORAGE/viggo"
LOCAL_OUTPUTS_PATH="/mnt/cluster_storage/viggo/outputs"
LOCAL_SAVES_PATH="/mnt/cluster_storage/viggo/saves"

# AWS S3 operations.
if [[ "$STORAGE_PATH" == s3://* ]]; then
    if aws s3 ls "$STORAGE_PATH" > /dev/null 2>&1; then
        aws s3 rm "$STORAGE_PATH" --recursive --quiet
    fi
    aws s3 cp "$LOCAL_OUTPUTS_PATH" "$STORAGE_PATH/outputs" --recursive --quiet
    aws s3 cp "$LOCAL_SAVES_PATH" "$STORAGE_PATH/saves" --recursive --quiet

# Google Cloud Storage operations.
elif [[ "$STORAGE_PATH" == gs://* ]]; then
    if gsutil ls "$STORAGE_PATH" > /dev/null 2>&1; then
        gsutil -m -q rm -r "$STORAGE_PATH"
    fi
    gsutil -m -q cp -r "$LOCAL_OUTPUTS_PATH" "$STORAGE_PATH/outputs"
    gsutil -m -q cp -r "$LOCAL_SAVES_PATH" "$STORAGE_PATH/saves"

else
    echo "Unsupported storage protocol: $STORAGE_PATH"
    exit 1
fi
```

```
%%bash
ls /mnt/cluster_storage/viggo/saves/lora_sft_ray
```

```
TorchTrainer_95d16_00000_0_2025-04-11_14-47-37
TorchTrainer_f9e4e_00000_0_2025-04-11_12-41-34
basic-variant-state-2025-04-11_12-41-34.json
basic-variant-state-2025-04-11_14-47-37.json
experiment_state-2025-04-11_12-41-34.json
experiment_state-2025-04-11_14-47-37.json
trainer.pkl
tuner.pkl
```

```
# LoRA paths.
save_dir = Path("/mnt/cluster_storage/viggo/saves/lora_sft_ray")
trainer_dirs = [d for d in save_dir.iterdir() if d.name.startswith("TorchTrainer_") and d.is_dir()]
latest_trainer = max(trainer_dirs, key=lambda d: d.stat().st_mtime, default=None)
lora_path = f"{latest_trainer}/checkpoint_000000/checkpoint"
cloud_lora_path = os.path.join(os.getenv("ANYSCALE_ARTIFACT_STORAGE"), lora_path.split("/mnt/cluster_storage/")[-1])
dynamic_lora_path, lora_id = cloud_lora_path.rsplit("/", 1)
print (lora_path)
print (cloud_lora_path)
print (dynamic_lora_path)
print (lora_id)
```

```
/mnt/cluster_storage/viggo/saves/lora_sft_ray/TorchTrainer_95d16_00000_0_2025-04-11_14-47-37/checkpoint_000000/checkpoint
s3://anyscale-test-data-cld-i2w99rzq8b6lbjkke9y94vi5/org_7c1Kalm9WcX2bNIjW53GUT/cld_kvedZWag2qA8i5BjxUevf5i7/artifact_storage/viggo/saves/lora_sft_ray/TorchTrainer_95d16_00000_0_2025-04-11_14-47-37/checkpoint_000000/checkpoint
s3://anyscale-test-data-cld-i2w99rzq8b6lbjkke9y94vi5/org_7c1Kalm9WcX2bNIjW53GUT/cld_kvedZWag2qA8i5BjxUevf5i7/artifact_storage/viggo/saves/lora_sft_ray/TorchTrainer_95d16_00000_0_2025-04-11_14-47-37/checkpoint_000000
checkpoint
```

```
%%bash -s "$lora_path"
ls $1
```

```
README.md
adapter_config.json
adapter_model.safetensors
added_tokens.json
merges.txt
optimizer.pt
rng_state_0.pth
rng_state_1.pth
rng_state_2.pth
rng_state_3.pth
scheduler.pt
special_tokens_map.json
tokenizer.json
tokenizer_config.json
trainer_state.json
training_args.bin
vocab.json
```

## Batch inference[#](#batch-inference "Link to this heading")

[`Overview`](https://docs.ray.io/en/latest/data/working-with-llms.html) | [`API reference`](https://docs.ray.io/en/latest/data/api/llm.html)

The `ray.data.llm` module integrates with key large language model (LLM) inference engines and deployed models to enable LLM batch inference. These LLM modules use [Ray Data](https://docs.ray.io/en/latest/data/data.html) under the hood, which makes it extremely easy to distribute workloads but also ensures that they happen:

* **efficiently**: minimizing CPU/GPU idle time with heterogeneous resource scheduling.
* **at scale**: with streaming execution to petabyte-scale datasets, especially when [working with LLMs](https://docs.ray.io/en/latest/data/working-with-llms.html).
* **reliably** by checkpointing processes, especially when running workloads on spot instances with on-demand fallback.
* **flexibly**: connecting to data from any source, applying transformations, and saving to any format and location for your next workload.

[![https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/ray_data_solution.png](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/ray_data_solution.png)](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/ray_data_solution.png)

[RayTurbo Data](https://docs.anyscale.com/rayturbo/rayturbo-data) has more features on top of Ray Data:

* **accelerated metadata fetching** to improve reading first time from large datasets
* **optimized autoscaling** where Jobs can kick off before waiting for the entire cluster to start
* **high reliability** where entire failed jobs, like head node, cluster, uncaptured exceptions, etc., can resume from checkpoints. OSS Ray can only recover from worker node failures.

Start by defining the [vLLM engine processor config](https://docs.ray.io/en/latest/data/api/doc/ray.data.llm.vLLMEngineProcessorConfig.html#ray.data.llm.vLLMEngineProcessorConfig) where you can select the model to use and the [engine behavior](https://docs.vllm.ai/en/stable/serving/engine_args.html). The model can come from [Hugging Face (HF) Hub](https://huggingface.co/models) or a local model path `/path/to/your/model`. Anyscale supports GPTQ, GGUF, or LoRA model formats.

[![https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/data_llm.png](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/data_llm.png)](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/data_llm.png)

### vLLM engine processor[#](#vllm-engine-processor "Link to this heading")

```
import os
import ray
from ray.data.llm import vLLMEngineProcessorConfig
```

```
INFO 04-11 14:58:40 __init__.py:194] No platform detected, vLLM is running on UnspecifiedPlatform
```

```
config = vLLMEngineProcessorConfig(
    model_source=model_source,
    runtime_env={
        "env_vars": {
            "VLLM_USE_V1": "0",  # v1 doesn't support lora adapters yet
            # "HF_TOKEN": os.environ.get("HF_TOKEN"),
        },
    },
    engine_kwargs={
        "enable_lora": True,
        "max_lora_rank": 8,
        "max_loras": 1,
        "pipeline_parallel_size": 1,
        "tensor_parallel_size": 1,
        "enable_prefix_caching": True,
        "enable_chunked_prefill": True,
        "max_num_batched_tokens": 4096,
        "max_model_len": 4096,  # or increase KV cache size
        # complete list: https://docs.vllm.ai/en/stable/serving/engine_args.html
    },
    concurrency=1,
    batch_size=16,
    accelerator_type="L4",
)
```

### LLM processor[#](#llm-processor "Link to this heading")

Next, pass the config to an [LLM processor](https://docs.ray.io/en/master/data/api/doc/ray.data.llm.build_processor.html#ray.data.llm.build_processor) where you can define the preprocessing and postprocessing steps around inference. With your base model defined in the processor config, you can define the LoRA adapter layers as part of the preprocessing step of the LLM processor itself.

```
from ray.data.llm import build_processor
```

```
processor = build_processor(
    config,
    preprocess=lambda row: dict(
        model=lora_path,  # REMOVE this line if doing inference with just the base model
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": row["input"]}
        ],
        sampling_params={
            "temperature": 0.3,
            "max_tokens": 250,
            # complete list: https://docs.vllm.ai/en/stable/api/inference_params.html
        },
    ),
    postprocess=lambda row: {
        **row,  # all contents
        "generated_output": row["generated_text"],
        # add additional outputs
    },
)
```

```
2025-04-11 14:58:40,942	INFO worker.py:1660 -- Connecting to existing Ray cluster at address: 10.0.51.51:6379...
2025-04-11 14:58:40,953	INFO worker.py:1843 -- Connected to Ray cluster. View the dashboard at https://session-zt5t77xa58pyp3uy28glg2g24d.i.anyscaleuserdata.com 
2025-04-11 14:58:40,960	INFO packaging.py:367 -- Pushing file package 'gcs://_ray_pkg_e71d58b4dc01d065456a9fc0325ee2682e13de88.zip' (2.16MiB) to Ray cluster...
2025-04-11 14:58:40,969	INFO packaging.py:380 -- Successfully pushed file package 'gcs://_ray_pkg_e71d58b4dc01d065456a9fc0325ee2682e13de88.zip'.
```

```
(pid=51260) INFO 04-11 14:58:47 __init__.py:194] No platform detected, vLLM is running on UnspecifiedPlatform
```

```
# Evaluation on test dataset
ds = ray.data.read_json("/mnt/cluster_storage/viggo/test.jsonl")  # complete list: https://docs.ray.io/en/latest/data/api/input_output.html
ds = processor(ds)
results = ds.take_all()
results[0]
```

```
{
  "batch_uuid": "d7a6b5341cbf4986bb7506ff277cc9cf",
  "embeddings": null,
  "generated_text": "request(esrb)",
  "generated_tokens": [2035, 50236, 10681, 8, 151645],
  "input": "Do you have a favorite ESRB content rating?",
  "instruction": "Given a target sentence construct the underlying meaning representation of the input sentence as a single function with attributes and attribute values. This function should describe the target string accurately and the function must be one of the following ['inform', 'request', 'give_opinion', 'confirm', 'verify_attribute', 'suggest', 'request_explanation', 'recommend', 'request_attribute']. The attributes must be one of the following: ['name', 'exp_release_date', 'release_year', 'developer', 'esrb', 'rating', 'genres', 'player_perspective', 'has_multiplayer', 'platforms', 'available_on_steam', 'has_linux_release', 'has_mac_release', 'specifier']",
  "messages": [
    {
      "content": "Given a target sentence construct the underlying meaning representation of the input sentence as a single function with attributes and attribute values. This function should describe the target string accurately and the function must be one of the following ['inform', 'request', 'give_opinion', 'confirm', 'verify_attribute', 'suggest', 'request_explanation', 'recommend', 'request_attribute']. The attributes must be one of the following: ['name', 'exp_release_date', 'release_year', 'developer', 'esrb', 'rating', 'genres', 'player_perspective', 'has_multiplayer', 'platforms', 'available_on_steam', 'has_linux_release', 'has_mac_release', 'specifier']",
      "role": "system"
    },
    {
      "content": "Do you have a favorite ESRB content rating?",
      "role": "user"
    }
  ],
  "metrics": {
    "arrival_time": 1744408857.148983,
    "finished_time": 1744408863.09091,
    "first_scheduled_time": 1744408859.130259,
    "first_token_time": 1744408862.7087252,
    "last_token_time": 1744408863.089174,
    "model_execute_time": null,
    "model_forward_time": null,
    "scheduler_time": 0.04162892400017881,
    "time_in_queue": 1.981276035308838
  },
  "model": "/mnt/cluster_storage/viggo/saves/lora_sft_ray/TorchTrainer_95d16_00000_0_2025-04-11_14-47-37/checkpoint_000000/checkpoint",
  "num_generated_tokens": 5,
  "num_input_tokens": 164,
  "output": "request_attribute(esrb[])",
  "params": "SamplingParams(n=1, presence_penalty=0.0, frequency_penalty=0.0, repetition_penalty=1.0, temperature=0.3, top_p=1.0, top_k=-1, min_p=0.0, seed=None, stop=[], stop_token_ids=[], bad_words=[], include_stop_str_in_output=False, ignore_eos=False, max_tokens=250, min_tokens=0, logprobs=None, prompt_logprobs=None, skip_special_tokens=True, spaces_between_special_tokens=True, truncate_prompt_tokens=None, guided_decoding=None)",
  "prompt": "<|im_start|>system
Given a target sentence construct the underlying meaning representation of the input sentence as a single function with attributes and attribute values. This function should describe the target string accurately and the function must be one of the following ['inform', 'request', 'give_opinion', 'confirm', 'verify_attribute', 'suggest', 'request_explanation', 'recommend', 'request_attribute']. The attributes must be one of the following: ['name', 'exp_release_date', 'release_year', 'developer', 'esrb', 'rating', 'genres', 'player_perspective', 'has_multiplayer', 'platforms', 'available_on_steam', 'has_linux_release', 'has_mac_release', 'specifier']<|im_end|>
<|im_start|>user
Do you have a favorite ESRB content rating?<|im_end|>
<|im_start|>assistant
",
  "prompt_token_ids": [151644, "...", 198],
  "request_id": 94,
  "time_taken_llm": 6.028705836999961,
  "generated_output": "request(esrb)"
}
```

```
# Exact match (strict!)
matches = 0
for item in results:
    if item["output"] == item["generated_output"]:
        matches += 1
matches / float(len(results))
```

```
0.6879039704524469
```

**Note**: The objective of fine-tuning here isn’t to create the most performant model but to show that you can leverage it for downstream workloads, like batch inference and online serving at scale. However, you can increase `num_train_epochs` if you want to.

Observe the individual steps in the batch inference workload through the Anyscale Ray Data dashboard:

[![https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/data_dashboard.png](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/data_dashboard.png)](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/data_dashboard.png)

💡 For more advanced guides on topics like optimized model loading, multi-LoRA, OpenAI-compatible endpoints, etc., see [more examples](https://docs.ray.io/en/latest/data/working-with-llms.html) and the [API reference](https://docs.ray.io/en/latest/data/api/llm.html).

## Online serving[#](#online-serving "Link to this heading")

[`Overview`](https://docs.ray.io/en/latest/serve/llm/serving-llms.html) | [`API reference`](https://docs.ray.io/en/latest/serve/api/index.html#llm-api)

[![https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/ray_serve.png](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/ray_serve.png)](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/ray_serve.png)

`ray.serve.llm` APIs allow users to deploy multiple LLM models together with a familiar Ray Serve API, while providing compatibility with the OpenAI API.

[![https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/serve_llm.png](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/serve_llm.png)](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/serve_llm.png)

Ray Serve LLM is designed with the following features:

* Automatic scaling and load balancing
* Unified multi-node multi-model deployment
* OpenAI compatibility
* Multi-LoRA support with shared base models
* Deep integration with inference engines, vLLM to start
* Composable multi-model LLM pipelines

[RayTurbo Serve](https://docs.anyscale.com/rayturbo/rayturbo-serve) on Anyscale has more features on top of Ray Serve:

* **fast autoscaling and model loading** to get services up and running even faster: [5x improvements](https://www.anyscale.com/blog/autoscale-large-ai-models-faster) even for LLMs
* 54% **higher QPS** and up-to 3x **streaming tokens per second** for high traffic serving use-cases
* **replica compaction** into fewer nodes where possible to reduce resource fragmentation and improve hardware utilization
* **zero-downtime** [incremental rollouts](https://docs.anyscale.com/platform/services/update-a-service/#resource-constrained-updates) so your service is never interrupted
* [**different environments**](https://docs.anyscale.com/platform/services/multi-app/#multiple-applications-in-different-containers) for each service in a multi-serve application
* **multi availability-zone** aware scheduling of Ray Serve replicas to provide higher redundancy to availability zone failures

### LLM serve config[#](#llm-serve-config "Link to this heading")

```
import os
from openai import OpenAI  # to use openai api format
from ray import serve
from ray.serve.llm import LLMConfig, build_openai_app
```

Define an [LLM config](https://docs.ray.io/en/latest/serve/api/doc/ray.serve.llm.LLMConfig.html#ray.serve.llm.LLMConfig) where you can define where the model comes from, its [autoscaling behavior](https://docs.ray.io/en/latest/serve/autoscaling-guide.html#serve-autoscaling), what hardware to use and [engine arguments](https://docs.vllm.ai/en/stable/serving/engine_args.html).

**Note**: If you’re using AWS S3, replace `AWS_REGION` in the `runtime_env`’s `env_vars` below with the cloud storage and respective region you saved your model artifacts to. Do the same if using other cloud storage options as well.

```
# Define config.
llm_config = LLMConfig(
    model_loading_config={
        "model_id": model_id,
        "model_source": model_source
    },
    lora_config={  # REMOVE this section if you're only using a base model.
        "dynamic_lora_loading_path": dynamic_lora_path,
        "max_num_adapters_per_replica": 16,  # You only have 1.
    },
    runtime_env={"env_vars": {"AWS_REGION": "us-west-2"}},
    # runtime_env={"env_vars": {"HF_TOKEN": os.environ.get("HF_TOKEN")}},
    deployment_config={
        "autoscaling_config": {
            "min_replicas": 1,
            "max_replicas": 2,
            # complete list: https://docs.ray.io/en/latest/serve/autoscaling-guide.html#serve-autoscaling
        }
    },
    accelerator_type="L4",
    engine_kwargs={
        "max_model_len": 4096,  # Or increase KV cache size.
        "tensor_parallel_size": 1,
        "enable_lora": True,
        # complete list: https://docs.vllm.ai/en/stable/serving/engine_args.html
    },
)
```

Now deploy the LLM config as an application. And because this application is all built on top of [Ray Serve](https://docs.ray.io/en/latest/serve/index.html), you can have advanced service logic around composing models together, deploying multiple applications, model multiplexing, observability, etc.

```
# Deploy.
app = build_openai_app({"llm_configs": [llm_config]})
serve.run(app)
```

```
DeploymentHandle(deployment='LLMRouter')
```

### Service request[#](#service-request "Link to this heading")

```
# Initialize client.
client = OpenAI(base_url="http://localhost:8000/v1", api_key="fake-key")
response = client.chat.completions.create(
    model=f"{model_id}:{lora_id}",
    messages=[
        {"role": "system", "content": "Given a target sentence construct the underlying meaning representation of the input sentence as a single function with attributes and attribute values. This function should describe the target string accurately and the function must be one of the following ['inform', 'request', 'give_opinion', 'confirm', 'verify_attribute', 'suggest', 'request_explanation', 'recommend', 'request_attribute']. The attributes must be one of the following: ['name', 'exp_release_date', 'release_year', 'developer', 'esrb', 'rating', 'genres', 'player_perspective', 'has_multiplayer', 'platforms', 'available_on_steam', 'has_linux_release', 'has_mac_release', 'specifier']"},
        {"role": "user", "content": "Blizzard North is mostly an okay developer, but they released Diablo II for the Mac and so that pushes the game from okay to good in my view."},
    ],
    stream=True
)
for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

```
Avg prompt throughput: 20.3 tokens/s, Avg generation throughput: 0.1 tokens/s, Running: 1 reqs, Swapped: 0 reqs, Pending: 0 reqs, GPU KV cache usage: 0.3%, CPU KV cache usage: 0.0%.

_opinion(name[Diablo II], developer[Blizzard North], rating[good], has_mac_release[yes])
```

And of course, you can observe the running service, the deployments, and metrics like QPS, latency, etc., through the [Ray Dashboard](https://docs.ray.io/en/latest/ray-observability/getting-started.html)’s [Serve view](https://docs.ray.io/en/latest/ray-observability/getting-started.html#dash-serve-view):

[![https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/serve_dashboard.png](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/serve_dashboard.png)](https://raw.githubusercontent.com/anyscale/e2e-llm-workflows/refs/heads/main/images/serve_dashboard.png)

💡 See [more examples](https://docs.ray.io/en/latest/serve/llm/serving-llms.html) and the [API reference](https://docs.ray.io/en/latest/serve/llm/api.html) for advanced guides on topics like structured outputs (like JSON), vision LMs, multi-LoRA on shared base models, using other inference engines (like `sglang`), fast model loading, etc.

## Production[#](#production "Link to this heading")

Seamlessly integrate with your existing CI/CD pipelines by leveraging the Anyscale [CLI](https://docs.anyscale.com/reference/quickstart-cli) or [SDK](https://docs.anyscale.com/reference/quickstart-sdk) to run [reliable batch jobs](https://docs.anyscale.com/platform/jobs) and deploy [highly available services](https://docs.anyscale.com/platform/services). Given you’ve been developing in an environment that’s almost identical to production with a multi-node cluster, this integration should drastically speed up your dev to prod velocity.

[![https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/cicd.png](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/cicd.png)](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/cicd.png)

### Jobs[#](#jobs "Link to this heading")

[Anyscale Jobs](https://docs.anyscale.com/platform/jobs/) ([API ref](https://docs.anyscale.com/reference/job-api/)) allows you to execute discrete workloads in production such as batch inference, embeddings generation, or model fine-tuning.

* [define and manage](https://docs.anyscale.com/platform/jobs/manage-jobs) your Jobs in many different ways, like CLI and Python SDK
* set up [queues](https://docs.anyscale.com/platform/jobs/job-queues) and [schedules](https://docs.anyscale.com/platform/jobs/schedules)
* set up all the [observability, alerting, etc.](https://docs.anyscale.com/platform/jobs/monitoring-and-debugging) around your Jobs

[![https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/job_result.png](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/job_result.png)](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/job_result.png)

### Services[#](#services "Link to this heading")

[Anyscale Services](https://docs.anyscale.com/platform/services/) ([API ref](https://docs.anyscale.com/reference/service-api/)) offers an extremely fault tolerant, scalable, and optimized way to serve your Ray Serve applications:

* you can [rollout and update](https://docs.anyscale.com/platform/services/update-a-service) services with canary deployment with zero-downtime upgrades
* [monitor](https://docs.anyscale.com/platform/services/monitoring) your Services through a dedicated Service page, unified log viewer, tracing, set up alerts, etc.
* scale a service (`num_replicas=auto`) and utilize replica compaction to consolidate nodes that are fractionally utilized
* [head node fault tolerance](https://docs.anyscale.com/platform/services/production-best-practices#head-node-ft) because OSS Ray recovers from failed workers and replicas but not head node crashes
* serving [multiple applications](https://docs.anyscale.com/platform/services/multi-app) in a single Service

[![https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/canary.png](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/canary.png)](https://raw.githubusercontent.com/anyscale/foundational-ray-app/refs/heads/main/images/canary.png)

```
%%bash
# clean up
rm -rf /mnt/cluster_storage/viggo
STORAGE_PATH="$ANYSCALE_ARTIFACT_STORAGE/viggo"
if [[ "$STORAGE_PATH" == s3://* ]]; then
    aws s3 rm "$STORAGE_PATH" --recursive --quiet
elif [[ "$STORAGE_PATH" == gs://* ]]; then
    gsutil -m -q rm -r "$STORAGE_PATH"
fi
```

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/ray-overview/examples/entity-recognition-with-llms/README.ipynb)