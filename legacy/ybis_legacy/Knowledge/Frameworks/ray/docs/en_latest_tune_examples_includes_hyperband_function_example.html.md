HyperBand Function Example — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# HyperBand Function Example[#](#hyperband-function-example "Link to this heading")

```
#!/usr/bin/env python

import argparse
import json
import os
import tempfile

import numpy as np

import ray
from ray import tune
from ray.tune import Checkpoint
from ray.tune.schedulers import HyperBandScheduler


def train_func(config):
    step = 0
    checkpoint = tune.get_checkpoint()
    if checkpoint:
        with checkpoint.as_directory() as checkpoint_dir:
            with open(os.path.join(checkpoint_dir, "checkpoint.json")) as f:
                step = json.load(f)["timestep"] + 1

    for timestep in range(step, 100):
        v = np.tanh(float(timestep) / config.get("width", 1))
        v *= config.get("height", 1)

        # Checkpoint the state of the training every 3 steps
        # Note that this is only required for certain schedulers
        with tempfile.TemporaryDirectory() as temp_checkpoint_dir:
            checkpoint = None
            if timestep % 3 == 0:
                with open(
                    os.path.join(temp_checkpoint_dir, "checkpoint.json"), "w"
                ) as f:
                    json.dump({"timestep": timestep}, f)
                checkpoint = Checkpoint.from_directory(temp_checkpoint_dir)

            # Here we use `episode_reward_mean`, but you can also report other
            # objectives such as loss or accuracy.
            tune.report({"episode_reward_mean": v}, checkpoint=checkpoint)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--smoke-test", action="store_true", help="Finish quickly for testing"
    )
    args, _ = parser.parse_known_args()

    ray.init(num_cpus=4 if args.smoke_test else None)

    # Hyperband early stopping, configured with `episode_reward_mean` as the
    # objective and `training_iteration` as the time unit,
    # which is automatically filled by Tune.
    hyperband = HyperBandScheduler(max_t=200)

    tuner = tune.Tuner(
        train_func,
        run_config=tune.RunConfig(
            name="hyperband_test",
            stop={"training_iteration": 10 if args.smoke_test else 99999},
            failure_config=tune.FailureConfig(
                fail_fast=True,
            ),
        ),
        tune_config=tune.TuneConfig(
            num_samples=20,
            metric="episode_reward_mean",
            mode="max",
            scheduler=hyperband,
        ),
        param_space={"height": tune.uniform(0, 100)},
    )
    results = tuner.fit()
    print("Best hyperparameters found were: ", results.get_best_result().config)
```

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/tune/examples/includes/hyperband_function_example.rst)