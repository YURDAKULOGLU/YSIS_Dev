Errors | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

This reference lists possible [Workflow Task](/tasks#workflow-task) errors and how to resolve them.

> For other types of errors, see [Temporal Failures](https://docs.temporal.io/kb/failures).

Each of the below errors corresponds with a [WorkflowTaskFailedCause](https://api-docs.temporal.io/#temporal.api.enums.v1.WorkflowTaskFailedCause), which appears in [Events](/workflow-execution/event#event) under `workflow_task_failed_event_attributes`.

## Bad Cancel Timer Attributes[​](#bad-cancel-timer-attributes "Direct link to Bad Cancel Timer Attributes")

This error indicates that the [Workflow Task](/tasks#workflow-task) failed while attempting to cancel a Timer.

Check your Timer attributes for a missing Timer Id value.
Add a valid Timer Id and redeploy the code.

## Bad Cancel Workflow Execution Attributes[​](#bad-cancel-workflow-execution-attributes "Direct link to Bad Cancel Workflow Execution Attributes")

The [Workflow Task](/tasks#workflow-task) failed due to unset [CancelWorkflowExecution](/references/commands#cancelworkflowexecution) attributes.

Reset any missing attributes and redeploy the Workflow Task.

## Bad Complete Workflow Execution Attributes[​](#bad-complete-workflow-execution-attributes "Direct link to Bad Complete Workflow Execution Attributes")

This error indicates that the [Workflow Task](/tasks#workflow-task) failed due to unset attributes on [CompleteWorkflowExecution](/references/commands#completeworkflowexecution).

Reset any missing attributes.
Adjust the size of your Payload if it exceeds size limits.

## Bad Continue as New Attributes[​](#bad-continue-as-new-attributes "Direct link to Bad Continue as New Attributes")

This error indicates that the [Workflow Task](/tasks#workflow-task) failed to validate a [ContinueAsNew](/references/commands#continueasnewworkflowexecution) attribute.
The attribute could be unset or invalid.

Reset any missing attributes.
If the payload or memo exceeded size limits, adjust the input size.

Check that the [Workflow](/workflows) is validating search attributes after unaliasing keys.

## Bad Fail Workflow Execution Attributes[​](#bad-fail-workflow-execution-attributes "Direct link to Bad Fail Workflow Execution Attributes")

This error indicates that the [Workflow Task](/tasks#workflow-task) failed due to unset [FailWorkflowExecution](/references/commands#failworkflowexecution) attributes.

If you encounter this error, make sure that `StartToClostTimeout` or `ScheduleToCloseTimeout` are set.
Restart the [Worker](/workers) that the [Workflow](/workflows) and [Activity](/activities) are registered to.

## Bad Modify Workflow Properties Attributes[​](#bad-modify-workflow-properties-attributes "Direct link to Bad Modify Workflow Properties Attributes")

This error indicates that the [Workflow Task](/tasks#workflow-task) failed to validate attributes on a property in the Upsert Memo or in a payload.
These attributes are either unset or exceeding size limits.

Reset any unset and empty attributes.
Adjust the size of the [Memo](/workflow-execution#memo) or payload to fit within the system's limits.

## Bad Record Marker Attributes[​](#bad-record-marker-attributes "Direct link to Bad Record Marker Attributes")

This error indicates that the [Workflow Task](/tasks#workflow-task) failed due to an unset or incorrect [Marker](/references/events#markerrecorded) name.

Enter a valid Marker name and redeploy the Task.

## Bad Request Cancel Activity Attributes[​](#bad-request-cancel-activity-attributes "Direct link to Bad Request Cancel Activity Attributes")

This error either indicates the possibility of unset attributes for [RequestCancelActivity](/references/commands#requestcancelactivitytask), or an invalid History Builder state.

Update the [Temporal SDK](/encyclopedia/temporal-sdks) to the most recent release.
Reset any unset attributes before retrying the [Workflow Task](/tasks#workflow-task).

If you continue to see this error, review your code for [nondeterministic causes](/workflow-definition#non-deterministic-change).

## Bad Request Cancel External Workflow Execution Attributes[​](#bad-request-cancel-external-workflow-execution "Direct link to Bad Request Cancel External Workflow Execution Attributes")

This error indicates that the [Workflow Task](/tasks#workflow-task) failed while trying to cancel an external Workflow.
Unset or invalid attributes can cause this to occur.

Reset any missing attributes, such as Workflow Id or Run Id.
Adjust any fields that exceed length limits.

If [Child Workflow](/child-workflows) is set to `Start` and `RequestCancel`, remove one of these attributes.
A Child Workflow cannot perform both actions in the same Workflow Task.

## Bad Schedule Activity Attributes[​](#bad-schedule-activity-attributes "Direct link to Bad Schedule Activity Attributes")

This error indicates unset or invalid attributes for [`ScheduleActivityTask`](/references/commands#scheduleactivitytask) or [`CompleteWorkflowExecution`](/references/commands#completeworkflowexecution).

Reset any unset or empty attributes.
Adjust the size of the received payload to stay within the given size limit.

## Bad Schedule Nexus Operation Attributes[​](#bad-schedule-nexus-operation-attributes "Direct link to Bad Schedule Nexus Operation Attributes")

This error indicates unset or invalid attributes for ScheduleNexusOperation, for example if the Nexus Endpoint name used in the caller Workflow doesn't exist.

Inspect the reason given in the error for mitigation when possible.

## Bad Search Attributes[​](#bad-search-attributes "Direct link to Bad Search Attributes")

This error indicates that the [Workflow Task](/tasks#workflow-task) has unset or invalid [Search Attributes](/search-attribute).
This can cause Workflow Tasks to continue to retry without success.

Make sure that all attributes are defined before retrying the Task.
Adjust the size of the Payload to fit within the system's size limits.

## Bad Signal Input Size[​](#bad-signal-input-size "Direct link to Bad Signal Input Size")

This error indicates that the Payload has exceeded the [Signal's](/sending-messages#sending-signals) available input size.

Adjust the size of the Payload, and redeploy the [Workflow Task](/tasks#workflow-task).

## Bad Signal Workflow Execution Attributes[​](#bad-signal-workflow-execution-attributes "Direct link to Bad Signal Workflow Execution Attributes")

This error indicates that the [Workflow Task](/tasks#workflow-task) failed to validate attributes for [SignalExternalWorkflowExecution](/references/commands#signalexternalworkflowexecution).

Reset any unset, missing, nil, or invalid attributes.
Adjust the input to fit within the system's size limits.

## Bad Start Child Execution Attributes[​](#bad-start-child-execution-attributes "Direct link to Bad Start Child Execution Attributes")

This error indicates that the [Workflow Task](/tasks#workflow-task) failed to validate attributes for [`StartChildWorkflowExecution`](/references/commands#startchildworkflowexecution)

Adjust the input size of the attributes to fall within the system's size limits.

Make sure that [Search Attribute](/search-attribute) validation is performed after unaliasing keys.

## Bad Start Timer Attributes[​](#bad-start-timer-attributes "Direct link to Bad Start Timer Attributes")

This error indicates that the scheduled [Event](/workflow-execution/event#event) is missing a Timer Id.

Set a valid Timer Id and retry the [Workflow Task](/tasks#workflow-task).

## Cause Bad Binary[​](#cause-bad-binary "Direct link to Cause Bad Binary")

This error indicates that the [Worker](/workers) deployment returned a bad binary checksum.

## Cause Bad Update[​](#cause-bad-update "Direct link to Cause Bad Update")

This error indicates that a [Workflow Execution](/workflow-execution) tried to complete before receiving an Update.

`BadUpdate` can happen when a [Worker](/workers#worker) generates a [Workflow Task Completed](/references/events#workflowtaskcompleted) message with missing fields or an invalid Update response format.

This error might indicate usage of an unsupported SDK.
Make sure you're using a [supported SDK](/encyclopedia/temporal-sdks).

## Cause Reset Workflow[​](#cause-reset-workflow "Direct link to Cause Reset Workflow")

This error indicates that the [Workflow Task](/tasks#workflow-task) failed due to a request to reset the [Workflow](/workflows).

If the system hasn't started a new Workflow, manually reset the Workflow.

## Cause Unhandled Update[​](#cause-unhandled-update "Direct link to Cause Unhandled Update")

`UnhandledUpdate` occurs when a Workflow Update is received by the Temporal Server while a Workflow Task being processed on a Worker produces a Command that would cause the Workflow to transition to a closed state.

Temporal rejects the Workflow Task completion to guarantee that the Update is eventually handled by Workflow code and rewinds the Workflow so it can handle the pending Update.

This error can happen when the Workflow receives frequent Updates.

## Cause Unspecified[​](#cause-unspecified "Direct link to Cause Unspecified")

This error indicates that the [Workflow Task](/tasks#workflow-task) has failed for an unknown reason.

If you see this error, examine your Workflow Definition.

## Failover Close Command[​](#failover-close-command "Direct link to Failover Close Command")

This error indicates that a [Namespace](/namespaces) failover forced the [Workflow Task](/tasks#workflow-task) to close.
The system automatically schedules a retry when this error occurs.

## Force Close Command[​](#force-close-command "Direct link to Force Close Command")

This error indicates that the [Workflow Task](/tasks#workflow-task) was forced to close.
A retry will be scheduled if the error is recoverable.

## Nondeterminism Error[​](#non-deterministic-error "Direct link to Nondeterminism Error")

The [Workflow Task](/tasks#workflow-task) failed due to a [nondeterminism error](/workflow-definition#non-deterministic-change).

## Pending Activities Limit Exceeded[​](#pending-activities-limit-exceeded "Direct link to Pending Activities Limit Exceeded")

The [Workflow](/workflows) has reached capacity for pending [Activities](/activities).
Therefore, the [Workflow Task](/tasks#workflow-task) was failed to prevent the creation of another Activity.

Let the Workflow complete any current Activities before redeploying the code.

## Pending Child Workflows Limit Exceeded[​](#pending-child-workflows-limit-exceeded "Direct link to Pending Child Workflows Limit Exceeded")

This error indicates that the [Workflow](/workflows) has reached capacity for pending [Child Workflows](/child-workflows).
Therefore, the [Workflow Task](/tasks#workflow-task) was failed to prevent additional Child Workflows from being added.

Wait for the system to finish any currently running Child Workflows before redeploying this Task.

## Pending Nexus Operations Limit Exceeded[​](#pending-nexus-operations-limit-exceeded "Direct link to Pending Nexus Operations Limit Exceeded")

The Workflow has reached capacity for pending Nexus Operations. Therefore, the Workflow Task was failed to prevent the creation of another Nexus Operation.

Let the Workflow complete any current Nexus Operation before retrying the Task.

See [Per Workflow Nexus Operation Limits](/cloud/limits#per-workflow-nexus-operation-limits) for details.

## Pending Request Cancel Limit Exceeded[​](#pending-request-cancel-limit-exceeded "Direct link to Pending Request Cancel Limit Exceeded")

This error indicates that the [Workflow Task](/tasks#workflow-task) failed after attempting to add more cancel requests.
The [Workflow](/workflows) has reached capacity for pending requests to cancel other Workflows, and cannot accept more requests.

If you see this error, give the system time to process pending requests before retrying the Task.

## Pending Signals Limit Exceeded[​](#pending-signals-limit-exceeded "Direct link to Pending Signals Limit Exceeded")

The Workflow has reached capacity for pending Signals.
Therefore, the [Workflow Task](/tasks#workflow-task) was failed after attempting to add more [Signals](/sending-messages#sending-signals) to an external Workflow.

Wait for Signals to be processed by the Workflow before retrying the Task.

## Reset Sticky Task Queue[​](#reset-sticky-task-queue "Direct link to Reset Sticky Task Queue")

This error indicates that the Sticky [Task Queue](/task-queue) needs to be reset.

If you see this error, reset the Sticky Task Queue.
The system will retry automatically.

## Resource Exhausted Cause Concurrent Limit[​](#resource-exhausted-cause-concurrent-limit "Direct link to Resource Exhausted Cause Concurrent Limit")

This error indicates that the concurrent [poller count](/develop/worker-performance#poller-count) has been exhausted.

Adjust the poller count per [Worker](/workers).

## Resource Exhausted Cause Persistence Limit[​](#resource-exhausted-cause-persistence-limit "Direct link to Resource Exhausted Cause Persistence Limit")

This error indicates that the persistence rate limit has been reached.

## Resource Exhausted Cause RPS Limit[​](#resource-exhausted-cause-rps-limit "Direct link to Resource Exhausted Cause RPS Limit")

This error indicates that the [Workflow](/workflows) has exhausted its RPS limit.

## Resource Exhausted Cause System Overload[​](#resource-exhausted-cause-system-overload "Direct link to Resource Exhausted Cause System Overload")

This error indicates that the system is overloaded and cannot allocate further resources to [Workflow Tasks](/tasks#workflow-task).

## Resource Exhausted Cause Unspecified[​](#resource-exhausted-cause-unspecified "Direct link to Resource Exhausted Cause Unspecified")

This error indicates that an unknown cause is preventing resources from being allocated to further [Workflow Tasks](/tasks#workflow-task).

## Schedule Activity Duplicate Id[​](#schedule-activity-duplicate-id "Direct link to Schedule Activity Duplicate Id")

The [Workflow Task](/tasks#workflow-task) failed because the [Activity](/activities) Id is already in use.

Check your code to see if you've already specified the same Activity Id in your [Workflow](/workflows).
Enter another Activity Id, and try running the Workflow Task again.

## Start Timer Duplicate Id[​](#start-timer-duplicate-id "Direct link to Start Timer Duplicate Id")

This error indicates that a Timer with the given Timer Id has already started.

Try entering a different Timer Id, and retry the [Workflow Task](/tasks#workflow-task).

## Unhandled Command[​](#unhandled-command "Direct link to Unhandled Command")

This error indicates new available [Events](/references/events) since the last [Workflow Task](/tasks#workflow-task) started.
The Workflow Task was failed because the [Workflow](/workflows) attempted to close itself without handling the new Events.

`UnhandledCommand` can happen when the Workflow is receiving a high number of [Signals](/sending-messages#sending-signals).
If the Workflow doesn't have enough time to handle these Signals, a RetryWorkflow Task is scheduled to handle these new Events.

To prevent this error, drain the Signal Channel with the ReceiveAsync function.

If you continue to see this error, check your logs for failing Workflow Tasks.
The Workflow may have been picked up by a different [Worker](/workers#worker).

## Workflow Worker Unhandled Failure[​](#workflow-worker-unhandled-failure "Direct link to Workflow Worker Unhandled Failure")

This error indicates that the [Workflow Task](/tasks#workflow-task) encountered an unhandled failure from the [Workflow Definition](/workflow-definition).

* [Bad Cancel Timer Attributes](#bad-cancel-timer-attributes)* [Bad Cancel Workflow Execution Attributes](#bad-cancel-workflow-execution-attributes)* [Bad Complete Workflow Execution Attributes](#bad-complete-workflow-execution-attributes)* [Bad Continue as New Attributes](#bad-continue-as-new-attributes)* [Bad Fail Workflow Execution Attributes](#bad-fail-workflow-execution-attributes)* [Bad Modify Workflow Properties Attributes](#bad-modify-workflow-properties-attributes)* [Bad Record Marker Attributes](#bad-record-marker-attributes)* [Bad Request Cancel Activity Attributes](#bad-request-cancel-activity-attributes)* [Bad Request Cancel External Workflow Execution Attributes](#bad-request-cancel-external-workflow-execution)* [Bad Schedule Activity Attributes](#bad-schedule-activity-attributes)* [Bad Schedule Nexus Operation Attributes](#bad-schedule-nexus-operation-attributes)* [Bad Search Attributes](#bad-search-attributes)* [Bad Signal Input Size](#bad-signal-input-size)* [Bad Signal Workflow Execution Attributes](#bad-signal-workflow-execution-attributes)* [Bad Start Child Execution Attributes](#bad-start-child-execution-attributes)* [Bad Start Timer Attributes](#bad-start-timer-attributes)* [Cause Bad Binary](#cause-bad-binary)* [Cause Bad Update](#cause-bad-update)* [Cause Reset Workflow](#cause-reset-workflow)* [Cause Unhandled Update](#cause-unhandled-update)* [Cause Unspecified](#cause-unspecified)* [Failover Close Command](#failover-close-command)* [Force Close Command](#force-close-command)* [Nondeterminism Error](#non-deterministic-error)* [Pending Activities Limit Exceeded](#pending-activities-limit-exceeded)* [Pending Child Workflows Limit Exceeded](#pending-child-workflows-limit-exceeded)* [Pending Nexus Operations Limit Exceeded](#pending-nexus-operations-limit-exceeded)* [Pending Request Cancel Limit Exceeded](#pending-request-cancel-limit-exceeded)* [Pending Signals Limit Exceeded](#pending-signals-limit-exceeded)* [Reset Sticky Task Queue](#reset-sticky-task-queue)* [Resource Exhausted Cause Concurrent Limit](#resource-exhausted-cause-concurrent-limit)* [Resource Exhausted Cause Persistence Limit](#resource-exhausted-cause-persistence-limit)* [Resource Exhausted Cause RPS Limit](#resource-exhausted-cause-rps-limit)* [Resource Exhausted Cause System Overload](#resource-exhausted-cause-system-overload)* [Resource Exhausted Cause Unspecified](#resource-exhausted-cause-unspecified)* [Schedule Activity Duplicate Id](#schedule-activity-duplicate-id)* [Start Timer Duplicate Id](#start-timer-duplicate-id)* [Unhandled Command](#unhandled-command)* [Workflow Worker Unhandled Failure](#workflow-worker-unhandled-failure)