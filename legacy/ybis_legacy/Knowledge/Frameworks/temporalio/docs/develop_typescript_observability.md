Observability - TypeScript SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

The observability section of the TypeScript developer guide covers the many ways to view the current state of your [Temporal Application](/temporal#temporal-application)—that is, ways to view which [Workflow Executions](/workflow-execution) are tracked by the [Temporal Platform](/temporal#temporal-platform) and the state of any specified Workflow Execution, either currently or at points of an execution.

This section covers features related to viewing the state of the application, including:

* [Emit metrics](#metrics)
* [Set up tracing](#tracing)
* [Log from a Workflow](#logging)
* [Visibility APIs](#visibility)

## Emit metrics[​](#metrics "Direct link to Emit metrics")

Each Temporal SDK is capable of emitting an optional set of metrics from either the Client or the Worker process.
For a complete list of metrics capable of being emitted, see the [SDK metrics reference](/references/sdk-metrics).

* For an overview of Prometheus and Grafana integration, refer to the [Monitoring](/self-hosted-guide/monitoring) guide.
* For a list of metrics, see the [SDK metrics reference](/references/sdk-metrics).
* For an end-to-end example that exposes metrics with the TypeScript SDK, refer to the [samples-typescript](https://github.com/temporalio/samples-typescript/tree/main/interceptors-opentelemetry) repo.

Workers can emit metrics and traces. There are a few [telemetry options](https://typescript.temporal.io/api/interfaces/worker.TelemetryOptions) that can be provided to [`Runtime.install`](https://typescript.temporal.io/api/classes/worker.Runtime/#install). The common options are:

* `metrics: { otel: { url } }`: The URL of a gRPC [OpenTelemetry collector](https://opentelemetry.io/docs/collector/).
* `metrics: { prometheus: { bindAddress } }`: Address on the Worker host that will have metrics for [Prometheus](https://prometheus.io/) to scrape.

To set up tracing of Workflows and Activities, use our `opentelemetry-interceptors` package.
(For details, see the next section.)

```
telemetryOptions: {  
    metrics: {  
      prometheus: { bindAddress: '0.0.0.0:9464' },  
    },  
    logging: { forward: { level: 'DEBUG' } },  
  },
```

## Set up tracing[​](#tracing "Direct link to Set up tracing")

Tracing allows you to view the call graph of a Workflow along with its Activities and any Child Workflows.

Temporal Web's tracing capabilities mainly track Activity Execution within a Temporal context. If you need custom tracing specific for your use case, you should make use of context propagation to add tracing logic accordingly.

The [`interceptors-opentelemetry`](https://github.com/temporalio/samples-typescript/tree/main/interceptors-opentelemetry) sample shows how to use the SDK's built-in OpenTelemetry tracing to trace everything from starting a Workflow to Workflow Execution to running an Activity from that Workflow.

The built-in tracing uses protobuf message headers (like [this one](https://github.com/temporalio/api/blob/b2b8ae6592a8730dd5be6d90569d1aea84e1712f/temporal/api/workflowservice/v1/request_response.proto#L161) when starting a Workflow) to propagate the tracing information from the client to the Workflow and from the Workflow to its successors (when Continued As New), children, and Activities.
All of these executions are linked with a single trace identifier and have the proper `parent -> child` span relation.

Tracing is compatible between different Temporal SDKs as long as compatible [context propagators](https://opentelemetry.io/docs/concepts/context-propagation/) are used.

**Context propagation**

The TypeScript SDK uses the global OpenTelemetry propagator.

To extend the default ([Trace Context](https://github.com/open-telemetry/opentelemetry-js/blob/main/packages/opentelemetry-core/README.md#w3ctracecontextpropagator-propagator) and [Baggage](https://github.com/open-telemetry/opentelemetry-js/blob/main/packages/opentelemetry-core/README.md#baggage-propagator) propagators) to also include the [Jaeger propagator](https://www.npmjs.com/package/@opentelemetry/propagator-jaeger), follow these steps:

* `npm i @opentelemetry/propagator-jaeger`
* At the top level of your Workflow code, add the following lines:

  ```
  import { propagation } from '@opentelemetry/api';  
  import {  
    CompositePropagator,  
    W3CBaggagePropagator,  
    W3CTraceContextPropagator,  
  } from '@opentelemetry/core';  
  import { JaegerPropagator } from '@opentelemetry/propagator-jaeger';  
    
  propagation.setGlobalPropagator(  
    new CompositePropagator({  
      propagators: [  
        new W3CTraceContextPropagator(),  
        new W3CBaggagePropagator(),  
        new JaegerPropagator(),  
      ],  
    }),  
  );
  ```

Similarly, you can customize the OpenTelemetry `NodeSDK` propagators by following the instructions in the [Initialize the SDK](https://github.com/open-telemetry/opentelemetry-js/tree/main/experimental/packages/opentelemetry-sdk-node#initialize-the-sdk) section of the `README.md` file.

## Log from a Workflow[​](#logging "Direct link to Log from a Workflow")

Logging enables you to record critical information during code execution.
Loggers create an audit trail and capture information about your Workflow's operation.
An appropriate logging level depends on your specific needs.
During development or troubleshooting, you might use debug or even trace.
In production, you might use info or warn to avoid excessive log volume.

The logger supports the following logging levels:

|  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Level Use|  |  |  |  |  |  |  |  |  |  | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | `TRACE` The most detailed level of logging, used for very fine-grained information.|  |  |  |  |  |  |  |  | | --- | --- | --- | --- | --- | --- | --- | --- | | `DEBUG` Detailed information, typically useful for debugging purposes.|  |  |  |  |  |  | | --- | --- | --- | --- | --- | --- | | `INFO` General information about the application's operation.|  |  |  |  | | --- | --- | --- | --- | | `WARN` Indicates potentially harmful situations or minor issues that don't prevent the application from working.|  |  | | --- | --- | | `ERROR` Indicates error conditions that might still allow the application to continue running. | | | | | | | | | | | |

The Temporal SDK core normally uses `WARN` as its default logging level.

### Logging from Activities[​](#logging-from-activities "Direct link to Logging from Activities")

Activities run in the standard Node.js environment and may therefore use any Node.js logger directly.

The Temporal SDK however provides a convenient Activity Context logger, which funnels log messages to the [Runtime's logger](/develop/typescript/observability#customizing-the-default-logger). Attributes from the current Activity context are automatically included as metadata on every log entries emitted using the Activity context logger, and some key events of the Activity's lifecycle are automatically logged (at DEBUG level for most messages; WARN for failures).

Using the Activity Context logger

```
import { log } from '@temporalio/activity';  
  
export async function greet(name: string): Promise<string> {  
  log.info('Log from activity', { name });  
  return `Hello, ${name}!`;  
}
```



### Logging from Workflows[​](#logging-from-workflows "Direct link to Logging from Workflows")

Workflows may not use regular Node.js loggers because:

1. Workflows run in a sandboxed environment and cannot do any I/O.
2. Workflow code might get replayed at any time, which would result in duplicated log messages.

The Temporal SDK however provides a Workflow Context logger, which funnels log messages to the [Runtime's logger](/develop/typescript/observability#customizing-the-default-logger). Attributes from the current Workflow context are automatically included as metadata on every log entries emitted using the Workflow context logger, and some key events of the Workflow's lifecycle are automatically logged (at DEBUG level for most messages; WARN for failures).

Using the Workflow Context logger

```
import { log } from '@temporalio/workflow';  
  
export async function myWorkflow(name: string): Promise<string> {  
  log.info('Log from workflow', { name });  
  return `Hello, ${name}!`;  
}
```

The Workflow Context Logger tries to avoid reemitting log messages on Workflow Replays.

#### Limitations of Workflow logs[​](#limitations-of-workflow-logs "Direct link to Limitations of Workflow logs")

Internally, Workflow logging uses Sinks, and is consequently subject to the same limitations as Sinks.
Notably, logged objects must be serializable using the V8 serialization.

### What is the Runtime's Logger[​](#what-is-the-runtimes-logger "Direct link to What is the Runtime's Logger")

A Temporal Worker may emit logs in various ways, including:

* Messages emitted using the [Workflow Context Logger](#logging);
* Messages emitted using the [Activity Context Logger](#logging-from-activities);
* Messages emitted by the TypeScript SDK Worker itself;
* Messages emitted by the underlying Temporal Core SDK (native code).

All of these messages are internally routed to a single logger object, called the Runtime's Logger.
By default, the Runtime's Logger simply write messages to the console (i.e. the process's `STDOUT`).

#### How to customize the Runtime's Logger[​](#how-to-customize-the-runtimes-logger "Direct link to How to customize the Runtime's Logger")

A custom Runtime Logger may be registered when the SDK `Runtime` is instantiated. This is done only once per process.

To register a custom Runtime Logger, you must explicitly instantiate the Runtime, using the [`Runtime.install()`](https://typescript.temporal.io/api/classes/worker.Runtime/#install) function.
For example:

```
import {  
  DefaultLogger,  
  makeTelemetryFilterString,  
  Runtime,  
} from '@temporalio/worker';  
  
// This is your custom Logger.  
const logger = new DefaultLogger('WARN', ({ level, message }) => {  
  console.log(`Custom logger: ${level} — ${message}`);  
});  
  
Runtime.install({  
  logger,  
  // The following block is optional, but generally desired.  
  // It allows capturing log messages emitted by the underlying Temporal Core SDK (native code).  
  // The Telemetry Filter String determine the desired verboseness of messages emitted by the  
  // Temporal Core SDK itself ("core"), and by other native libraries ("other").  
  telemetryOptions: {  
    logging: {  
      filter: makeTelemetryFilterString({ core: 'INFO', other: 'INFO' }),  
      forward: {},  
    },  
  },  
});
```

A common use case for this is to write log messages to a file to be picked up by a collector service, such as the [Datadog Agent](https://docs.datadoghq.com/logs/log_collection/nodejs/?tab=winston30).
For example:

```
import {  
  DefaultLogger,  
  makeTelemetryFilterString,  
  Runtime,  
} from '@temporalio/worker';  
import winston from 'winston';  
  
const logger = winston.createLogger({  
  level: 'info',  
  format: winston.format.json(),  
  transports: [new transports.File({ filename: '/path/to/worker.log' })],  
});  
  
Runtime.install({  
  logger,  
  // The following block is optional, but generally desired.  
  // It allows capturing log messages emitted by the underlying Temporal Core SDK (native code).  
  // The Telemetry Filter String determine the desired verboseness of messages emitted by the  
  // Temporal Core SDK itself ("core"), and by other native libraries ("other").  
  telemetryOptions: {  
    logging: {  
      filter: makeTelemetryFilterString({ core: 'INFO', other: 'INFO' }),  
      forward: {},  
    },  
  },  
});
```

### Implementing custom Logging-like features based on Workflow Sinks[​](#implementing-custom-logging-like-features-based-on-workflow-sinks "Direct link to Implementing custom Logging-like features based on Workflow Sinks")

Sinks enable one-way export of logs, metrics, and traces from the Workflow isolate to the Node.js environment.

Sinks are written as objects with methods.
Similar to Activities, they are declared in the Worker and then proxied in Workflow code, and it helps to share types between both.

#### Comparing Sinks and Activities[​](#comparing-sinks-and-activities "Direct link to Comparing Sinks and Activities")

Sinks are similar to Activities in that they are both registered on the Worker and proxied into the Workflow.
However, they differ from Activities in important ways:

* A sink function doesn't return any value back to the Workflow and cannot be awaited.
* A sink call isn't recorded in the Event History of a Workflow Execution (no timeouts or retries).
* A sink function *always* runs on the same Worker that runs the Workflow Execution it's called from.

#### Declare the sink interface[​](#declare-the-sink-interface "Direct link to Declare the sink interface")

Explicitly declaring a sink's interface is optional but is useful for ensuring type safety in subsequent steps:

[sinks/src/workflows.ts](https://github.com/temporalio/samples-typescript/blob/main/sinks/src/workflows.ts)

```
import { log, proxySinks, Sinks } from '@temporalio/workflow';  
  
export interface AlertSinks extends Sinks {  
  alerter: {  
    alert(message: string): void;  
  };  
}  
  
export type MySinks = AlertSinks;
```

#### Implement sinks[​](#implement-sinks "Direct link to Implement sinks")

Implementing sinks is a two-step process.

Implement and inject the Sink function into a Worker

[sinks/src/worker.ts](https://github.com/temporalio/samples-typescript/blob/main/sinks/src/worker.ts)

```
import { InjectedSinks, Worker } from '@temporalio/worker';  
import { MySinks } from './workflows';  
  
async function main() {  
  const sinks: InjectedSinks<MySinks> = {  
    alerter: {  
      alert: {  
        fn(workflowInfo, message) {  
          console.log('sending SMS alert!', {  
            workflowId: workflowInfo.workflowId,  
            workflowRunId: workflowInfo.runId,  
            message,  
          });  
        },  
        callDuringReplay: false, // The default  
      },  
    },  
  };  
  const worker = await Worker.create({  
    workflowsPath: require.resolve('./workflows'),  
    taskQueue: 'sinks',  
    sinks,  
  });  
  await worker.run();  
  console.log('Worker gracefully shutdown');  
}  
  
main().catch((err) => {  
  console.error(err);  
  process.exit(1);  
});
```

* Sink function implementations are passed as an object into [WorkerOptions](https://typescript.temporal.io/api/interfaces/worker.WorkerOptions/#sinks).
* You can specify whether you want the injected function to be called during Workflow replay by setting the `callDuringReplay` option.

#### Proxy and call a sink function from a Workflow[​](#proxy-and-call-a-sink-function-from-a-workflow "Direct link to Proxy and call a sink function from a Workflow")

[sinks/src/workflows.ts](https://github.com/temporalio/samples-typescript/blob/main/sinks/src/workflows.ts)

```
const { alerter } = proxySinks<MySinks>();  
  
export async function sinkWorkflow(): Promise<string> {  
  log.info('Workflow Execution started');  
  alerter.alert('alerter: Workflow Execution started');  
  return 'Hello, Temporal!';  
}
```

Some important features of the [InjectedSinkFunction](https://typescript.temporal.io/api/interfaces/worker.InjectedSinkFunction) interface:

* **Injected WorkflowInfo argument:** The first argument of a Sink function implementation is a [`workflowInfo` object](https://typescript.temporal.io/api/interfaces/workflow.WorkflowInfo/) that contains useful metadata.
* **Limited arguments types:** The remaining Sink function arguments are copied between the sandbox and the Node.js environment using the [structured clone algorithm](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm).
* **No return value:** To prevent breaking determinism, Sink functions cannot return values to the Workflow.

**Advanced: Performance considerations and non-blocking Sinks**

The injected sink function contributes to the overall Workflow Task processing duration.

* If you have a long-running sink function, such as one that tries to communicate with external services, you might start seeing Workflow Task timeouts.
* The effect is multiplied when using `callDuringReplay: true` and replaying long Workflow histories because the Workflow Task timer starts when the first history page is delivered to the Worker.

### How to provide a custom logger[​](#custom-logger "Direct link to How to provide a custom logger")

Use a custom logger for logging.

#### Logging in Workers and Clients[​](#logging-in-workers-and-clients "Direct link to Logging in Workers and Clients")

The Worker comes with a default logger, which defaults to log any messages with level `INFO` and higher to `STDERR` using `console.error`.
The following [log levels](https://typescript.temporal.io/api/namespaces/worker#loglevel) are listed in increasing order of severity.

#### Customizing the default logger[​](#customizing-the-default-logger "Direct link to Customizing the default logger")

Temporal uses a [`DefaultLogger`](https://typescript.temporal.io/api/classes/worker.DefaultLogger/) that implements the basic interface:

```
import { DefaultLogger, Runtime } from '@temporalio/worker';  
  
const logger = new DefaultLogger('WARN', ({ level, message }) => {  
  console.log(`Custom logger: ${level} — ${message}`);  
});  
Runtime.install({ logger });
```

The previous code example sets the default logger to log only messages with level `WARN` and higher.

#### Accumulate logs for testing and reporting[​](#accumulate-logs-for-testing-and-reporting "Direct link to Accumulate logs for testing and reporting")

```
import { DefaultLogger, LogEntry, LogLevel } from '@temporalio/worker';  
  
const logs: LogEntry[] = [];  
const logger = new DefaultLogger(LogLevel.TRACE, (entry) => logs.push(entry));  
  
logger.debug('hey', { a: 1 });  
logger.info('ho');  
logger.warn('lets', { a: 1 });  
logger.error('go');
```

A common logging use case is logging to a file to be picked up by a collector like the [Datadog Agent](https://docs.datadoghq.com/logs/log_collection/nodejs/?tab=winston30).

```
import { Runtime } from '@temporalio/worker';  
import winston from 'winston';  
  
const logger = winston.createLogger({  
  level: 'info',  
  format: winston.format.json(),  
  transports: [new transports.File({ filename: '/path/to/worker.log' })],  
});  
Runtime.install({ logger });
```

## Visibility APIs[​](#visibility "Direct link to Visibility APIs")

The term Visibility, within the Temporal Platform, refers to the subsystems and APIs that enable an operator to view Workflow Executions that currently exist within a Temporal Service.

### How to use Search Attributes[​](#search-attributes "Direct link to How to use Search Attributes")

The typical method of retrieving a Workflow Execution is by its Workflow Id.

However, sometimes you'll want to retrieve one or more Workflow Executions based on another property. For example, imagine you want to get all Workflow Executions of a certain type that have failed within a time range, so that you can start new ones with the same arguments.

You can do this with [Search Attributes](/search-attribute).

* [Default Search Attributes](/search-attribute#default-search-attribute) like `WorkflowType`, `StartTime` and `ExecutionStatus` are automatically added to Workflow Executions.
* *Custom Search Attributes* can contain their own domain-specific data (like `customerId` or `numItems`).
  + A few [generic Custom Search Attributes](/search-attribute#custom-search-attribute) like `CustomKeywordField` and `CustomIntField` are created by default in Temporal's [Docker Compose](https://github.com/temporalio/docker-compose).

The steps to using custom Search Attributes are:

* Create a new Search Attribute in your Temporal Service using `temporal operator search-attribute create` or the Cloud UI.
* Set the value of the Search Attribute for a Workflow Execution:
  + On the Client by including it as an option when starting the Execution.
  + In the Workflow by calling `UpsertSearchAttributes`.
* Read the value of the Search Attribute:
  + On the Client by calling `DescribeWorkflow`.
  + In the Workflow by looking at `WorkflowInfo`.
* Query Workflow Executions by the Search Attribute using a [List Filter](/list-filter):
  + [With the Temporal CLI](/cli/workflow#list).
  + In code by calling `ListWorkflowExecutions`.

Here is how to query Workflow Executions:

Use [`WorkflowService.listWorkflowExecutions`](https://typescript.temporal.io/api/classes/proto.temporal.api.workflowservice.v1.WorkflowService-1#listworkflowexecutions):

```
import { Connection } from '@temporalio/client';  
  
const connection = await Connection.connect();  
const response = await connection.workflowService.listWorkflowExecutions({  
  query: `ExecutionStatus = "Running"`,  
});
```

where `query` is a [List Filter](/list-filter).

### How to set custom Search Attributes[​](#custom-search-attributes "Direct link to How to set custom Search Attributes")

After you've created custom Search Attributes in your Temporal Service (using `temporal operator search-attribute create` or the Cloud UI), you can set the values of the custom Search Attributes when starting a Workflow.

Use [`WorkflowOptions.searchAttributes`](https://typescript.temporal.io/api/interfaces/client.WorkflowOptions#searchattributes).

[search-attributes/src/client.ts](https://github.com/temporalio/samples-typescript/blob/main/search-attributes/src/client.ts)

```
const handle = await client.workflow.start(example, {  
  taskQueue: 'search-attributes',  
  workflowId: 'search-attributes-example-0',  
  searchAttributes: {  
    CustomIntField: [2],  
    CustomKeywordListField: ['keywordA', 'keywordB'],  
    CustomBoolField: [true],  
    CustomDatetimeField: [new Date()],  
    CustomTextField: [  
      'String field is for text. When queried, it will be tokenized for partial match. StringTypeField cannot be used in Order By',  
    ],  
  },  
});  
  
const { searchAttributes } = await handle.describe();
```

The type of `searchAttributes` is `Record<string, string[] | number[] | boolean[] | Date[]>`.

### How to upsert Search Attributes[​](#upsert-search-attributes "Direct link to How to upsert Search Attributes")

You can upsert Search Attributes to add or update Search Attributes from within Workflow code.

Inside a Workflow, we can read from [`WorkflowInfo.searchAttributes`](https://typescript.temporal.io/api/interfaces/workflow.WorkflowInfo#searchattributes) and call [`upsertSearchAttributes`](https://typescript.temporal.io/api/namespaces/workflow#upsertsearchattributes):

[search-attributes/src/workflows.ts](https://github.com/temporalio/samples-typescript/blob/main/search-attributes/src/workflows.ts)

```
export async function example(): Promise<SearchAttributes> {  
  const customInt = (workflowInfo().searchAttributes.CustomIntField?.[0] as number) || 0;  
  upsertSearchAttributes({  
    // overwrite the existing CustomIntField: [2]  
    CustomIntField: [customInt + 1],  
  
    // delete the existing CustomBoolField: [true]  
    CustomBoolField: [],  
  
    // add a new value  
    CustomDoubleField: [3.14],  
  });  
  return workflowInfo().searchAttributes;  
}
```

### How to remove a Search Attribute from a Workflow[​](#remove-search-attribute "Direct link to How to remove a Search Attribute from a Workflow")

To remove a Search Attribute that was previously set, set it to an empty array: `[]`.

```
import { upsertSearchAttributes } from '@temporalio/workflow';  
  
async function yourWorkflow() {  
  upsertSearchAttributes({ CustomIntField: [1, 2, 3] });  
  
  // ... later, to remove:  
  upsertSearchAttributes({ CustomIntField: [] });  
}
```

* [Emit metrics](#metrics)* [Set up tracing](#tracing)* [Log from a Workflow](#logging)
      + [Logging from Activities](#logging-from-activities)+ [Logging from Workflows](#logging-from-workflows)+ [What is the Runtime's Logger](#what-is-the-runtimes-logger)+ [Implementing custom Logging-like features based on Workflow Sinks](#implementing-custom-logging-like-features-based-on-workflow-sinks)+ [How to provide a custom logger](#custom-logger)* [Visibility APIs](#visibility)
        + [How to use Search Attributes](#search-attributes)+ [How to set custom Search Attributes](#custom-search-attributes)+ [How to upsert Search Attributes](#upsert-search-attributes)+ [How to remove a Search Attribute from a Workflow](#remove-search-attribute)