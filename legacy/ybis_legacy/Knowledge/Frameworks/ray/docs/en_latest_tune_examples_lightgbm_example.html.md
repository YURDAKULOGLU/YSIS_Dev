Using LightGBM with Tune — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Using LightGBM with Tune[#](#using-lightgbm-with-tune "Link to this heading")

[![try-anyscale-quickstart](../../_static/img/run-on-anyscale.svg)](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=ray-tune-lightgbm_example)
  
[![LightGBM Logo](../../_images/lightgbm_logo.png)](https://lightgbm.readthedocs.io)

This tutorial shows how to use Ray Tune to optimize hyperparameters for a LightGBM model. We’ll use the breast cancer classification dataset from scikit-learn to demonstrate how to:

1. Set up a LightGBM training function with Ray Tune
2. Configure hyperparameter search spaces
3. Use the ASHA scheduler for efficient hyperparameter tuning
4. Report and checkpoint training progress

## Installation[#](#installation "Link to this heading")

First, let’s install the required dependencies:

```
pip install "ray[tune]" lightgbm scikit-learn numpy
```

```
import lightgbm as lgb
import numpy as np
import sklearn.datasets
import sklearn.metrics
from sklearn.model_selection import train_test_split

from ray import tune
from ray.tune.schedulers import ASHAScheduler
from ray.tune.integration.lightgbm import TuneReportCheckpointCallback


def train_breast_cancer(config):

    data, target = sklearn.datasets.load_breast_cancer(return_X_y=True)
    train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.25)
    train_set = lgb.Dataset(train_x, label=train_y)
    test_set = lgb.Dataset(test_x, label=test_y)
    gbm = lgb.train(
        config,
        train_set,
        valid_sets=[test_set],
        valid_names=["eval"],
        callbacks=[
            TuneReportCheckpointCallback(
                {
                    "binary_error": "eval-binary_error",
                    "binary_logloss": "eval-binary_logloss",
                }
            )
        ],
    )
    preds = gbm.predict(test_x)
    pred_labels = np.rint(preds)
    tune.report(
        {
            "mean_accuracy": sklearn.metrics.accuracy_score(test_y, pred_labels),
            "done": True,
        }
    )


if __name__ == "__main__":
    config = {
        "objective": "binary",
        "metric": ["binary_error", "binary_logloss"],
        "verbose": -1,
        "boosting_type": tune.grid_search(["gbdt", "dart"]),
        "num_leaves": tune.randint(10, 1000),
        "learning_rate": tune.loguniform(1e-8, 1e-1),
    }

    tuner = tune.Tuner(
        train_breast_cancer,
        tune_config=tune.TuneConfig(
            metric="binary_error",
            mode="min",
            scheduler=ASHAScheduler(),
            num_samples=2,
        ),
        param_space=config,
    )
    results = tuner.fit()

    print(f"Best hyperparameters found were: {results.get_best_result().config}")
```

Show code cell output
Hide code cell output

### Tune Status

|  |  |
| --- | --- |
| Current time: | 2025-02-18 17:33:55 |
| Running for: | 00:00:01.27 |
| Memory: | 25.8/36.0 GiB |

### System Info

Using AsyncHyperBand: num\_stopped=4  
Bracket: Iter 64.000: -0.1048951048951049 | Iter 16.000: -0.3076923076923077 | Iter 4.000: -0.3076923076923077 | Iter 1.000: -0.32342657342657344  
Logical resource usage: 1.0/12 CPUs, 0/0 GPUs

### Trial Status

| Trial name | status | loc | boosting\_type | learning\_rate | num\_leaves | iter | total time (s) | binary\_error | binary\_logloss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train\_breast\_cancer\_945ea\_00000 | TERMINATED | 127.0.0.1:26189 | gbdt | 0.00372129 | 622 | 100 | 0.0507247 | 0.104895 | 0.45487 |
| train\_breast\_cancer\_945ea\_00001 | TERMINATED | 127.0.0.1:26191 | dart | 0.0065691 | 998 | 1 | 0.013751 | 0.391608 | 0.665636 |
| train\_breast\_cancer\_945ea\_00002 | TERMINATED | 127.0.0.1:26190 | gbdt | 1.17012e-07 | 995 | 1 | 0.0146749 | 0.412587 | 0.68387 |
| train\_breast\_cancer\_945ea\_00003 | TERMINATED | 127.0.0.1:26192 | dart | 0.000194983 | 53 | 1 | 0.00605583 | 0.328671 | 0.6405 |

```
2025-02-18 17:33:55,300	INFO tune.py:1009 -- Wrote the latest version of all result files and experiment state to '/Users/rdecal/ray_results/train_breast_cancer_2025-02-18_17-33-54' in 0.0035s.
2025-02-18 17:33:55,302	INFO tune.py:1041 -- Total run time: 1.28 seconds (1.27 seconds for the tuning loop).
```

```
Best hyperparameters found were: {'objective': 'binary', 'metric': ['binary_error', 'binary_logloss'], 'verbose': -1, 'boosting_type': 'gbdt', 'num_leaves': 622, 'learning_rate': 0.003721286118355498}
```

This should give an output like:

```
Best hyperparameters found were: {'objective': 'binary', 'metric': ['binary_error', 'binary_logloss'], 'verbose': -1, 'boosting_type': 'gbdt', 'num_leaves': 622, 'learning_rate': 0.003721286118355498}
```

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/tune/examples/lightgbm_example.ipynb)