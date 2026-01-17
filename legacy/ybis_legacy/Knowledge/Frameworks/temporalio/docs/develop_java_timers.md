Durable Timers - Java SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

## What is a Timer?[​](#timers "Direct link to What is a Timer?")

A Workflow can set a durable Timer for a fixed time period.
In some SDKs, the function is called `sleep()`, and in others, it's called `timer()`.

A Workflow can sleep for months.

Timers are persisted, so even if your Worker or Temporal Service is down when the time period completes, as soon as your Worker and Temporal Service are back up, the `Workflow.sleep()` call resolves and your code continues executing.

Sleeping is a resource-light operation: it does not tie up the process, and you can run millions of Timers off a single Worker.

To set a Timer in Java, use [`sleep()`](https://www.javadoc.io/doc/io.temporal/temporal-sdk/latest/io/temporal/workflow/Workflow.html#sleep) and pass the number of seconds you want to wait before continuing.

```
sleep(5);
```

* [What is a Timer?](#timers)