“The Big Instance” Refactor — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](reference/index.html "Internal Module Reference") |
* [previous](protocol.html "Message Protocol") |
* [Celery 5.6.2 documentation](../index.html) »
* [Internals](index.html) »
* “The Big Instance” Refactor

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/app-overview.html).

# “The Big Instance” Refactor[¶](#the-big-instance-refactor "Link to this heading")

The app branch is a work-in-progress to remove
the use of a global configuration in Celery.

Celery can now be instantiated and several
instances of Celery may exist in the same process space.
Also, large parts can be customized without resorting to monkey
patching.

## Examples[¶](#examples "Link to this heading")

Creating a Celery instance:

```
>>> from celery import Celery
>>> app = Celery()
>>> app.config_from_object('celeryconfig')
>>> #app.config_from_envvar('CELERY_CONFIG_MODULE')
```

Creating tasks:

```
@app.task
def add(x, y):
    return x + y
```

Creating custom Task subclasses:

```
Task = celery.create_task_cls()

class DebugTask(Task):

    def on_failure(self, *args, **kwargs):
        import pdb
        pdb.set_trace()

@app.task(base=DebugTask)
def add(x, y):
    return x + y
```

Starting a worker:

```
worker = celery.Worker(loglevel='INFO')
```

Getting access to the configuration:

```
celery.conf.task_always_eager = True
celery.conf['task_always_eager'] = True
```

Controlling workers:

```
>>> celery.control.inspect().active()
>>> celery.control.rate_limit(add.name, '100/m')
>>> celery.control.broadcast('shutdown')
>>> celery.control.discard_all()
```

Other interesting attributes:

```
# Establish broker connection.
>>> celery.broker_connection()

# AMQP Specific features.
>>> celery.amqp
>>> celery.amqp.Router
>>> celery.amqp.get_queues()
>>> celery.amqp.get_task_consumer()

# Loader
>>> celery.loader

# Default backend
>>> celery.backend
```

As you can probably see, this really opens up another
dimension of customization abilities.

## Deprecated[¶](#deprecated "Link to this heading")

* `celery.task.ping`
  `celery.task.PingTask`

  Inferior to the ping remote control command.
  Will be removed in Celery 2.3.

## Aliases (Pending deprecation)[¶](#aliases-pending-deprecation "Link to this heading")

* `celery.execute`
  :   + `.send_task` -> {`app.send_task`}
      + `.delay_task` -> *no alternative*
* `celery.log`
  :   + `.get_default_logger` -> {`app.log.get_default_logger`}
      + `.setup_logger` -> {`app.log.setup_logger`}
      + `.get_task_logger` -> {`app.log.get_task_logger`}
      + `.setup_task_logger` -> {`app.log.setup_task_logger`}
      + `.setup_logging_subsystem` -> {`app.log.setup_logging_subsystem`}
      + `.redirect_stdouts_to_logger` -> {`app.log.redirect_stdouts_to_logger`}
* `celery.messaging`
  :   + `.establish_connection` -> {`app.broker_connection`}
      + `.with_connection` -> {`app.with_connection`}
      + `.get_consumer_set` -> {`app.amqp.get_task_consumer`}
      + `.TaskPublisher` -> {`app.amqp.TaskPublisher`}
      + `.TaskConsumer` -> {`app.amqp.TaskConsumer`}
      + `.ConsumerSet` -> {`app.amqp.ConsumerSet`}
* `celery.conf.*` -> {`app.conf`}

  > **NOTE**: All configuration keys are now named the same
  > as in the configuration. So the key `task_always_eager`
  > is accessed as:
  >
  > ```
  > >>> app.conf.task_always_eager
  > ```
  >
  > instead of:
  >
  > ```
  > >>> from celery import conf
  > >>> conf.always_eager
  > ```
  >
  > + `.get_queues` -> {`app.amqp.get_queues`}
* `celery.utils.info`
  :   + `.humanize_seconds` -> `celery.utils.time.humanize_seconds`
      + `.textindent` -> `celery.utils.textindent`
      + `.get_broker_info` -> {`app.amqp.get_broker_info`}
      + `.format_broker_info` -> {`app.amqp.format_broker_info`}
      + `.format_queues` -> {`app.amqp.format_queues`}

## Default App Usage[¶](#default-app-usage "Link to this heading")

To be backward compatible, it must be possible
to use all the classes/functions without passing
an explicit app instance.

This is achieved by having all app-dependent objects
use [`default_app`](../reference/celery.app.html#celery.app.default_app "celery.app.default_app") if the app instance
is missing.

```
from celery.app import app_or_default

class SomeClass:

    def __init__(self, app=None):
        self.app = app_or_default(app)
```

The problem with this approach is that there’s a chance
that the app instance is lost along the way, and everything
seems to be working normally. Testing app instance leaks
is hard. The environment variable `CELERY_TRACE_APP`
can be used, when this is enabled [`celery.app.app_or_default()`](../reference/celery.app.html#celery.app.app_or_default "celery.app.app_or_default")
will raise an exception whenever it has to go back to the default app
instance.

### App Dependency Tree[¶](#app-dependency-tree "Link to this heading")

* {`app`}
  :   + `celery.loaders.base.BaseLoader`
      + `celery.backends.base.BaseBackend`
      + {`app.TaskSet`}
        :   - `celery.task.sets.TaskSet` (`app.TaskSet`)
      + [`app.TaskSetResult`]
        :   - `celery.result.TaskSetResult` (`app.TaskSetResult`)
* {`app.AsyncResult`}
  :   + `celery.result.BaseAsyncResult` / `celery.result.AsyncResult`
* `celery.bin.worker.WorkerCommand`
  :   + `celery.apps.worker.Worker`
        :   - `celery.worker.WorkerController`
              :   * `celery.worker.consumer.Consumer`
                    :   + `celery.worker.request.Request`
                        + `celery.events.EventDispatcher`
                        + `celery.worker.control.ControlDispatch`
                          :   - `celery.worker.control.registry.Panel`
                              - `celery.pidbox.BroadcastPublisher`
                        + `celery.pidbox.BroadcastConsumer`
                  * `celery.beat.EmbeddedService`
* `celery.bin.events.EvCommand`
  :   + `celery.events.snapshot.evcam`
        :   - `celery.events.snapshot.Polaroid`
            - `celery.events.EventReceiver`
      + `celery.events.cursesmon.evtop`
        :   - `celery.events.EventReceiver`
            - `celery.events.cursesmon.CursesMonitor`
      + `celery.events.dumper`
        :   - `celery.events.EventReceiver`
* `celery.bin.amqp.AMQPAdmin`
* `celery.bin.beat.BeatCommand`
  :   + `celery.apps.beat.Beat`
        :   - `celery.beat.Service`
              :   * `celery.beat.Scheduler`

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[Message Protocol](protocol.html "previous chapter")

#### Next topic

[Internal Module Reference](reference/index.html "next chapter")

### This Page

* [Show Source](../_sources/internals/app-overview.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](reference/index.html "Internal Module Reference") |
* [previous](protocol.html "Message Protocol") |
* [Celery 5.6.2 documentation](../index.html) »
* [Internals](index.html) »
* “The Big Instance” Refactor

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.