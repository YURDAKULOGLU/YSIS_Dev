Durable Timers - Python SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

A Workflow can set a durable Timer for a fixed time period.
In some SDKs, the function is called `sleep()`, and in others, it's called `timer()`.

A Workflow can sleep for months.
Timers are persisted, so even if your Worker or Temporal Service is down when the time period completes, as soon as your Worker and Temporal Service are back up, the `sleep()` call will resolve and your code will continue executing.

Sleeping is a resource-light operation: it does not tie up the process, and you can run millions of Timers off a single Worker.

To set a Timer in Python, call the [`asyncio.sleep()`](https://docs.python.org/3/library/asyncio-task.html#sleeping) function and pass the duration in seconds you want to wait before continuing.

[View the source code](https://github.com/temporalio/documentation/blob/main/sample-apps/python/continue_as_new/your_workflows_dacx.py)

in the context of the rest of the application code.

```
# ...  
        await asyncio.sleep(10)
```