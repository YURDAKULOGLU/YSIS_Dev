Running Tune experiments with Optuna — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Running Tune experiments with Optuna[#](#running-tune-experiments-with-optuna "Link to this heading")

[![try-anyscale-quickstart](../../_static/img/run-on-anyscale.svg)](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=ray-tune-optuna_example)
  

In this tutorial we introduce Optuna, while running a simple Ray Tune experiment. Tune’s Search Algorithms integrate with Optuna and, as a result, allow you to seamlessly scale up a Optuna optimization process - without sacrificing performance.

Similar to Ray Tune, Optuna is an automatic hyperparameter optimization software framework, particularly designed for machine learning. It features an imperative (“how” over “what” emphasis), define-by-run style user API. With Optuna, a user has the ability to dynamically construct the search spaces for the hyperparameters. Optuna falls in the domain of “derivative-free optimization” and “black-box optimization”.

In this example we minimize a simple objective to briefly demonstrate the usage of Optuna with Ray Tune via `OptunaSearch`, including examples of conditional search spaces (string together relationships between hyperparameters), and the multi-objective problem (measure trade-offs among all important metrics). It’s useful to keep in mind that despite the emphasis on machine learning experiments, Ray Tune optimizes any implicit or explicit objective. Here we assume `optuna>=3.0.0` library is installed. To learn more, please refer to [Optuna website](https://optuna.org/).

Please note that sophisticated schedulers, such as `AsyncHyperBandScheduler`, may not work correctly with multi-objective optimization, since they typically expect a scalar score to compare fitness among trials.

## Prerequisites[#](#prerequisites "Link to this heading")

```
# !pip install "ray[tune]"
!pip install -q "optuna>=3.0.0"
```

Next, import the necessary libraries:

```
import time
from typing import Dict, Optional, Any

import ray
from ray import tune
from ray.tune.search import ConcurrencyLimiter
from ray.tune.search.optuna import OptunaSearch
```

```
ray.init(configure_logging=False)  # initialize Ray
```

Show code cell output
Hide code cell output

Let’s start by defining a simple evaluation function.
An explicit math formula is queried here for demonstration, yet in practice this is typically a black-box function– e.g. the performance results after training an ML model.
We artificially sleep for a bit (`0.1` seconds) to simulate a long-running ML experiment.
This setup assumes that we’re running multiple `step`s of an experiment while tuning three hyperparameters,
namely `width`, `height`, and `activation`.

```
def evaluate(step, width, height, activation):
    time.sleep(0.1)
    activation_boost = 10 if activation=="relu" else 0
    return (0.1 + width * step / 100) ** (-1) + height * 0.1 + activation_boost
```

Next, our `objective` function to be optimized takes a Tune `config`, evaluates the `score` of your experiment in a training loop,
and uses `tune.report` to report the `score` back to Tune.

```
def objective(config):
    for step in range(config["steps"]):
        score = evaluate(step, config["width"], config["height"], config["activation"])
        tune.report({"iterations": step, "mean_loss": score})
```

Next we define a search space. The critical assumption is that the optimal hyperparameters live within this space. Yet, if the space is very large, then those hyperparameters may be difficult to find in a short amount of time.

The simplest case is a search space with independent dimensions. In this case, a config dictionary will suffice.

```
search_space = {
    "steps": 100,
    "width": tune.uniform(0, 20),
    "height": tune.uniform(-100, 100),
    "activation": tune.choice(["relu", "tanh"]),
}
```

Here we define the Optuna search algorithm:

```
algo = OptunaSearch()
```

We also constrain the number of concurrent trials to `4` with a `ConcurrencyLimiter`.

```
algo = ConcurrencyLimiter(algo, max_concurrent=4)
```

The number of samples is the number of hyperparameter combinations that will be tried out. This Tune run is set to `1000` samples.
(you can decrease this if it takes too long on your machine).

```
num_samples = 1000
```

Finally, we run the experiment to `"min"`imize the “mean\_loss” of the `objective` by searching `search_space` via `algo`, `num_samples` times. This previous sentence is fully characterizes the search problem we aim to solve. With this in mind, notice how efficient it is to execute `tuner.fit()`.

```
tuner = tune.Tuner(
    objective,
    tune_config=tune.TuneConfig(
        metric="mean_loss",
        mode="min",
        search_alg=algo,
        num_samples=num_samples,
    ),
    param_space=search_space,
)
results = tuner.fit()
```

Show code cell output
Hide code cell output

### Tune Status

|  |  |
| --- | --- |
| Current time: | 2025-02-10 18:06:12 |
| Running for: | 00:00:35.68 |
| Memory: | 22.7/36.0 GiB |

### System Info

Using FIFO scheduling algorithm.  
Logical resource usage: 1.0/12 CPUs, 0/0 GPUs

### Trial Status

| Trial name | status | loc | activation | height | width | loss | iter | total time (s) | iterations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| objective\_989a402c | TERMINATED | 127.0.0.1:42307 | relu | 6.57558 | 8.66313 | 10.7728 | 100 | 10.3642 | 99 |
| objective\_d99d28c6 | TERMINATED | 127.0.0.1:42321 | tanh | 51.2103 | 19.2804 | 5.17314 | 100 | 10.3775 | 99 |
| objective\_ce34b92b | TERMINATED | 127.0.0.1:42323 | tanh | -49.4554 | 17.2683 | -4.88739 | 100 | 10.3741 | 99 |
| objective\_f650ea5f | TERMINATED | 127.0.0.1:42332 | tanh | 20.6147 | 3.19539 | 2.3679 | 100 | 10.3804 | 99 |
| objective\_e72e976e | TERMINATED | 127.0.0.1:42356 | relu | -12.5302 | 3.45152 | 9.03132 | 100 | 10.372 | 99 |
| objective\_d00b4e1a | TERMINATED | 127.0.0.1:42362 | tanh | 65.8592 | 3.14335 | 6.89726 | 100 | 10.3776 | 99 |
| objective\_30c6ec86 | TERMINATED | 127.0.0.1:42367 | tanh | -82.0713 | 14.2595 | -8.13679 | 100 | 10.3755 | 99 |
| objective\_691ce63c | TERMINATED | 127.0.0.1:42368 | tanh | 29.406 | 2.21881 | 3.37602 | 100 | 10.3653 | 99 |
| objective\_3051162c | TERMINATED | 127.0.0.1:42404 | relu | 61.1787 | 12.9673 | 16.1952 | 100 | 10.3885 | 99 |
| objective\_04a38992 | TERMINATED | 127.0.0.1:42405 | relu | 6.28688 | 11.4537 | 10.7161 | 100 | 10.4051 | 99 |

And now we have the hyperparameters found to minimize the mean loss.

```
print("Best hyperparameters found were: ", results.get_best_result().config)
```

```
Best hyperparameters found were:  {'steps': 100, 'width': 14.259467682064852, 'height': -82.07132174642958, 'activation': 'tanh'}
```

## Providing an initial set of hyperparameters[#](#providing-an-initial-set-of-hyperparameters "Link to this heading")

While defining the search algorithm, we may choose to provide an initial set of hyperparameters that we believe are especially promising or informative, and
pass this information as a helpful starting point for the `OptunaSearch` object.

```
initial_params = [
    {"width": 1, "height": 2, "activation": "relu"},
    {"width": 4, "height": 2, "activation": "relu"},
]
```

Now the `search_alg` built using `OptunaSearch` takes `points_to_evaluate`.

```
searcher = OptunaSearch(points_to_evaluate=initial_params)
algo = ConcurrencyLimiter(searcher, max_concurrent=4)
```

And run the experiment with initial hyperparameter evaluations:

```
tuner = tune.Tuner(
    objective,
    tune_config=tune.TuneConfig(
        metric="mean_loss",
        mode="min",
        search_alg=algo,
        num_samples=num_samples,
    ),
    param_space=search_space,
)
results = tuner.fit()
```

Show code cell output
Hide code cell output

### Tune Status

|  |  |
| --- | --- |
| Current time: | 2025-02-10 18:06:47 |
| Running for: | 00:00:35.44 |
| Memory: | 22.7/36.0 GiB |

### System Info

Using FIFO scheduling algorithm.  
Logical resource usage: 1.0/12 CPUs, 0/0 GPUs

### Trial Status

| Trial name | status | loc | activation | height | width | loss | iter | total time (s) | iterations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| objective\_1d2e715f | TERMINATED | 127.0.0.1:42435 | relu | 2 | 1 | 11.1174 | 100 | 10.3556 | 99 |
| objective\_f7c2aed0 | TERMINATED | 127.0.0.1:42436 | relu | 2 | 4 | 10.4463 | 100 | 10.3702 | 99 |
| objective\_09dcce33 | TERMINATED | 127.0.0.1:42438 | tanh | 28.5547 | 17.4195 | 2.91312 | 100 | 10.3483 | 99 |
| objective\_b9955517 | TERMINATED | 127.0.0.1:42443 | tanh | -73.0995 | 13.8859 | -7.23773 | 100 | 10.3682 | 99 |
| objective\_d81ebd5c | TERMINATED | 127.0.0.1:42464 | relu | -1.86597 | 1.46093 | 10.4601 | 100 | 10.3969 | 99 |
| objective\_3f0030e7 | TERMINATED | 127.0.0.1:42465 | relu | 38.7166 | 1.3696 | 14.5585 | 100 | 10.3741 | 99 |
| objective\_86bf6402 | TERMINATED | 127.0.0.1:42470 | tanh | 40.269 | 5.13015 | 4.21999 | 100 | 10.3769 | 99 |
| objective\_75d06a83 | TERMINATED | 127.0.0.1:42471 | tanh | -11.2824 | 3.10251 | -0.812933 | 100 | 10.3695 | 99 |
| objective\_0d197811 | TERMINATED | 127.0.0.1:42496 | tanh | 91.7076 | 15.1032 | 9.2372 | 100 | 10.3631 | 99 |
| objective\_5156451f | TERMINATED | 127.0.0.1:42497 | tanh | 58.9282 | 3.96315 | 6.14136 | 100 | 10.4732 | 99 |

We take another look at the optimal hyperparameters.

```
print("Best hyperparameters found were: ", results.get_best_result().config)
```

```
Best hyperparameters found were:  {'steps': 100, 'width': 13.885889617119432, 'height': -73.09947583621019, 'activation': 'tanh'}
```

## Conditional search spaces[#](#conditional-search-spaces "Link to this heading")

Sometimes we may want to build a more complicated search space that has conditional dependencies on other hyperparameters. In this case, we pass a define-by-run function to the `search_alg` argument in `ray.tune()`.

```
def define_by_run_func(trial) -> Optional[Dict[str, Any]]:
    """Define-by-run function to construct a conditional search space.

    Ensure no actual computation takes place here. That should go into
    the trainable passed to ``Tuner()`` (in this example, that's
    ``objective``).

    For more information, see https://optuna.readthedocs.io/en/stable\
    /tutorial/10_key_features/002_configurations.html

    Args:
        trial: Optuna Trial object
        
    Returns:
        Dict containing constant parameters or None
    """

    activation = trial.suggest_categorical("activation", ["relu", "tanh"])

    # Define-by-run allows for conditional search spaces.
    if activation == "relu":
        trial.suggest_float("width", 0, 20)
        trial.suggest_float("height", -100, 100)
    else:
        trial.suggest_float("width", -1, 21)
        trial.suggest_float("height", -101, 101)
        
    # Return all constants in a dictionary.
    return {"steps": 100}
```

As before, we create the `search_alg` from `OptunaSearch` and `ConcurrencyLimiter`, this time we define the scope of search via the `space` argument and provide no initialization. We also must specific metric and mode when using `space`.

```
searcher = OptunaSearch(space=define_by_run_func, metric="mean_loss", mode="min")
algo = ConcurrencyLimiter(searcher, max_concurrent=4)
```

```
[I 2025-02-10 18:06:47,670] A new study created in memory with name: optuna
```

Running the experiment with a define-by-run search space:

```
tuner = tune.Tuner(
    objective,
    tune_config=tune.TuneConfig(
        search_alg=algo,
        num_samples=num_samples,
    ),
)
results = tuner.fit()
```

Show code cell output
Hide code cell output

### Tune Status

|  |  |
| --- | --- |
| Current time: | 2025-02-10 18:07:23 |
| Running for: | 00:00:35.58 |
| Memory: | 22.9/36.0 GiB |

### System Info

Using FIFO scheduling algorithm.  
Logical resource usage: 1.0/12 CPUs, 0/0 GPUs

### Trial Status

| Trial name | status | loc | activation | height | steps | width | loss | iter | total time (s) | iterations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| objective\_48aa8fed | TERMINATED | 127.0.0.1:42529 | relu | -76.595 | 100 | 9.90896 | 2.44141 | 100 | 10.3957 | 99 |
| objective\_5f395194 | TERMINATED | 127.0.0.1:42531 | relu | -34.1447 | 100 | 12.9999 | 6.66263 | 100 | 10.3823 | 99 |
| objective\_e64a7441 | TERMINATED | 127.0.0.1:42532 | relu | -50.3172 | 100 | 3.95399 | 5.21738 | 100 | 10.3839 | 99 |
| objective\_8e668790 | TERMINATED | 127.0.0.1:42537 | tanh | 30.9768 | 100 | 16.22 | 3.15957 | 100 | 10.3818 | 99 |
| objective\_78ca576b | TERMINATED | 127.0.0.1:42559 | relu | 80.5037 | 100 | 0.906139 | 19.0533 | 100 | 10.3731 | 99 |
| objective\_4cd9e37a | TERMINATED | 127.0.0.1:42560 | relu | 77.0988 | 100 | 8.43807 | 17.8282 | 100 | 10.3881 | 99 |
| objective\_a40498d5 | TERMINATED | 127.0.0.1:42565 | tanh | -24.0393 | 100 | 12.7274 | -2.32519 | 100 | 10.4031 | 99 |
| objective\_43e7ea7e | TERMINATED | 127.0.0.1:42566 | tanh | -92.349 | 100 | 15.8595 | -9.17161 | 100 | 10.4602 | 99 |
| objective\_cb92227e | TERMINATED | 127.0.0.1:42591 | relu | 3.58988 | 100 | 17.3259 | 10.417 | 100 | 10.3817 | 99 |
| objective\_abed5125 | TERMINATED | 127.0.0.1:42608 | tanh | 86.0127 | 100 | 11.2746 | 8.69007 | 100 | 10.3995 | 99 |

We take a look again at the optimal hyperparameters.

```
print("Best hyperparameters for loss found were: ", results.get_best_result("mean_loss", "min").config)
```

```
Best hyperparameters for loss found were:  {'activation': 'tanh', 'width': 15.859495323836288, 'height': -92.34898015005697, 'steps': 100}
```

## Multi-objective optimization[#](#multi-objective-optimization "Link to this heading")

Finally, let’s take a look at the multi-objective case. This permits us to optimize multiple metrics at once, and organize our results based on the different objectives.

```
def multi_objective(config):
    # Hyperparameters
    width, height = config["width"], config["height"]

    for step in range(config["steps"]):
        # Iterative training function - can be any arbitrary training procedure
        intermediate_score = evaluate(step, config["width"], config["height"], config["activation"])
        # Feed the score back back to Tune.
        tune.report({
           "iterations": step, "loss": intermediate_score, "gain": intermediate_score * width
        })
```

We define the `OptunaSearch` object this time with metric and mode as list arguments.

```
searcher = OptunaSearch(metric=["loss", "gain"], mode=["min", "max"])
algo = ConcurrencyLimiter(searcher, max_concurrent=4)

tuner = tune.Tuner(
    multi_objective,
    tune_config=tune.TuneConfig(
        search_alg=algo,
        num_samples=num_samples,
    ),
    param_space=search_space
)
results = tuner.fit();
```

Show code cell output
Hide code cell output

### Tune Status

|  |  |
| --- | --- |
| Current time: | 2025-02-10 18:07:58 |
| Running for: | 00:00:35.27 |
| Memory: | 22.7/36.0 GiB |

### System Info

Using FIFO scheduling algorithm.  
Logical resource usage: 1.0/12 CPUs, 0/0 GPUs

### Trial Status

| Trial name | status | loc | activation | height | width | iter | total time (s) | iterations | loss | gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| multi\_objective\_0534ec01 | TERMINATED | 127.0.0.1:42659 | tanh | 18.3209 | 8.1091 | 100 | 10.3653 | 99 | 1.95513 | 15.8543 |
| multi\_objective\_d3a487a7 | TERMINATED | 127.0.0.1:42660 | relu | -67.8896 | 2.58816 | 100 | 10.3682 | 99 | 3.58666 | 9.28286 |
| multi\_objective\_f481c3db | TERMINATED | 127.0.0.1:42665 | relu | 46.6439 | 19.5326 | 100 | 10.3677 | 99 | 14.7158 | 287.438 |
| multi\_objective\_74a41d72 | TERMINATED | 127.0.0.1:42666 | tanh | -31.9508 | 11.413 | 100 | 10.3685 | 99 | -3.10735 | -35.4643 |
| multi\_objective\_d673b1ae | TERMINATED | 127.0.0.1:42695 | relu | 83.6004 | 5.04972 | 100 | 10.3494 | 99 | 18.5561 | 93.7034 |
| multi\_objective\_25ddc340 | TERMINATED | 127.0.0.1:42701 | relu | -81.7161 | 4.45303 | 100 | 10.382 | 99 | 2.05019 | 9.12955 |
| multi\_objective\_f8554c17 | TERMINATED | 127.0.0.1:42702 | tanh | 43.5854 | 6.84585 | 100 | 10.3638 | 99 | 4.50394 | 30.8333 |
| multi\_objective\_a144e315 | TERMINATED | 127.0.0.1:42707 | tanh | 39.8075 | 19.1985 | 100 | 10.3706 | 99 | 4.03309 | 77.4292 |
| multi\_objective\_50540842 | TERMINATED | 127.0.0.1:42739 | relu | 75.2805 | 11.4041 | 100 | 10.3529 | 99 | 17.6158 | 200.893 |
| multi\_objective\_f322a9e3 | TERMINATED | 127.0.0.1:42740 | relu | -51.3587 | 5.31683 | 100 | 10.3756 | 99 | 5.05057 | 26.853 |

Now there are two hyperparameter sets for the two objectives.

```
print("Best hyperparameters for loss found were: ", results.get_best_result("loss", "min").config)
print("Best hyperparameters for gain found were: ", results.get_best_result("gain", "max").config)
```

```
Best hyperparameters for loss found were:  {'steps': 100, 'width': 11.41302483988651, 'height': -31.950786209072476, 'activation': 'tanh'}
Best hyperparameters for gain found were:  {'steps': 100, 'width': 19.532566002677832, 'height': 46.643925051045784, 'activation': 'relu'}
```

We can mix-and-match the use of initial hyperparameter evaluations, conditional search spaces via define-by-run functions, and multi-objective tasks. This is also true of scheduler usage, with the exception of multi-objective optimization– schedulers typically rely on a single scalar score, rather than the two scores we use here: loss, gain.

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/tune/examples/optuna_example.ipynb)