LlamaIndex - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#llamaindex)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# LlamaIndex

[LlamaIndex](https://github.com/run-llama/llama_index) is a data framework for LLM applications to ingest, structure, and access private or domain-specific data. Makes it super easy to connect LLMs with your own data. But in order to figure out the best configuration for LlamaIndex and your data you need an object measure of the performance. This is where ragas comes in. Ragas will help you evaluate your `QueryEngine` and gives you the confidence to tweak the configuration to get the highest score.

This guide assumes you are familiar with the LlamaIndex framework.

## Building the Testset

You will need a testset to evaluate your `QueryEngine` against. You can either build one yourself or use the [Testset Generator Module](../../../getstarted/rag_testset_generation/) in Ragas to get started with a small synthetic one.

Let's see how that works with LlamaIndex

## load the documents

```
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./nyc_wikipedia").load_data()
```

Now let's initialize the `TestsetGenerator` object with the corresponding generator and critic LLMs

```
from ragas.testset import TestsetGenerator

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# generator with openai models
generator_llm = OpenAI(model="gpt-4o")
embeddings = OpenAIEmbedding(model="text-embedding-3-large")

generator = TestsetGenerator.from_llama_index(
    llm=generator_llm,
    embedding_model=embeddings,
)
```

Now you are all set to generate the dataset

```
# generate testset
testset = generator.generate_with_llamaindex_docs(
    documents,
    testset_size=5,
)
```

```
df = testset.to_pandas()
df.head()
```

|  | user\_input | reference\_contexts | reference | synthesizer\_name |
| --- | --- | --- | --- | --- |
| 0 | Cud yu pleese explane the role of New York Cit... | [New York, often called New York City or NYC, ... | New York City serves as the geographical and d... | single\_hop\_specifc\_query\_synthesizer |
| 1 | So like, what was New York City called before ... | [History == === Early history === In the pre-C... | Before it was called New York, the area was kn... | single\_hop\_specifc\_query\_synthesizer |
| 2 | what happen in new york with slavery and how i... | [and rechristened it "New Orange" after Willia... | In the early 18th century, New York became a c... | single\_hop\_specifc\_query\_synthesizer |
| 3 | What historical significance does Long Island ... | [<1-hop>\n\nHistory == === Early history === I... | Long Island holds historical significance in t... | multi\_hop\_specific\_query\_synthesizer |
| 4 | What role does the Staten Island Ferry play in... | [<1-hop>\n\nto start service in 2017; this wou... | The Staten Island Ferry plays a significant ro... | multi\_hop\_specific\_query\_synthesizer |

with a test dataset to test our `QueryEngine` lets now build one and evaluate it.

## Building the `QueryEngine`

To start lets build a `VectorStoreIndex` over the New York Cities' [Wikipedia page](https://en.wikipedia.org/wiki/New_York_City) as an example and use ragas to evaluate it.

Since we already loaded the dataset into `documents` lets use that.

```
# build query engine
from llama_index.core import VectorStoreIndex

vector_index = VectorStoreIndex.from_documents(documents)

query_engine = vector_index.as_query_engine()
```

Let's try a sample question from the generated testset to see if it is working

```
# convert it to pandas dataset
df = testset.to_pandas()
df["user_input"][0]
```

```
'Cud yu pleese explane the role of New York City within the Northeast megalopolis, and how it contributes to the cultural and economic vibrancy of the region?'
```

```
response_vector = query_engine.query(df["user_input"][0])

print(response_vector)
```

```
New York City serves as a key hub within the Northeast megalopolis, playing a significant role in enhancing the cultural and economic vibrancy of the region. Its status as a global center of creativity, entrepreneurship, and cultural diversity contributes to the overall dynamism of the area. The city's renowned arts scene, including Broadway theatre and numerous cultural institutions, attracts artists and audiences from around the world, enriching the cultural landscape of the Northeast megalopolis. Economically, New York City's position as a leading financial and fintech center, home to major stock exchanges and a bustling real estate market, bolsters the region's economic strength and influence. Additionally, the city's diverse culinary scene, influenced by its immigrant history, adds to the cultural richness of the region, making New York City a vital component of the Northeast megalopolis's cultural and economic tapestry.
```

## Evaluating the `QueryEngine`

Now that we have a `QueryEngine` for the `VectorStoreIndex` we can use the llama\_index integration Ragas has to evaluate it.

In order to run an evaluation with Ragas and LlamaIndex you need 3 things

1. LlamaIndex `QueryEngine`: what we will be evaluating
2. Metrics: Ragas defines a set of metrics that can measure different aspects of the `QueryEngine`. The available metrics and their meaning can be found [here](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/)
3. Questions: A list of questions that ragas will test the `QueryEngine` against.

first let's generate the questions. Ideally you should use that you see in production so that the distribution of question with which we evaluate matches the distribution of questions seen in production. This ensures that the scores reflect the performance seen in production but to start off we'll be using a few example questions.

Now let's import the metrics we will be using to evaluate

```
# import metrics
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)

# init metrics with evaluator LLM
from ragas.llms import LlamaIndexLLMWrapper

evaluator_llm = LlamaIndexLLMWrapper(OpenAI(model="gpt-4o"))
metrics = [
    Faithfulness(llm=evaluator_llm),
    AnswerRelevancy(llm=evaluator_llm),
    ContextPrecision(llm=evaluator_llm),
    ContextRecall(llm=evaluator_llm),
]
```

the `evaluate()` function expects a dict of "question" and "ground\_truth" for metrics. You can easily convert the `testset` to that format

```
# convert to Ragas Evaluation Dataset
ragas_dataset = testset.to_evaluation_dataset()
ragas_dataset
```

```
EvaluationDataset(features=['user_input', 'reference_contexts', 'reference'], len=6)
```

Finally, let's run the evaluation

```
from ragas.integrations.llama_index import evaluate

result = evaluate(
    query_engine=query_engine,
    metrics=metrics,
    dataset=ragas_dataset,
)
```

```
# final scores
print(result)
```

```
{'faithfulness': 0.7454, 'answer_relevancy': 0.9348, 'context_precision': 0.6667, 'context_recall': 0.4667}
```

You can convert into a pandas DataFrame to run more analysis on it.

```
result.to_pandas()
```

|  | user\_input | retrieved\_contexts | reference\_contexts | response | reference | faithfulness | answer\_relevancy | context\_precision | context\_recall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Cud yu pleese explane the role of New York Cit... | [and its ideals of liberty and peace. In the 2... | [New York, often called New York City or NYC, ... | New York City plays a significant role within ... | New York City serves as the geographical and d... | 0.615385 | 0.918217 | 0.0 | 0.0 |
| 1 | So like, what was New York City called before ... | [New York City is the headquarters of the glob... | [History == === Early history === In the pre-C... | New York City was named New Amsterdam before i... | Before it was called New York, the area was kn... | 1.000000 | 0.967821 | 1.0 | 1.0 |
| 2 | what happen in new york with slavery and how i... | [=== Province of New York and slavery ===\n\nI... | [and rechristened it "New Orange" after Willia... | Slavery became a significant part of New York'... | In the early 18th century, New York became a c... | 1.000000 | 0.919264 | 1.0 | 1.0 |
| 3 | What historical significance does Long Island ... | [==== River crossings ====\n\nNew York City is... | [<1-hop>\n\nHistory == === Early history === I... | Long Island played a significant role in the e... | Long Island holds historical significance in t... | 0.500000 | 0.931895 | 0.0 | 0.0 |
| 4 | What role does the Staten Island Ferry play in... | [==== Buses ====\n\nNew York City's public bus... | [<1-hop>\n\nto start service in 2017; this wou... | The Staten Island Ferry serves as a vital mode... | The Staten Island Ferry plays a significant ro... | 0.500000 | 0.936920 | 1.0 | 0.0 |
| 5 | How does Central Park's role as a cultural and... | [==== State parks ====\n\nThere are seven stat... | [<1-hop>\n\nCity has over 28,000 acres (110 km... | Central Park's role as a cultural and historic... | Central Park, located in middle-upper Manhatta... | 0.857143 | 0.934841 | 1.0 | 0.8 |

November 28, 2025




November 28, 2025

Back to top