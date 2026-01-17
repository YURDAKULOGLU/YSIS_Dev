Celery Deprecation Time-line — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](worker.html "Internals: The worker") |
* [previous](guide.html "Contributors Guide to the Code") |
* [Celery 5.6.2 documentation](../index.html) »
* [Internals](index.html) »
* Celery Deprecation Time-line

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/deprecation.html).

# Celery Deprecation Time-line[¶](#celery-deprecation-time-line "Link to this heading")

## [Removals for version 5.0](#id2)[¶](#removals-for-version-5-0 "Link to this heading")

### [Old Task API](#id3)[¶](#old-task-api "Link to this heading")

#### [Compat Task Modules](#id4)[¶](#compat-task-modules "Link to this heading")

* Module `celery.decorators` will be removed:

  > This means you need to change:
  >
  > ```
  > from celery.decorators import task
  > ```
  >
  > Into:
  >
  > ```
  > from celery import task
  > ```
* Module `celery.task` will be removed

  > This means you should change:
  >
  > ```
  > from celery.task import task
  > ```
  >
  > into:
  >
  > ```
  > from celery import shared_task
  > ```
  >
  > —and:

  > ```
  > from celery import task
  > ```
  >
  > into:
  >
  > ```
  > from celery import shared_task
  > ```
  >
  > —and:

  > ```
  > from celery.task import Task
  > ```
  >
  > into:
  >
  > ```
  > from celery import Task
  > ```

Note that the new `Task` class no longer
uses [`classmethod()`](https://docs.python.org/dev/library/functions.html#classmethod "(in Python v3.15)") for these methods:

> * delay
> * apply\_async
> * retry
> * apply
> * AsyncResult
> * subtask

This also means that you can’t call these methods directly
on the class, but have to instantiate the task first:

```
>>> MyTask.delay()          # NO LONGER WORKS


>>> MyTask().delay()        # WORKS!
```

### [Task attributes](#id5)[¶](#task-attributes "Link to this heading")

The task attributes:

* `queue`
* `exchange`
* `exchange_type`
* `routing_key`
* `delivery_mode`
* `priority`

is deprecated and must be set by [`task_routes`](../userguide/configuration.html#std-setting-task_routes) instead.

### [Modules to Remove](#id6)[¶](#modules-to-remove "Link to this heading")

* `celery.execute`

  This module only contains `send_task`: this must be replaced with
  [`app.send_task`](../reference/celery.html#celery.Celery.send_task "celery.Celery.send_task") instead.
* `celery.decorators`

  > See [Compat Task Modules](#deprecate-compat-task-modules)
* `celery.log`

  > Use [`app.log`](../reference/celery.app.log.html#celery.app.log.Logging "celery.app.log.Logging") instead.
* `celery.messaging`

  > Use [`app.amqp`](../reference/celery.app.amqp.html#celery.app.amqp.AMQP "celery.app.amqp.AMQP") instead.
* `celery.registry`

  > Use [`celery.app.registry`](../reference/celery.app.registry.html#module-celery.app.registry "celery.app.registry") instead.
* `celery.task.control`

  > Use [`app.control`](../reference/celery.app.control.html#celery.app.control.Control "celery.app.control.Control") instead.
* `celery.task.schedules`

  > Use [`celery.schedules`](../reference/celery.schedules.html#module-celery.schedules "celery.schedules") instead.
* `celery.task.chords`

  > Use [`celery.chord()`](../reference/celery.html#celery.chord "celery.chord") instead.

### [Settings](#id7)[¶](#settings "Link to this heading")

#### [`BROKER` Settings](#id8)[¶](#broker-settings "Link to this heading")

| **Setting name** | **Replace with** |
| --- | --- |
| `BROKER_HOST` | [`broker_url`](../userguide/configuration.html#std-setting-broker_url) |
| `BROKER_PORT` | [`broker_url`](../userguide/configuration.html#std-setting-broker_url) |
| `BROKER_USER` | [`broker_url`](../userguide/configuration.html#std-setting-broker_url) |
| `BROKER_PASSWORD` | [`broker_url`](../userguide/configuration.html#std-setting-broker_url) |
| `BROKER_VHOST` | [`broker_url`](../userguide/configuration.html#std-setting-broker_url) |

#### [`REDIS` Result Backend Settings](#id9)[¶](#redis-result-backend-settings "Link to this heading")

| **Setting name** | **Replace with** |
| --- | --- |
| `CELERY_REDIS_HOST` | [`result_backend`](../userguide/configuration.html#std-setting-result_backend) |
| `CELERY_REDIS_PORT` | [`result_backend`](../userguide/configuration.html#std-setting-result_backend) |
| `CELERY_REDIS_DB` | [`result_backend`](../userguide/configuration.html#std-setting-result_backend) |
| `CELERY_REDIS_PASSWORD` | [`result_backend`](../userguide/configuration.html#std-setting-result_backend) |
| `REDIS_HOST` | [`result_backend`](../userguide/configuration.html#std-setting-result_backend) |
| `REDIS_PORT` | [`result_backend`](../userguide/configuration.html#std-setting-result_backend) |
| `REDIS_DB` | [`result_backend`](../userguide/configuration.html#std-setting-result_backend) |
| `REDIS_PASSWORD` | [`result_backend`](../userguide/configuration.html#std-setting-result_backend) |

### [Task\_sent signal](#id10)[¶](#task-sent-signal "Link to this heading")

The [`task_sent`](../userguide/signals.html#std-signal-task_sent) signal will be removed in version 4.0.
Please use the [`before_task_publish`](../userguide/signals.html#std-signal-before_task_publish) and [`after_task_publish`](../userguide/signals.html#std-signal-after_task_publish)
signals instead.

### [Result](#id11)[¶](#result "Link to this heading")

Apply to: [`AsyncResult`](../reference/celery.result.html#celery.result.AsyncResult "celery.result.AsyncResult"),
[`EagerResult`](../reference/celery.result.html#celery.result.EagerResult "celery.result.EagerResult"):

* `Result.wait()` -> `Result.get()`
* `Result.task_id()` -> `Result.id`
* `Result.status` -> `Result.state`.

#### [Settings](#id12)[¶](#deprecations-v3-1 "Link to this heading")

| **Setting name** | **Replace with** |
| --- | --- |
| `CELERY_AMQP_TASK_RESULT_EXPIRES` | [`result_expires`](../userguide/configuration.html#std-setting-result_expires) |

## [Removals for version 2.0](#id13)[¶](#removals-for-version-2-0 "Link to this heading")

* The following settings will be removed:

| **Setting name** | **Replace with** |
| --- | --- |
| CELERY\_AMQP\_CONSUMER\_QUEUES | task\_queues |
| CELERY\_AMQP\_CONSUMER\_QUEUES | task\_queues |
| CELERY\_AMQP\_EXCHANGE | task\_default\_exchange |
| CELERY\_AMQP\_EXCHANGE\_TYPE | task\_default\_exchange\_type |
| CELERY\_AMQP\_CONSUMER\_ROUTING\_KEY | task\_queues |
| CELERY\_AMQP\_PUBLISHER\_ROUTING\_KEY | task\_default\_routing\_key |

* `CELERY_LOADER` definitions without class name.

  > For example,, celery.loaders.default, needs to include the class name:
  > celery.loaders.default.Loader.
* `TaskSet.run()`. Use `celery.task.base.TaskSet.apply_async()`
  :   instead.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[Contributors Guide to the Code](guide.html "previous chapter")

#### Next topic

[Internals: The worker](worker.html "next chapter")

### This Page

* [Show Source](../_sources/internals/deprecation.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](worker.html "Internals: The worker") |
* [previous](guide.html "Contributors Guide to the Code") |
* [Celery 5.6.2 documentation](../index.html) »
* [Internals](index.html) »
* Celery Deprecation Time-line

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.