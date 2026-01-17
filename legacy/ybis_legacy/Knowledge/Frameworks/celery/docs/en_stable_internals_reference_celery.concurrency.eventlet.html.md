celery.concurrency.eventlet — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.concurrency.gevent.html "celery.concurrency.gevent") |
* [previous](celery.concurrency.prefork.html "celery.concurrency.prefork") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.concurrency.eventlet`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.eventlet.html).

# `celery.concurrency.eventlet`[¶](#celery-concurrency-eventlet "Link to this heading")

Eventlet execution pool.

*class* celery.concurrency.eventlet.TaskPool(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool)[¶](#celery.concurrency.eventlet.TaskPool "Link to this definition")
:   Eventlet Task Pool.

    *class* Timer(*\*args*, *\*\*kwargs*)[¶](#celery.concurrency.eventlet.TaskPool.Timer "Link to this definition")
    :   Eventlet Timer.

        cancel(*tref*)[¶](#celery.concurrency.eventlet.TaskPool.Timer.cancel "Link to this definition")

        clear()[¶](#celery.concurrency.eventlet.TaskPool.Timer.clear "Link to this definition")

        *property* queue[¶](#celery.concurrency.eventlet.TaskPool.Timer.queue "Link to this definition")
        :   Snapshot of underlying datastructure.

    grow(*n=1*)[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.grow)[¶](#celery.concurrency.eventlet.TaskPool.grow "Link to this definition")

    is\_green *= True*[¶](#celery.concurrency.eventlet.TaskPool.is_green "Link to this definition")
    :   set to true if pool uses greenlets.

    on\_apply(*target*, *args=None*, *kwargs=None*, *callback=None*, *accept\_callback=None*, *\*\*\_*)[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.on_apply)[¶](#celery.concurrency.eventlet.TaskPool.on_apply "Link to this definition")

    on\_start()[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.on_start)[¶](#celery.concurrency.eventlet.TaskPool.on_start "Link to this definition")

    on\_stop()[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.on_stop)[¶](#celery.concurrency.eventlet.TaskPool.on_stop "Link to this definition")

    shrink(*n=1*)[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.shrink)[¶](#celery.concurrency.eventlet.TaskPool.shrink "Link to this definition")

    signal\_safe *= False*[¶](#celery.concurrency.eventlet.TaskPool.signal_safe "Link to this definition")
    :   set to true if the pool can be shutdown from within
        a signal handler.

    task\_join\_will\_block *= False*[¶](#celery.concurrency.eventlet.TaskPool.task_join_will_block "Link to this definition")

    terminate\_job(*pid*, *signal=None*)[[source]](../../_modules/celery/concurrency/eventlet.html#TaskPool.terminate_job)[¶](#celery.concurrency.eventlet.TaskPool.terminate_job "Link to this definition")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.concurrency.prefork`](celery.concurrency.prefork.html "previous chapter")

#### Next topic

[`celery.concurrency.gevent`](celery.concurrency.gevent.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.concurrency.eventlet.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.concurrency.gevent.html "celery.concurrency.gevent") |
* [previous](celery.concurrency.prefork.html "celery.concurrency.prefork") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.concurrency.eventlet`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.