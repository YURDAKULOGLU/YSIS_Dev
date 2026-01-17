tune\_basic\_example — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# tune\_basic\_example[#](#tune-basic-example "Link to this heading")

```
"""This example demonstrates basic Ray Tune random search and grid search."""
import time

import ray
from ray import tune


def evaluation_fn(step, width, height):
    time.sleep(0.1)
    return (0.1 + width * step / 100) ** (-1) + height * 0.1


def easy_objective(config):
    # Hyperparameters
    width, height = config["width"], config["height"]

    for step in range(config["steps"]):
        # Iterative training function - can be any arbitrary training procedure
        intermediate_score = evaluation_fn(step, width, height)
        # Feed the score back back to Tune.
        tune.report({"iterations": step, "mean_loss": intermediate_score})


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--smoke-test", action="store_true", help="Finish quickly for testing"
    )
    args, _ = parser.parse_known_args()

    ray.init(configure_logging=False)

    # This will do a grid search over the `activation` parameter. This means
    # that each of the two values (`relu` and `tanh`) will be sampled once
    # for each sample (`num_samples`). We end up with 2 * 50 = 100 samples.
    # The `width` and `height` parameters are sampled randomly.
    # `steps` is a constant parameter.

    tuner = tune.Tuner(
        easy_objective,
        tune_config=tune.TuneConfig(
            metric="mean_loss",
            mode="min",
            num_samples=5 if args.smoke_test else 50,
        ),
        param_space={
            "steps": 5 if args.smoke_test else 100,
            "width": tune.uniform(0, 20),
            "height": tune.uniform(-100, 100),
            "activation": tune.grid_search(["relu", "tanh"]),
        },
    )
    results = tuner.fit()

    print("Best hyperparameters found were: ", results.get_best_result().config)
```

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/tune/examples/includes/tune_basic_example.rst)