celery.worker.consumer.tasks — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.worker.html "celery.worker.worker") |
* [previous](celery.worker.consumer.mingle.html "celery.worker.consumer.mingle") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.tasks`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.tasks.html).

# `celery.worker.consumer.tasks`[¶](#celery-worker-consumer-tasks "Link to this heading")

Worker Task Consumer Bootstep.

*class* celery.worker.consumer.tasks.Tasks(*c*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks)[¶](#celery.worker.consumer.tasks.Tasks "Link to this definition")
:   Bootstep starting the task message consumer.

    info(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.info)[¶](#celery.worker.consumer.tasks.Tasks.info "Link to this definition")
    :   Return task consumer info.

    name *= 'celery.worker.consumer.tasks.Tasks'*[¶](#celery.worker.consumer.tasks.Tasks.name "Link to this definition")

    qos\_global(*c*) → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.qos_global)[¶](#celery.worker.consumer.tasks.Tasks.qos_global "Link to this definition")
    :   Determine if global QoS should be applied.

        Additional information:
        :   <https://www.rabbitmq.com/docs/consumer-prefetch>
            <https://www.rabbitmq.com/docs/quorum-queues#global-qos>

    requires *= (step:celery.worker.consumer.mingle.Mingle{(step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)},)*[¶](#celery.worker.consumer.tasks.Tasks.requires "Link to this definition")

    shutdown(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.shutdown)[¶](#celery.worker.consumer.tasks.Tasks.shutdown "Link to this definition")
    :   Shutdown task consumer.

    start(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.start)[¶](#celery.worker.consumer.tasks.Tasks.start "Link to this definition")
    :   Start task consumer.

    stop(*c*)[[source]](../_modules/celery/worker/consumer/tasks.html#Tasks.stop)[¶](#celery.worker.consumer.tasks.Tasks.stop "Link to this definition")
    :   Stop task consumer.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.worker.consumer.mingle`](celery.worker.consumer.mingle.html "previous chapter")

#### Next topic

[`celery.worker.worker`](celery.worker.worker.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.worker.consumer.tasks.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.worker.html "celery.worker.worker") |
* [previous](celery.worker.consumer.mingle.html "celery.worker.consumer.mingle") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.tasks`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.