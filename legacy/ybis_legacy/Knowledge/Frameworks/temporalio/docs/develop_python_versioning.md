Versioning - Python SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

Since Workflow Executions in Temporal can run for long periods — sometimes months or even years — it's common to need to make changes to a Workflow Definition, even while a particular Workflow Execution is in progress.

The Temporal Platform requires that Workflow code is [deterministic](/workflow-definition#deterministic-constraints).
If you make a change to your Workflow code that would cause non-deterministic behavior on Replay, you'll need to use one of our Versioning methods to gracefully update your running Workflows.
With Versioning, you can modify your Workflow Definition so that new executions use the updated code, while existing ones continue running the original version.
There are two primary Versioning methods that you can use:

* [Worker Versioning](/production-deployment/worker-deployments/worker-versioning). The Worker Versioning feature allows you to tag your Workers and programmatically roll them out in versioned deployments, so that old Workers can run old code paths and new Workers can run new code paths.
* [Versioning with Patching](#patching). This method works by adding branches to your code tied to specific revisions. It applies a code change to new Workflow Executions while avoiding disruptive changes to in-progress Workflow Executions.

danger

Support for the experimental Worker Versioning method before 2025 will be removed from Temporal Server in March 2026. Refer to the [latest Worker Versioning docs](/worker-versioning) for guidance. You can still refer to the [Worker Versioning Legacy](/develop/python/worker-versioning-legacy) docs if needed.

## Worker Versioning[​](#worker-versioning "Direct link to Worker Versioning")

Temporal's [Worker Versioning](/production-deployment/worker-deployments/worker-versioning) feature allows you to tag your Workers and programmatically roll them out in Deployment Versions, so that old Workers can run old code paths and new Workers can run new code paths. This way, you can pin your Workflows to specific revisions, avoiding the need for patching.

## Versioning with Patching[​](#patching "Direct link to Versioning with Patching")

### Adding a patch[​](#adding-a-patch "Direct link to Adding a patch")

A Patch defines a logical branch in a Workflow for a specific change, similar to a feature flag.
It applies a code change to new Workflow Executions while avoiding disruptive changes to in-progress Workflow Executions.
When you want to make substantive code changes that may affect existing Workflow Executions, create a patch. Note that there's no need to patch [Pinned Workflows](/worker-versioning).

Suppose you have an initial Workflow version called `pre_patch_activity`:

[View the source code](https://github.com/temporalio/documentation/blob/main/sample-apps/python/version_your_workflows/workflow_1_initial_dacx.py)

in the context of the rest of the application code.

```
from datetime import timedelta  
  
from temporalio import workflow  
  
with workflow.unsafe.imports_passed_through():  
    from activities import pre_patch_activity  
# ...  
@workflow.defn  
class MyWorkflow:  
    @workflow.run  
    async def run(self) -> None:  
        self._result = await workflow.execute_activity(  
            pre_patch_activity,  
            schedule_to_close_timeout=timedelta(minutes=5),  
        )
```

Now, you want to update your code to run `post_patch_activity` instead. This represents your desired end state.

[View the source code](https://github.com/temporalio/documentation/blob/main/sample-apps/python/version_your_workflows/workflow_4_patch_complete_dacx.py)

in the context of the rest of the application code.

```
from datetime import timedelta  
  
from temporalio import workflow  
  
with workflow.unsafe.imports_passed_through():  
    from activities import post_patch_activity  
# ...  
@workflow.defn  
class MyWorkflow:  
    @workflow.run  
    async def run(self) -> None:  
        self._result = await workflow.execute_activity(  
            post_patch_activity,  
            schedule_to_close_timeout=timedelta(minutes=5),  
        )
```

The problem is that you cannot deploy `post_patch_activity` directly until you're certain there are no more running Workflows created using the `pre_patch_activity` code, otherwise you are likely to cause a nondeterminism error.
Instead, you'll need to deploy `post_patched_activity` and use the [patched](https://python.temporal.io/temporalio.workflow.html#patched) function to determine which version of the code to execute.

Patching is a three-step process:

1. Patch in any new, updated code using the `patched()` function. Run the new patched code alongside old code.
2. Remove old code and use `deprecate_patch()` to mark a particular patch as deprecated.
3. Once there are no longer any open Worklow Executions of the previous version of the code, remove `deprecate_patch()`.
   Let's walk through this process in sequence.

### Patching in new code[​](#using-patched-for-workflow-history-markers "Direct link to Patching in new code")

Using `patched` inserts a marker into the Workflow History.
During Replay, if a Worker encounters a history with that marker, it will fail the Workflow task when the Workflow code doesn't produce the same patch marker (in this case, `my-patch`).
This ensures you can safely deploy code from `post_patch_activity` as a "feature flag" alongside the original version (`pre_patch_activity`).

[View the source code](https://github.com/temporalio/documentation/blob/main/sample-apps/python/version_your_workflows/workflow_2_patched_dacx.py)

in the context of the rest of the application code.

```
# ...  
@workflow.defn  
class MyWorkflow:  
    @workflow.run  
    async def run(self) -> None:  
        if workflow.patched("my-patch"):  
            self._result = await workflow.execute_activity(  
                post_patch_activity,  
                schedule_to_close_timeout=timedelta(minutes=5),  
            )  
        else:  
            self._result = await workflow.execute_activity(  
                pre_patch_activity,  
                schedule_to_close_timeout=timedelta(minutes=5),  
            )
```

### Deprecating patches[​](#deprecated-patches "Direct link to Deprecating patches")

After ensuring that all Workflows started with `pre_patch_activity` code have left retention, you can [deprecate the patch](https://python.temporal.io/temporalio.workflow.html#deprecate_patch).

Once your Workflows are no longer running the pre-patch code paths, you can deploy your code with `deprecate_patch()`.
These Workers will be running the most up-to-date version of the Workflow code, which no longer requires the patch.
Deprecated patches serve as a bridge between the final stage of the patching process and the final state that no longer has patches. They function similarly to regular patches by adding a marker to the Workflow History. However, this marker won't cause a replay failure when the Workflow code doesn't produce it.

[View the source code](https://github.com/temporalio/documentation/blob/main/sample-apps/python/version_your_workflows/workflow_3_patch_deprecated_dacx.py)

in the context of the rest of the application code.

```
# ...  
@workflow.defn  
class MyWorkflow:  
    @workflow.run  
    async def run(self) -> None:  
        workflow.deprecate_patch("my-patch")  
        self._result = await workflow.execute_activity(  
            post_patch_activity,  
            schedule_to_close_timeout=timedelta(minutes=5),  
        )
```

### Removing a patch[​](#deploy-new-code "Direct link to Removing a patch")

Once your pre-patch Workflows have left retention, you can then safely deploy Workers that no longer use either the `patched()` or `deprecate_patch()` calls:

[View the source code](https://github.com/temporalio/documentation/blob/main/sample-apps/python/version_your_workflows/workflow_4_patch_complete_dacx.py)

in the context of the rest of the application code.

```
# ...  
@workflow.defn  
class MyWorkflow:  
    @workflow.run  
    async def run(self) -> None:  
        self._result = await workflow.execute_activity(  
            post_patch_activity,  
            schedule_to_close_timeout=timedelta(minutes=5),  
        )
```

Patching allows you to make changes to currently running Workflows.
It is a powerful method for introducing compatible changes without introducing non-determinism errors.

### Detailed Description of the Patched Function[​](#detailed-description-of-the-patched-function "Direct link to Detailed Description of the Patched Function")

This video provides an overview of how the `patched()` function works:

  

For a more in-depth explanation, refer to the [Patching](/patching) Encyclopedia entry.

### Workflow cutovers[​](#workflow-cutovers "Direct link to Workflow cutovers")

To understand why Patching is useful, it's helpful to demonstrate cutting over an entire Workflow.

Since incompatible changes only affect open Workflow Executions of the same type, you can avoid determinism errors by creating a whole new Workflow when making changes.
To do this, you can copy the Workflow Definition function, giving it a different name, and register both names with your Workers.

For example, you would duplicate `PizzaWorkflow` as `PizzaWorkflowV2`:

```
@workflow.defn(name="PizzaWorkflow")  
class PizzaWorkflow:  
    @workflow.run  
    async def run(self, name: str) -> str:  
        # this function contains the original code  
  
@workflow.defn(name="PizzaWorkflowV2")  
class PizzaWorkflowV2:  
    @workflow.run  
    async def run(self, name: str) -> str:  
        # this function contains the updated code
```

You would then need to update the Worker configuration, and any other identifier strings, to register both Workflow Types:

```
worker = Worker(  
    client,  
    task_queue="your-task-queue",  
    workflows=[PizzaWorkflow, PizzaWorkflowV2],  
)
```

The downside of this method is that it requires you to duplicate code and to update any commands used to start the Workflow.
This can become impractical over time.
This method also does not provide a way to version any still-running Workflows -- it is essentially just a cutover, unlike Patching.

### Testing a Workflow for replay safety[​](#testing-a-workflow-for-replay-safety "Direct link to Testing a Workflow for replay safety")

To determine whether your Workflow your needs a patch, or that you've patched it successfully, you should incorporate [Replay Testing](/develop/python/testing-suite#replay).

* [Worker Versioning](#worker-versioning)* [Versioning with Patching](#patching)
    + [Adding a patch](#adding-a-patch)+ [Patching in new code](#using-patched-for-workflow-history-markers)+ [Deprecating patches](#deprecated-patches)+ [Removing a patch](#deploy-new-code)+ [Detailed Description of the Patched Function](#detailed-description-of-the-patched-function)+ [Workflow cutovers](#workflow-cutovers)+ [Testing a Workflow for replay safety](#testing-a-workflow-for-replay-safety)