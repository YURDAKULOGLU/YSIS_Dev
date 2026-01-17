RLlib: Industry-Grade, Scalable Reinforcement Learning — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# RLlib: Industry-Grade, Scalable Reinforcement Learning[#](#rllib-industry-grade-scalable-reinforcement-learning "Link to this heading")

![../_images/rllib-logo.png](../_images/rllib-logo.png)

**RLlib** is an open source library for reinforcement learning (**RL**), offering support for
production-level, highly scalable, and fault-tolerant RL workloads, while maintaining simple and unified
APIs for a large variety of industry applications.

Whether training policies in a **multi-agent** setup, from historic **offline** data,
or using **externally connected simulators**, RLlib offers simple solutions for each of
these autonomous decision making needs and enables you to start running your experiments within hours.

Industry leaders use RLlib in production in many different verticals, such as
[gaming](https://www.anyscale.com/events/2021/06/22/using-reinforcement-learning-to-optimize-iap-offer-recommendations-in-mobile-games),
[robotics](https://www.anyscale.com/events/2021/06/23/introducing-amazon-sagemaker-kubeflow-reinforcement-learning-pipelines-for),
[finance](https://www.anyscale.com/events/2021/06/22/a-24x-speedup-for-reinforcement-learning-with-rllib-+-ray),
[climate- and industrial control](https://www.anyscale.com/events/2021/06/23/applying-ray-and-rllib-to-real-life-industrial-use-cases),
[manufacturing and logistics](https://www.anyscale.com/events/2022/03/29/alphadow-leveraging-rays-ecosystem-to-train-and-deploy-an-rl-industrial),
[automobile](https://www.anyscale.com/events/2021/06/23/using-rllib-in-an-enterprise-scale-reinforcement-learning-solution),
and
[boat design](https://www.youtube.com/watch?v=cLCK13ryTpw).

## RLlib in 60 seconds[#](#rllib-in-60-seconds "Link to this heading")

![../_images/rllib-index-header.svg](../_images/rllib-index-header.svg)

It only takes a few steps to get your first RLlib workload up and running on your laptop.
Install RLlib and [PyTorch](https://pytorch.org), as shown below:

```
pip install "ray[rllib]" torch
```

Note

For installation on computers running Apple Silicon, such as M1,
[follow instructions here.](https://docs.ray.io/en/latest/ray-overview/installation.html#m1-mac-apple-silicon-support)

Note

To be able to run the Atari or MuJoCo examples, you also need to do:

```
pip install "gymnasium[atari,accept-rom-license,mujoco]"
```

This is all, you can now start coding against RLlib. Here is an example for running the [PPO Algorithm](rllib-algorithms.html#ppo) on the
[Taxi domain](https://gymnasium.farama.org/environments/toy_text/taxi/).
You first create a `config` for the algorithm, which defines the [RL environment](key-concepts.html#rllib-key-concepts-environments) and any other needed settings and parameters.

```
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.connectors.env_to_module import FlattenObservations

# Configure the algorithm.
config = (
    PPOConfig()
    .environment("Taxi-v3")
    .env_runners(
        num_env_runners=2,
        # Observations are discrete (ints) -> We need to flatten (one-hot) them.
        env_to_module_connector=lambda env: FlattenObservations(),
    )
    .evaluation(evaluation_num_env_runners=1)
)
```

Next, `build` the algorithm and `train` it for a total of five iterations.
One training iteration includes parallel, distributed sample collection by the
[`EnvRunner`](package_ref/env/doc/ray.rllib.env.env_runner.EnvRunner.html#ray.rllib.env.env_runner.EnvRunner "ray.rllib.env.env_runner.EnvRunner") actors, followed by loss calculation
on the collected data, and a model update step.

```
from pprint import pprint

# Build the algorithm.
algo = config.build_algo()

# Train it for 5 iterations ...
for _ in range(5):
    pprint(algo.train())
```

At the end of your script, you evaluate the trained Algorithm and release all its resources:

```
# ... and evaluate it.
pprint(algo.evaluate())

# Release the algo's resources (remote actors, like EnvRunners and Learners).
algo.stop()
```

You can use any [Farama-Foundation Gymnasium](https://github.com/Farama-Foundation/Gymnasium) registered environment
with the `env` argument.

In `config.env_runners()` you can specify - amongst many other things - the number of parallel
[`EnvRunner`](package_ref/env/doc/ray.rllib.env.env_runner.EnvRunner.html#ray.rllib.env.env_runner.EnvRunner "ray.rllib.env.env_runner.EnvRunner") actors to collect samples from the environment.

You can also tweak the NN architecture used by tweaking RLlib’s `DefaultModelConfig`,
as well as, set up a separate config for the evaluation
[`EnvRunner`](package_ref/env/doc/ray.rllib.env.env_runner.EnvRunner.html#ray.rllib.env.env_runner.EnvRunner "ray.rllib.env.env_runner.EnvRunner") actors through the `config.evaluation()` method.

[See here](getting-started.html#rllib-python-api), if you want to learn more about the RLlib training APIs.
Also, [see here](https://github.com/ray-project/ray/blob/master/rllib/examples/inference/policy_inference_after_training.py)
for a simple example on how to write an action inference loop after training.

If you want to get a quick preview of which **algorithms** and **environments** RLlib supports,
click the dropdowns below:

**RLlib Algorithms**

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| **On-Policy** | | | | | | |
| [PPO (Proximal Policy Optimization)](rllib-algorithms.html#ppo) | [single_agent](../_images/single-agent.svg) | [multi_agent](../_images/multi-agent.svg) | [discr_act](../_images/discr-actions.svg) | [cont_act](../_images/cont-actions.svg) | [multi_gpu](../_images/multi-gpu.svg) | [Only on the Anyscale Platform!](../_images/multi-node-multi-gpu.svg) |
| **Off-Policy** | | | | | | |
| [SAC (Soft Actor Critic)](rllib-algorithms.html#sac) | [single_agent](../_images/single-agent.svg) | [multi_agent](../_images/multi-agent.svg) |  | [cont_act](../_images/cont-actions.svg) | [multi_gpu](../_images/multi-gpu.svg) | [Only on the Anyscale Platform!](../_images/multi-node-multi-gpu.svg) |
| [DQN/Rainbow (Deep Q Networks)](rllib-algorithms.html#dqn) | [single_agent](../_images/single-agent.svg) | [multi_agent](../_images/multi-agent.svg) | [discr_act](../_images/discr-actions.svg) |  | [multi_gpu](../_images/multi-gpu.svg) | [Only on the Anyscale Platform!](../_images/multi-node-multi-gpu.svg) |
| **High-throughput Architectures** | | | | | | |
| [APPO (Asynchronous Proximal Policy Optimization)](rllib-algorithms.html#appo) | [single_agent](../_images/single-agent.svg) | [multi_agent](../_images/multi-agent.svg) | [discr_act](../_images/discr-actions.svg) | [cont_act](../_images/cont-actions.svg) | [multi_gpu](../_images/multi-gpu.svg) | [Only on the Anyscale Platform!](../_images/multi-node-multi-gpu.svg) |
| [IMPALA (Importance Weighted Actor-Learner Architecture)](rllib-algorithms.html#impala) | [single_agent](../_images/single-agent.svg) | [multi_agent](../_images/multi-agent.svg) | [discr_act](../_images/discr-actions.svg) |  | [multi_gpu](../_images/multi-gpu.svg) | [Only on the Anyscale Platform!](../_images/multi-node-multi-gpu.svg) |
| **Model-based RL** | | | | | | |
| [DreamerV3](rllib-algorithms.html#dreamerv3) | [single_agent](../_images/single-agent.svg) |  | [discr_act](../_images/discr-actions.svg) | [cont_act](../_images/cont-actions.svg) | [multi_gpu](../_images/multi-gpu.svg) | [Only on the Anyscale Platform!](../_images/multi-node-multi-gpu.svg) |
| **Offline RL and Imitation Learning** | | | | | | |
| [BC (Behavior Cloning)](rllib-algorithms.html#bc) | [single_agent](../_images/single-agent.svg) |  | [discr_act](../_images/discr-actions.svg) | [cont_act](../_images/cont-actions.svg) |  |  |
| [CQL (Conservative Q-Learning)](rllib-algorithms.html#cql) | [single_agent](../_images/single-agent.svg) |  |  | [cont_act](../_images/cont-actions.svg) |  |  |
| [MARWIL (Advantage Re-Weighted Imitation Learning)](rllib-algorithms.html#marwil) | [single_agent](../_images/single-agent.svg) |  | [discr_act](../_images/discr-actions.svg) | [cont_act](../_images/cont-actions.svg) |  |  |

**RLlib Environments**

|  |
| --- |
| **Farama-Foundation Environments** |
| [gymnasium](https://gymnasium.farama.org/index.html) [single_agent](../_images/single-agent.svg)  ``` pip install "gymnasium[atari,accept-rom-license,mujoco]"`` ```  ``` config.environment("CartPole-v1")  # Classic Control config.environment("ale_py:ALE/Pong-v5")  # Atari config.environment("Hopper-v5")  # MuJoCo ``` |
| [PettingZoo](https://pettingzoo.farama.org/index.html) [multi_agent](../_images/multi-agent.svg)  ``` pip install "pettingzoo[all]" ```  ``` from ray.tune.registry import register_env from ray.rllib.env.wrappers.pettingzoo_env import PettingZooEnv from pettingzoo.sisl import waterworld_v4 register_env("env", lambda _: PettingZooEnv(waterworld_v4.env())) config.environment("env") ``` |
| **RLlib Multi-Agent** |
| [RLlib’s MultiAgentEnv API](rllib-env.html#multi-agent-and-hierarchical) [multi_agent](../_images/multi-agent.svg)  ``` from ray.rllib.examples.envs.classes.multi_agent import MultiAgentCartPole from ray import tune tune.register_env("env", lambda cfg: MultiAgentCartPole(cfg)) config.environment("env", env_config={"num_agents": 2}) config.multi_agent(     policies={"p0", "p1"},     policy_mapping_fn=lambda aid, *a, **kw: f"p{aid}", ) ``` |

## Why chose RLlib?[#](#why-chose-rllib "Link to this heading")

**Scalable and Fault-Tolerant**

RLlib workloads scale along various axes:

* The number of [`EnvRunner`](package_ref/env/doc/ray.rllib.env.env_runner.EnvRunner.html#ray.rllib.env.env_runner.EnvRunner "ray.rllib.env.env_runner.EnvRunner") actors to use.
  This is configurable through `config.env_runners(num_env_runners=...)` and
  allows you to scale the speed of your (simulator) data collection step.
  This `EnvRunner` axis is fully **fault tolerant**, meaning you can train against
  custom environments that are unstable or frequently stall execution and even place all
  your `EnvRunner` actors on spot machines.
* The number of `Learner` actors to use for **multi-GPU training**.
  This is configurable through `config.learners(num_learners=...)` and you normally
  set this to the number of GPUs available (make sure you then also set
  `config.learners(num_gpus_per_learner=1)`) or - if you do not have GPUs - you can
  use this setting for **DDP-style learning on CPUs** instead.

**Multi-Agent Reinforcement Learning (MARL)**

RLlib natively supports multi-agent reinforcement learning (MARL), thereby allowing you to run
in any complex configuration.

* **Independent** multi-agent learning (the default): Every agent collects data for updating its own
  policy network, interpreting other agents as part of the environment.
* **Collaborative** training: Train a team of agents that either all share the same policy (shared parameters)
  or in which some agents have their own policy network(s). You can also share value functions between all
  members of the team or some of them, as you see fit, thus allowing for global vs local objectives to be
  optimized.
* **Adversarial** training: Have agents play against other agents in competitive environments. Use self-play,
  or league based self-play to train your agents to learn how to play throughout various stages of
  ever increasing difficulty.
* **Any combination of the above!** Yes, you can train teams of arbitrary sizes of agents playing against
  other teams where the agents in each team might have individual sub-objectives and there are groups
  of neutral agents not participating in any competition.

**Offline RL and Behavior Cloning**

**Ray.Data** has been integrated into RLlib, enabling **large-scale data ingestion** for offline RL and behavior
cloning (BC) workloads.

See here for a basic [tuned example for the behavior cloning algo](https://github.com/ray-project/ray/blob/master/rllib/tuned_examples/bc/cartpole_bc.py)
and here for how to [pre-train a policy with BC, then finetuning it with online PPO](https://github.com/ray-project/ray/blob/master/rllib/examples/offline_rl/train_w_bc_finetune_w_ppo.py).

**Support for External Env Clients**

**Support for externally connecting RL environments** is achieved through customizing the [`EnvRunner`](package_ref/env/doc/ray.rllib.env.env_runner.EnvRunner.html#ray.rllib.env.env_runner.EnvRunner "ray.rllib.env.env_runner.EnvRunner") logic
from RLlib-owned, internal gymnasium envs to external, TCP-connected Envs that act independently and may even perform their own
action inference, e.g. through ONNX.

See here for an example of [RLlib acting as a server with connecting external env TCP-clients](https://github.com/ray-project/ray/blob/master/rllib/examples/envs/env_connecting_to_rllib_w_tcp_client.py).

## Learn More[#](#learn-more "Link to this heading")

**RLlib Key Concepts**

Learn more about the core concepts of RLlib, such as Algorithms, environments,
models, and learners.

[Key Concepts](key-concepts.html#rllib-key-concepts)

**RL Environments**

Get started with environments supported by RLlib, such as Farama foundation’s Gymnasium, Petting Zoo,
and many custom formats for vectorized and multi-agent environments.

[Environments](rllib-env.html#rllib-environments-doc)

**Models (RLModule)**

Learn how to configure RLlib’s default models and implement your own
custom models through the RLModule APIs, which support arbitrary architectures
with PyTorch, complex multi-model setups, and multi-agent models with components
shared between agents.

[Models (RLModule)](rl-modules.html#rlmodule-guide)

**Algorithms**

See the many available RL algorithms of RLlib for on-policy and off-policy training,
offline- and model-based RL, multi-agent RL, and more.

[Algorithms](rllib-algorithms.html#rllib-algorithms-doc)

## Customizing RLlib[#](#customizing-rllib "Link to this heading")

RLlib provides powerful, yet easy to use APIs for customizing all aspects of your experimental- and
production training-workflows.
For example, you may code your own [environments](rllib-env.html#configuring-environments)
in python using the [Farama Foundation’s gymnasium](https://farama.org) or DeepMind’s OpenSpiel,
provide custom [PyTorch models](https://github.com/ray-project/ray/blob/master/rllib/examples/rl_modules/custom_cnn_rl_module.py),
write your own [optimizer setups and loss definitions](https://github.com/ray-project/ray/blob/master/rllib/examples/learners/ppo_with_custom_loss_fn.py),
or define custom [exploratory behavior](https://github.com/ray-project/ray/blob/master/rllib/examples/curiosity/count_based_curiosity.py).

[![../_images/rllib-new-api-stack-simple.svg](../_images/rllib-new-api-stack-simple.svg)](../_images/rllib-new-api-stack-simple.svg)


**RLlib’s API stack:** Built on top of Ray, RLlib offers off-the-shelf, distributed and fault-tolerant
algorithms and loss functions, PyTorch default models, multi-GPU training, and multi-agent support.
Users customize their experiments by subclassing the existing abstractions.[#](#id1 "Link to this image")

## Citing RLlib[#](#citing-rllib "Link to this heading")

If RLlib helps with your academic research, the Ray RLlib team encourages you to cite these papers:

```
@inproceedings{liang2021rllib,
    title={{RLlib} Flow: Distributed Reinforcement Learning is a Dataflow Problem},
    author={
        Wu, Zhanghao and
        Liang, Eric and
        Luo, Michael and
        Mika, Sven and
        Gonzalez, Joseph E. and
        Stoica, Ion
    },
    booktitle={Conference on Neural Information Processing Systems ({NeurIPS})},
    year={2021},
    url={https://proceedings.neurips.cc/paper/2021/file/2bce32ed409f5ebcee2a7b417ad9beed-Paper.pdf}
}

@inproceedings{liang2018rllib,
    title={{RLlib}: Abstractions for Distributed Reinforcement Learning},
    author={
        Eric Liang and
        Richard Liaw and
        Robert Nishihara and
        Philipp Moritz and
        Roy Fox and
        Ken Goldberg and
        Joseph E. Gonzalez and
        Michael I. Jordan and
        Ion Stoica,
    },
    booktitle = {International Conference on Machine Learning ({ICML})},
    year={2018},
    url={https://arxiv.org/pdf/1712.09381}
}
```

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/rllib/index.rst)