celery.concurrency.prefork — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.concurrency.eventlet.html "celery.concurrency.eventlet") |
* [previous](celery.concurrency.solo.html "celery.concurrency.solo") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.concurrency.prefork`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.prefork.html).

# `celery.concurrency.prefork`[¶](#celery-concurrency-prefork "Link to this heading")

Prefork execution pool.

Pool implementation using [`multiprocessing`](https://docs.python.org/dev/library/multiprocessing.html#module-multiprocessing "(in Python v3.15)").

*class* celery.concurrency.prefork.TaskPool(*limit=None*, *putlocks=True*, *forking\_enable=True*, *callbacks\_propagate=()*, *app=None*, *\*\*options*)[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool)[¶](#celery.concurrency.prefork.TaskPool "Link to this definition")
:   Multiprocessing Pool implementation.

    BlockingPool[¶](#celery.concurrency.prefork.TaskPool.BlockingPool "Link to this definition")
    :   alias of `Pool`

    Pool[¶](#celery.concurrency.prefork.TaskPool.Pool "Link to this definition")
    :   alias of `AsynPool`

    did\_start\_ok()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.did_start_ok)[¶](#celery.concurrency.prefork.TaskPool.did_start_ok "Link to this definition")

    *property* num\_processes[¶](#celery.concurrency.prefork.TaskPool.num_processes "Link to this definition")

    on\_close()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.on_close)[¶](#celery.concurrency.prefork.TaskPool.on_close "Link to this definition")

    on\_start()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.on_start)[¶](#celery.concurrency.prefork.TaskPool.on_start "Link to this definition")

    on\_stop()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.on_stop)[¶](#celery.concurrency.prefork.TaskPool.on_stop "Link to this definition")
    :   Gracefully stop the pool.

    on\_terminate()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.on_terminate)[¶](#celery.concurrency.prefork.TaskPool.on_terminate "Link to this definition")
    :   Force terminate the pool.

    register\_with\_event\_loop(*loop*)[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.register_with_event_loop)[¶](#celery.concurrency.prefork.TaskPool.register_with_event_loop "Link to this definition")

    restart()[[source]](../../_modules/celery/concurrency/prefork.html#TaskPool.restart)[¶](#celery.concurrency.prefork.TaskPool.restart "Link to this definition")

    uses\_semaphore *= True*[¶](#celery.concurrency.prefork.TaskPool.uses_semaphore "Link to this definition")
    :   only used by multiprocessing pool

    write\_stats *= None*[¶](#celery.concurrency.prefork.TaskPool.write_stats "Link to this definition")

celery.concurrency.prefork.process\_destructor(*pid*, *exitcode*)[[source]](../../_modules/celery/concurrency/prefork.html#process_destructor)[¶](#celery.concurrency.prefork.process_destructor "Link to this definition")
:   Pool child process destructor.

    Dispatch the [`worker_process_shutdown`](../../userguide/signals.html#std-signal-worker_process_shutdown) signal.

celery.concurrency.prefork.process\_initializer(*app*, *hostname*)[[source]](../../_modules/celery/concurrency/prefork.html#process_initializer)[¶](#celery.concurrency.prefork.process_initializer "Link to this definition")
:   Pool child process initializer.

    Initialize the child pool process to ensure the correct
    app instance is used and things like logging works.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.concurrency.solo`](celery.concurrency.solo.html "previous chapter")

#### Next topic

[`celery.concurrency.eventlet`](celery.concurrency.eventlet.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.concurrency.prefork.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.concurrency.eventlet.html "celery.concurrency.eventlet") |
* [previous](celery.concurrency.solo.html "celery.concurrency.solo") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.concurrency.prefork`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.