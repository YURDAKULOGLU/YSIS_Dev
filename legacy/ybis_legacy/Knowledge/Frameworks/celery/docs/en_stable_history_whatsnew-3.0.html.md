What’s new in Celery 3.0 (Chiastic Slide) — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](changelog-3.0.html "Change history for Celery 3.0") |
* [previous](changelog-3.1.html "Change history") |
* [Celery 5.6.2 documentation](../index.html) »
* [History](index.html) »
* What’s new in Celery 3.0 (Chiastic Slide)

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/history/whatsnew-3.0.html).

# What’s new in Celery 3.0 (Chiastic Slide)[¶](#what-s-new-in-celery-3-0-chiastic-slide "Link to this heading")

Celery is a simple, flexible, and reliable distributed system to
process vast amounts of messages, while providing operations with
the tools required to maintain such a system.

It’s a task queue with focus on real-time processing, while also
supporting task scheduling.

Celery has a large and diverse community of users and contributors,
you should come join us on IRC
or our mailing-list.

To read more about Celery you should go read the [introduction](../getting-started/introduction.html#intro).

While this version is backward compatible with previous versions
it’s important that you read the following section.

If you use Celery in combination with Django you must also
read the [django-celery changelog](https://github.com/celery/django-celery/tree/master/Changelog) and upgrade
to [django-celery 3.0](https://pypi.org/project/django-celery/).

This version is officially supported on CPython 2.5, 2.6, 2.7, 3.2 and 3.3,
as well as PyPy and Jython.

## Highlights[¶](#highlights "Link to this heading")

Overview

* A new and improved API, that’s both simpler and more powerful.

  > Everyone must read the new [First Steps with Celery](../getting-started/first-steps-with-celery.html#first-steps) tutorial,
  > and the new [Next Steps](../getting-started/next-steps.html#next-steps) tutorial. Oh, and
  > why not reread the user guide while you’re at it :)
  >
  > There are no current plans to deprecate the old API,
  > so you don’t have to be in a hurry to port your applications.
* The worker is now thread-less, giving great performance improvements.
* The new “Canvas” makes it easy to define complex work-flows.

  > Ever wanted to chain tasks together? This is possible, but
  > not just that, now you can even chain together groups and chords,
  > or even combine multiple chains.
  >
  > Read more in the [Canvas](../userguide/canvas.html#guide-canvas) user guide.
* All of Celery’s command-line programs are now available from a single
  **celery** umbrella command.
* This is the last version to support Python 2.5.

  > Starting with Celery 3.1, Python 2.6 or later is required.
* Support for the new <https://pypi.org/project/librabbitmq/> C client.

  > Celery will automatically use the <https://pypi.org/project/librabbitmq/> module
  > if installed, which is a very fast and memory-optimized
  > replacement for the <https://pypi.org/project/amqp/> module.
* Redis support is more reliable with improved ack emulation.
* Celery now always uses UTC
* Over 600 commits, 30k additions/36k deletions.

  > In comparison 1.0➝ 2.0 had 18k additions/8k deletions.

## Important Notes[¶](#important-notes "Link to this heading")

### Broadcast exchanges renamed[¶](#broadcast-exchanges-renamed "Link to this heading")

The workers remote control command exchanges has been renamed
(a new [pidbox](../glossary.html#term-pidbox) name), this is because the `auto_delete` flag on
the exchanges has been removed, and that makes it incompatible with
earlier versions.

You can manually delete the old exchanges if you want,
using the **celery amqp** command (previously called `camqadm`):

```
$ celery amqp exchange.delete celeryd.pidbox
$ celery amqp exchange.delete reply.celeryd.pidbox
```

### Event-loop[¶](#event-loop "Link to this heading")

The worker is now running *without threads* when used with RabbitMQ (AMQP),
or Redis as a broker, resulting in:

* Much better overall performance.
* Fixes several edge case race conditions.
* Sub-millisecond timer precision.
* Faster shutdown times.

The transports supported are: `py-amqp` `librabbitmq`, `redis`,
and `amqplib`.
Hopefully this can be extended to include additional broker transports
in the future.

For increased reliability the `CELERY_FORCE_EXECV` setting is enabled
by default if the event-loop isn’t used.

### New `celery` umbrella command[¶](#new-celery-umbrella-command "Link to this heading")

All Celery’s command-line programs are now available from a single
**celery** umbrella command.

You can see a list of sub-commands and options by running:

```
$ celery help
```

Commands include:

* `celery worker` (previously `celeryd`).
* `celery beat` (previously `celerybeat`).
* `celery amqp` (previously `camqadm`).

The old programs are still available (`celeryd`, `celerybeat`, etc),
but you’re discouraged from using them.

### Now depends on <https://pypi.org/project/billiard/>[¶](#now-depends-on-https-pypi-org-project-billiard "Link to this heading")

Billiard is a fork of the multiprocessing containing
the no-execv patch by `sbt` (<http://bugs.python.org/issue8713>),
and also contains the pool improvements previously located in Celery.

This fork was necessary as changes to the C extension code was required
for the no-execv patch to work.

* Issue #625
* Issue #627
* Issue #640
* django-celery #122 <https://github.com/celery/django-celery/issues/122
* django-celery #124 <https://github.com/celery/django-celery/issues/122

### [`celery.app.task`](../reference/celery.app.task.html#module-celery.app.task "celery.app.task") no longer a package[¶](#celery-app-task-no-longer-a-package "Link to this heading")

The [`celery.app.task`](../reference/celery.app.task.html#module-celery.app.task "celery.app.task") module is now a module instead of a package.

The `setup.py` install script will try to remove the old package,
but if that doesn’t work for some reason you have to remove
it manually. This command helps:

```
$ rm -r $(dirname $(python -c 'import celery;print(celery.__file__)'))/app/task/
```

If you experience an error like `ImportError: cannot import name _unpickle_task`,
you just have to remove the old package and everything is fine.

### Last version to support Python 2.5[¶](#last-version-to-support-python-2-5 "Link to this heading")

The 3.0 series will be last version to support Python 2.5,
and starting from 3.1 Python 2.6 and later will be required.

With several other distributions taking the step to discontinue
Python 2.5 support, we feel that it is time too.

Python 2.6 should be widely available at this point, and we urge
you to upgrade, but if that’s not possible you still have the option
to continue using the Celery 3.0, and important bug fixes
introduced in Celery 3.1 will be back-ported to Celery 3.0 upon request.

### UTC timezone is now used[¶](#utc-timezone-is-now-used "Link to this heading")

This means that ETA/countdown in messages aren’t compatible with Celery
versions prior to 2.5.

You can disable UTC and revert back to old local time by setting
the `CELERY_ENABLE_UTC` setting.

### Redis: Ack emulation improvements[¶](#redis-ack-emulation-improvements "Link to this heading")

> Reducing the possibility of data loss.
>
> Acks are now implemented by storing a copy of the message when the message
> is consumed. The copy isn’t removed until the consumer acknowledges
> or rejects it.
>
> This means that unacknowledged messages will be redelivered either
> when the connection is closed, or when the visibility timeout is exceeded.
>
> * Visibility timeout
>
>   > This is a timeout for acks, so that if the consumer
>   > doesn’t ack the message within this time limit, the message
>   > is redelivered to another consumer.
>   >
>   > The timeout is set to one hour by default, but
>   > can be changed by configuring a transport option:
>   >
>   > ```
>   > BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 18000}  # 5 hours
>   > ```
>
> Note
>
> Messages that haven’t been acked will be redelivered
> if the visibility timeout is exceeded, for Celery users
> this means that ETA/countdown tasks that are scheduled to execute
> with a time that exceeds the visibility timeout will be executed
> twice (or more). If you plan on using long ETA/countdowns you
> should tweak the visibility timeout accordingly.
>
> Setting a long timeout means that it’ll take a long time
> for messages to be redelivered in the event of a power failure,
> but if so happens you could temporarily set the visibility timeout lower
> to flush out messages when you start up the systems again.

## News[¶](#news "Link to this heading")

### Chaining Tasks[¶](#chaining-tasks "Link to this heading")

Tasks can now have callbacks and errbacks, and dependencies are recorded

* The task message format have been updated with two new extension keys

  > Both keys can be empty/undefined or a list of subtasks.
  >
  > + `callbacks`
  >
  >   > Applied if the task exits successfully, with the result
  >   > of the task as an argument.
  > + `errbacks`
  >
  >   > Applied if an error occurred while executing the task,
  >   > with the uuid of the task as an argument. Since it may not be possible
  >   > to serialize the exception instance, it passes the uuid of the task
  >   > instead. The uuid can then be used to retrieve the exception and
  >   > traceback of the task from the result backend.
  > + `link` and `link_error` keyword arguments has been added
  >   to `apply_async`.
  >
  >   > These add callbacks and errbacks to the task, and
  >   > you can read more about them at [Linking (callbacks/errbacks)](../userguide/calling.html#calling-links).
  > + We now track what subtasks a task sends, and some result backends
  >   supports retrieving this information.
  >
  >   > > - task.request.children
  >   > >
  >   > >   > Contains the result instances of the subtasks
  >   > >   > the currently executing task has applied.
  >   > > - AsyncResult.children
  >   > >
  >   > >   > Returns the tasks dependencies, as a list of
  >   > >   > `AsyncResult`/`ResultSet` instances.
  >   > > - AsyncResult.iterdeps
  >   > >
  >   > >   > Recursively iterates over the tasks dependencies,
  >   > >   > yielding (parent, node) tuples.
  >   > >   >
  >   > >   > Raises IncompleteStream if any of the dependencies
  >   > >   > hasn’t returned yet.
  >   >
  >   > - AsyncResult.graph
  >   >
  >   >   > A [`DependencyGraph`](../internals/reference/celery.utils.graph.html#celery.utils.graph.DependencyGraph "celery.utils.graph.DependencyGraph") of the tasks
  >   >   > dependencies. With this you can also convert to dot format:
  >   >   >
  >   >   > ```
  >   >   > with open('graph.dot') as fh:
  >   >   >     result.graph.to_dot(fh)
  >   >   > ```
  >   >   >
  >   >   > then produce an image of the graph:
  >   >   >
  >   >   > ```
  >   >   > $ dot -Tpng graph.dot -o graph.png
  >   >   > ```
* A new special subtask called `chain` is also included:

  > ```
  > >>> from celery import chain
  >
  > # (2 + 2) * 8 / 2
  > >>> res = chain(add.subtask((2, 2)),
  >                 mul.subtask((8,)),
  >                 div.subtask((2,))).apply_async()
  > >>> res.get() == 16
  >
  > >>> res.parent.get() == 32
  >
  > >>> res.parent.parent.get() == 4
  > ```
* Adds `AsyncResult.get_leaf()`

  > Waits and returns the result of the leaf subtask.
  > That’s the last node found when traversing the graph,
  > but this means that the graph can be 1-dimensional only (in effect
  > a list).
* Adds `subtask.link(subtask)` + `subtask.link_error(subtask)`

  > Shortcut to `s.options.setdefault('link', []).append(subtask)`
* Adds `subtask.flatten_links()`

  > Returns a flattened list of all dependencies (recursively)

### Redis: Priority support[¶](#redis-priority-support "Link to this heading")

The message’s `priority` field is now respected by the Redis
transport by having multiple lists for each named queue.
The queues are then consumed by in order of priority.

The priority field is a number in the range of 0 - 9, where
0 is the default and highest priority.

The priority range is collapsed into four steps by default, since it is
unlikely that nine steps will yield more benefit than using four steps.
The number of steps can be configured by setting the `priority_steps`
transport option, which must be a list of numbers in **sorted order**:

```
>>> BROKER_TRANSPORT_OPTIONS = {
...     'priority_steps': [0, 2, 4, 6, 8, 9],
... }
```

Priorities implemented in this way isn’t as reliable as
priorities on the server side, which is why
the feature is nicknamed “quasi-priorities”;
**Using routing is still the suggested way of ensuring
quality of service**, as client implemented priorities
fall short in a number of ways, for example if the worker
is busy with long running tasks, has prefetched many messages,
or the queues are congested.

Still, it is possible that using priorities in combination
with routing can be more beneficial than using routing
or priorities alone. Experimentation and monitoring
should be used to prove this.

Contributed by Germán M. Bravo.

### Redis: Now cycles queues so that consuming is fair[¶](#redis-now-cycles-queues-so-that-consuming-is-fair "Link to this heading")

This ensures that a very busy queue won’t block messages
from other queues, and ensures that all queues have
an equal chance of being consumed from.

This used to be the case before, but the behavior was
accidentally changed while switching to using blocking pop.

### group/chord/chain are now subtasks[¶](#group-chord-chain-are-now-subtasks "Link to this heading")

* group is no longer an alias to `TaskSet`, but new all together,
  since it was very difficult to migrate the `TaskSet` class to become
  a subtask.
* A new shortcut has been added to tasks:

  > ```
  > >>> task.s(arg1, arg2, kw=1)
  > ```
  >
  > as a shortcut to:
  >
  > ```
  > >>> task.subtask((arg1, arg2), {'kw': 1})
  > ```
* Tasks can be chained by using the `|` operator:

  > ```
  > >>> (add.s(2, 2), pow.s(2)).apply_async()
  > ```
* Subtasks can be “evaluated” using the `~` operator:

  > ```
  > >>> ~add.s(2, 2)
  > 4
  >
  > >>> ~(add.s(2, 2) | pow.s(2))
  > ```
  >
  > is the same as:
  >
  > ```
  > >>> chain(add.s(2, 2), pow.s(2)).apply_async().get()
  > ```
* A new subtask\_type key has been added to the subtask dictionary.

  > This can be the string `"chord"`, `"group"`, `"chain"`,
  > `"chunks"`, `"xmap"`, or `"xstarmap"`.
* maybe\_subtask now uses subtask\_type to reconstruct
  the object, to be used when using non-pickle serializers.
* The logic for these operations have been moved to dedicated
  tasks celery.chord, celery.chain and celery.group.
* subtask no longer inherits from AttributeDict.

  > It’s now a pure dict subclass with properties for attribute
  > access to the relevant keys.
* The repr’s now outputs how the sequence would like imperatively:

  > ```
  > >>> from celery import chord
  >
  > >>> (chord([add.s(i, i) for i in xrange(10)], xsum.s())
  >       | pow.s(2))
  > tasks.xsum([tasks.add(0, 0),
  >             tasks.add(1, 1),
  >             tasks.add(2, 2),
  >             tasks.add(3, 3),
  >             tasks.add(4, 4),
  >             tasks.add(5, 5),
  >             tasks.add(6, 6),
  >             tasks.add(7, 7),
  >             tasks.add(8, 8),
  >             tasks.add(9, 9)]) | tasks.pow(2)
  > ```

### New remote control commands[¶](#new-remote-control-commands "Link to this heading")

These commands were previously experimental, but they’ve proven
stable and is now documented as part of the official API.

* [`add_consumer`](../userguide/workers.html#std-control-add_consumer)/[`cancel_consumer`](../userguide/workers.html#std-control-cancel_consumer)

  > Tells workers to consume from a new queue, or cancel consuming from a
  > queue. This command has also been changed so that the worker remembers
  > the queues added, so that the change will persist even if
  > the connection is re-connected.
  >
  > These commands are available programmatically as
  > [`app.control.add_consumer()`](../reference/celery.app.control.html#celery.app.control.Control.add_consumer "celery.app.control.Control.add_consumer") / [`app.control.cancel_consumer()`](../reference/celery.app.control.html#celery.app.control.Control.cancel_consumer "celery.app.control.Control.cancel_consumer"):
  >
  > ```
  > >>> celery.control.add_consumer(queue_name,
  > ...     destination=['w1.example.com'])
  > >>> celery.control.cancel_consumer(queue_name,
  > ...     destination=['w1.example.com'])
  > ```
  >
  > or using the **celery control** command:
  >
  > ```
  > $ celery control -d w1.example.com add_consumer queue
  > $ celery control -d w1.example.com cancel_consumer queue
  > ```
  >
  > Note
  >
  > Remember that a control command without *destination* will be
  > sent to **all workers**.
* `autoscale`

  > Tells workers with `--autoscale` enabled to change autoscale
  > max/min concurrency settings.
  >
  > This command is available programmatically as [`app.control.autoscale()`](../reference/celery.app.control.html#celery.app.control.Control.autoscale "celery.app.control.Control.autoscale"):
  >
  > ```
  > >>> celery.control.autoscale(max=10, min=5,
  > ...     destination=['w1.example.com'])
  > ```
  >
  > or using the **celery control** command:
  >
  > ```
  > $ celery control -d w1.example.com autoscale 10 5
  > ```
* `pool_grow`/`pool_shrink`

  > Tells workers to add or remove pool processes.
  >
  > These commands are available programmatically as
  > [`app.control.pool_grow()`](../reference/celery.app.control.html#celery.app.control.Control.pool_grow "celery.app.control.Control.pool_grow") / [`app.control.pool_shrink()`](../reference/celery.app.control.html#celery.app.control.Control.pool_shrink "celery.app.control.Control.pool_shrink"):
  >
  > ```
  > >>> celery.control.pool_grow(2, destination=['w1.example.com'])
  > >>> celery.control.pool_shrink(2, destination=['w1.example.com'])
  > ```
  >
  > or using the **celery control** command:
  >
  > ```
  > $ celery control -d w1.example.com pool_grow 2
  > $ celery control -d w1.example.com pool_shrink 2
  > ```
* **celery control** now supports [`rate_limit`](../userguide/workers.html#std-control-rate_limit) and
  `time_limit` commands.

  > See `celery control --help` for details.

### Crontab now supports Day of Month, and Month of Year arguments[¶](#crontab-now-supports-day-of-month-and-month-of-year-arguments "Link to this heading")

See the updated list of examples at [Crontab schedules](../userguide/periodic-tasks.html#beat-crontab).

### Immutable subtasks[¶](#immutable-subtasks "Link to this heading")

`subtask`’s can now be immutable, which means that the arguments
won’t be modified when calling callbacks:

```
>>> chain(add.s(2, 2), clear_static_electricity.si())
```

means it’ll not receive the argument of the parent task,
and `.si()` is a shortcut to:

```
>>> clear_static_electricity.subtask(immutable=True)
```

### Logging Improvements[¶](#logging-improvements "Link to this heading")

Logging support now conforms better with best practices.

* Classes used by the worker no longer uses app.get\_default\_logger, but uses
  celery.utils.log.get\_logger which simply gets the logger not setting the
  level, and adds a NullHandler.
* Loggers are no longer passed around, instead every module using logging
  defines a module global logger that’s used throughout.
* All loggers inherit from a common logger called “celery”.
* Before `task.get_logger` would setup a new logger for every task,
  and even set the log level. This is no longer the case.

  > + Instead all task loggers now inherit from a common “celery.task” logger
  >   that’s set up when programs call setup\_logging\_subsystem.
  > + Instead of using LoggerAdapter to augment the formatter with
  >   the task\_id and task\_name field, the task base logger now use
  >   a special formatter adding these values at run-time from the
  >   currently executing task.
* In fact, `task.get_logger` is no longer recommended, it is better
  to add a module-level logger to your tasks module.

  > For example, like this:
  >
  > ```
  > from celery.utils.log import get_task_logger
  >
  > logger = get_task_logger(__name__)
  >
  > @celery.task
  > def add(x, y):
  >     logger.debug('Adding %r + %r' % (x, y))
  >     return x + y
  > ```
  >
  > The resulting logger will then inherit from the `"celery.task"` logger
  > so that the current task name and id is included in logging output.
* Redirected output from stdout/stderr is now logged to a “celery.redirected”
  logger.
* In addition a few warnings.warn have been replaced with logger.warn.
* Now avoids the ‘no handlers for logger multiprocessing’ warning

### Task registry no longer global[¶](#task-registry-no-longer-global "Link to this heading")

Every Celery instance now has its own task registry.

You can make apps share registries by specifying it:

```
>>> app1 = Celery()
>>> app2 = Celery(tasks=app1.tasks)
```

Note that tasks are shared between registries by default, so that
tasks will be added to every subsequently created task registry.
As an alternative tasks can be private to specific task registries
by setting the `shared` argument to the `@task` decorator:

```
@celery.task(shared=False)
def add(x, y):
    return x + y
```

### Abstract tasks are now lazily bound[¶](#abstract-tasks-are-now-lazily-bound "Link to this heading")

The `Task` class is no longer bound to an app
by default, it will first be bound (and configured) when
a concrete subclass is created.

This means that you can safely import and make task base classes,
without also initializing the app environment:

```
from celery.task import Task

class DebugTask(Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        print('CALLING %r' % (self,))
        return self.run(*args, **kwargs)
```

```
>>> DebugTask
<unbound DebugTask>

>>> @celery1.task(base=DebugTask)
... def add(x, y):
...     return x + y
>>> add.__class__
<class add of <Celery default:0x101510d10>>
```

### Lazy task decorators[¶](#lazy-task-decorators "Link to this heading")

The `@task` decorator is now lazy when used with custom apps.

That is, if `accept_magic_kwargs` is enabled (her by called “compat mode”), the task
decorator executes inline like before, however for custom apps the @task
decorator now returns a special PromiseProxy object that’s only evaluated
on access.

All promises will be evaluated when [`app.finalize()`](../reference/celery.html#celery.Celery.finalize "celery.Celery.finalize") is called, or implicitly
when the task registry is first used.

### Smart –app option[¶](#smart-app-option "Link to this heading")

The [`--app`](../reference/cli.html#cmdoption-celery-A) option now ‘auto-detects’

> * If the provided path is a module it tries to get an
>   attribute named ‘celery’.
> * If the provided path is a package it tries
>   to import a sub module named celery’,
>   and get the celery attribute from that module.

For example, if you have a project named `proj` where the
celery app is located in `from proj.celery import app`,
then the following will be equivalent:

```
$ celery worker --app=proj
$ celery worker --app=proj.celery:
$ celery worker --app=proj.celery:app
```

### In Other News[¶](#in-other-news "Link to this heading")

* New `CELERYD_WORKER_LOST_WAIT` to control the timeout in
  seconds before `billiard.WorkerLostError` is raised
  when a worker can’t be signaled (Issue #595).

  > Contributed by Brendon Crawford.
* Redis event monitor queues are now automatically deleted (Issue #436).
* App instance factory methods have been converted to be cached
  descriptors that creates a new subclass on access.

  > For example, this means that `app.Worker` is an actual class
  > and will work as expected when:
  >
  > ```
  > class Worker(app.Worker):
  >     ...
  > ```
* New signal: [`task_success`](../userguide/signals.html#std-signal-task_success).
* Multiprocessing logs are now only emitted if the `MP_LOG`
  environment variable is set.
* The Celery instance can now be created with a broker URL

  > ```
  > app = Celery(broker='redis://')
  > ```
* Result backends can now be set using a URL

  > Currently only supported by redis. Example use:
  >
  > ```
  > CELERY_RESULT_BACKEND = 'redis://localhost/1'
  > ```
* Heartbeat frequency now every 5s, and frequency sent with event

  > The heartbeat frequency is now available in the worker event messages,
  > so that clients can decide when to consider workers offline based on
  > this value.
* Module celery.actors has been removed, and will be part of cl instead.
* Introduces new `celery` command, which is an entry-point for all other
  commands.

  > The main for this command can be run by calling `celery.start()`.
* Annotations now supports decorators if the key starts with ‘@’.

  > For example:
  >
  > ```
  > def debug_args(fun):
  >
  >     @wraps(fun)
  >     def _inner(*args, **kwargs):
  >         print('ARGS: %r' % (args,))
  >     return _inner
  >
  > CELERY_ANNOTATIONS = {
  >     'tasks.add': {'@__call__': debug_args},
  > }
  > ```
  >
  > Also tasks are now always bound by class so that
  > annotated methods end up being bound.
* Bug-report now available as a command and broadcast command

  > + Get it from a Python REPL:
  >
  >   > ```
  >   > >>> import celery
  >   > >>> print(celery.bugreport())
  >   > ```
  > + Using the `celery` command line program:
  >
  >   > ```
  >   > $ celery report
  >   > ```
  > + Get it from remote workers:
  >
  >   > ```
  >   > $ celery inspect report
  >   > ```
* Module `celery.log` moved to [`celery.app.log`](../reference/celery.app.log.html#module-celery.app.log "celery.app.log").
* Module `celery.task.control` moved to [`celery.app.control`](../reference/celery.app.control.html#module-celery.app.control "celery.app.control").
* New signal: [`task_revoked`](../userguide/signals.html#std-signal-task_revoked)

  > Sent in the main process when the task is revoked or terminated.
* `AsyncResult.task_id` renamed to `AsyncResult.id`
* `TasksetResult.taskset_id` renamed to `.id`
* `xmap(task, sequence)` and `xstarmap(task, sequence)`

  > Returns a list of the results applying the task function to every item
  > in the sequence.
  >
  > Example:
  >
  > ```
  > >>> from celery import xstarmap
  >
  > >>> xstarmap(add, zip(range(10), range(10)).apply_async()
  > [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
  > ```
* `chunks(task, sequence, chunksize)`
* `group.skew(start=, stop=, step=)`

  > Skew will skew the countdown for the individual tasks in a group – for
  > example with this group:
  >
  > ```
  > >>> g = group(add.s(i, i) for i in xrange(10))
  > ```

  Skewing the tasks from 0 seconds to 10 seconds:

  > ```
  > >>> g.skew(stop=10)
  > ```

  Will have the first task execute in 0 seconds, the second in 1 second,
  the third in 2 seconds and so on.
* 99% test Coverage
* `CELERY_QUEUES` can now be a list/tuple of [`Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)")
  instances.

  > Internally [`app.amqp.queues`](../reference/celery.app.amqp.html#celery.app.amqp.AMQP.queues "celery.app.amqp.AMQP.queues") is now a mapping of name/Queue instances,
  > instead of converting on the fly.
* Can now specify connection for [`app.control.inspect`](../reference/celery.app.control.html#celery.app.control.Control.inspect "celery.app.control.Control.inspect").

  > ```
  > from kombu import Connection
  >
  > i = celery.control.inspect(connection=Connection('redis://'))
  > i.active_queues()
  > ```
* `CELERY_FORCE_EXECV` is now enabled by default.

  > If the old behavior is wanted the setting can be set to False,
  > or the new –no-execv option to **celery worker**.
* Deprecated module `celery.conf` has been removed.
* The `CELERY_TIMEZONE` now always require the <https://pypi.org/project/pytz/>
  library to be installed (except if the timezone is set to UTC).
* The Tokyo Tyrant backend has been removed and is no longer supported.
* Now uses [`maybe_declare()`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.common.html#kombu.common.maybe_declare "(in Kombu v5.6)") to cache queue declarations.
* There’s no longer a global default for the
  `CELERYBEAT_MAX_LOOP_INTERVAL` setting, it is instead
  set by individual schedulers.
* Worker: now truncates very long message bodies in error reports.
* No longer deep-copies exceptions when trying to serialize errors.
* `CELERY_BENCH` environment variable, will now also list
  memory usage statistics at worker shutdown.
* Worker: now only ever use a single timer for all timing needs,
  and instead set different priorities.
* An exceptions arguments are now safely pickled

  > Contributed by Matt Long.
* Worker/Beat no longer logs the start-up banner.

  > Previously it would be logged with severity warning,
  > now it’s only written to stdout.
* The `contrib/` directory in the distribution has been renamed to
  `extra/`.
* New signal: [`task_revoked`](../userguide/signals.html#std-signal-task_revoked)
* [`celery.contrib.migrate`](../reference/celery.contrib.migrate.html#module-celery.contrib.migrate "celery.contrib.migrate"): Many improvements, including;
  filtering, queue migration, and support for acking messages on the broker
  migrating from.

  > Contributed by John Watson.
* Worker: Prefetch count increments are now optimized and grouped together.
* Worker: No longer calls `consume` on the remote control command queue
  twice.

  > Probably didn’t cause any problems, but was unnecessary.

### Internals[¶](#internals "Link to this heading")

* `app.broker_connection` is now `app.connection`

  > Both names still work.
* Compatibility modules are now generated dynamically upon use.

  > These modules are `celery.messaging`, `celery.log`,
  > `celery.decorators` and `celery.registry`.
* [`celery.utils`](../internals/reference/celery.utils.html#module-celery.utils "celery.utils") refactored into multiple modules:

  > [`celery.utils.text`](../internals/reference/celery.utils.text.html#module-celery.utils.text "celery.utils.text")
  > [`celery.utils.imports`](../internals/reference/celery.utils.imports.html#module-celery.utils.imports "celery.utils.imports")
  > [`celery.utils.functional`](../internals/reference/celery.utils.functional.html#module-celery.utils.functional "celery.utils.functional")
* Now using [`kombu.utils.encoding`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.utils.encoding.html#module-kombu.utils.encoding "(in Kombu v5.6)") instead of
  `celery.utils.encoding`.
* Renamed module `celery.routes` -> [`celery.app.routes`](../internals/reference/celery.app.routes.html#module-celery.app.routes "celery.app.routes").
* Renamed package `celery.db` -> [`celery.backends.database`](../internals/reference/celery.backends.database.html#module-celery.backends.database "celery.backends.database").
* Renamed module `celery.abstract` -> `celery.worker.bootsteps`.
* Command line docs are now parsed from the module docstrings.
* Test suite directory has been reorganized.
* **setup.py** now reads docs from the `requirements/` directory.
* Celery commands no longer wraps output (Issue #700).

  > Contributed by Thomas Johansson.

## Experimental[¶](#experimental "Link to this heading")

### `celery.contrib.methods`: Task decorator for methods[¶](#celery-contrib-methods-task-decorator-for-methods "Link to this heading")

This is an experimental module containing a task
decorator, and a task decorator filter, that can be used
to create tasks out of methods:

```
from celery.contrib.methods import task_method

class Counter(object):

    def __init__(self):
        self.value = 1

    @celery.task(name='Counter.increment', filter=task_method)
    def increment(self, n=1):
        self.value += 1
        return self.value
```

See `celery.contrib.methods` for more information.

## Unscheduled Removals[¶](#unscheduled-removals "Link to this heading")

Usually we don’t make backward incompatible removals,
but these removals should have no major effect.

* The following settings have been renamed:

  > + `CELERYD_ETA_SCHEDULER` -> `CELERYD_TIMER`
  > + `CELERYD_ETA_SCHEDULER_PRECISION` -> `CELERYD_TIMER_PRECISION`

## Deprecation Time-line Changes[¶](#deprecation-time-line-changes "Link to this heading")

See the [Celery Deprecation Time-line](../internals/deprecation.html#deprecation-timeline).

* The `celery.backends.pyredis` compat module has been removed.

  > Use [`celery.backends.redis`](../internals/reference/celery.backends.redis.html#module-celery.backends.redis "celery.backends.redis") instead!
* The following undocumented API’s has been moved:

  > + `control.inspect.add_consumer` -> [`app.control.add_consumer()`](../reference/celery.app.control.html#celery.app.control.Control.add_consumer "celery.app.control.Control.add_consumer").
  > + `control.inspect.cancel_consumer` -> [`app.control.cancel_consumer()`](../reference/celery.app.control.html#celery.app.control.Control.cancel_consumer "celery.app.control.Control.cancel_consumer").
  > + `control.inspect.enable_events` -> [`app.control.enable_events()`](../reference/celery.app.control.html#celery.app.control.Control.enable_events "celery.app.control.Control.enable_events").
  > + `control.inspect.disable_events` -> [`app.control.disable_events()`](../reference/celery.app.control.html#celery.app.control.Control.disable_events "celery.app.control.Control.disable_events").
  >
  > This way `inspect()` is only used for commands that don’t
  > modify anything, while idempotent control commands that make changes
  > are on the control objects.

## Fixes[¶](#fixes "Link to this heading")

* Retry SQLAlchemy backend operations on DatabaseError/OperationalError
  (Issue #634)
* Tasks that called `retry` wasn’t acknowledged if acks late was enabled

  > Fix contributed by David Markey.
* The message priority argument wasn’t properly propagated to Kombu
  (Issue #708).

  > Fix contributed by Eran Rundstein

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[Change history](changelog-3.1.html "previous chapter")

#### Next topic

[Change history for Celery 3.0](changelog-3.0.html "next chapter")

### This Page

* [Show Source](../_sources/history/whatsnew-3.0.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](changelog-3.0.html "Change history for Celery 3.0") |
* [previous](changelog-3.1.html "Change history") |
* [Celery 5.6.2 documentation](../index.html) »
* [History](index.html) »
* What’s new in Celery 3.0 (Chiastic Slide)

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.