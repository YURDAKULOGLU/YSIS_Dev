Adapting Metrics to Target Language - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#adapting-metrics-to-target-language)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Adapting Metrics to Target Language

When evaluating LLM applications in languages other than English, adapt your metrics to the target language. Ragas uses an LLM to translate the few-shot examples in prompts.

## Setup

```
from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import Faithfulness

client = AsyncOpenAI()
llm = llm_factory("gpt-4o-mini", client=client)

metric = Faithfulness(llm=llm)
```

## Adapt Prompts to Target Language

Collections metrics have prompts as direct attributes. Use the `adapt()` method to translate the few-shot examples:

```
# Check original language
print(metric.statement_generator_prompt.language)
# english

# Adapt prompts to Hindi
metric.statement_generator_prompt = await metric.statement_generator_prompt.adapt(
    target_language="hindi", llm=llm
)
metric.nli_statement_prompt = await metric.nli_statement_prompt.adapt(
    target_language="hindi", llm=llm
)

# Verify adaptation
print(metric.statement_generator_prompt.language)
# hindi

# See translated example
print(metric.statement_generator_prompt.examples[0][0].question)
# अल्बर्ट आइंस्टीन कौन थे और वे किस चीज़ के लिए सबसे अधिक जाने जाते हैं?
```

Note

By default, only few-shot examples are translated. Instructions remain in English. To also translate instructions, set `adapt_instruction=True`.

## Evaluate with Adapted Metric

```
result = await metric.ascore(
    user_input="भारत की राजधानी क्या है?",
    response="भारत की राजधानी नई दिल्ली है।",
    retrieved_contexts=["भारत की राजधानी नई दिल्ली है, जो देश का सबसे बड़ा शहर भी है।"],
)

print(f"Faithfulness: {result.value}")
# Faithfulness: 1.0
```

## Adapting Other Metrics

The same pattern works for any collections metric with prompts:

```
from ragas.metrics.collections import AnswerRelevancy
from ragas.embeddings.base import embedding_factory

embeddings = embedding_factory("openai", client=client)
relevancy = AnswerRelevancy(llm=llm, embeddings=embeddings)

# Adapt the prompt
relevancy.prompt = await relevancy.prompt.adapt(
    target_language="spanish", llm=llm
)

# See translated example
print(relevancy.prompt.examples[0][0].response)
# Albert Einstein nació en Alemania.
```

December 12, 2025




December 12, 2025

Back to top