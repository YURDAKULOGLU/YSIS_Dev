End-to-end: Offline Batch Inference — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# End-to-end: Offline Batch Inference[#](#end-to-end-offline-batch-inference "Link to this heading")

Offline batch inference is a process for generating model predictions on a fixed set of input data. Ray Data offers an efficient and scalable solution for batch inference, providing faster execution and cost-effectiveness for deep learning applications.

[![../_images/stream-example.png](../_images/stream-example.png)](../_images/stream-example.png)

Note

This guide is primarily focused on batch inference with deep learning frameworks.
For more information on batch inference with LLMs, see [Working with LLMs](working-with-llms.html#working-with-llms).

## Quickstart[#](#quickstart "Link to this heading")

To start, install Ray Data:

```
pip install -U "ray[data]"
```

Using Ray Data for offline inference involves four basic steps:

* **Step 1:** Load your data into a Ray Dataset. Ray Data supports many different datasources and formats. For more details, see [Loading Data](loading-data.html#loading-data).
* **Step 2:** Define a Python class to load the pre-trained model.
* **Step 3:** Transform your dataset using the pre-trained model by calling [`ds.map_batches()`](api/doc/ray.data.Dataset.map_batches.html#ray.data.Dataset.map_batches "ray.data.Dataset.map_batches"). For more details, see [Transforming Data](transforming-data.html#transforming-data).
* **Step 4:** Get the final predictions by either iterating through the output or saving the results. For more details, see the [Iterating over data](iterating-over-data.html#iterating-over-data) and [Saving data](saving-data.html#saving-data) user guides.

For more in-depth examples for your use case, see [the batch inference examples](examples.html).
For how to configure batch inference, see [the configuration guide](#batch-inference-configuration).

HuggingFace

```
from typing import Dict
import numpy as np

import ray

# Step 1: Create a Ray Dataset from in-memory Numpy arrays.
# You can also create a Ray Dataset from many other sources and file
# formats.
ds = ray.data.from_numpy(np.asarray(["Complete this", "for me"]))

# Step 2: Define a Predictor class for inference.
# Use a class to initialize the model just once in `__init__`
# and reuse it for inference across multiple batches.
class HuggingFacePredictor:
    def __init__(self):
        from transformers import pipeline
        # Initialize a pre-trained GPT2 Huggingface pipeline.
        self.model = pipeline("text-generation", model="gpt2")

    # Logic for inference on 1 batch of data.
    def __call__(self, batch: Dict[str, np.ndarray]) -> Dict[str, list]:
        # Get the predictions from the input batch.
        predictions = self.model(list(batch["data"]), max_length=20, num_return_sequences=1)
        # `predictions` is a list of length-one lists. For example:
        # [[{'generated_text': 'output_1'}], ..., [{'generated_text': 'output_2'}]]
        # Modify the output to get it into the following format instead:
        # ['output_1', 'output_2']
        batch["output"] = [sequences[0]["generated_text"] for sequences in predictions]
        return batch

# Step 2: Map the Predictor over the Dataset to get predictions.
# Use 2 parallel actors for inference. Each actor predicts on a
# different partition of data.
predictions = ds.map_batches(HuggingFacePredictor, compute=ray.data.ActorPoolStrategy(size=2))
# Step 3: Show one prediction output.
predictions.show(limit=1)
```

```
{'data': 'Complete this', 'output': 'Complete this information or purchase any item from this site.\n\nAll purchases are final and non-'}
```


PyTorch

```
from typing import Dict
import numpy as np
import torch
import torch.nn as nn

import ray

# Step 1: Create a Ray Dataset from in-memory Numpy arrays.
# You can also create a Ray Dataset from many other sources and file
# formats.
ds = ray.data.from_numpy(np.ones((1, 100)))

# Step 2: Define a Predictor class for inference.
# Use a class to initialize the model just once in `__init__`
# and reuse it for inference across multiple batches.
class TorchPredictor:
    def __init__(self):
        # Load a dummy neural network.
        # Set `self.model` to your pre-trained PyTorch model.
        self.model = nn.Sequential(
            nn.Linear(in_features=100, out_features=1),
            nn.Sigmoid(),
        )
        self.model.eval()

    # Logic for inference on 1 batch of data.
    def __call__(self, batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        tensor = torch.as_tensor(batch["data"], dtype=torch.float32)
        with torch.inference_mode():
            # Get the predictions from the input batch.
            return {"output": self.model(tensor).numpy()}

# Step 2: Map the Predictor over the Dataset to get predictions.
# Use 2 parallel actors for inference. Each actor predicts on a
# different partition of data.
predictions = ds.map_batches(TorchPredictor, compute=ray.data.ActorPoolStrategy(size=2))
# Step 3: Show one prediction output.
predictions.show(limit=1)
```

```
{'output': array([0.5590901], dtype=float32)}
```


TensorFlow

```
from typing import Dict
import numpy as np

import ray

# Step 1: Create a Ray Dataset from in-memory Numpy arrays.
# You can also create a Ray Dataset from many other sources and file
# formats.
ds = ray.data.from_numpy(np.ones((1, 100)))

# Step 2: Define a Predictor class for inference.
# Use a class to initialize the model just once in `__init__`
# and reuse it for inference across multiple batches.
class TFPredictor:
    def __init__(self):
        from tensorflow import keras

        # Load a dummy neural network.
        # Set `self.model` to your pre-trained Keras model.
        input_layer = keras.Input(shape=(100,))
        output_layer = keras.layers.Dense(1, activation="sigmoid")
        self.model = keras.Sequential([input_layer, output_layer])

    # Logic for inference on 1 batch of data.
    def __call__(self, batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        # Get the predictions from the input batch.
        return {"output": self.model(batch["data"]).numpy()}

# Step 2: Map the Predictor over the Dataset to get predictions.
# Use 2 parallel actors for inference. Each actor predicts on a
# different partition of data.
predictions = ds.map_batches(TFPredictor, compute=ray.data.ActorPoolStrategy(size=2))
 # Step 3: Show one prediction output.
predictions.show(limit=1)
```

```
{'output': array([0.625576], dtype=float32)}
```


LLM Inference

Ray Data offers native integration with vLLM, a high-performance inference engine for large language models (LLMs).

```
import ray
from ray.data.llm import vLLMEngineProcessorConfig, build_processor
import numpy as np

config = vLLMEngineProcessorConfig(
    model="unsloth/Llama-3.1-8B-Instruct",
    engine_kwargs={
        "enable_chunked_prefill": True,
        "max_num_batched_tokens": 4096,
        "max_model_len": 16384,
    },
    concurrency=1,
    batch_size=64,
)
processor = build_processor(
    config,
    preprocess=lambda row: dict(
        messages=[
            {"role": "system", "content": "You are a bot that responds with haikus."},
            {"role": "user", "content": row["item"]}
        ],
        sampling_params=dict(
            temperature=0.3,
            max_tokens=250,
        )
    ),
    postprocess=lambda row: dict(
        answer=row["generated_text"]
    ),
)

ds = ray.data.from_items(["Start of the haiku is: Complete this for me..."])

ds = processor(ds)
ds.show(limit=1)
```

```
{'answer': 'Snowflakes gently fall\nBlanketing the winter scene\nFrozen peaceful hush'}
```

## Configuration and troubleshooting[#](#configuration-and-troubleshooting "Link to this heading")

### Using GPUs for inference[#](#using-gpus-for-inference "Link to this heading")

To use GPUs for inference, make the following changes to your code:

1. Update the class implementation to move the model and data to and from GPU.
2. Specify `num_gpus=1` in the [`ds.map_batches()`](api/doc/ray.data.Dataset.map_batches.html#ray.data.Dataset.map_batches "ray.data.Dataset.map_batches") call to indicate that each actor should use 1 GPU.
3. Specify a `batch_size` for inference. For more details on how to configure the batch size, see [Configuring Batch Size](#batch-inference-batch-size).

The remaining is the same as the [Quickstart](#batch-inference-quickstart).

HuggingFace

```
from typing import Dict
import numpy as np

import ray

ds = ray.data.from_numpy(np.asarray(["Complete this", "for me"]))

class HuggingFacePredictor:
    def __init__(self):
        from transformers import pipeline
        # Set "cuda:0" as the device so the Huggingface pipeline uses GPU.
        self.model = pipeline("text-generation", model="gpt2", device="cuda:0")

    def __call__(self, batch: Dict[str, np.ndarray]) -> Dict[str, list]:
        predictions = self.model(list(batch["data"]), max_length=20, num_return_sequences=1)
        batch["output"] = [sequences[0]["generated_text"] for sequences in predictions]
        return batch

# Use 2 actors, each actor using 1 GPU. 2 GPUs total.
predictions = ds.map_batches(
    HuggingFacePredictor,
    num_gpus=1,
    # Specify the batch size for inference.
    # Increase this for larger datasets.
    batch_size=1,
    # Set the concurrency to the number of GPUs in your cluster.
    compute=ray.data.ActorPoolStrategy(size=2),
    )
predictions.show(limit=1)
```

```
{'data': 'Complete this', 'output': 'Complete this poll. Which one do you think holds the most promise for you?\n\nThank you'}
```


PyTorch

```
from typing import Dict
import numpy as np
import torch
import torch.nn as nn

import ray

ds = ray.data.from_numpy(np.ones((1, 100)))

class TorchPredictor:
    def __init__(self):
        # Move the neural network to GPU device by specifying "cuda".
        self.model = nn.Sequential(
            nn.Linear(in_features=100, out_features=1),
            nn.Sigmoid(),
        ).cuda()
        self.model.eval()

    def __call__(self, batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        # Move the input batch to GPU device by specifying "cuda".
        tensor = torch.as_tensor(batch["data"], dtype=torch.float32, device="cuda")
        with torch.inference_mode():
            # Move the prediction output back to CPU before returning.
            return {"output": self.model(tensor).cpu().numpy()}

# Use 2 actors, each actor using 1 GPU. 2 GPUs total.
predictions = ds.map_batches(
    TorchPredictor,
    num_gpus=1,
    # Specify the batch size for inference.
    # Increase this for larger datasets.
    batch_size=1,
    # Set the concurrency to the number of GPUs in your cluster.
    compute=ray.data.ActorPoolStrategy(size=2),
    )
predictions.show(limit=1)
```

```
{'output': array([0.5590901], dtype=float32)}
```


TensorFlow

```
from typing import Dict
import numpy as np

import ray

ds = ray.data.from_numpy(np.ones((1, 100)))

class TFPredictor:
    def __init__(self):
        import tensorflow as tf
        from tensorflow import keras

        # Move the neural network to GPU by specifying the GPU device.
        with tf.device("GPU:0"):
            input_layer = keras.Input(shape=(100,))
            output_layer = keras.layers.Dense(1, activation="sigmoid")
            self.model = keras.Sequential([input_layer, output_layer])

    def __call__(self, batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        import tensorflow as tf

        # Move the input batch to GPU by specifying GPU device.
        with tf.device("GPU:0"):
            return {"output": self.model(batch["data"]).numpy()}

# Use 2 actors, each actor using 1 GPU. 2 GPUs total.
predictions = ds.map_batches(
    TFPredictor,
    num_gpus=1,
    # Specify the batch size for inference.
    # Increase this for larger datasets.
    batch_size=1,
    # Set the concurrency to the number of GPUs in your cluster.
    compute=ray.data.ActorPoolStrategy(size=2),
)
predictions.show(limit=1)
```

```
{'output': array([0.625576], dtype=float32)}
```

### Configuring Batch Size[#](#configuring-batch-size "Link to this heading")

Configure the size of the input batch that’s passed to `__call__` by setting the `batch_size` argument for [`ds.map_batches()`](api/doc/ray.data.Dataset.map_batches.html#ray.data.Dataset.map_batches "ray.data.Dataset.map_batches")

Increasing batch size results in faster execution because inference is a vectorized operation. For GPU inference, increasing batch size increases GPU utilization. Set the batch size to as large possible without running out of memory. If you encounter out-of-memory errors, decreasing `batch_size` may help.

```
import numpy as np

import ray

ds = ray.data.from_numpy(np.ones((10, 100)))

def assert_batch(batch: Dict[str, np.ndarray]):
    assert len(batch) == 2
    return batch

# Specify that each input batch should be of size 2.
ds.map_batches(assert_batch, batch_size=2)
```

Caution

The default `batch_size` of `4096` may be too large for datasets with large rows
(for example, tables with many columns or a collection of large images).

### Handling GPU out-of-memory failures[#](#handling-gpu-out-of-memory-failures "Link to this heading")

If you run into CUDA out-of-memory issues, your batch size is likely too large. Decrease
the batch size by following [these steps](#batch-inference-batch-size). If your
batch size is already set to 1, then use either a smaller model or GPU devices with more
memory.

For advanced users working with large models, you can use model parallelism to shard the model across multiple GPUs.

### Optimizing expensive CPU preprocessing[#](#optimizing-expensive-cpu-preprocessing "Link to this heading")

If your workload involves expensive CPU preprocessing in addition to model inference, you can optimize throughput by separating the preprocessing and inference logic into separate operations. This separation allows inference on batch \(N\) to execute concurrently with preprocessing on batch \(N+1\).

For an example where preprocessing is done in a separate `map` call, see [Image Classification Batch Inference with PyTorch ResNet18](examples/pytorch_resnet_batch_prediction.html).

### Handling CPU out-of-memory failures[#](#handling-cpu-out-of-memory-failures "Link to this heading")

If you run out of CPU RAM, you likely have too many model replicas that are running concurrently on the same node. For example, if a model
uses 5 GB of RAM when created / run, and a machine has 16 GB of RAM total, then no more
than three of these models can be run at the same time. The default resource assignments
of one CPU per task/actor might lead to `OutOfMemoryError` from Ray in this situation.

Suppose your cluster has 4 nodes, each with 16 CPUs. To limit to at most
3 of these actors per node, you can override the CPU or memory:

```
from typing import Dict
import numpy as np

import ray

ds = ray.data.from_numpy(np.asarray(["Complete this", "for me"]))

class HuggingFacePredictor:
    def __init__(self):
        from transformers import pipeline
        self.model = pipeline("text-generation", model="gpt2")

    def __call__(self, batch: Dict[str, np.ndarray]) -> Dict[str, list]:
        predictions = self.model(list(batch["data"]), max_length=20, num_return_sequences=1)
        batch["output"] = [sequences[0]["generated_text"] for sequences in predictions]
        return batch

predictions = ds.map_batches(
    HuggingFacePredictor,
    # Require 5 CPUs per actor (so at most 3 can fit per 16 CPU node).
    num_cpus=5,
    # 3 actors per node, with 4 nodes in the cluster means concurrency of 12.
    compute=ray.data.ActorPoolStrategy(size=12),
    )
predictions.show(limit=1)
```

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/data/batch_inference.rst)