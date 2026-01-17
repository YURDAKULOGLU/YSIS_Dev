Evaluate an AI Agent - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#evaluate-an-ai-agent)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Evaluate an AI agent

This tutorial demonstrates how to evaluate an AI agent using Ragas, specifically a mathematical agent that can solve complex expressions using atomic operations and function calling capabilities. By the end of this tutorial, you will learn how to evaluate and iterate on an agent using evaluation-driven development.

```
graph TD
    A[User Input<br/>Math Expression] --> B[MathToolsAgent]

    subgraph LLM Agent Loop
        B --> D{Need to use a Tool?}
        D -- Yes --> E[Call Tool<br/>add/sub/mul/div]
        E --> F[Tool Result]
        F --> B
        D -- No --> G[Emit Final Answer]
    end

    G --> H[Final Answer]
```

We will start by testing our simple agent that can solve mathematical expressions using atomic operations and function calling capabilities.

```
python -m ragas_examples.agent_evals.agent
```

Next, we will create a few sample expressions and expected outputs for our agent, then convert them to a CSV file.

```
import pandas as pd

dataset = [
    {"expression": "(2 + 3) * (4 - 1)", "expected": 15},
    {"expression": "5 * (6 + 2)", "expected": 40},
    {"expression": "10 - (3 + 2)", "expected": 5},
]

df = pd.DataFrame(dataset)
df.to_csv("datasets/test_dataset.csv", index=False)
```

To evaluate the performance of our agent, we will define a non-LLM metric that compares if our agent's output is within a certain tolerance of the expected output and returns 1/0 based on the comparison.

```
from ragas.metrics import numeric_metric
from ragas.metrics.result import MetricResult

@numeric_metric(name="correctness")
def correctness_metric(prediction: float, actual: float):
    """Calculate correctness of the prediction."""
    if isinstance(prediction, str) and "ERROR" in prediction:
        return 0.0
    result = 1.0 if abs(prediction - actual) < 1e-5 else 0.0
    return MetricResult(value=result, reason=f"Prediction: {prediction}, Actual: {actual}")
```

Next, we will write the experiment loop that will run our agent on the test dataset and evaluate it using the metric, and store the results in a CSV file.

```
from ragas import experiment

@experiment()
async def run_experiment(row):
    expression = row["expression"]
    expected_result = row["expected"]

    # Get the model's prediction
    prediction = math_agent.solve(expression)

    # Calculate the correctness metric
    correctness = correctness_metric.score(prediction=prediction.get("result"), actual=expected_result)

    return {
        "expression": expression,
        "expected_result": expected_result,
        "prediction": prediction.get("result"),
        "log_file": prediction.get("log_file"),
        "correctness": correctness.value
    }
```

Now whenever you make a change to your agent, you can run the experiment and see how it affects the performance of your agent.

## Running the example end to end

1. Set up your OpenAI API key

   ```
   export OPENAI_API_KEY="your_api_key_here"
   ```
2. Run the evaluation

   ```
   python -m ragas_examples.agent_evals.evals
   ```

Voilà! You have successfully evaluated an AI agent using Ragas. You can now view the results by opening the `experiments/experiment_name.csv` file.

November 28, 2025




November 28, 2025

Back to top