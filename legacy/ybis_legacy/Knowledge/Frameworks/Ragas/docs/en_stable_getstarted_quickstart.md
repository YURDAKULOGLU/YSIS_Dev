Quick Start - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#quick-start-get-evaluations-running-in-a-flash)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Quick Start: Get Evaluations Running in a Flash

Get started with Ragas in minutes. Create a complete evaluation project with just a few commands.

## Step 1: Create Your Project

Choose one of the following methods:

uvx (Recommended)Install Ragas First

No installation required. `uvx` automatically downloads and runs ragas:

```
uvx ragas quickstart rag_eval
cd rag_eval
```

Install ragas first, then create the project:

```
pip install ragas
ragas quickstart rag_eval
cd rag_eval
```

## Step 2: Install Dependencies

Install the project dependencies:

```
uv sync
```

Or if you prefer `pip`:

```
pip install -e .
```

## Step 3: Set Your API Key

By default, the quickstart example uses OpenAI. Set your API key and you're ready to go. You can also use some other provider with a minor change:

OpenAI (Default)Anthropic ClaudeGoogle GeminiLocal Models (Ollama)Custom / Other Providers

```
export OPENAI_API_KEY="your-openai-key"
```

The quickstart project is already configured to use OpenAI. You're all set!

Set your Anthropic API key:

```
export ANTHROPIC_API_KEY="your-anthropic-key"
```

Then update the LLM initialization in `evals.py`:

```
from anthropic import Anthropic
from ragas.llms import llm_factory

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
llm = llm_factory("claude-3-5-sonnet-20241022", provider="anthropic", client=client)
```

Set up your Google credentials:

```
export GOOGLE_API_KEY="your-google-api-key"
```

Then update the LLM initialization in `evals.py`:

**Option 1: Using Google's Official Library (Recommended)**

```
import google.generativeai as genai
from ragas.llms import llm_factory

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
client = genai.GenerativeModel("gemini-2.0-flash")
llm = llm_factory("gemini-2.0-flash", provider="google", client=client)
# Adapter is auto-detected as "litellm" for google provider
```

For more Gemini options and detailed setup, see the [Google Gemini Integration Guide](../../howtos/integrations/gemini/).

Install and run Ollama locally, then update the LLM initialization in `evals.py`:

```
from openai import OpenAI
from ragas.llms import llm_factory

# Create an OpenAI-compatible client for Ollama
client = OpenAI(
    api_key="ollama",  # Ollama doesn't require a real key
    base_url="http://localhost:11434/v1"
)
llm = llm_factory("mistral", provider="openai", client=client)
```

For any LLM with OpenAI-compatible API:

```
from openai import OpenAI
from ragas.llms import llm_factory

client = OpenAI(
    api_key="your-api-key",
    base_url="https://your-api-endpoint"
)
llm = llm_factory("model-name", provider="openai", client=client)
```

For more details, learn about [LLM integrations](../../concepts/metrics/).

## Project Structure

Your generated project includes:

```
rag_eval/
├── README.md              # Project documentation
├── pyproject.toml         # Project configuration
├── rag.py                 # Your RAG application
├── evals.py               # Evaluation workflow
├── __init__.py            # Makes this a Python package
└── evals/
    ├── datasets/          # Test data files
    ├── experiments/       # Evaluation results
    └── logs/              # Execution logs
```

## Step 4: Run Your Evaluation

Run the evaluation script:

```
uv run python evals.py
```

Or if you installed with `pip`:

```
python evals.py
```

The evaluation will:
- Load test data from the `load_dataset()` function in `evals.py`
- Query your RAG application with test questions
- Evaluate responses
- Display results in the console
- Save results to CSV in the `evals/experiments/` directory

[![](../../_static/imgs/results/rag_eval_result.png)](../../_static/imgs/results/rag_eval_result.png)

Congratulations! You have a complete evaluation setup running. 🎉

---

## Customize Your Evaluation

### Add More Test Cases

Edit the `load_dataset()` function in `evals.py` to add more test questions:

```
from ragas import Dataset

def load_dataset():
    """Load test dataset for evaluation."""
    dataset = Dataset(
        name="test_dataset",
        backend="local/csv",
        root_dir=".",
    )

    data_samples = [
        {
            "question": "What is Ragas?",
            "grading_notes": "Ragas is an evaluation framework for LLM applications",
        },
        {
            "question": "How do metrics work?",
            "grading_notes": "Metrics evaluate the quality and performance of LLM responses",
        },
        # Add more test cases here
    ]

    for sample in data_samples:
        dataset.append(sample)

    dataset.save()
    return dataset
```

### Customize Evaluation Metrics

The template includes a `DiscreteMetric` for custom evaluation logic. You can customize the evaluation by:

1. **Modify the metric prompt** - Change the evaluation criteria
2. **Adjust allowed values** - Update valid output categories
3. **Add more metrics** - Create additional metrics for different aspects

Example of modifying the metric:

```
from ragas.metrics import DiscreteMetric
from ragas.llms import llm_factory

my_metric = DiscreteMetric(
    name="custom_evaluation",
    prompt="Evaluate this response: {response} based on: {context}. Return 'excellent', 'good', or 'poor'.",
    allowed_values=["excellent", "good", "poor"],
)
```

## What's Next?

* **Learn the concepts**: Read the [Evaluate a Simple LLM Application](../evals/) guide for deeper understanding
* **Custom metrics**: [Create your own metrics](../../concepts/metrics/overview/#output-types) using simple decorators
* **Production integration**: [Integrate evaluations into your CI/CD pipeline](../../howtos/)
* **RAG evaluation**: Evaluate [RAG systems](../rag_eval/) with specialized metrics
* **Agent evaluation**: Explore [AI agent evaluation](../../howtos/applications/text2sql/)
* **Test data generation**: [Generate synthetic test datasets](../rag_testset_generation/) for your evaluations

## Getting Help

* 📚 [Full Documentation](https://docs.ragas.io/)
* 💬 [Join our Discord Community](https://discord.gg/5djav8GGNZ)
* 🐛 [Report Issues](https://github.com/vibrantlabsai/ragas/issues)

December 12, 2025




November 28, 2025




GitHub

Back to top