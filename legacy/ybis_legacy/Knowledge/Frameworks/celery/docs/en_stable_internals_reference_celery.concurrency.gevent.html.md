celery.concurrency.gevent — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.concurrency.thread.html "celery.concurrency.thread") |
* [previous](celery.concurrency.eventlet.html "celery.concurrency.eventlet") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.concurrency.gevent`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.gevent.html).

# `celery.concurrency.gevent`[¶](#celery-concurrency-gevent "Link to this heading")

Gevent execution pool.

*class* celery.concurrency.gevent.TaskPool(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool)[¶](#celery.concurrency.gevent.TaskPool "Link to this definition")
:   GEvent Pool.

    *class* Timer(*\*args*, *\*\*kwargs*)[¶](#celery.concurrency.gevent.TaskPool.Timer "Link to this definition")
    :   clear()[¶](#celery.concurrency.gevent.TaskPool.Timer.clear "Link to this definition")

        *property* queue[¶](#celery.concurrency.gevent.TaskPool.Timer.queue "Link to this definition")
        :   Snapshot of underlying datastructure.

    grow(*n=1*)[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.grow)[¶](#celery.concurrency.gevent.TaskPool.grow "Link to this definition")

    is\_green *= True*[¶](#celery.concurrency.gevent.TaskPool.is_green "Link to this definition")
    :   set to true if pool uses greenlets.

    *property* num\_processes[¶](#celery.concurrency.gevent.TaskPool.num_processes "Link to this definition")

    on\_apply(*target*, *args=None*, *kwargs=None*, *callback=None*, *accept\_callback=None*, *timeout=None*, *timeout\_callback=None*, *apply\_target=<function apply\_target>*, *\*\*\_*)[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.on_apply)[¶](#celery.concurrency.gevent.TaskPool.on_apply "Link to this definition")

    on\_start()[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.on_start)[¶](#celery.concurrency.gevent.TaskPool.on_start "Link to this definition")

    on\_stop()[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.on_stop)[¶](#celery.concurrency.gevent.TaskPool.on_stop "Link to this definition")

    shrink(*n=1*)[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.shrink)[¶](#celery.concurrency.gevent.TaskPool.shrink "Link to this definition")

    signal\_safe *= False*[¶](#celery.concurrency.gevent.TaskPool.signal_safe "Link to this definition")
    :   set to true if the pool can be shutdown from within
        a signal handler.

    task\_join\_will\_block *= False*[¶](#celery.concurrency.gevent.TaskPool.task_join_will_block "Link to this definition")

    terminate\_job(*pid*, *signal=None*)[[source]](../../_modules/celery/concurrency/gevent.html#TaskPool.terminate_job)[¶](#celery.concurrency.gevent.TaskPool.terminate_job "Link to this definition")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.concurrency.eventlet`](celery.concurrency.eventlet.html "previous chapter")

#### Next topic

[`celery.concurrency.thread`](celery.concurrency.thread.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.concurrency.gevent.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.concurrency.thread.html "celery.concurrency.thread") |
* [previous](celery.concurrency.eventlet.html "celery.concurrency.eventlet") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.concurrency.gevent`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.