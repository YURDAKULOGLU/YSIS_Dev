celery.worker.consumer.events — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.gossip.html "celery.worker.consumer.gossip") |
* [previous](celery.worker.consumer.control.html "celery.worker.consumer.control") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.events`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.events.html).

# `celery.worker.consumer.events`[¶](#celery-worker-consumer-events "Link to this heading")

Worker Event Dispatcher Bootstep.

`Events` -> [`celery.events.EventDispatcher`](celery.events.html#celery.events.EventDispatcher "celery.events.EventDispatcher").

*class* celery.worker.consumer.events.Events(*c*, *task\_events=True*, *without\_heartbeat=False*, *without\_gossip=False*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/events.html#Events)[¶](#celery.worker.consumer.events.Events "Link to this definition")
:   Service used for sending monitoring events.

    name *= 'celery.worker.consumer.events.Events'*[¶](#celery.worker.consumer.events.Events.name "Link to this definition")

    requires *= (step:celery.worker.consumer.connection.Connection{()},)*[¶](#celery.worker.consumer.events.Events.requires "Link to this definition")

    shutdown(*c*)[[source]](../_modules/celery/worker/consumer/events.html#Events.shutdown)[¶](#celery.worker.consumer.events.Events.shutdown "Link to this definition")

    start(*c*)[[source]](../_modules/celery/worker/consumer/events.html#Events.start)[¶](#celery.worker.consumer.events.Events.start "Link to this definition")

    stop(*c*)[[source]](../_modules/celery/worker/consumer/events.html#Events.stop)[¶](#celery.worker.consumer.events.Events.stop "Link to this definition")

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.worker.consumer.control`](celery.worker.consumer.control.html "previous chapter")

#### Next topic

[`celery.worker.consumer.gossip`](celery.worker.consumer.gossip.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.worker.consumer.events.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.gossip.html "celery.worker.consumer.gossip") |
* [previous](celery.worker.consumer.control.html "celery.worker.consumer.control") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.events`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.