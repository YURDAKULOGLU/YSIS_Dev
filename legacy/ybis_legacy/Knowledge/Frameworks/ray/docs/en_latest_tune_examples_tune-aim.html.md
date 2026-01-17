Using Aim with Tune — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Using Aim with Tune[#](#using-aim-with-tune "Link to this heading")

[![try-anyscale-quickstart](../../_static/img/run-on-anyscale.svg)](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=tune-aim)
  

[Aim](https://aimstack.io) is an easy-to-use and supercharged open-source experiment tracker.
Aim logs your training runs, enables a well-designed UI to compare them, and provides an API to query them programmatically.

[![Aim](../../_images/aim_logo_full.png)](https://aimstack.io)

Ray Tune currently offers built-in integration with Aim.
The [AimLoggerCallback](#tune-aim-logger) automatically logs metrics that are reported to Tune by using the Aim API.

## Logging Tune Hyperparameter Configurations and Results to Aim[#](#logging-tune-hyperparameter-configurations-and-results-to-aim "Link to this heading")

The following example demonstrates how the `AimLoggerCallback` can be used in a Tune experiment.
Begin by installing and importing the necessary modules:

```
%pip install aim
%pip install ray[tune]
```

```
import numpy as np

import ray
from ray import tune
from ray.tune.logger.aim import AimLoggerCallback
```

Next, define a simple `train_function`, which is a [`Trainable`](../api/trainable.html#trainable-docs) that reports a loss to Tune.
The objective function itself is not important for this example, as our main focus is on the integration with Aim.

```
def train_function(config):
    for _ in range(50):
        loss = config["mean"] + config["sd"] * np.random.randn()
        tune.report({"loss": loss})
```

Here is an example of how you can use the `AimLoggerCallback` with simple grid-search Tune experiment.
The logger will log each of the 9 grid-search trials as separate Aim runs.

```
tuner = tune.Tuner(
    train_function,
    run_config=tune.RunConfig(
        callbacks=[AimLoggerCallback()],
        storage_path="/tmp/ray_results",
        name="aim_example",
    ),
    param_space={
        "mean": tune.grid_search([1, 2, 3, 4, 5, 6, 7, 8, 9]),
        "sd": tune.uniform(0.1, 0.9),
    },
    tune_config=tune.TuneConfig(
        metric="loss",
        mode="min",
    ),
)
tuner.fit()
```

```
2023-02-07 00:04:11,228	INFO worker.py:1544 -- Started a local Ray instance. View the dashboard at http://127.0.0.1:8265
```

### Tune Status

|  |  |
| --- | --- |
| Current time: | 2023-02-07 00:04:19 |
| Running for: | 00:00:06.86 |
| Memory: | 32.8/64.0 GiB |

### System Info

Using FIFO scheduling algorithm.  
Resources requested: 0/10 CPUs, 0/0 GPUs, 0.0/26.93 GiB heap, 0.0/2.0 GiB objects

### Trial Status

| Trial name | status | loc | mean | sd | iter | total time (s) | loss |
| --- | --- | --- | --- | --- | --- | --- | --- |
| train\_function\_01a3b\_00000 | TERMINATED | 127.0.0.1:10277 | 1 | 0.385428 | 50 | 4.48031 | 1.01928 |
| train\_function\_01a3b\_00001 | TERMINATED | 127.0.0.1:10296 | 2 | 0.819716 | 50 | 2.97272 | 3.01491 |
| train\_function\_01a3b\_00002 | TERMINATED | 127.0.0.1:10301 | 3 | 0.769197 | 50 | 2.39572 | 3.87155 |
| train\_function\_01a3b\_00003 | TERMINATED | 127.0.0.1:10307 | 4 | 0.29466 | 50 | 2.41568 | 4.1507 |
| train\_function\_01a3b\_00004 | TERMINATED | 127.0.0.1:10313 | 5 | 0.152208 | 50 | 1.68383 | 5.10225 |
| train\_function\_01a3b\_00005 | TERMINATED | 127.0.0.1:10321 | 6 | 0.879814 | 50 | 1.54015 | 6.20238 |
| train\_function\_01a3b\_00006 | TERMINATED | 127.0.0.1:10329 | 7 | 0.487499 | 50 | 1.44706 | 7.79551 |
| train\_function\_01a3b\_00007 | TERMINATED | 127.0.0.1:10333 | 8 | 0.639783 | 50 | 1.4261 | 7.94189 |
| train\_function\_01a3b\_00008 | TERMINATED | 127.0.0.1:10341 | 9 | 0.12285 | 50 | 1.07701 | 8.82304 |

### Trial Progress

| Trial name | date | done | episodes\_total | experiment\_id | experiment\_tag | hostname | iterations\_since\_restore | loss | node\_ip | pid | time\_since\_restore | time\_this\_iter\_s | time\_total\_s | timestamp | timesteps\_since\_restore | timesteps\_total | training\_iteration | trial\_id | warmup\_time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train\_function\_01a3b\_00000 | 2023-02-07\_00-04-18 | True |  | c8447fdceea6436c9edd6f030a5b1d82 | 0\_mean=1,sd=0.3854 | Justins-MacBook-Pro-16 | 50 | 1.01928 | 127.0.0.1 | 10277 | 4.48031 | 0.013865 | 4.48031 | 1675757058 | 0 |  | 50 | 01a3b\_00000 | 0.00264072 |
| train\_function\_01a3b\_00001 | 2023-02-07\_00-04-18 | True |  | 7dd6d3ee24244a0885b354c285064728 | 1\_mean=2,sd=0.8197 | Justins-MacBook-Pro-16 | 50 | 3.01491 | 127.0.0.1 | 10296 | 2.97272 | 0.0584073 | 2.97272 | 1675757058 | 0 |  | 50 | 01a3b\_00001 | 0.0316792 |
| train\_function\_01a3b\_00002 | 2023-02-07\_00-04-18 | True |  | e3da49ebad034c4b8fdaf0aa87927b1a | 2\_mean=3,sd=0.7692 | Justins-MacBook-Pro-16 | 50 | 3.87155 | 127.0.0.1 | 10301 | 2.39572 | 0.0695491 | 2.39572 | 1675757058 | 0 |  | 50 | 01a3b\_00002 | 0.0315411 |
| train\_function\_01a3b\_00003 | 2023-02-07\_00-04-18 | True |  | 95c60c4f67c4481ebccff25b0a49e75d | 3\_mean=4,sd=0.2947 | Justins-MacBook-Pro-16 | 50 | 4.1507 | 127.0.0.1 | 10307 | 2.41568 | 0.0175381 | 2.41568 | 1675757058 | 0 |  | 50 | 01a3b\_00003 | 0.0310779 |
| train\_function\_01a3b\_00004 | 2023-02-07\_00-04-18 | True |  | a216253cb41e47caa229e65488deb019 | 4\_mean=5,sd=0.1522 | Justins-MacBook-Pro-16 | 50 | 5.10225 | 127.0.0.1 | 10313 | 1.68383 | 0.064441 | 1.68383 | 1675757058 | 0 |  | 50 | 01a3b\_00004 | 0.00450182 |
| train\_function\_01a3b\_00005 | 2023-02-07\_00-04-18 | True |  | 23834104277f476cb99d9c696281fceb | 5\_mean=6,sd=0.8798 | Justins-MacBook-Pro-16 | 50 | 6.20238 | 127.0.0.1 | 10321 | 1.54015 | 0.00910306 | 1.54015 | 1675757058 | 0 |  | 50 | 01a3b\_00005 | 0.0480251 |
| train\_function\_01a3b\_00006 | 2023-02-07\_00-04-18 | True |  | 15f650121df747c3bd2720481d47b265 | 6\_mean=7,sd=0.4875 | Justins-MacBook-Pro-16 | 50 | 7.79551 | 127.0.0.1 | 10329 | 1.44706 | 0.00600386 | 1.44706 | 1675757058 | 0 |  | 50 | 01a3b\_00006 | 0.00202489 |
| train\_function\_01a3b\_00007 | 2023-02-07\_00-04-19 | True |  | 78b1673cf2034ed99135b80a0cb31e0e | 7\_mean=8,sd=0.6398 | Justins-MacBook-Pro-16 | 50 | 7.94189 | 127.0.0.1 | 10333 | 1.4261 | 0.00225306 | 1.4261 | 1675757059 | 0 |  | 50 | 01a3b\_00007 | 0.00209713 |
| train\_function\_01a3b\_00008 | 2023-02-07\_00-04-19 | True |  | c7f5d86154cb46b6aa27bef523edcd6f | 8\_mean=9,sd=0.1228 | Justins-MacBook-Pro-16 | 50 | 8.82304 | 127.0.0.1 | 10341 | 1.07701 | 0.00291467 | 1.07701 | 1675757059 | 0 |  | 50 | 01a3b\_00008 | 0.00240111 |

```
2023-02-07 00:04:19,366	INFO tune.py:798 -- Total run time: 7.38 seconds (6.85 seconds for the tuning loop).
```

```
<ray.tune.result_grid.ResultGrid at 0x137de07c0>
```

When the script executes, a grid-search is carried out and the results are saved to the Aim repo,
stored at the default location – the experiment log directory (in this case, it’s at `/tmp/ray_results/aim_example`).

### More Configuration Options for Aim[#](#more-configuration-options-for-aim "Link to this heading")

In the example above, we used the default configuration for the `AimLoggerCallback`.
There are a few options that can be configured as arguments to the callback. For example,
setting `AimLoggerCallback(repo="/path/to/repo")` will log results to the Aim repo at that
filepath, which could be useful if you have a central location where the results of multiple
Tune experiments are stored. Relative paths to the working directory where Tune script is
launched can be used as well. By default, the repo will be set to the experiment log
directory. See [the API reference](#tune-aim-logger) for more configurations.

## Launching the Aim UI[#](#launching-the-aim-ui "Link to this heading")

Now that we have logged our results to the Aim repository, we can view it in Aim’s web UI.
To do this, we first find the directory where the Aim repository lives, then we use
the Aim CLI to launch the web interface.

```
# Uncomment the following line to launch the Aim UI!
#!aim up --repo=/tmp/ray_results/aim_example
```

```
--------------------------------------------------------------------------
                Aim UI collects anonymous usage analytics.                
                        Read how to opt-out here:                         
    https://aimstack.readthedocs.io/en/latest/community/telemetry.html    
--------------------------------------------------------------------------
Running Aim UI on repo `<Repo#-5734997863388805469 path=/tmp/ray_results/aim_example/.aim read_only=None>`
Open http://127.0.0.1:43800
Press Ctrl+C to exit
^C
```

After launching the Aim UI, we can open the web interface at `localhost:43800`.

[![Aim Metrics Explorer](../../_images/aim_example_metrics_page.png)](https://aimstack.readthedocs.io/en/latest/ui/pages/explorers.html#metrics-explorer)

The next sections contain more in-depth information on the API of the Tune-Aim integration.

## Tune Aim Logger API[#](#tune-aim-logger-api "Link to this heading")

*class* ray.tune.logger.aim.AimLoggerCallback(*repo: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *experiment\_name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *metrics: [List](https://docs.python.org/3/library/typing.html#typing.List "(in Python v3.14)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")] | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *\*\*aim\_run\_kwargs*)[[source]](../../_modules/ray/tune/logger/aim.html#AimLoggerCallback)
:   Aim Logger: logs metrics in Aim format.

    Aim is an open-source, self-hosted ML experiment tracking tool.
    It’s good at tracking lots (thousands) of training runs, and it allows you to
    compare them with a performant and well-designed UI.

    Source: [aimhubio/aim](https://github.com/aimhubio/aim)

    Parameters:
    :   * **repo** – Aim repository directory or a `Repo` object that the Run object will
          log results to. If not provided, a default repo will be set up in the
          experiment directory (one level above trial directories).
        * **experiment** – Sets the `experiment` property of each Run object, which is the
          experiment name associated with it. Can be used later to query
          runs/sequences.
          If not provided, the default will be the Tune experiment name set
          by `RunConfig(name=...)`.
        * **metrics** – List of metric names (out of the metrics reported by Tune) to
          track in Aim. If no metric are specified, log everything that
          is reported.
        * **aim\_run\_kwargs** – Additional arguments that will be passed when creating the
          individual `Run` objects for each trial. For the full list of arguments,
          please see the Aim documentation:
          <https://aimstack.readthedocs.io/en/latest/refs/sdk.html>

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/tune/examples/tune-aim.ipynb)