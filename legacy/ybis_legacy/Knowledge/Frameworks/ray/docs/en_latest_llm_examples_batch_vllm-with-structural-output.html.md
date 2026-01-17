Batch Inference with Structural Outputs (Guided Decoding) — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Batch Inference with Structural Outputs (Guided Decoding)[#](#batch-inference-with-structural-outputs-guided-decoding "Link to this heading")

Structural output (or named guided decoding, JSON mode) is a useful feature that ensures the LLM responses following the given output schema in either JSON or the context free grammar.

In this example, we show how to perform batch inference using Ray Data LLM with structural outputs in JSON format. To run this example, we need to install the following dependencies:

```
pip install -qU "ray[llm]"
```

```
from pydantic import BaseModel

import ray
from ray.data.llm import build_processor, vLLMEngineProcessorConfig

# 1. Construct a guided decoding schema. It can be:
# choice: List[str]
# json: str
# grammar: str
# See https://docs.vllm.ai/en/latest/getting_started/examples/structured_outputs.html
# for more details about how to construct the schema. Here we use JSON as an example.
class AnswerWithExplain(BaseModel):
    problem: str
    answer: int
    explain: str

json_schema = AnswerWithExplain.model_json_schema()

# 2. construct a vLLM processor config.
processor_config = vLLMEngineProcessorConfig(
    # The base model.
    model_source="unsloth/Llama-3.2-1B-Instruct",
    # vLLM engine config.
    engine_kwargs=dict(
        # Specify the structured outputs backend to use. The default is "xgrammar".
        # See https://docs.vllm.ai/en/latest/serving/engine_args.html
        # for other available backends.
        structured_outputs_config={"backend": "xgrammar"},
        # Older GPUs (e.g. T4) don't support bfloat16. You should remove
        # this line if you're using later GPUs.
        dtype="half",
        # Reduce the model length to fit small GPUs. You should remove
        # this line if you're using large GPUs.
        max_model_len=1024,
    ),
    # The batch size used in Ray Data.
    batch_size=16,
    # Use one GPU in this example.
    concurrency=1,
)

# 3. construct a processor using the processor config.
processor = build_processor(
    processor_config,
    # Convert the input data to the OpenAI chat form.
    preprocess=lambda row: dict(
        messages=[
            {
                "role": "system",
                "content": "You are a math teacher. Give the answer to "
                "the equation and explain it. Output the problem, answer and "
                "explanation in JSON",
            },
            {
                "role": "user",
                "content": f"3 * {row['id']} + 5 = ?",
            },
        ],
        sampling_params=dict(
            temperature=0.3,
            max_tokens=150,
            detokenize=False,
            # Specify the guided decoding schema.
            guided_decoding=dict(json=json_schema),
        ),
    ),
    # Only keep the generated text in the output dataset.
    postprocess=lambda row: {
        "resp": row["generated_text"],
    },
)

# 4. Synthesize a dataset with 30 rows.
# Each row has a single column "id" ranging from 0 to 29.
ds = ray.data.range(30)
# 5. Apply the processor to the dataset. Note that this line won't kick off
# anything because processor is execution lazily.
ds = processor(ds)
# Materialization kicks off the pipeline execution.
ds = ds.materialize()

# 6. Print all outputs.
# Example output:
# {
#     "problem": "3 * 6 + 5 = ?",
#     "answer": 23,
#     "explain": "To solve this equation, we need to follow the order of
#       operations (PEMDAS): Parentheses, Exponents, Multiplication and Division,
#       and Addition and Subtraction. In this case, we first multiply 3 and 6,
#       which equals 18. Then we add 5 to 18, which equals 23."
# }
for out in ds.take_all():
    print(out["resp"])
    print("==========")

# 7. Shutdown Ray to release resources.
ray.shutdown()
```

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/llm/examples/batch/vllm-with-structural-output.ipynb)