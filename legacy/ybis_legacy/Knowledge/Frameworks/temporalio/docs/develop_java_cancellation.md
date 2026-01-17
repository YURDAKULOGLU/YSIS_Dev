Interrupt a Workflow Execution - Java SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

You can interrupt a Workflow Execution in one of the following ways:

* [Cancel](#cancellation): Canceling a Workflow provides a graceful way to stop Workflow Execution.
* [Terminate](#termination): Terminating a Workflow forcefully stops Workflow Execution.

Terminating a Workflow forcefully stops Workflow Execution. This action resembles killing a process.

* The system records a `WorkflowExecutionTerminated` event in the Workflow History.
* The termination forcefully and immediately stops the Workflow Execution.
* The Workflow code gets no chance to handle termination.
* A Workflow Task doesn't get scheduled.

In most cases, canceling is preferable because it allows the Workflow to finish gracefully. Terminate only if the
Workflow is stuck and cannot be canceled normally.

## Cancel a Workflow Execution[​](#cancellation "Direct link to Cancel a Workflow Execution")

Canceling a Workflow provides a graceful way to stop Workflow Execution. This action resembles sending a `SIGTERM` to a
process.

* The system records a `WorkflowExecutionCancelRequested` event in the Workflow History.
* A Workflow Task gets scheduled to process the cancelation.
* The Workflow code can handle the cancelation and execute any cleanup logic.
* The system doesn't forcefully stop the Workflow.

To cancel a Workflow Execution in Java, use the
[cancel()](https://javadoc.io/doc/io.temporal/temporal-sdk/latest/io/temporal/client/WorkflowStub.html#cancel())
function on the WorkflowStub.

```
WorkflowStub workflowStub = WorkflowStub.fromTyped(workflow);  
workflowStub.cancel();
```

## Cancellation scopes in Java[​](#cancellation-scopes "Direct link to Cancellation scopes in Java")

In the Java SDK, Workflows are represented internally by a tree of cancellation scopes, each with cancellation behaviors
you can specify. By default, everything runs in the "root" scope.

Scopes are created using the
[Workflow.newCancellationScope](https://javadoc.io/doc/io.temporal/temporal-sdk/latest/io/temporal/workflow/Workflow.html#newCancellationScope(io.temporal.workflow.Functions.Proc1))
constructor

Cancellations are applied to cancellation scopes, which can encompass an entire Workflow or just part of one. Scopes can
be nested, and cancellation propagates from outer scopes to inner ones. A Workflow's method runs in the outermost scope.
Cancellations are handled by catching `CanceledFailure`s thrown by cancelable operations.

You can also use the following APIs:

* `CancellationScope.current()`: Get the current scope.
* `scope.cancel()`: Cancel all operations inside a `scope`.
* `scope.getCancellationRequest()`: A promise that resolves when a scope cancellation is requested, such as when
  Workflow code calls `cancel()` or the entire Workflow is cancelled by an external client.

When a `CancellationScope` is cancelled, it propagates cancellation in any child scopes and of any cancelable operations
created within it, such as the following:

* Activities
* Timers (created with the
  [sleep](https://javadoc.io/doc/io.temporal/temporal-sdk/latest/io/temporal/workflow/Workflow.html#sleep(java.time.Duration))
  function)
* Child Workflows
* Nexus Operations

### Cancel an Activity from a Workflow[​](#cancel-activity "Direct link to Cancel an Activity from a Workflow")

Canceling an Activity from within a Workflow requires that the Activity Execution sends Heartbeats and sets a Heartbeat
Timeout. If the Heartbeat is not invoked, the Activity cannot receive a cancellation request. When any non-immediate
Activity is executed, the Activity Execution should send Heartbeats and set a
[Heartbeat Timeout](/encyclopedia/detecting-activity-failures#heartbeat-timeout) to ensure that the server knows it is
still working.

When an Activity is canceled, an error is raised in the Activity at the next available opportunity. If cleanup logic
needs to be performed, it can be done in a `finally` clause or inside a caught cancel error. However, for the Activity
to appear canceled the exception needs to be re-raised.

note

Unlike regular Activities, [Local Activities](/local-activity) currently do not support cancellation.

To cancel an Activity from a Workflow Execution, call the
[cancel()](https://javadoc.io/doc/io.temporal/temporal-sdk/latest/io/temporal/workflow/CancellationScope.html#cancel())
method on the CancellationScope that the activity was started in.

```
public class GreetingWorkflowImpl implements GreetingWorkflow {  
    @Override  
    public String getGreeting(String name) {  
      List<Promise<String>> results = new ArrayList<>(greetings.length);  
  
      /*  
       * Create our CancellationScope. Within this scope we call the workflow activity  
       * composeGreeting method asynchronously for each of our defined greetings in different  
       * languages.  
       */  
      CancellationScope scope =  
          Workflow.newCancellationScope(  
              () -> {  
                for (String greeting : greetings) {  
                  results.add(Async.function(activities::composeGreeting, greeting, name));  
                }  
              });  
  
      /*  
       * Execute all activities within the CancellationScope. Note that this execution is  
       * non-blocking as the code inside our cancellation scope is also non-blocking.  
       */  
      scope.run();  
  
      // We use "anyOf" here to wait for one of the activity invocations to return  
      String result = Promise.anyOf(results).get();  
  
      // Trigger cancellation of all uncompleted activity invocations within the cancellation scope  
      scope.cancel();  
  
      /*  
       *  Wait for all activities to perform cleanup if needed.  
       *  For the sake of the example we ignore cancellations and  
       *  get all the results so that we can print them in the end.  
       *  
       *  Note that we cannot use "allOf" here as that fails on any Promise failures  
       */  
      for (Promise<String> activityResult : results) {  
        try {  
          activityResult.get();  
        } catch (ActivityFailure e) {  
          if (!(e.getCause() instanceof CanceledFailure)) {  
            throw e;  
          }  
        }  
      }  
      return result;  
    }  
}
```

## Terminate a Workflow Execution[​](#termination "Direct link to Terminate a Workflow Execution")

Terminating a Workflow forcefully stops Workflow Execution. This action resembles killing a process.

* The system records a `WorkflowExecutionTerminated` event in the Workflow History.
* The termination forcefully and immediately stops the Workflow Execution.
* The Workflow code gets no chance to handle termination.
* A Workflow Task doesn't get scheduled.

To terminate a Workflow Execution in Java, use the
[terminate()](https://javadoc.io/doc/io.temporal/temporal-sdk/latest/io/temporal/client/WorkflowStub.html#terminate(java.lang.String,java.lang.Object...))
function on the WorkflowStub.

```
WorkflowStub untyped = WorkflowStub.fromTyped(myWorkflowStub);  
untyped.terminate("Sample reason");
```

## Reset a Workflow Execution[​](#reset "Direct link to Reset a Workflow Execution")

Resetting a Workflow Execution terminates the current Workflow Execution and starts a new Workflow Execution from a
point you specify in its Event History. Use reset when a Workflow is blocked due to a non-deterministic error or other
issues that prevent it from completing.

When you reset a Workflow, the Event History up to the reset point is copied to the new Workflow Execution, and the
Workflow resumes from that point with the current code. Reset only works if you've fixed the underlying issue, such as
removing non-deterministic code. Any progress made after the reset point will be discarded. Provide a reason when
resetting, as it will be recorded in the Event History.

* Web UI* Temporal CLI

1. Navigate to the Workflow Execution details page,
2. Click the **Reset** button in the top right dropdown menu,
3. Select the Event ID to reset to,
4. Provide a reason for the reset,
5. Confirm the reset.

The Web UI shows available reset points and creates a link to the new Workflow Execution after the reset completes.

Use the `temporal workflow reset` command to reset a Workflow Execution:

```
temporal workflow reset \  
    --workflow-id <workflow-id> \  
    --event-id <event-id> \  
    --reason "Reason for reset"
```

For example:

```
temporal workflow reset \  
    --workflow-id my-background-check \  
    --event-id 4 \  
    --reason "Fixed non-deterministic code"
```

By default, the command resets the latest Workflow Execution in the `default` Namespace. Use `--run-id` to reset a
specific run. Use `--namespace` to specify a different Namespace:

```
temporal workflow reset \  
    --workflow-id my-background-check \  
    --event-id 4 \  
    --reason "Fixed non-deterministic code" \  
    --namespace my-namespace \  
    --tls-cert-path /path/to/cert.pem \  
    --tls-key-path /path/to/key.pem
```

Monitor the new Workflow Execution after resetting to ensure it completes successfully.

* [Cancel a Workflow Execution](#cancellation)* [Cancellation scopes in Java](#cancellation-scopes)
    + [Cancel an Activity from a Workflow](#cancel-activity)* [Terminate a Workflow Execution](#termination)* [Reset a Workflow Execution](#reset)