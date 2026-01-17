celery.concurrency.thread — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.concurrency.base.html "celery.concurrency.base") |
* [previous](celery.concurrency.gevent.html "celery.concurrency.gevent") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.concurrency.thread`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.concurrency.thread.html).

# `celery.concurrency.thread`[¶](#celery-concurrency-thread "Link to this heading")

Thread execution pool.

*class* celery.concurrency.thread.TaskPool(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../../_modules/celery/concurrency/thread.html#TaskPool)[¶](#celery.concurrency.thread.TaskPool "Link to this definition")
:   Thread Task Pool.

    body\_can\_be\_buffer *= True*[¶](#celery.concurrency.thread.TaskPool.body_can_be_buffer "Link to this definition")

    limit*: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*[¶](#celery.concurrency.thread.TaskPool.limit "Link to this definition")

    on\_apply(*target: TargetFunction*, *args: [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[Any, ...] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *kwargs: [dict](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), Any] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *callback: Callable[..., Any] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *accept\_callback: Callable[..., Any] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *\*\*\_: Any*) → ApplyResult[[source]](../../_modules/celery/concurrency/thread.html#TaskPool.on_apply)[¶](#celery.concurrency.thread.TaskPool.on_apply "Link to this definition")

    on\_stop() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/concurrency/thread.html#TaskPool.on_stop)[¶](#celery.concurrency.thread.TaskPool.on_stop "Link to this definition")

    signal\_safe *= False*[¶](#celery.concurrency.thread.TaskPool.signal_safe "Link to this definition")
    :   set to true if the pool can be shutdown from within
        a signal handler.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.concurrency.gevent`](celery.concurrency.gevent.html "previous chapter")

#### Next topic

[`celery.concurrency.base`](celery.concurrency.base.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.concurrency.thread.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.concurrency.base.html "celery.concurrency.base") |
* [previous](celery.concurrency.gevent.html "celery.concurrency.gevent") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.concurrency.thread`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.