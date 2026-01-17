Ray Tune Examples — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Ray Tune Examples[#](#ray-tune-examples "Link to this heading")

Tip

See [Ray Tune: Hyperparameter Tuning](../index.html#tune-main) to learn more about Tune features.

Below are examples for using Ray Tune for a variety of use cases and sorted by categories:

* [ML frameworks](#id1)
* [Experiment tracking tools](#id2)
* [Hyperparameter optimization frameworks](#id3)
* [Others](#others)
* [Exercises](#exercises)

## ML frameworks[#](#ml-frameworks "Link to this heading")

Ray Tune integrates with many popular machine learning frameworks. Here you find a few practical examples showing you how to tune your models. At the end of these guides you will often find links to even more examples.

|  |
| --- |
| [How to use Tune with Keras and TensorFlow models](tune_mnist_keras.html) |
| [How to use Tune with PyTorch models](tune-pytorch-cifar.html) |
| [How to tune PyTorch Lightning models](tune-pytorch-lightning.html) |
| [Tuning RL experiments with Ray Tune and Ray Serve](pbt_ppo_example.html) |
| [Tuning XGBoost parameters with Tune](tune-xgboost.html) |
| [Tuning LightGBM parameters with Tune](lightgbm_example.html) |
| [Tuning Hugging Face Transformers with Tune](pbt_transformers.html) |

## Experiment tracking tools[#](#experiment-tracking-tools "Link to this heading")

Ray Tune integrates with some popular Experiment tracking and management tools,
such as CometML, or Weights & Biases. For how
to use Ray Tune with Tensorboard, see
[Guide to logging and outputs](../tutorials/tune-output.html#tune-logging).

|  |
| --- |
| [Using Aim with Ray Tune for experiment management](tune-aim.html) |
| [Using Comet with Ray Tune for experiment management](tune-comet.html) |
| [Tracking your experiment process Weights & Biases](tune-wandb.html) |
| [Using MLflow tracking and auto logging with Tune](tune-mlflow.html) |

## Hyperparameter optimization frameworks[#](#hyperparameter-optimization-frameworks "Link to this heading")

Tune integrates with a wide variety of hyperparameter optimization frameworks
and their respective search algorithms. See the following detailed examples
for each integration:

|  |
| --- |
| [Running Tune experiments with AxSearch](ax_example.html) |
| [Running Tune experiments with HyperOpt](hyperopt_example.html) |
| [Running Tune experiments with BayesOpt](bayesopt_example.html) |
| [Running Tune experiments with BOHB](bohb_example.html) |
| [Running Tune experiments with Nevergrad](nevergrad_example.html) |
| [Running Tune experiments with Optuna](optuna_example.html) |

## Others[#](#others "Link to this heading")

|  |
| --- |
| [Simple example for doing a basic random and grid search](includes/tune_basic_example.html) |
| [Example of using a simple tuning function with AsyncHyperBandScheduler](includes/async_hyperband_example.html) |
| [Example of using a trainable function with HyperBandScheduler and the AsyncHyperBandScheduler](includes/hyperband_function_example.html) |
| [Configuring and running (synchronous) PBT and understanding the underlying algorithm behavior with a simple example](pbt_visualization/pbt_visualization.html) |
| [PBT Function Example](includes/pbt_function.html) |
| [PB2 Example](includes/pb2_example.html) |
| [Logging Example](includes/logging_example.html) |

## Exercises[#](#exercises "Link to this heading")

Learn how to use Tune in your browser with the following Colab-based exercises.

| Description | Library | Colab link |
| --- | --- | --- |
| Basics of using Tune | PyTorch | [Open in Colab](https://colab.research.google.com/github/ray-project/tutorial/blob/master/tune_exercises/exercise_1_basics.ipynb) |
| Using search algorithms and trial schedulers to optimize your model | PyTorch | [Open in Colab](https://colab.research.google.com/github/ray-project/tutorial/blob/master/tune_exercises/exercise_2_optimize.ipynb) |
| Using Population-Based Training (PBT) | PyTorch | [Open in Colab](https://colab.research.google.com/github/ray-project/tutorial/blob/master/tune_exercises/exercise_3_pbt.ipynb"target="_parent) |
| Fine-tuning Hugging Face Transformers with PBT | Hugging Face Transformers and PyTorch | [Open in Colab](https://colab.research.google.com/drive/1tQgAKgcKQzheoh503OzhS4N9NtfFgmjF?usp=sharing) |
| Logging Tune runs to Comet ML | Comet | [Open in Colab](https://colab.research.google.com/drive/1dp3VwVoAH1acn_kG7RuT62mICnOqxU1z?usp=sharing) |

Tutorial source files are on [GitHub](https://github.com/ray-project/tutorial).

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/tune/examples/index.rst)