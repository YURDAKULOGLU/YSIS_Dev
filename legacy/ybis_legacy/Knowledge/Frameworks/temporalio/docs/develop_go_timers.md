Durable Timers - Go SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

A Workflow can set a Durable Timer for a fixed time period.
In some SDKs, the function is called `sleep()`, and in others, it's called `timer()`.

A Workflow can sleep for days, months, or even years.
Timers are persisted, so even if your Worker or Temporal Service is down when the time period completes, as soon as your Worker and Temporal Service are back up, the `sleep()` call will resolve and your code will continue executing.

Sleeping is a resource-light operation: it does not tie up the process, and you can run millions of Timers off a single Worker.

To set a Timer in Go, use the [`NewTimer()`](https://pkg.go.dev/go.temporal.io/sdk/workflow#NewTimer) function and pass the duration you want to wait before continuing.

```
timer := workflow.NewTimer(timerCtx, duration)
```

To set a sleep duration in Go, use the [`sleep()`](https://pkg.go.dev/go.temporal.io/sdk/workflow#Sleep) function and pass the duration you want to wait before continuing.
A zero or negative sleep duration causes the function to return immediately.

```
sleep = workflow.Sleep(ctx, 10*time.Second)
```

For more information, see the [Timer](https://github.com/temporalio/samples-go/tree/main/timer) example in the [Go Samples repository](https://github.com/temporalio/samples-go).