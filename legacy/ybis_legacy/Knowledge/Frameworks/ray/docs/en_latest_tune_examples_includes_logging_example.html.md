Logging Example — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Logging Example[#](#logging-example "Link to this heading")

```
#!/usr/bin/env python

import argparse
import time

from ray import tune
from ray.tune.logger import LoggerCallback


class TestLoggerCallback(LoggerCallback):
    def on_trial_result(self, iteration, trials, trial, result, **info):
        print(f"TestLogger for trial {trial}: {result}")


def trial_str_creator(trial):
    return "{}_{}_123".format(trial.trainable_name, trial.trial_id)


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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--smoke-test", action="store_true", help="Finish quickly for testing"
    )
    args, _ = parser.parse_known_args()

    tuner = tune.Tuner(
        easy_objective,
        run_config=tune.RunConfig(
            name="hyperband_test",
            callbacks=[TestLoggerCallback()],
            stop={"training_iteration": 1 if args.smoke_test else 100},
        ),
        tune_config=tune.TuneConfig(
            metric="mean_loss",
            mode="min",
            num_samples=5,
            trial_name_creator=trial_str_creator,
            trial_dirname_creator=trial_str_creator,
        ),
        param_space={
            "steps": 100,
            "width": tune.randint(10, 100),
            "height": tune.loguniform(10, 100),
        },
    )
    results = tuner.fit()

    print("Best hyperparameters: ", results.get_best_result().config)
```

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/tune/examples/includes/logging_example.rst)