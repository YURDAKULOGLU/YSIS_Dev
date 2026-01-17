Cost Analysis - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#how-to-estimate-cost-and-usage-of-evaluations-and-testset-generation)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# How to estimate Cost and Usage of evaluations and testset generation

When using LLMs for evaluation and test set generation, cost will be an important factor. Ragas provides you some tools to help you with that.

## Implement `TokenUsageParser`

By default, Ragas does not calculate the usage of tokens for `evaluate()`. This is because langchain's LLMs do not always return information about token usage in a uniform way. So in order to get the usage data, we have to implement a `TokenUsageParser`.

A `TokenUsageParser` is function that parses the `LLMResult` or `ChatResult` from langchain models `generate_prompt()` function and outputs `TokenUsage` which Ragas expects.

For an example here is one that will parse OpenAI by using a parser we have defined.

```
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompt_values import StringPromptValue

gpt4o = ChatOpenAI(model="gpt-4o")
p = StringPromptValue(text="hai there")
llm_result = gpt4o.generate_prompt([p])

# lets import a parser for OpenAI
from ragas.cost import get_token_usage_for_openai

get_token_usage_for_openai(llm_result)
```

Output

```
TokenUsage(input_tokens=9, output_tokens=9, model='')
```

You can define your own or import parsers if they are defined. If you would like to suggest parser for LLM providers or contribute your own ones please check out this [issue](https://github.com/vibrantlabsai/ragas/issues/1151) 🙂.

## Token Usage for Evaluations

Let's use the `get_token_usage_for_openai` parser to calculate the token usage for an evaluation.

```
from ragas import EvaluationDataset
from datasets import load_dataset

dataset = load_dataset("vibrantlabsai/amnesty_qa", "english_v3")

eval_dataset = EvaluationDataset.from_hf_dataset(dataset["eval"])
```

Output

```
Repo card metadata block was not found. Setting CardData to empty.
```

You can pass in the parser to the `evaluate()` function and the cost will be calculated and returned in the `Result` object.

```
from ragas import evaluate
from ragas.metrics import LLMContextRecall

from ragas.cost import get_token_usage_for_openai

result = evaluate(
    eval_dataset,
    metrics=[LLMContextRecall()],
    llm=gpt4o,
    token_usage_parser=get_token_usage_for_openai,
)
```

Output

```
Evaluating:   0%|          | 0/20 [00:00<?, ?it/s]
```

```
result.total_tokens()
```

Output

```
TokenUsage(input_tokens=25097, output_tokens=3757, model='')
```

You can compute the cost for each run by passing in the cost per token to `Result.total_cost()` function.

In this case GPT-4o costs $5 for 1M input tokens and $15 for 1M output tokens.

```
result.total_cost(cost_per_input_token=5 / 1e6, cost_per_output_token=15 / 1e6)
```

Output

```
1.1692900000000002
```

## Token Usage for Testset Generation

You can use the same parser for testset generation, but you need to pass in the `token_usage_parser` to the `generate()` function. For now, it only calculates the cost for the generation process and not the cost for the transforms.

For an example let's load an existing KnowledgeGraph and generate a testset. If you want to know more about how to generate a testset please check out the [testset generation](../../../getstarted/rag_testset_generation/#a-deeper-look).

```
from ragas.testset.graph import KnowledgeGraph

# loading an existing KnowledgeGraph
# make sure to change the path to the location of the KnowledgeGraph file
kg = KnowledgeGraph.load("../../../experiments/scratchpad_kg.json")
kg
```

Output

```
KnowledgeGraph(nodes: 47, relationships: 109)



### Choose your LLM

=== "OpenAI"
    Install the langchain-openai package

    ```bash
    pip install langchain-openai
    ```

    Then ensure you have your OpenAI key ready and available in your environment

    ```python
    import os
    os.environ["OPENAI_API_KEY"] = "your-openai-key"
    ```

    Wrap the LLMs in `LangchainLLMWrapper` so that it can be used with ragas.

    ```python
    from ragas.llms import LangchainLLMWrapper
    from langchain_openai import ChatOpenAI
    from ragas.embeddings import OpenAIEmbeddings
    import openai

    generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
    openai_client = openai.OpenAI()
    generator_embeddings = OpenAIEmbeddings(client=openai_client)
    ```


=== "AWS"
    Install the langchain-aws package

    ```bash
    pip install langchain-aws
    ```

    Then you have to set your AWS credentials and configurations

    ```python
    config = {
        "credentials_profile_name": "your-profile-name",  # E.g "default"
        "region_name": "your-region-name",  # E.g. "us-east-1"
        "llm": "your-llm-model-id",  # E.g "anthropic.claude-3-5-sonnet-20241022-v2:0"
        "embeddings": "your-embedding-model-id",  # E.g "amazon.titan-embed-text-v2:0"
        "temperature": 0.4,
    }
    ```

    Define your LLMs and wrap them in `LangchainLLMWrapper` so that it can be used with ragas.

    ```python
    from langchain_aws import ChatBedrockConverse
    from langchain_aws import BedrockEmbeddings
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper

    generator_llm = LangchainLLMWrapper(ChatBedrockConverse(
        credentials_profile_name=config["credentials_profile_name"],
        region_name=config["region_name"],
        base_url=f"https://bedrock-runtime.{config['region_name']}.amazonaws.com",
        model=config["llm"],
        temperature=config["temperature"],
    ))
    generator_embeddings = LangchainEmbeddingsWrapper(BedrockEmbeddings(
        credentials_profile_name=config["credentials_profile_name"],
        region_name=config["region_name"],
        model_id=config["embeddings"],
    ))
    ```

    If you want more information on how to use other AWS services, please refer to the [langchain-aws](https://python.langchain.com/docs/integrations/providers/aws/) documentation.

=== "Google Cloud"
    Google offers two ways to access their models: Google AI and Google Cloud Vertex AI. Google AI requires just a Google account and API key, while Vertex AI requires a Google Cloud account with enterprise features.

    First, install the required packages:

    ```bash
    pip install langchain-google-genai langchain-google-vertexai
    ```

    Then set up your credentials based on your chosen API:

    For Google AI:

    ```python
    import os
    os.environ["GOOGLE_API_KEY"] = "your-google-ai-key"  # From https://ai.google.dev/
    ```

    For Vertex AI:

    ```python
    # Ensure you have credentials configured (gcloud, workload identity, etc.)
    # Or set service account JSON path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/service-account.json"
    ```

    Define your configuration:

    ```python
    config = {
        "model": "gemini-1.5-pro",  # or other model IDs
        "temperature": 0.4,
        "max_tokens": None,
        "top_p": 0.8,
        # For Vertex AI only:
        "project": "your-project-id",  # Required for Vertex AI
        "location": "us-central1",     # Required for Vertex AI
    }
    ```

    Initialize the LLM and wrap it for use with ragas:

    ```python
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper

    # Choose the appropriate import based on your API:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_google_vertexai import ChatVertexAI

    # Initialize with Google AI Studio
    generator_llm = LangchainLLMWrapper(ChatGoogleGenerativeAI(
        model=config["model"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        top_p=config["top_p"],
    ))

    # Or initialize with Vertex AI
    generator_llm = LangchainLLMWrapper(ChatVertexAI(
        model=config["model"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        top_p=config["top_p"],
        project=config["project"],
        location=config["location"],
    ))
    ```


    You can optionally configure safety settings:

    ```python
    from langchain_google_genai import HarmCategory, HarmBlockThreshold

    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        # Add other safety settings as needed
    }

    # Apply to your LLM initialization
    generator_llm = LangchainLLMWrapper(ChatGoogleGenerativeAI(
        model=config["model"],
        temperature=config["temperature"],
        safety_settings=safety_settings,
    ))
    ```

    Initialize the embeddings and wrap them for use with ragas:

    ```python
    # Google AI Studio Embeddings
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    generator_embeddings = LangchainEmbeddingsWrapper(GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",  # Google's text embedding model
        task_type="retrieval_document"  # Optional: specify the task type
    ))
    ```

    ```python
    # Vertex AI Embeddings
    from langchain_google_vertexai import VertexAIEmbeddings

    generator_embeddings = LangchainEmbeddingsWrapper(VertexAIEmbeddings(
        model_name="textembedding-gecko@001",  # or other available model
        project=config["project"],  # Your GCP project ID
        location=config["location"]  # Your GCP location
    ))
    ```

    For more information on available models, features, and configurations, refer to: [Google AI documentation](https://ai.google.dev/docs)
    - [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
    - [LangChain Google AI integration](https://python.langchain.com/docs/integrations/chat/google_generative_ai)
    - [LangChain Vertex AI integration](https://python.langchain.com/docs/integrations/chat/google_vertex_ai)


=== "Azure"
    Install the langchain-openai package

    ```bash
    pip install langchain-openai
    ```

    Ensure you have your Azure OpenAI key ready and available in your environment.

    ```python
    import os
    os.environ["AZURE_OPENAI_API_KEY"] = "your-azure-openai-key"

    # other configuration
    azure_config = {
        "base_url": "",  # your endpoint
        "model_deployment": "",  # your model deployment name
        "model_name": "",  # your model name
        "embedding_deployment": "",  # your embedding deployment name
        "embedding_name": "",  # your embedding name
    }

    ```

    Define your LLMs and wrap them in `LangchainLLMWrapper` so that it can be used with ragas.

    ```python
    from langchain_openai import AzureChatOpenAI
    from langchain_openai import AzureOpenAIEmbeddings
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper
    generator_llm = LangchainLLMWrapper(AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_endpoint=azure_configs["base_url"],
        azure_deployment=azure_configs["model_deployment"],
        model=azure_configs["model_name"],
        validate_base_url=False,
    ))

    # init the embeddings for answer_relevancy, answer_correctness and answer_similarity
    generator_embeddings = LangchainEmbeddingsWrapper(AzureOpenAIEmbeddings(
        openai_api_version="2023-05-15",
        azure_endpoint=azure_configs["base_url"],
        azure_deployment=azure_configs["embedding_deployment"],
        model=azure_configs["embedding_name"],
    ))
    ```

    If you want more information on how to use other Azure services, please refer to the [langchain-azure](https://python.langchain.com/docs/integrations/chat/azure_chat_openai/) documentation.

=== "Others"
    If you are using a different LLM provider and using LangChain to interact with it, you can wrap your LLM in `LangchainLLMWrapper` so that it can be used with ragas.

    ```python
    from ragas.llms import LangchainLLMWrapper
    generator_llm = LangchainLLMWrapper(your_llm_instance)
    ```

    For a more detailed guide, checkout [the guide on customizing models](../../howtos/customizations/customize_models.md).

    If you using LlamaIndex, you can use the `LlamaIndexLLMWrapper` to wrap your LLM so that it can be used with ragas.

    ```python
    from ragas.llms import LlamaIndexLLMWrapper
    generator_llm = LlamaIndexLLMWrapper(your_llm_instance)
    ```

    For more information on how to use LlamaIndex, please refer to the [LlamaIndex Integration guide](./../../howtos/integrations/_llamaindex.md).

    If your still not able use Ragas with your favorite LLM provider, please let us know by by commenting on this [issue](https://github.com/vibrantlabsai/ragas/issues/1617) and we'll add support for it 🙂.


```python
from ragas.testset import TestsetGenerator
from ragas.llms import llm_factory

tg = TestsetGenerator(llm=llm_factory(), knowledge_graph=kg)
# generating a testset
testset = tg.generate(testset_size=10, token_usage_parser=get_token_usage_for_openai)
```

```
# total cost for the generation process
testset.total_cost(cost_per_input_token=5 / 1e6, cost_per_output_token=15 / 1e6)
```

Output

```
0.20967000000000002
```

November 28, 2025




November 28, 2025




GitHub

Back to top