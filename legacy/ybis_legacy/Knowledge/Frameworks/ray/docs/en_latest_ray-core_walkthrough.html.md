What’s Ray Core? — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# What’s Ray Core?[#](#what-s-ray-core "Link to this heading")

Ray Core is a powerful distributed computing framework that provides a small set of essential primitives (tasks, actors, and objects) for building and scaling distributed applications.
This walk-through introduces you to these core concepts with simple examples that demonstrate how to transform your Python functions and classes into distributed Ray tasks and actors, and how to work effectively with Ray objects.

Note

Ray has introduced an experimental API for high-performance workloads that’s
especially well suited for applications using multiple GPUs.
See [Ray Compiled Graph](compiled-graph/ray-compiled-graph.html#ray-compiled-graph) for more details.

## Getting Started[#](#getting-started "Link to this heading")

To get started, install Ray using `pip install -U ray`. For additional installation options, see [Installing Ray](../ray-overview/installation.html#installation).

The first step is to import and initialize Ray:

```
import ray

ray.init()
```

Note

Unless you explicitly call `ray.init()`, the first use of a Ray remote API call will implicitly call `ray.init()` with no arguments.

## Running a Task[#](#running-a-task "Link to this heading")

Tasks are the simplest way to parallelize your Python functions across a Ray cluster. To create a task:

1. Decorate your function with `@ray.remote` to indicate it should run remotely
2. Call the function with `.remote()` instead of a normal function call
3. Use `ray.get()` to retrieve the result from the returned future (Ray *object reference*)

Here’s a simple example:

```
# Define the square task.
@ray.remote
def square(x):
    return x * x

# Launch four parallel square tasks.
futures = [square.remote(i) for i in range(4)]

# Retrieve results.
print(ray.get(futures))
# -> [0, 1, 4, 9]
```

## Calling an Actor[#](#calling-an-actor "Link to this heading")

While tasks are stateless, Ray actors allow you to create stateful workers that maintain their internal state between method calls.
When you instantiate a Ray actor:

1. Ray starts a dedicated worker process somewhere in your cluster
2. The actor’s methods run on that specific worker and can access and modify its state
3. The actor executes method calls serially in the order it receives them, preserving consistency

Here’s a simple Counter example:

```
# Define the Counter actor.
@ray.remote
class Counter:
    def __init__(self):
        self.i = 0

    def get(self):
        return self.i

    def incr(self, value):
        self.i += value

# Create a Counter actor.
c = Counter.remote()

# Submit calls to the actor. These calls run asynchronously but in
# submission order on the remote actor process.
for _ in range(10):
    c.incr.remote(1)

# Retrieve final actor state.
print(ray.get(c.get.remote()))
# -> 10
```

The preceding example demonstrates basic actor usage. For a more comprehensive example that combines both tasks and actors, see the [Monte Carlo Pi estimation example](examples/monte_carlo_pi.html#monte-carlo-pi).

## Passing Objects[#](#passing-objects "Link to this heading")

Ray’s distributed object store efficiently manages data across your cluster. There are three main ways to work with objects in Ray:

1. **Implicit creation**: When tasks and actors return values, they are automatically stored in Ray’s [distributed object store](objects.html#objects-in-ray), returning *object references* that can be later retrieved.
2. **Explicit creation**: Use `ray.put()` to directly place objects in the store.
3. **Passing references**: You can pass object references to other tasks and actors, avoiding unnecessary data copying and enabling lazy execution.

Here’s an example showing these techniques:

```
import numpy as np

# Define a task that sums the values in a matrix.
@ray.remote
def sum_matrix(matrix):
    return np.sum(matrix)

# Call the task with a literal argument value.
print(ray.get(sum_matrix.remote(np.ones((100, 100)))))
# -> 10000.0

# Put a large array into the object store.
matrix_ref = ray.put(np.ones((1000, 1000)))

# Call the task with the object reference as an argument.
print(ray.get(sum_matrix.remote(matrix_ref)))
# -> 1000000.0
```

## Next Steps[#](#next-steps "Link to this heading")

Tip

To monitor your application’s performance and resource usage, check out the [Ray dashboard](../ray-observability/getting-started.html#observability-getting-started).

You can combine Ray’s simple primitives in powerful ways to express virtually any distributed computation pattern. To dive deeper into Ray’s [key concepts](key-concepts.html#core-key-concepts),
explore these user guides:

![](../_images/tasks.png)

[Using remote functions (Tasks)](tasks.html#ray-remote-functions)

![](../_images/actors.png)

[Using remote classes (Actors)](actors.html#ray-remote-classes)

![](../_images/objects.png)

[Working with Ray Objects](objects.html#objects-in-ray)

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/ray-core/walkthrough.rst)