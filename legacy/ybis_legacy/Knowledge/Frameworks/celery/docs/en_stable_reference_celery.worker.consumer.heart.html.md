celery.worker.consumer.heart — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.mingle.html "celery.worker.consumer.mingle") |
* [previous](celery.worker.consumer.gossip.html "celery.worker.consumer.gossip") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.heart`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.heart.html).

# `celery.worker.consumer.heart`[¶](#celery-worker-consumer-heart "Link to this heading")

Worker Event Heartbeat Bootstep.

*class* celery.worker.consumer.heart.Heart(*c*, *without\_heartbeat=False*, *heartbeat\_interval=None*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/heart.html#Heart)[¶](#celery.worker.consumer.heart.Heart "Link to this definition")
:   Bootstep sending event heartbeats.

    This service sends a `worker-heartbeat` message every n seconds.

    Note

    Not to be confused with AMQP protocol level heartbeats.

    name *= 'celery.worker.consumer.heart.Heart'*[¶](#celery.worker.consumer.heart.Heart.name "Link to this definition")

    requires *= (step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)*[¶](#celery.worker.consumer.heart.Heart.requires "Link to this definition")

    shutdown(*c*)[¶](#celery.worker.consumer.heart.Heart.shutdown "Link to this definition")

    start(*c*)[[source]](../_modules/celery/worker/consumer/heart.html#Heart.start)[¶](#celery.worker.consumer.heart.Heart.start "Link to this definition")

    stop(*c*)[[source]](../_modules/celery/worker/consumer/heart.html#Heart.stop)[¶](#celery.worker.consumer.heart.Heart.stop "Link to this definition")

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.worker.consumer.gossip`](celery.worker.consumer.gossip.html "previous chapter")

#### Next topic

[`celery.worker.consumer.mingle`](celery.worker.consumer.mingle.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.worker.consumer.heart.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.mingle.html "celery.worker.consumer.mingle") |
* [previous](celery.worker.consumer.gossip.html "celery.worker.consumer.gossip") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.heart`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.