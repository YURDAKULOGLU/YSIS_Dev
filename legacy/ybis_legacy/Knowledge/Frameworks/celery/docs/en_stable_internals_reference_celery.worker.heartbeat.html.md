celery.worker.heartbeat — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.worker.control.html "celery.worker.control") |
* [previous](celery.worker.loops.html "celery.worker.loops") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.worker.heartbeat`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.worker.heartbeat.html).

# `celery.worker.heartbeat`[¶](#celery-worker-heartbeat "Link to this heading")

Heartbeat service.

This is the internal thread responsible for sending heartbeat events
at regular intervals (may not be an actual thread).

*class* celery.worker.heartbeat.Heart(*timer*, *eventer*, *interval=None*)[[source]](../../_modules/celery/worker/heartbeat.html#Heart)[¶](#celery.worker.heartbeat.Heart "Link to this definition")
:   Timer sending heartbeats at regular intervals.

    Parameters:
    :   * **timer** ([*kombu.asynchronous.timer.Timer*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.asynchronous.timer.html#kombu.asynchronous.timer.Timer "(in Kombu v5.6)")) – Timer to use.
        * **eventer** ([*celery.events.EventDispatcher*](../../reference/celery.events.html#celery.events.EventDispatcher "celery.events.EventDispatcher")) – Event dispatcher
          to use.
        * **interval** ([*float*](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)")) – Time in seconds between sending
          heartbeats. Default is 2 seconds.

    start()[[source]](../../_modules/celery/worker/heartbeat.html#Heart.start)[¶](#celery.worker.heartbeat.Heart.start "Link to this definition")

    stop()[[source]](../../_modules/celery/worker/heartbeat.html#Heart.stop)[¶](#celery.worker.heartbeat.Heart.stop "Link to this definition")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.worker.loops`](celery.worker.loops.html "previous chapter")

#### Next topic

[`celery.worker.control`](celery.worker.control.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.worker.heartbeat.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.worker.control.html "celery.worker.control") |
* [previous](celery.worker.loops.html "celery.worker.loops") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.worker.heartbeat`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.