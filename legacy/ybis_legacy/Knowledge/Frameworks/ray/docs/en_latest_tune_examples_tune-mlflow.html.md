Using MLflow with Tune — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Using MLflow with Tune[#](#using-mlflow-with-tune "Link to this heading")

[![try-anyscale-quickstart](../../_static/img/run-on-anyscale.svg)](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=tune-mlflow)
  

[MLflow](https://mlflow.org/) is an open source platform to manage the ML lifecycle, including experimentation,
reproducibility, deployment, and a central model registry. It currently offers four components, including
MLflow Tracking to record and query experiments, including code, data, config, and results.

[![MLflow](../../_images/mlflow.png)](https://www.mlflow.org/)

Ray Tune currently offers two lightweight integrations for MLflow Tracking.
One is the [MLflowLoggerCallback](#tune-mlflow-logger), which automatically logs
metrics reported to Tune to the MLflow Tracking API.

The other one is the [setup\_mlflow](#tune-mlflow-setup) function, which can be
used with the function API. It automatically
initializes the MLflow API with Tune’s training information and creates a run for each Tune trial.
Then within your training function, you can just use the
MLflow like you would normally do, e.g. using `mlflow.log_metrics()` or even `mlflow.autolog()`
to log to your training process.

## Running an MLflow Example[#](#running-an-mlflow-example "Link to this heading")

In the following example we’re going to use both of the above methods, namely the `MLflowLoggerCallback` and
the `setup_mlflow` function to log metrics.
Let’s start with a few crucial imports:

```
import os
import tempfile
import time

import mlflow

from ray import tune
from ray.air.integrations.mlflow import MLflowLoggerCallback, setup_mlflow
```

Next, let’s define an easy training function (a Tune `Trainable`) that iteratively computes steps and evaluates
intermediate scores that we report to Tune.

```
def evaluation_fn(step, width, height):
    return (0.1 + width * step / 100) ** (-1) + height * 0.1


def train_function(config):
    width, height = config["width"], config["height"]

    for step in range(config.get("steps", 100)):
        # Iterative training function - can be any arbitrary training procedure
        intermediate_score = evaluation_fn(step, width, height)
        # Feed the score back to Tune.
        tune.report({"iterations": step, "mean_loss": intermediate_score})
        time.sleep(0.1)
```

Given an MLFlow tracking URI, you can now simply use the `MLflowLoggerCallback` as a `callback` argument to
your `RunConfig()`:

```
def tune_with_callback(mlflow_tracking_uri, finish_fast=False):
    tuner = tune.Tuner(
        train_function,
        tune_config=tune.TuneConfig(num_samples=5),
        run_config=tune.RunConfig(
            name="mlflow",
            callbacks=[
                MLflowLoggerCallback(
                    tracking_uri=mlflow_tracking_uri,
                    experiment_name="mlflow_callback_example",
                    save_artifact=True,
                )
            ],
        ),
        param_space={
            "width": tune.randint(10, 100),
            "height": tune.randint(0, 100),
            "steps": 5 if finish_fast else 100,
        },
    )
    results = tuner.fit()
```

To use the `setup_mlflow` utility, you simply call this function in your training function.
Note that we also use `mlflow.log_metrics(...)` to log metrics to MLflow.
Otherwise, this version of our training function is identical to its original.

```
def train_function_mlflow(config):
    tracking_uri = config.pop("tracking_uri", None)
    setup_mlflow(
        config,
        experiment_name="setup_mlflow_example",
        tracking_uri=tracking_uri,
    )

    # Hyperparameters
    width, height = config["width"], config["height"]

    for step in range(config.get("steps", 100)):
        # Iterative training function - can be any arbitrary training procedure
        intermediate_score = evaluation_fn(step, width, height)
        # Log the metrics to mlflow
        mlflow.log_metrics(dict(mean_loss=intermediate_score), step=step)
        # Feed the score back to Tune.
        tune.report({"iterations": step, "mean_loss": intermediate_score})
        time.sleep(0.1)
```

With this new objective function ready, you can now create a Tune run with it as follows:

```
def tune_with_setup(mlflow_tracking_uri, finish_fast=False):
    # Set the experiment, or create a new one if does not exist yet.
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow.set_experiment(experiment_name="setup_mlflow_example")

    tuner = tune.Tuner(
        train_function_mlflow,
        tune_config=tune.TuneConfig(num_samples=5),
        run_config=tune.RunConfig(
            name="mlflow",
        ),
        param_space={
            "width": tune.randint(10, 100),
            "height": tune.randint(0, 100),
            "steps": 5 if finish_fast else 100,
            "tracking_uri": mlflow.get_tracking_uri(),
        },
    )
    results = tuner.fit()
```

If you hapen to have an MLFlow tracking URI, you can set it below in the `mlflow_tracking_uri` variable and set
`smoke_test=False`.
Otherwise, you can just run a quick test of the `tune_function` and `tune_decorated` functions without using MLflow.

```
smoke_test = True

if smoke_test:
    mlflow_tracking_uri = os.path.join(tempfile.gettempdir(), "mlruns")
else:
    mlflow_tracking_uri = "<MLFLOW_TRACKING_URI>"

tune_with_callback(mlflow_tracking_uri, finish_fast=smoke_test)
if not smoke_test:
    df = mlflow.search_runs(
        [mlflow.get_experiment_by_name("mlflow_callback_example").experiment_id]
    )
    print(df)

tune_with_setup(mlflow_tracking_uri, finish_fast=smoke_test)
if not smoke_test:
    df = mlflow.search_runs(
        [mlflow.get_experiment_by_name("setup_mlflow_example").experiment_id]
    )
    print(df)
```

```
2022-12-22 10:37:53,580	INFO worker.py:1542 -- Started a local Ray instance. View the dashboard at http://127.0.0.1:8265
```

### Tune Status

|  |  |
| --- | --- |
| Current time: | 2022-12-22 10:38:04 |
| Running for: | 00:00:06.73 |
| Memory: | 10.4/16.0 GiB |

### System Info

Using FIFO scheduling algorithm.  
Resources requested: 0/16 CPUs, 0/0 GPUs, 0.0/4.03 GiB heap, 0.0/2.0 GiB objects

### Trial Status

| Trial name | status | loc | height | width | loss | iter | total time (s) | iterations | neg\_mean\_loss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train\_function\_b275b\_00000 | TERMINATED | 127.0.0.1:801 | 66 | 36 | 7.24935 | 5 | 0.587302 | 4 | -7.24935 |
| train\_function\_b275b\_00001 | TERMINATED | 127.0.0.1:813 | 33 | 35 | 3.96667 | 5 | 0.507423 | 4 | -3.96667 |
| train\_function\_b275b\_00002 | TERMINATED | 127.0.0.1:814 | 75 | 29 | 8.29365 | 5 | 0.518995 | 4 | -8.29365 |
| train\_function\_b275b\_00003 | TERMINATED | 127.0.0.1:815 | 28 | 63 | 3.18168 | 5 | 0.567739 | 4 | -3.18168 |
| train\_function\_b275b\_00004 | TERMINATED | 127.0.0.1:816 | 20 | 18 | 3.21951 | 5 | 0.526536 | 4 | -3.21951 |

### Trial Progress

| Trial name | date | done | episodes\_total | experiment\_id | experiment\_tag | hostname | iterations | iterations\_since\_restore | mean\_loss | neg\_mean\_loss | node\_ip | pid | time\_since\_restore | time\_this\_iter\_s | time\_total\_s | timestamp | timesteps\_since\_restore | timesteps\_total | training\_iteration | trial\_id | warmup\_time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train\_function\_b275b\_00000 | 2022-12-22\_10-38-01 | True |  | 28feaa4dd8ab4edab810e8109e77502e | 0\_height=66,width=36 | kais-macbook-pro.anyscale.com.beta.tailscale.net | 4 | 5 | 7.24935 | -7.24935 | 127.0.0.1 | 801 | 0.587302 | 0.126818 | 0.587302 | 1671705481 | 0 |  | 5 | b275b\_00000 | 0.00293493 |
| train\_function\_b275b\_00001 | 2022-12-22\_10-38-04 | True |  | 245010d0c3d0439ebfb664764ae9db3c | 1\_height=33,width=35 | kais-macbook-pro.anyscale.com.beta.tailscale.net | 4 | 5 | 3.96667 | -3.96667 | 127.0.0.1 | 813 | 0.507423 | 0.122086 | 0.507423 | 1671705484 | 0 |  | 5 | b275b\_00001 | 0.00553799 |
| train\_function\_b275b\_00002 | 2022-12-22\_10-38-04 | True |  | 898afbf9b906448c980f399c72a2324c | 2\_height=75,width=29 | kais-macbook-pro.anyscale.com.beta.tailscale.net | 4 | 5 | 8.29365 | -8.29365 | 127.0.0.1 | 814 | 0.518995 | 0.123554 | 0.518995 | 1671705484 | 0 |  | 5 | b275b\_00002 | 0.0040431 |
| train\_function\_b275b\_00003 | 2022-12-22\_10-38-04 | True |  | 03a4476f82734642b6ab0a5040ca58f8 | 3\_height=28,width=63 | kais-macbook-pro.anyscale.com.beta.tailscale.net | 4 | 5 | 3.18168 | -3.18168 | 127.0.0.1 | 815 | 0.567739 | 0.125471 | 0.567739 | 1671705484 | 0 |  | 5 | b275b\_00003 | 0.00406194 |
| train\_function\_b275b\_00004 | 2022-12-22\_10-38-04 | True |  | ff8c7c55ce6e404f9b0552c17f7a0c40 | 4\_height=20,width=18 | kais-macbook-pro.anyscale.com.beta.tailscale.net | 4 | 5 | 3.21951 | -3.21951 | 127.0.0.1 | 816 | 0.526536 | 0.123327 | 0.526536 | 1671705484 | 0 |  | 5 | b275b\_00004 | 0.00332022 |

```
2022-12-22 10:38:04,477	INFO tune.py:772 -- Total run time: 7.99 seconds (6.71 seconds for the tuning loop).
```

### Tune Status

|  |  |
| --- | --- |
| Current time: | 2022-12-22 10:38:11 |
| Running for: | 00:00:07.00 |
| Memory: | 10.7/16.0 GiB |

### System Info

Using FIFO scheduling algorithm.  
Resources requested: 0/16 CPUs, 0/0 GPUs, 0.0/4.03 GiB heap, 0.0/2.0 GiB objects

### Trial Status

| Trial name | status | loc | height | width | loss | iter | total time (s) | iterations | neg\_mean\_loss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train\_function\_mlflow\_b73bd\_00000 | TERMINATED | 127.0.0.1:842 | 37 | 68 | 4.05461 | 5 | 0.750435 | 4 | -4.05461 |
| train\_function\_mlflow\_b73bd\_00001 | TERMINATED | 127.0.0.1:853 | 50 | 20 | 6.11111 | 5 | 0.652748 | 4 | -6.11111 |
| train\_function\_mlflow\_b73bd\_00002 | TERMINATED | 127.0.0.1:854 | 38 | 83 | 4.0924 | 5 | 0.6513 | 4 | -4.0924 |
| train\_function\_mlflow\_b73bd\_00003 | TERMINATED | 127.0.0.1:855 | 15 | 93 | 1.76178 | 5 | 0.650586 | 4 | -1.76178 |
| train\_function\_mlflow\_b73bd\_00004 | TERMINATED | 127.0.0.1:856 | 75 | 43 | 8.04945 | 5 | 0.656046 | 4 | -8.04945 |

### Trial Progress

| Trial name | date | done | episodes\_total | experiment\_id | experiment\_tag | hostname | iterations | iterations\_since\_restore | mean\_loss | neg\_mean\_loss | node\_ip | pid | time\_since\_restore | time\_this\_iter\_s | time\_total\_s | timestamp | timesteps\_since\_restore | timesteps\_total | training\_iteration | trial\_id | warmup\_time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train\_function\_mlflow\_b73bd\_00000 | 2022-12-22\_10-38-08 | True |  | 62703cfe82e54d74972377fbb525b000 | 0\_height=37,width=68 | kais-macbook-pro.anyscale.com.beta.tailscale.net | 4 | 5 | 4.05461 | -4.05461 | 127.0.0.1 | 842 | 0.750435 | 0.108625 | 0.750435 | 1671705488 | 0 |  | 5 | b73bd\_00000 | 0.0030272 |
| train\_function\_mlflow\_b73bd\_00001 | 2022-12-22\_10-38-11 | True |  | 03ea89852115465392ed318db8021614 | 1\_height=50,width=20 | kais-macbook-pro.anyscale.com.beta.tailscale.net | 4 | 5 | 6.11111 | -6.11111 | 127.0.0.1 | 853 | 0.652748 | 0.110796 | 0.652748 | 1671705491 | 0 |  | 5 | b73bd\_00001 | 0.00303078 |
| train\_function\_mlflow\_b73bd\_00002 | 2022-12-22\_10-38-11 | True |  | 3731fc2966f9453ba58c650d89035ab4 | 2\_height=38,width=83 | kais-macbook-pro.anyscale.com.beta.tailscale.net | 4 | 5 | 4.0924 | -4.0924 | 127.0.0.1 | 854 | 0.6513 | 0.108578 | 0.6513 | 1671705491 | 0 |  | 5 | b73bd\_00002 | 0.00310016 |
| train\_function\_mlflow\_b73bd\_00003 | 2022-12-22\_10-38-11 | True |  | fb35841742b348b9912d10203c730f1e | 3\_height=15,width=93 | kais-macbook-pro.anyscale.com.beta.tailscale.net | 4 | 5 | 1.76178 | -1.76178 | 127.0.0.1 | 855 | 0.650586 | 0.109097 | 0.650586 | 1671705491 | 0 |  | 5 | b73bd\_00003 | 0.0576491 |
| train\_function\_mlflow\_b73bd\_00004 | 2022-12-22\_10-38-11 | True |  | 6d3cbf9ecc3446369e607ff78c67bc29 | 4\_height=75,width=43 | kais-macbook-pro.anyscale.com.beta.tailscale.net | 4 | 5 | 8.04945 | -8.04945 | 127.0.0.1 | 856 | 0.656046 | 0.109869 | 0.656046 | 1671705491 | 0 |  | 5 | b73bd\_00004 | 0.00265694 |

```
2022-12-22 10:38:11,514	INFO tune.py:772 -- Total run time: 7.01 seconds (6.98 seconds for the tuning loop).
```

This completes our Tune and MLflow walk-through.
In the following sections you can find more details on the API of the Tune-MLflow integration.

## MLflow AutoLogging[#](#mlflow-autologging "Link to this heading")

You can also check out [here](includes/mlflow_ptl_example.html) for an example on how you can
leverage MLflow auto-logging, in this case with Pytorch Lightning

## MLflow Logger API[#](#mlflow-logger-api "Link to this heading")

*class* ray.air.integrations.mlflow.MLflowLoggerCallback(*tracking\_uri: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *\**, *registry\_uri: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *experiment\_name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *tags: [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *tracking\_token: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *save\_artifact: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") = False*, *log\_params\_on\_trial\_end: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") = False*)[[source]](../../_modules/ray/air/integrations/mlflow.html#MLflowLoggerCallback)
:   MLflow Logger to automatically log Tune results and config to MLflow.

    MLflow (<https://mlflow.org>) Tracking is an open source library for
    recording and querying experiments. This Ray Tune `LoggerCallback`
    sends information (config parameters, training results & metrics,
    and artifacts) to MLflow for automatic experiment tracking.

    Keep in mind that the callback will open an MLflow session on the driver and
    not on the trainable. Therefore, it is not possible to call MLflow functions
    like `mlflow.log_figure()` inside the trainable as there is no MLflow session
    on the trainable. For more fine grained control, use
    [`ray.air.integrations.mlflow.setup_mlflow()`](../api/doc/ray.air.integrations.mlflow.setup_mlflow.html#ray.air.integrations.mlflow.setup_mlflow "ray.air.integrations.mlflow.setup_mlflow").

    Parameters:
    :   * **tracking\_uri** – The tracking URI for where to manage experiments
          and runs. This can either be a local file path or a remote server.
          This arg gets passed directly to mlflow
          initialization. When using Tune in a multi-node setting, make sure
          to set this to a remote server and not a local file path.
        * **registry\_uri** – The registry URI that gets passed directly to
          mlflow initialization.
        * **experiment\_name** – The experiment name to use for this Tune run.
          If the experiment with the name already exists with MLflow,
          it will be reused. If not, a new experiment will be created with
          that name.
        * **tags** – An optional dictionary of string keys and values to set
          as tags on the run
        * **tracking\_token** – Tracking token used to authenticate with MLflow.
        * **save\_artifact** – If set to True, automatically save the entire
          contents of the Tune local\_dir as an artifact to the
          corresponding run in MlFlow.
        * **log\_params\_on\_trial\_end** – If set to True, log parameters to MLflow
          at the end of the trial instead of at the beginning

    Example:

    ```
    from ray.air.integrations.mlflow import MLflowLoggerCallback

    tags = { "user_name" : "John",
             "git_commit_hash" : "abc123"}

    tune.run(
        train_fn,
        config={
            # define search space here
            "parameter_1": tune.choice([1, 2, 3]),
            "parameter_2": tune.choice([4, 5, 6]),
        },
        callbacks=[MLflowLoggerCallback(
            experiment_name="experiment1",
            tags=tags,
            save_artifact=True,
            log_params_on_trial_end=True)])
    ```

## MLflow setup API[#](#mlflow-setup-api "Link to this heading")

ray.air.integrations.mlflow.setup\_mlflow(*config: [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *tracking\_uri: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *registry\_uri: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *experiment\_id: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *experiment\_name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *tracking\_token: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *artifact\_location: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *run\_name: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *create\_experiment\_if\_not\_exists: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") = False*, *tags: [Dict](https://docs.python.org/3/library/typing.html#typing.Dict "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") = None*, *rank\_zero\_only: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") = True*) → [ModuleType](https://docs.python.org/3/library/types.html#types.ModuleType "(in Python v3.14)") | \_NoopModule[[source]](../../_modules/ray/air/integrations/mlflow.html#setup_mlflow)
:   Set up a MLflow session.

    This function can be used to initialize an MLflow session in a
    (distributed) training or tuning run. The session will be created on the trainable.

    By default, the MLflow experiment ID is the Ray trial ID and the
    MLlflow experiment name is the Ray trial name. These settings can be overwritten by
    passing the respective keyword arguments.

    The `config` dict is automatically logged as the run parameters (excluding the
    mlflow settings).

    In distributed training with Ray Train, only the zero-rank worker will initialize
    mlflow. All other workers will return a noop client, so that logging is not
    duplicated in a distributed run. This can be disabled by passing
    `rank_zero_only=False`, which will then initialize mlflow in every training
    worker. Note: for Ray Tune, there’s no concept of worker ranks, so the `rank_zero_only` is ignored.

    This function will return the `mlflow` module or a noop module for
    non-rank zero workers `if rank_zero_only=True`. By using
    `mlflow = setup_mlflow(config)` you can ensure that only the rank zero worker
    calls the mlflow API.

    Parameters:
    :   * **config** – Configuration dict to be logged to mlflow as parameters.
        * **tracking\_uri** – The tracking URI for MLflow tracking. If using
          Tune in a multi-node setting, make sure to use a remote server for
          tracking.
        * **registry\_uri** – The registry URI for the MLflow model registry.
        * **experiment\_id** – The id of an already created MLflow experiment.
          All logs from all trials in `tune.Tuner()` will be reported to this
          experiment. If this is not provided or the experiment with this
          id does not exist, you must provide an``experiment\_name``. This
          parameter takes precedence over `experiment_name`.
        * **experiment\_name** – The name of an already existing MLflow
          experiment. All logs from all trials in `tune.Tuner()` will be
          reported to this experiment. If this is not provided, you must
          provide a valid `experiment_id`.
        * **tracking\_token** – A token to use for HTTP authentication when
          logging to a remote tracking server. This is useful when you
          want to log to a Databricks server, for example. This value will
          be used to set the MLFLOW\_TRACKING\_TOKEN environment variable on
          all the remote training processes.
        * **artifact\_location** – The location to store run artifacts.
          If not provided, MLFlow picks an appropriate default.
          Ignored if experiment already exists.
        * **run\_name** – Name of the new MLflow run that will be created.
          If not set, will default to the `experiment_name`.
        * **create\_experiment\_if\_not\_exists** – Whether to create an
          experiment with the provided name if it does not already
          exist. Defaults to False.
        * **tags** – Tags to set for the new run.
        * **rank\_zero\_only** – If True, will return an initialized session only for the
          rank 0 worker in distributed training. If False, will initialize a
          session for all workers. Defaults to True.

    Example

    Per default, you can just call `setup_mlflow` and continue to use
    MLflow like you would normally do:

    ```
    from ray.air.integrations.mlflow import setup_mlflow

    def training_loop(config):
        mlflow = setup_mlflow(config)
        # ...
        mlflow.log_metric(key="loss", val=0.123, step=0)
    ```

    In distributed data parallel training, you can utilize the return value of
    `setup_mlflow`. This will make sure it is only invoked on the first worker
    in distributed training runs.

    ```
    from ray.air.integrations.mlflow import setup_mlflow

    def training_loop(config):
        mlflow = setup_mlflow(config)
        # ...
        mlflow.log_metric(key="loss", val=0.123, step=0)
    ```

    You can also use MlFlow’s autologging feature if using a training
    framework like Pytorch Lightning, XGBoost, etc. More information can be
    found here
    (<https://mlflow.org/docs/latest/tracking.html#automatic-logging>).

    ```
    from ray.air.integrations.mlflow import setup_mlflow

    def train_fn(config):
        mlflow = setup_mlflow(config)
        mlflow.autolog()
        xgboost_results = xgb.train(config, ...)
    ```

    **PublicAPI (alpha):** This API is in alpha and may change before becoming stable.

## More MLflow Examples[#](#more-mlflow-examples "Link to this heading")

* [MLflow PyTorch Lightning Example](includes/mlflow_ptl_example.html): Example for using [MLflow](https://github.com/mlflow/mlflow/)
  and [Pytorch Lightning](https://github.com/PyTorchLightning/pytorch-lightning) with Ray Tune.

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/tune/examples/tune-mlflow.ipynb)