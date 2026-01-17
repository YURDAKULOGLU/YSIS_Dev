User Guides — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# User Guides[#](#user-guides "Link to this heading")

* [Running Basic Experiments](tune-run.html)
  + [Running Independent Tune Trials in Parallel](tune-run.html#running-independent-tune-trials-in-parallel)
  + [How does Tune compare to using Ray Core (`ray.remote`)?](tune-run.html#how-does-tune-compare-to-using-ray-core-ray-remote)
* [Logging and Outputs in Tune](tune-output.html)
  + [How to configure logging in Tune?](tune-output.html#how-to-configure-logging-in-tune)
  + [How to log your Tune runs to TensorBoard?](tune-output.html#how-to-log-your-tune-runs-to-tensorboard)
  + [How to control console output with Tune?](tune-output.html#how-to-control-console-output-with-tune)
  + [How to redirect Trainable logs to files in a Tune run?](tune-output.html#how-to-redirect-trainable-logs-to-files-in-a-tune-run)
  + [How do you log arbitrary files from a Tune Trainable?](tune-output.html#how-do-you-log-arbitrary-files-from-a-tune-trainable)
  + [How to Build Custom Tune Loggers?](tune-output.html#how-to-build-custom-tune-loggers)
* [Setting Trial Resources](tune-resources.html)
  + [How to leverage GPUs in Tune?](tune-resources.html#how-to-leverage-gpus-in-tune)
  + [How to run distributed training with Tune?](tune-resources.html#how-to-run-distributed-training-with-tune)
  + [How to limit concurrency in Tune?](tune-resources.html#how-to-limit-concurrency-in-tune)
* [Using Search Spaces](tune-search-spaces.html)
  + [How to use Custom and Conditional Search Spaces in Tune?](tune-search-spaces.html#how-to-use-custom-and-conditional-search-spaces-in-tune)
* [How to Define Stopping Criteria for a Ray Tune Experiment](tune-stopping.html)
  + [Stop a Tune experiment manually](tune-stopping.html#stop-a-tune-experiment-manually)
  + [Stop using metric-based criteria](tune-stopping.html#stop-using-metric-based-criteria)
  + [Stop trials after a certain amount of time](tune-stopping.html#stop-trials-after-a-certain-amount-of-time)
  + [Stop on trial failures](tune-stopping.html#stop-on-trial-failures)
  + [Early stopping with Tune schedulers](tune-stopping.html#early-stopping-with-tune-schedulers)
  + [Summary](tune-stopping.html#summary)
* [How to Save and Load Trial Checkpoints](tune-trial-checkpoints.html)
  + [Function API Checkpointing](tune-trial-checkpoints.html#function-api-checkpointing)
  + [Class API Checkpointing](tune-trial-checkpoints.html#class-api-checkpointing)
  + [Configurations](tune-trial-checkpoints.html#configurations)
  + [Summary](tune-trial-checkpoints.html#summary)
  + [Appendix: Types of data stored by Tune](tune-trial-checkpoints.html#appendix-types-of-data-stored-by-tune)
* [How to Configure Persistent Storage in Ray Tune](tune-storage.html)
  + [Storage Options in Tune](tune-storage.html#storage-options-in-tune)
  + [Examples](tune-storage.html#examples)
  + [Advanced configuration](tune-storage.html#advanced-configuration)
* [How to Enable Fault Tolerance in Ray Tune](tune-fault-tolerance.html)
  + [Experiment-level Fault Tolerance in Tune](tune-fault-tolerance.html#experiment-level-fault-tolerance-in-tune)
  + [Trial-level Fault Tolerance in Tune](tune-fault-tolerance.html#trial-level-fault-tolerance-in-tune)
  + [Summary](tune-fault-tolerance.html#summary)
* [Using Callbacks and Metrics](tune-metrics.html)
  + [How to work with Callbacks in Ray Tune?](tune-metrics.html#how-to-work-with-callbacks-in-ray-tune)
  + [How to use log metrics in Tune?](tune-metrics.html#how-to-use-log-metrics-in-tune)
* [Getting Data in and out of Tune](tune_get_data_in_and_out.html)
  + [Getting data into Tune](tune_get_data_in_and_out.html#getting-data-into-tune)
  + [Getting data out of Ray Tune](tune_get_data_in_and_out.html#getting-data-out-of-ray-tune)
* [Analyzing Tune Experiment Results](../examples/tune_analyze_results.html)
  + [Loading experiment results from an directory](../examples/tune_analyze_results.html#loading-experiment-results-from-an-directory)
  + [Experiment-level Analysis: Working with `ResultGrid`](../examples/tune_analyze_results.html#experiment-level-analysis-working-with-resultgrid)
  + [Trial-level Analysis: Working with an individual `Result`](../examples/tune_analyze_results.html#trial-level-analysis-working-with-an-individual-result)
  + [Plotting metrics](../examples/tune_analyze_results.html#plotting-metrics)
  + [Accessing checkpoints and loading for test inference](../examples/tune_analyze_results.html#accessing-checkpoints-and-loading-for-test-inference)
  + [Summary](../examples/tune_analyze_results.html#summary)
* [A Guide to Population Based Training with Tune](../examples/pbt_guide.html)
  + [Function API with Population Based Training](../examples/pbt_guide.html#function-api-with-population-based-training)
  + [Replaying a PBT run](../examples/pbt_guide.html#replaying-a-pbt-run)
  + [Example: DCGAN with PBT](../examples/pbt_guide.html#example-dcgan-with-pbt)
  + [Visualization](../examples/pbt_guide.html#visualization)
  + [Summary](../examples/pbt_guide.html#summary)
* [Deploying Tune in the Cloud](tune-distributed.html)
  + [Summary](tune-distributed.html#summary)
  + [Example: Distributed Tune on AWS VMs](tune-distributed.html#example-distributed-tune-on-aws-vms)
  + [Running a Distributed Tune Experiment](tune-distributed.html#running-a-distributed-tune-experiment)
  + [Storage Options in a Distributed Tune Run](tune-distributed.html#storage-options-in-a-distributed-tune-run)
  + [Tune Runs on preemptible instances](tune-distributed.html#tune-runs-on-preemptible-instances)
  + [Fault Tolerance of Tune Runs](tune-distributed.html#fault-tolerance-of-tune-runs)
  + [Common Tune Commands](tune-distributed.html#common-tune-commands)
  + [Troubleshooting](tune-distributed.html#troubleshooting)
* [Tune Architecture](tune-lifecycle.html)
  + [What happens in `Tuner.fit`?](tune-lifecycle.html#what-happens-in-tuner-fit)
  + [Lifecycle of a Tune Trial](tune-lifecycle.html#lifecycle-of-a-tune-trial)
  + [Tune’s Architecture](tune-lifecycle.html#tune-s-architecture)
* [Scalability Benchmarks](tune-scalability.html)
  + [Result throughput](tune-scalability.html#result-throughput)
  + [Network overhead in Ray Tune](tune-scalability.html#network-overhead-in-ray-tune)

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/tune/tutorials/overview.rst)