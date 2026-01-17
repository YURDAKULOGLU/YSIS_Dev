Asynchronous HyperBand Example — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Asynchronous HyperBand Example[#](#asynchronous-hyperband-example "Link to this heading")

This example demonstrates how to use Ray Tune’s Asynchronous Successive Halving Algorithm (ASHA) scheduler
to efficiently optimize hyperparameters for a machine learning model. ASHA is particularly useful for
large-scale hyperparameter optimization as it can adaptively allocate resources and end
poorly performing trials early.

Requirements: `pip install "ray[tune]"`

```
#!/usr/bin/env python

import argparse
import time
from typing import Any, Dict

from ray import tune
from ray.tune.schedulers import AsyncHyperBandScheduler


def evaluation_fn(step, width, height) -> float:
    # simulate model evaluation
    time.sleep(0.1)
    return (0.1 + width * step / 100) ** (-1) + height * 0.1


def easy_objective(config: Dict[str, Any]) -> None:
    # Config contains the hyperparameters to tune
    width, height = config["width"], config["height"]

    for step in range(config["steps"]):
        # Iterative training function - can be an arbitrary training procedure
        intermediate_score = evaluation_fn(step, width, height)
        # Feed the score back back to Tune.
        tune.report({"iterations": step, "mean_loss": intermediate_score})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AsyncHyperBand optimization example")
    parser.add_argument(
        "--smoke-test", action="store_true", help="Finish quickly for testing"
    )
    args, _ = parser.parse_known_args()

    # AsyncHyperBand enables aggressive early stopping of poorly performing trials
    scheduler = AsyncHyperBandScheduler(
        grace_period=5,  # Minimum training iterations before stopping
        max_t=100,  # Maximum training iterations
    )

    tuner = tune.Tuner(
        tune.with_resources(easy_objective, {"cpu": 1, "gpu": 0}),
        run_config=tune.RunConfig(
            name="asynchyperband_test",
            stop={"training_iteration": 1 if args.smoke_test else 9999},
            verbose=1,
        ),
        tune_config=tune.TuneConfig(
            metric="mean_loss",
            mode="min",
            scheduler=scheduler,
            num_samples=20,  # Number of trials to run
        ),
        param_space={
            "steps": 100,
            "width": tune.uniform(10, 100),
            "height": tune.uniform(0, 100),
        },
    )

    # Run the hyperparameter optimization
    results = tuner.fit()
    print(f"Best hyperparameters found: {results.get_best_result().config}")
```

## See Also[#](#see-also "Link to this heading")

* [ASHA Paper](https://arxiv.org/abs/1810.05934)

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/tune/examples/includes/async_hyperband_example.rst)